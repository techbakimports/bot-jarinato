import asyncio
from datetime import datetime, timezone
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.ticket import Ticket, TicketStatus
from app.models.mensagem import Mensagem
from app.schemas.ticket import TicketOut, AssumirTicket, TransbordoPayload
from app.schemas.mensagem import MensagemOut, MensagemEnviar
from app.services.evolution import enviar_mensagem
from app.services.odoo import buscar_cliente_por_telefone
from app.services.notificacao import notificar_novo_ticket
from app.routers.ws import manager

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("/transbordo", status_code=201)
async def transbordo(payload: TransbordoPayload, db: AsyncSession = Depends(get_db)):
    """
    Chamado pelo nó HTTP Request do Typebot quando o cliente solicita atendimento humano.
    Consulta Odoo, cria o ticket e notifica atendentes.
    """
    result = await db.execute(
        select(Ticket).where(
            Ticket.remote_jid == payload.remoteJid,
            Ticket.status.in_([TicketStatus.aguardando, TicketStatus.em_atendimento]),
        )
    )
    if result.scalar_one_or_none():
        return {"ok": True, "msg": "Ticket já existe para este contato"}

    # Consulta Odoo em paralelo (não bloqueia se não estiver configurado)
    odoo_dados = await buscar_cliente_por_telefone(payload.remoteJid)

    nome = payload.nome or (odoo_dados.get('nome') if odoo_dados else None)

    ticket = Ticket(
        remote_jid=payload.remoteJid,
        nome_cliente=nome,
        status=TicketStatus.aguardando,
        odoo_partner_id=odoo_dados.get('partner_id') if odoo_dados else None,
        odoo_dados=odoo_dados,
    )
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)

    await manager.broadcast({
        "tipo":         "novo_ticket",
        "ticket_id":    str(ticket.id),
        "remote_jid":   ticket.remote_jid,
        "nome_cliente": ticket.nome_cliente,
        "odoo_dados":   ticket.odoo_dados,
    })

    # Notificação por e-mail (best-effort, não aguarda)
    asyncio.create_task(
        notificar_novo_ticket(ticket.nome_cliente or '', ticket.remote_jid, str(ticket.id))
    )

    return {"ok": True, "ticket_id": str(ticket.id)}


@router.get("", response_model=List[TicketOut])
async def listar_tickets(status: str = "aguardando", db: AsyncSession = Depends(get_db)):
    try:
        status_enum = TicketStatus(status)
    except ValueError:
        raise HTTPException(400, "Status inválido. Use: aguardando, em_atendimento ou encerrado")

    result = await db.execute(
        select(Ticket).where(Ticket.status == status_enum).order_by(Ticket.created_at.desc())
    )
    return result.scalars().all()


@router.post("/{ticket_id}/assumir", response_model=TicketOut)
async def assumir_ticket(ticket_id: UUID, dados: AssumirTicket, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    if not ticket:
        raise HTTPException(404, "Ticket não encontrado")

    ticket.status = TicketStatus.em_atendimento
    ticket.atendente_id = dados.atendente_id
    await db.commit()
    await db.refresh(ticket)

    await manager.broadcast({
        "tipo":        "ticket_assumido",
        "ticket_id":   str(ticket.id),
        "atendente_id": str(dados.atendente_id),
    })
    return ticket


@router.post("/{ticket_id}/encerrar", response_model=TicketOut)
async def encerrar_ticket(ticket_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    if not ticket:
        raise HTTPException(404, "Ticket não encontrado")

    ticket.status = TicketStatus.encerrado
    ticket.encerrado_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(ticket)

    await manager.broadcast({"tipo": "ticket_encerrado", "ticket_id": str(ticket.id)})
    return ticket


@router.get("/{ticket_id}/mensagens", response_model=List[MensagemOut])
async def listar_mensagens(ticket_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Mensagem).where(Mensagem.ticket_id == ticket_id).order_by(Mensagem.created_at)
    )
    return result.scalars().all()


@router.post("/{ticket_id}/enviar")
async def enviar_mensagem_atendente(
    ticket_id: UUID,
    dados: MensagemEnviar,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    if not ticket:
        raise HTTPException(404, "Ticket não encontrado")
    if ticket.status == TicketStatus.encerrado:
        raise HTTPException(400, "Ticket encerrado — não é possível enviar mensagem")

    await enviar_mensagem(ticket.remote_jid, dados.conteudo)

    mensagem = Mensagem(ticket_id=ticket_id, conteudo=dados.conteudo, de_cliente=False)
    db.add(mensagem)
    await db.commit()

    await manager.broadcast({
        "tipo":      "mensagem_enviada",
        "ticket_id": str(ticket_id),
        "conteudo":  dados.conteudo,
    })
    return {"ok": True}
