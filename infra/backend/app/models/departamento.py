import uuid
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class Departamento(Base):
    __tablename__ = "departamentos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
