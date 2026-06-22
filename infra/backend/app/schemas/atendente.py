from pydantic import BaseModel
from uuid import UUID


class AtendenteLogin(BaseModel):
    email: str
    senha: str


class AtendenteOut(BaseModel):
    id: UUID
    nome: str
    email: str
    ativo: bool

    model_config = {"from_attributes": True}


class AtendenteRegister(BaseModel):
    nome: str
    email: str
    senha: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    atendente: AtendenteOut
