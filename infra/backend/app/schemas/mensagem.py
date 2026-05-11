from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class MensagemOut(BaseModel):
    id: UUID
    ticket_id: UUID
    conteudo: str
    de_cliente: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class MensagemEnviar(BaseModel):
    conteudo: str
