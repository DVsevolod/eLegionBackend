from aiohttp import web
from aiohttp import WSMsgType

import json

from .model import ChatRoom
from logic.json_encoder import JSONEncoder


class WebSocket(web.View):
    async def get(self):

        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        await ws.send_str('connected')

        self.request.app['websockets'].append(ws)

        async for msg in ws:
            if msg.type == WSMsgType.text:
                if msg.data == 'close':
                    await ws.close()
                else:
                    json_msg = json.loads(msg.data)
                    msg_id = json_msg.get("id")
                    msg_text = json_msg.get("text")

                    await ws.send_str(msg_text)

                    if await ChatRoom(self.request.db).fetch_chatroom(msg_id):
                        await ChatRoom(self.request.db).update(msg_id, msg_text)
                    else:
                        await ChatRoom(self.request.db).create(msg_id)
                        await ChatRoom(self.request.db).update(msg_id, msg_text)

                    print(await ChatRoom(self.request.db).fetch_chatroom(msg_id))

                    ws_connections = self.request.app['websockets'][:]
                    for ws_connection in ws_connections:
                        if ws_connection == ws:
                            pass
                        await ws_connection.send_str(msg_text)

            elif msg == WSMsgType.error:
                print('ws connection closed with exception %s' % ws.exception())

        self.request.app['websockets'].remove(ws)
        print('ws connection closed')
        return ws


class ChatRoomController(web.View):
    async def get(self):
        data = self.request.query
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
