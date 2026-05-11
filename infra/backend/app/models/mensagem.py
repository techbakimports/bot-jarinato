import uuid
from sqlalchemy import Column, String, Boolean, BigInteger, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class Mensagem(Base):
    __tablename__ = "mensagens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.id"), nullable=False, index=True)
    conteudo = Column(String, nullable=False)
    de_cliente = Column(Boolean, nullable=False)  # True = cliente enviou, False = atendente/bot
    timestamp_wa = Column(BigInteger, nullable=True)  # timestamp original do WhatsApp
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    ticket = relationship("Ticket", back_populates="mensagens")
