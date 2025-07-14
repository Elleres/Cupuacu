import os

from motor.motor_asyncio import AsyncIOMotorClient


MONGO_URL = os.environ.get("MONGO_URL")

client = AsyncIOMotorClient(MONGO_URL)
db = client["chatdb"]