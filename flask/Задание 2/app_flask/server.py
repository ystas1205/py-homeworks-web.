from flask import Flask, jsonify, request
from sqlalchemy.exc import IntegrityError

from flask_bcrypt import Bcrypt
import pydantic

from models import Session, Token, Announcement
from schema import CreateToken, CreateAnnouncement, UpdateAnnouncement

app = Flask("app")
bcrypt = Bcrypt(app)


def hash_password(password: str):
    password = password.encode()
    hashed = bcrypt.generate_password_hash(password)
    return hashed.decode()


# def check_password(password: str, hashed_password: str):
#     password = password.encode()
#     hashed_password = hashed_password.encode()
#     return bcrypt.check_password_hash(password, hashed_password)


def validate(schema_class, json_data):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except pydantic.ValidationError as er:
        error = er.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)


@app.before_request
def before_request():
    session: Session = Session()
    request.session = session


@app.after_request
def after_request(response):
    request.session.close()
    return response


class HttpError(Exception):
    def __init__(self, status_code: int, description: str):
        self.status_code = status_code
        self.description = description


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error": error.description})
    response.status_code = error.status_code
    return response


# получение обьявление по id
def get_advertisement_by_id(announcement_id: int):
    announcement = request.session.get(Announcement, announcement_id)
    if announcement is None:
        raise HttpError(404, "announcement not found")
    return announcement


# получение токена по id
def get_token_by_id(token_id: int):
    token = request.session.get(Token, token_id)
    if token is None:
        raise HttpError(404, "token not found")
    return token


def add_announcement(announcement: Announcement):
    try:
        request.session.add(announcement)
        request.session.commit()
    except IntegrityError:
        raise HttpError(400, "the entry: already exists")


# получение токена из заголовка запроса
def token_headers():
    headers = request.headers
    headers_token = headers["Token"]
    return headers_token


# получение токена из талицы Тоken для сравнения с заголовком
def token_auth(token_id: int):
    user = get_advertisement_by_id(token_id)
    data_userid = user.user_id
    token = get_token_by_id(data_userid)
    data_token = str(token.token)
    return data_token


# Регестрация пользователя и получения токента

@app.route('/registration', methods=['POST'])
def post_token():
    json_data = validate(CreateToken, request.json)
    json_data['password'] = hash_password(json_data['password'])
    user = Token(**json_data)
    add_announcement(user)
    return jsonify(user.dict)


# Создание обьявление авторизованым пользователем

@app.route("/announcement", methods=['POST'])
def post():
    json_data = validate(CreateAnnouncement, request.json)
    announcement = Announcement(**json_data)
    userid = announcement.user_id
    get_token_by_id(userid)
    token = get_token_by_id(userid)
    if userid == token.id:
        add_announcement(announcement)
    return jsonify(announcement.dict)


# получения обьявление по id
@app.route("/announcement/<int:announcement_id>", methods=['GET'])
def get(announcement_id):
    advertisement = get_advertisement_by_id(announcement_id)
    return jsonify(advertisement.dict)


# Удаление обьявление владельцем
@app.route("/announcement/<int:announcement_id>", methods=['DELETE'])
def delete(announcement_id: int):
    headers_token = token_headers()
    token_user = token_auth(announcement_id)
    if headers_token == token_user:
        request.session.delete(get_advertisement_by_id(announcement_id))
        request.session.commit()
        return jsonify({"status": "deleted"})
    else:
        raise HttpError(404, "token not found")


# Изменение обьявление владельцем

@app.route("/announcement/<int:announcement_id>", methods=['PATCH'])
def patch(announcement_id: int):
    json_data = validate(UpdateAnnouncement, request.json)
    headers_token = token_headers()
    token_user = token_auth(announcement_id)
    if headers_token == token_user:
        for key, value in json_data.items():
            setattr(get_advertisement_by_id(announcement_id), key, value)
        add_announcement(get_advertisement_by_id(announcement_id))
        return jsonify(get_advertisement_by_id(announcement_id).dict)
    else:
        raise HttpError(404, "token not found")


if __name__ == '__main__':
    app.run()
