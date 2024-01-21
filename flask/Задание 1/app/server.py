from flask import Flask, jsonify, request
from flask.views import MethodView

from sqlalchemy.exc import IntegrityError
import pydantic

from models import Session, Announcement
from schema import CreateUser, UpdateUser

app = Flask("app")


def validate(schema_class, json_data):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except pydantic.ValidationError as er:
        error = er.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)


@app.before_request
def before_request():
    session = Session()
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


def get_announcement_by_id(announcement_id: int):
    announcement = request.session.get(Announcement, announcement_id)
    if announcement is None:
        raise HttpError(404, "announcement not found")
    return announcement


def add_announcement(announcement: Announcement):
    try:
        request.session.add(announcement)
        request.session.commit()
    except IntegrityError:
        raise HttpError(400, "announcement already exists")


class AnnouncementView(MethodView):
    def get(self, announcement_id):
        user = get_announcement_by_id(announcement_id)
        return jsonify(user.dict)

    def post(self):
        json_data = validate(CreateUser, request.json)
        user = Announcement(**json_data)
        add_announcement(user)
        return jsonify(user.dict)

    def patch(self, announcement_id):
        json_data = validate(UpdateUser, request.json)
        user = get_announcement_by_id(announcement_id)
        for key, value in json_data.items():
            setattr(user, key, value)
        add_announcement(user)
        return jsonify(user.dict)

    def delete(self, announcement_id):
        user = get_announcement_by_id(announcement_id)
        request.session.delete(user)
        request.session.commit()
        return jsonify({"status": "delete"})


user_view = AnnouncementView.as_view("announcement")

app.add_url_rule("/announcement/", view_func=user_view, methods=["POST"])
app.add_url_rule(
    "/announcement/<int:announcement_id>", view_func=user_view,
    methods=["GET", "PATCH", "DELETE"]
)
if __name__ == "__main__":
    app.run()
