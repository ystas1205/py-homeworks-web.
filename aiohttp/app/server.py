from aiohttp import web
from sqlalchemy.exc import IntegrityError

import pydantic

from models import Session, Announcement, Token, engine, init_orm
from schema import CreateToken, CreateAnnouncement, UpdateAnnouncement, \
    get_http_error
from auth import hash_password

app = web.Application()


def validate(schema_class, json_data):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except pydantic.ValidationError as er:
        error = er.errors()[0]
        error.pop("ctx", None)
        raise get_http_error(web.HTTPBadRequest,
                             f"error")


async def init_db(app: web.Application):
    print("START")
    await init_orm()
    yield
    print("FINISH")
    await engine.dispose()


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response


app.cleanup_ctx.append(init_db)
app.middlewares.append(session_middleware)


async def get_announcement_by_id(session: Session, announcement_id: int):
    announcement = await session.get(Announcement, announcement_id)
    if announcement is None:
        raise (get_http_error
               (web.HTTPNotFound,
                f"Announcement with id {announcement_id} not found"))
    return announcement


async def get_token_by_id(session: Session, token_id: int):
    token = await session.get(Token, token_id)
    if token is None:
        raise get_http_error(web.HTTPNotFound,
                             f"User with id {token_id} not found")
    return token


async def add_token_announcement(session: Session, data):
    try:
        session.add(data)
        await session.commit()
    except IntegrityError:
        raise get_http_error(
            web.HTTPConflict,
            f"The user with email {data.email} already exists"
        )
    return data


async def authorization_by_token(id_token):
    headers = id_token.request.headers
    headers_token = headers["Token"]

    user = await id_token.get_announcement()
    data_userid = user.user_id
    token = await get_token_by_id(id_token.session, data_userid)
    data_token = str(token.token)

    if headers_token == data_token:
        return user
    raise get_http_error(web.HTTPNotFound, (404, "token not found"))


class LoginView(web.View):

    async def post(self):
        json_data = await self.request.json()
        json_data = validate(CreateToken, json_data)
        json_data['password'] = await hash_password(json_data['password'])
        token = Token(**json_data)
        await add_token_announcement(self.request.session, token)
        return web.json_response(str(token.dict))


class AnnouncementView(web.View):

    @property
    def session(self) -> Session:
        return self.request.session

    @property
    def announcement_id(self):
        return int(self.request.match_info["announcement_id"])

    async def get_announcement(self):
        return await get_announcement_by_id(self.session, self.announcement_id)

    # Создание обьявление авторизованым пользователем

    async def post(self):
        json_data = await self.request.json()
        json_data = validate(CreateAnnouncement, json_data)
        announcement = Announcement(**json_data)
        userid = announcement.user_id
        token = await get_token_by_id(self.session, userid)
        if userid == token.id:
            await add_token_announcement(self.session, announcement)
        return web.json_response(str(announcement.dict))

    async def get(self):
        announcement = await self.get_announcement()
        return web.json_response(announcement.dict)

    async def delete(self):
        await self.session.delete(await authorization_by_token(self))
        await self.session.commit()
        return web.json_response({"status": "deleted"})

    async def patch(self):
        json_data = await self.request.json()
        json_data = validate(UpdateAnnouncement, json_data)
        announcement = await authorization_by_token(self)
        for key, value in json_data.items():
            setattr(announcement, key, value)
        await add_token_announcement(self.session, announcement)
        return web.json_response(announcement.dict)


app.add_routes(
    [
        web.get("/announcement/{announcement_id:\d+}", AnnouncementView),
        web.patch("/announcement/{announcement_id:\d+}", AnnouncementView),
        web.delete("/announcement/{announcement_id:\d+}", AnnouncementView),
        web.post("/announcement", AnnouncementView),
        web.post("/registration", LoginView),

    ]
)
if __name__ == "__main__":
    web.run_app(app, port=8080)
