from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.ticket import Ticket, TicketStatus
from app.models.mensagem import Mensagem
from app.routers.ws import manager

router = APIRouter(prefix="/webhook", tags=["webhook"])


@router.post("")
async def receber_evento(request: Request, db: AsyncSession = Depends(get_db)):
    payload = await request.json()
    event = payload.get("event", "")

    if event in ("messages.upsert", "MESSAGES_UPSERT"):
        await _processar_mensagem(payload.get("data", {}), db)

    return {"ok": True}


async def _processar_mensagem(data: dict, db: AsyncSession):
    key = data.get("key", {})
    remote_jid: str = key.get("remoteJid", "")
    from_me: bool = key.get("fromMe", False)

    # Ignora mensagens enviadas pelo próprio bot e mensagens de grupos
    if from_me or remote_jid.endswith("@g.us"):
        return

    msg_obj = data.get("message", {})
    texto: str = (
        msg_obj.get("conversation")
        or msg_obj.get("extendedTextMessage", {}).get("text")
        or "[mídia]"
    )
    nome_cliente: str = data.get("pushName", "")
    timestamp: int = data.get("messageTimestamp", 0)

    # Busca ticket aberto para este contato (aguardando ou em atendimento)
    result = await db.execute(
        select(Ticket)
        .where(
            Ticket.remote_jid == remote_jid,
            Ticket.status.in_([TicketStatus.aguardando, TicketStatus.em_atendimento]),
        )
        .order_by(Ticket.created_at.desc())
        .limit(1)
    )
    ticket = result.scalar_one_or_none()

    # Se não há ticket aberto, o Typebot ainda está manejando a conversa
    if not ticket:
        return

    mensagem = Mensagem(
        ticket_id=ticket.id,
        conteudo=texto,
        de_cliente=True,
        timestamp_wa=timestamp,
    )
    db.add(mensagem)
    await db.commit()

    await manager.broadcast({
        "tipo": "nova_mensagem",
        "ticket_id": str(ticket.id),
        "remote_jid": remote_jid,
        "nome_cliente": nome_cliente,
        "conteudo": texto,
    })
