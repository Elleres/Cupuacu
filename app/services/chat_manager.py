from datetime import datetime
from pyexpat.errors import messages
from typing import Dict, List
from uuid import UUID

from starlette.websockets import WebSocket


class ChatManager:
    def __init__(self):
        # Chave do dicionário é ticket_id, user_id (chaves primarias da tabela ticket)
        self.active_connections: Dict[UUID, List[WebSocket]] = {}

    def join(self, ticket_id: UUID, websocket: WebSocket):
        self.active_connections.setdefault(ticket_id, []).append(websocket)

    def leave(self, ticket_id: UUID, websocket: WebSocket):
        self.active_connections.get(ticket_id, []).remove(websocket)

    async def broadcast_message(self, ticket_id, message):
        for chat in chat_manager.active_connections[ticket_id]:
            await chat.send_json(message)

chat_manager = ChatManager()