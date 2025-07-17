from motor.motor_asyncio import AsyncIOMotorClient

from const.const import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
db = client["chatdb"]