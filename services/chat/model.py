

class ChatRoom:
    def __init__(self, db):
        self.db = db
        self.collection = self.db['CHATROOM']

    async def fetch_chatroom(self, user_id):
        query = {"user_id": user_id}
        chat_room = await self.collection.find_one(query)
        return chat_room

    async def create(self, user_id):
        result = await self.collection.insert_one(
            {
                "user_id": user_id,
                "messages": [0]
            }
        )
        return result

    async def update(self, user_id, message):
        query = {"user_id": user_id}
        chat_room = await self.collection.find_one(query)
        if not chat_room["messages"]:
            messages = [message]
            result = await self.collection.update_one(query,
                                                      {"$set": {"messages": messages}})
        else:
            messages = chat_room["messages"]
            messages.append(message)
            result = await self.collection.update_one(query,
                                                      {"$set": {"messages": messages}})
        return result

    async def fetch_chatrooms(self):
        chat_rooms = await self.collection.find().to_list(length=100)
        return chat_rooms
