from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # FastAPI / banco
    database_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 480

    # Evolution API
    evolution_url: str
    evolution_api_key: str
    evolution_instance: str

    # Odoo (opcional — deixar em branco para desabilitar)
    odoo_url: Optional[str] = None
    odoo_db: Optional[str] = None
    odoo_user: Optional[str] = None
    odoo_password: Optional[str] = None

    # Typebot (para sincronização do fluxo via painel)
    typebot_builder_url: str = "http://localhost:3001"
    typebot_token: Optional[str] = None
    typebot_id: Optional[str] = None
    typebot_start_event_id: Optional[str] = None

    # SMTP para notificações (opcional — deixar em branco para desabilitar)
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_from: str = "noreply@techbak.com"
    notif_email_destino: Optional[str] = None  # e-mail que recebe alertas de novo ticket
    painel_url: str = "http://localhost"        # URL do painel (usada no corpo do e-mail)

    class Config:
        env_file = ".env"


settings = Settings()
