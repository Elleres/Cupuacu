from uuid import UUID
from datetime import datetime
from typing import List

from db.mongo_connector import db


chat_collection = db["chat_messages"]


async def create_message(ticket_id: UUID, username: str, content: str) -> dict:
    message = {
        "ticket_id": str(ticket_id),
        "username": str(username),
        "content": content,
        "timestamp": datetime.now().timestamp()
    }
    result = await chat_collection.insert_one(message)
    message["_id"] = str(result.inserted_id)
    return message


async def get_recent_messages(ticket_id: UUID, limit: int = 20) -> List[dict]:
    cursor = chat_collection.find({"ticket_id": str(ticket_id)}).sort("timestamp", -1).limit(limit)
    messages = await cursor.to_list(length=limit)
    return [format_message(msg) for msg in reversed(messages)]


async def get_messages_before(ticket_id: UUID, before_ts: float, limit: int = 20) -> List[dict]:
    cursor = chat_collection.find({
        "ticket_id": str(ticket_id),
        "timestamp": {"$lt": before_ts}
    }).sort("timestamp", -1).limit(limit)

    messages = await cursor.to_list(length=limit)
    return [format_message(msg) for msg in reversed(messages)]


def format_message(msg: dict) -> dict:
    return {
        "id": str(msg.get("_id")),
        "ticket_id": msg["ticket_id"],
        "username": msg["username"],
        "content": msg["content"],
        "timestamp": msg["timestamp"]
    }
