from uuid import UUID

from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Query, HTTPException

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.chat_repositories import create_message, get_recent_messages, get_messages_before
from repositories.ticket_repositories import get_ticket
from const.enum import UserType
from db.db_connector import get_db
from services.auth_service import get_current_user
from utils.chat_manager import chat_manager

router = APIRouter()

@router.websocket("/chat")
async def websocket_endpoint(
        websocket: WebSocket,
        token: str = Query(...),
        ticket_id: UUID = Query(...),
        db: AsyncSession = Depends(get_db)
):
    await websocket.accept()

    try:
        user = await get_current_user(db, token)
    except HTTPException as err:
        print(err, flush=True)
        await websocket.close(code=1008, reason="Token inválido")
        return

    ticket = await get_ticket(db, ticket_id)

    if not ticket or (ticket.id_user != user.id and user.type != UserType.admin):
        await websocket.close(code=1008, reason="Ticket não encontrado, ou você não possui acesso a ele.")
        return

    chat_manager.join(ticket_id,  websocket)
    # Aqui as mensagens mais recentes devem ser enviadas ao usuario
    recent_messages = await get_recent_messages(ticket_id)
    await websocket.send_json(recent_messages)

    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")
            if action == "load_older":
                timestamp = data.get("timestamp")
                messages = await get_messages_before(ticket_id, timestamp)
                await websocket.send_json(messages)
            elif action == "send_msg":
                text_message = data.get("text")
                message = await create_message(ticket_id, user.name, text_message)
                await chat_manager.broadcast_message(ticket_id, message)
    except WebSocketDisconnect:
        chat_manager.leave(ticket_id, websocket)