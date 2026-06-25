"""
Router para configuração simplificada do bot.

Salva a config em bot_config.json local e atualiza o fluxo do Typebot
via API PATCH quando solicitado.
"""

import json
import os
from pathlib import Path
from typing import Optional
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import settings

router = APIRouter(prefix="/bot", tags=["bot-config"])

CONFIG_FILE = Path(__file__).resolve().parent.parent.parent / "bot_config.json"

# ── Schemas ──────────────────────────────────────────────────────────────────

class KnowledgeEntry(BaseModel):
    id: str
    title: str
    tags: list[str]
    answer: str

class MenuOption(BaseModel):
    id: str
    emoji: str
    label: str

class BotConfig(BaseModel):
    company_name: str = "TechBak Imports"
    welcome_message: str = "Olá! 👋 Bem-vindo ao suporte da *TechBak Imports*.\nVou coletar algumas informações para conectar você com nosso time de atendimento. 😊"
    ask_name_message: str = "Qual é o seu nome?"
    menu_message: str = "Como podemos te ajudar hoje?"
    menu_options: list[MenuOption] = [
        MenuOption(id="it1", emoji="📦", label="Rastreamento de pedido"),
        MenuOption(id="it2", emoji="🔧", label="Suporte técnico"),
        MenuOption(id="it3", emoji="💰", label="Financeiro / Pagamento"),
        MenuOption(id="it4", emoji="❓", label="Outra dúvida"),
    ]
    waiting_message: str = "⏳ Aguarde um momento, estou abrindo seu atendimento..."
    confirmation_message: str = "✅ Pronto, {nome}! Um atendente foi notificado e vai te responder em breve."
    business_hours: str = "Segunda a Sexta, das 8h às 18h"
    knowledge_base: list[KnowledgeEntry] = []

class TypebotSyncRequest(BaseModel):
    typebot_url: Optional[str] = None
    typebot_token: Optional[str] = None
    typebot_id: Optional[str] = None
    start_event_id: Optional[str] = None

# ── Helpers ──────────────────────────────────────────────────────────────────

def _load_config() -> dict:
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    return BotConfig().model_dump()

def _save_config(data: dict):
    tmp = CONFIG_FILE.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp.replace(CONFIG_FILE)

