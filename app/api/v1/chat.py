import json
from http import HTTPStatus
from uuid import UUID

from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Query
from typing import List, Optional

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.ticket_repositories import get_ticket
from const.enum import UserType
from db.db_connector import get_db
from schemas.chat import WSConnectionRequest
from services.auth_service import get_current_user

router = APIRouter()

@router.websocket("/chat")
async def websocket_endpoint(
        websocket: WebSocket,
        token: str = Query(...),
        ticket_id: UUID = Query(...),
        user_id: Optional[UUID] = Query(default=None),
        db: AsyncSession = Depends(get_db)
):
    await websocket.accept()

    # Verificando quem é o usuário
    user = await get_current_user(db, token)

    # user_id só deve ser preenchido se o usuário for admin
    if (user_id != None) and user.type != UserType.admin:
        await websocket.close(code=1008, reason="Somente admins podem ler tickets de outras pessoas")

    # Se o usuário não enviar um ID, usar o id relacionado ao token, caso contrário, usar ID enviado
    if not user_id:
        ticket = await get_ticket(db, ticket_id, user.id)
    else:
        ticket = await get_ticket(db, ticket_id, user_id)

    if not ticket:
        await websocket.close(code=1008, reason="Ticket não encontrado, ou você não possuia acesso a ele.")
        return

    try:
        while True:
            data = await websocket.receive_json()
            json_data = json.dumps(data['text'], ensure_ascii=False)
            await websocket.send_text("Recebido")
    except WebSocketDisconnect:
        print("client disconnected")