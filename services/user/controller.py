from aiohttp import web
from services.user.model import User

from logic.json_encoder import JSONEncoder
from utils import DotDict


class UserController(web.View):
    async def get(self):
        data = self.request.query
        user_id = data["id"]
        user = await User(self.request.db).fetchUserInfo(str(user_id))
        return web.Response(content_type='application/json', text=JSONEncoder().encode(user))

    async def post(self):
        data = await self.request.json()
        user_id = await User(self.request.db).create(data["name"], data["login"], data["password"])

        return web.Response(content_type='application/json', text=user_id)


class UsersController(web.View):
    async def get(self):
        users = await User(self.request.db).fetchUsersInfo()
        return web.Response(content_type='application/json', text=JSONEncoder().encode(users))