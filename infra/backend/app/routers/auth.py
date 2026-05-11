from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt
from passlib.context import CryptContext
from app.database import get_db
from app.models.atendente import Atendente
from app.schemas.atendente import AtendenteLogin, AtendenteOut, TokenOut
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _criar_token(atendente_id: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expire_minutes)
    return jwt.encode(
        {"sub": atendente_id, "exp": expire},
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


@router.post("/login", response_model=TokenOut)
async def login(dados: AtendenteLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Atendente).where(Atendente.email == dados.email))
    atendente = result.scalar_one_or_none()

    if not atendente or not pwd_ctx.verify(dados.senha, atendente.senha_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    if not atendente.ativo:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Conta inativa")

    return TokenOut(
        access_token=_criar_token(str(atendente.id)),
        atendente=AtendenteOut.model_validate(atendente),
    )
