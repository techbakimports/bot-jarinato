import httpx
from app.config import settings


async def enviar_mensagem(remote_jid: str, texto: str) -> dict:
    url = f"{settings.evolution_url}/message/sendText/{settings.evolution_instance}"
    headers = {"apikey": settings.evolution_api_key}
    payload = {
        "number": remote_jid,
        "text": texto,
        "delay": 1200,
    }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(url, json=payload, headers=headers)
        r.raise_for_status()
        return r.json()
