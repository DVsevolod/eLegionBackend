from aiohttp import web


class AuthController(web.View):
    async def get(self):
        return web.Response(content_type='application/json', text="")

    async def post(self):
        data = await self.request.json()
