from bson.objectid import ObjectId
import uuid


class User:
    def __init__(self, db):
        self.db = db
        self.collection = self.db["USERS"]

    async def fetchUserInfo(self, user_id):
        query = {"user_id": user_id}
        user = await self.collection.find_one(query)
        return user

    async def fetchUsersInfo(self):
        users = await self.collection.find()
        return users

    async def create(self, fullname, login, password):
        user_id = str(uuid.uuid4())
        result = await self.collection.insert_one(
            {
                "name": fullname,
                "login": login,
                "password": password,
                "user_id": user_id
            }
        )

        return user_id
