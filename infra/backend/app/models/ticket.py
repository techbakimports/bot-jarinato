import uuid
import enum
from sqlalchemy import Column, String, Integer, Enum, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database import Base


class TicketStatus(str, enum.Enum):
    aguardando     = "aguardando"
    em_atendimento = "em_atendimento"
    encerrado      = "encerrado"


class Ticket(Base):
    __tablename__ = "tickets"

    id             = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    remote_jid     = Column(String(100), nullable=False, index=True)
    nome_cliente   = Column(String(150), nullable=True)
    status         = Column(Enum(TicketStatus), default=TicketStatus.aguardando, nullable=False)
    atendente_id   = Column(UUID(as_uuid=True), ForeignKey("atendentes.id"), nullable=True)
    departamento_id= Column(UUID(as_uuid=True), ForeignKey("departamentos.id"), nullable=True)

    # Dados do Odoo (preenchidos no transbordo, se integração ativa)
    odoo_partner_id = Column(Integer, nullable=True)
    odoo_dados      = Column(JSONB, nullable=True)  # nome, cpf_cnpj, email, pedidos, etc.

    created_at  = Column(DateTime(timezone=True), server_default=func.now())
    updated_at  = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    encerrado_at= Column(DateTime(timezone=True), nullable=True)

    atendente = relationship("Atendente", back_populates="tickets")
    mensagens = relationship("Mensagem", back_populates="ticket", order_by="Mensagem.created_at")
