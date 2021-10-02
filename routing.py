from core.route import Router
from services.auth.controller import AuthController
from services.user.controller import UserController
from services.chat.controller import WebSocket, ChatRoomController


routings = [
    Router("GET", "auth", '/auth', AuthController),
    Router("GET", "ws", "/ws", WebSocket),
    Router("*", "user", "/user", UserController),
    Router("*", "chat-room", "/chat-room", ChatRoomController)
]
