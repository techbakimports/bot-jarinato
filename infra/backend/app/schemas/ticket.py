from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Any
from app.models.ticket import TicketStatus


class TicketOut(BaseModel):
    id:            UUID
    remote_jid:    str
    nome_cliente:  Optional[str]
    status:        TicketStatus
    atendente_id:  Optional[UUID]
    odoo_dados:    Optional[Any] = None
    created_at:    datetime
    updated_at:    datetime

    model_config = {"from_attributes": True}


class AssumirTicket(BaseModel):
    atendente_id: UUID


class TransbordoPayload(BaseModel):
    remoteJid: str
    nome:      Optional[str] = None