def _build_typebot_flow(cfg: BotConfig, start_event_id: str, fastapi_internal_url: str = "http://fastapi:8000") -> dict:
    """Monta o JSON do fluxo Typebot a partir da config simplificada."""

    # Grupo 1 — Saudação
    welcome_lines = cfg.welcome_message.split("\n")
    welcome_blocks = []
    for i, line in enumerate(welcome_lines):
        if not line.strip():
            continue
        welcome_blocks.append({
            "id": f"blk_s{i+1}",
            "type": "text",
            "content": {
                "richText": [{"type": "p", "children": [{"text": line.strip()}]}]
            }
        })

    groups = [
        {
            "id": "grp_saudacao",
            "title": "Saudacao",
            "graphCoordinates": {"x": 400, "y": 0},
            "blocks": welcome_blocks or [{
                "id": "blk_s1",
                "type": "text",
                "content": {"richText": [{"type": "p", "children": [{"text": cfg.welcome_message}]}]}
            }],
        },
        {
            "id": "grp_nome",
            "title": "Nome do cliente",
            "graphCoordinates": {"x": 750, "y": 0},
            "blocks": [
                {
                    "id": "blk_n1",
                    "type": "text",
                    "content": {"richText": [{"type": "p", "children": [{"text": cfg.ask_name_message}]}]},
                },
                {
                    "id": "blk_n2",
                    "type": "text input",
                    "options": {
                        "variableId": "var_nome",
                        "labels": {"placeholder": "Digite seu nome...", "button": "Enviar"},
                        "isLong": False,
                    },
                },
            ],
        },
    ]

    # Grupo 3 — Menu de motivos (dinâmico)
    menu_items = [
        {"id": opt.id, "content": f"{opt.emoji} {opt.label}"}
        for opt in cfg.menu_options
    ]
    groups.append({
        "id": "grp_motivo",
        "title": "Motivo do contato",
        "graphCoordinates": {"x": 1100, "y": 0},
        "blocks": [
            {
                "id": "blk_m1",
                "type": "text",
                "content": {"richText": [{"type": "p", "children": [{"text": cfg.menu_message}]}]},
            },
            {
                "id": "blk_m2",
                "type": "choice input",
                "items": menu_items,
                "options": {
                    "variableId": "var_motivo",
                    "buttonAlignment": "left",
                    "isMultipleChoice": False,
                    "isSearchable": False,
                },
            },
        ],
    })

    # Grupo 4 — Aguardando
    groups.append({
        "id": "grp_aguardar",
        "title": "Abrindo ticket",
        "graphCoordinates": {"x": 1450, "y": 0},
        "blocks": [{
            "id": "blk_a1",
            "type": "text",
            "content": {"richText": [{"type": "p", "children": [{"text": cfg.waiting_message}]}]},
        }],
    })

    # Grupo 5 — Webhook (agora com motivo!)
    webhook_body = json.dumps({
        "remoteJid": "{{Contact ID}}",
        "nome": "{{nome_cliente}}",
        "motivo": "{{motivo_contato}}"
    })
    groups.append({
        "id": "grp_webhook",
        "title": "Webhook FastAPI",
        "graphCoordinates": {"x": 1800, "y": 0},
        "blocks": [{
            "id": "blk_w1",
            "type": "Webhook",
            "options": {
                "url": f"{fastapi_internal_url}/tickets/transbordo",
                "method": "POST",
                "headers": [{"id": "h1", "key": "Content-Type", "value": "application/json"}],
                "isCustomBody": True,
                "body": webhook_body,
                "responseVariableMapping": [],
            },
        }],
    })

    # Grupo 6 — Confirmação
    confirm_text = cfg.confirmation_message.replace("{nome}", "{{nome_cliente}}")
    groups.append({
        "id": "grp_fim",
        "title": "Confirmacao",
        "graphCoordinates": {"x": 2150, "y": 0},
        "blocks": [
            {
                "id": "blk_f1",
                "type": "text",
                "content": {"richText": [{"type": "p", "children": [
                    {"text": confirm_text},
                ]}]},
            },
            {
                "id": "blk_f2",
                "type": "text",
                "content": {"richText": [{"type": "p", "children": [
                    {"text": f"🕐 Horário de atendimento: {cfg.business_hours}"},
                ]}]},
            },
        ],
    })

    last_welcome_block_id = welcome_blocks[-1]["id"] if welcome_blocks else groups[0]["blocks"][-1]["id"]

    # Edges — conectam os grupos em sequência
    edges = [
        {"id": "e0", "from": {"eventId": start_event_id}, "to": {"groupId": "grp_saudacao"}},
        {"id": "e1", "from": {"groupId": "grp_saudacao", "blockId": last_welcome_block_id}, "to": {"groupId": "grp_nome"}},
        {"id": "e2", "from": {"groupId": "grp_nome", "blockId": "blk_n2"}, "to": {"groupId": "grp_motivo"}},
    ]
    # Cada opção do menu leva ao mesmo grupo "aguardar"
    for i, opt in enumerate(cfg.menu_options):
        edges.append({
            "id": f"e{3+i}",
            "from": {"groupId": "grp_motivo", "blockId": "blk_m2", "itemId": opt.id},
            "to": {"groupId": "grp_aguardar"},
        })
    edge_idx = 3 + len(cfg.menu_options)
    edges.append({"id": f"e{edge_idx}", "from": {"groupId": "grp_aguardar", "blockId": "blk_a1"}, "to": {"groupId": "grp_webhook"}})
    edges.append({"id": f"e{edge_idx+1}", "from": {"groupId": "grp_webhook", "blockId": "blk_w1"}, "to": {"groupId": "grp_fim"}})

    variables = [
        {"id": "var_nome", "name": "nome_cliente"},
        {"id": "var_motivo", "name": "motivo_contato"},
        {"id": "var_cid", "name": "Contact ID"},
        {"id": "var_cname", "name": "Contact Name"},
        {"id": "var_cphone", "name": "Contact Phone Number"},
    ]

    return {
        "name": f"Atendimento {cfg.company_name}",
        "groups": groups,
        "edges": edges,
        "variables": variables,
    }

# ── Endpoints ────────────────────────────────────────────────────────────────

@router.get("/config")
async def get_config():
    """Retorna a configuração atual do bot."""
    return _load_config()


@router.post("/config")
async def save_config(cfg: BotConfig):
    """Salva a configuração do bot localmente."""
    _save_config(cfg.model_dump())
    return {"status": "ok", "message": "Configuração salva com sucesso."}


@router.post("/config/sync-typebot")
async def sync_typebot(req: TypebotSyncRequest):
    """
    Salva + aplica a config no Typebot via API PATCH.
    Usa variáveis de ambiente como fallback para os parâmetros de conexão.
    """
    cfg_data = _load_config()
    cfg = BotConfig(**cfg_data)

    typebot_url = req.typebot_url or settings.typebot_builder_url
    typebot_token = req.typebot_token or (settings.typebot_token or "")
    typebot_id = req.typebot_id or (settings.typebot_id or "")
    start_event_id = req.start_event_id or (settings.typebot_start_event_id or "")

    if not typebot_token or not typebot_id or not start_event_id:
        raise HTTPException(
            status_code=400,
            detail="Faltam credenciais do Typebot. Defina TYPEBOT_TOKEN, TYPEBOT_ID e TYPEBOT_START_EVENT_ID no .env ou envie no body."
        )

    flow = _build_typebot_flow(cfg, start_event_id, typebot_url)
    api_url = f"{typebot_url}/api/v1/typebots/{typebot_id}"

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.patch(
                api_url,
                json={"typebot": flow},
                headers={"Authorization": f"Bearer {typebot_token}"},
            )
        if resp.is_error:
            raise HTTPException(status_code=502, detail=f"Erro ao atualizar Typebot ({resp.status_code}): {resp.text[:500]}")
        return {
            "status": "ok",
            "message": "Fluxo atualizado no Typebot com sucesso!",
            "typebot_status": resp.status_code,
            "response": resp.text[:300],
        }
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Erro de conexão com Typebot: {str(e)}")
