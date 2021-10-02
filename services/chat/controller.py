from aiohttp import web
from aiohttp import WSMsgType

import json

from .model import ChatRoom
from logic.json_encoder import JSONEncoder


class WebSocket(web.View):
    async def get(self):

        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        await ws.send_str('hello my dear mister Popponi')

        self.request.app['websockets'].append(ws)

        async for msg in ws:
            if msg.type == WSMsgType.text:
                if msg.data == 'close':
                    await ws.close()
                else:
                    json_msg = json.loads(msg.data)
                    user_id = json_msg["user_id"]
                    text = json_msg["text"]

                    await ws.send_str(text)

                    if await ChatRoom(self.request.db).fetch_chatroom(user_id):
                        await ChatRoom(self.request.db).update(user_id, text)
                    else:
                        await ChatRoom(self.request.db).create(user_id)
                        await ChatRoom(self.request.db).update(user_id, text)

                    print(await ChatRoom(self.request.db).fetch_chatroom(user_id))

                    ws_connections = self.request.app['websockets'][:]
                    for ws_connection in ws_connections:
                        if ws_connection == ws:
                            pass
                        await ws_connection.send_str(text)

            elif msg == WSMsgType.error:
                print('ws connection closed with exception %s' % ws.exception())

        self.request.app['websockets'].remove(ws)
        print('ws connection closed')
        return ws


class ChatRoomController(web.View):
    async def get(self):
        data = self.request.query
        user_id = data["user_id"]
        chat_room = await ChatRoom(self.request.db).fetch_chatrooms()
        response = {"chatrooms": chat_room}
        return web.Response(content_type='application/json', text=JSONEncoder().encode(response))

    async def post(self):
        data = await self.request.json()
        result = await ChatRoom(self.request.db).create(data["user_id"])
        print(result.inserted_id)
        return web.Response(content_type='application/json', text="Success")

    async def update(self):
        data = await self.request.json()
        result = await ChatRoom(self.request.db).update(data["user_id"], data["message"])
        print(result)
        return web.Response(content_type='application/json', text="Success")
