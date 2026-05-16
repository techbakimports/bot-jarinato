import json
import os
import urllib.request

TOKEN = os.environ.get("TYPEBOT_TOKEN", "")
TYPEBOT_ID = os.environ.get("TYPEBOT_ID", "")
START_EVENT_ID = os.environ.get("TYPEBOT_START_EVENT_ID", "")

flow = {
    "name": "Atendimento TechBak",
    "groups": [
        {
            "id": "grp_saudacao",
            "title": "Saudacao",
            "graphCoordinates": {"x": 400, "y": 0},
            "blocks": [
                {
                    "id": "blk_s1",
                    "type": "text",
                    "content": {
                        "richText": [
                            {"type": "p", "children": [
                                {"text": "Olá! 👋 Bem-vindo ao suporte da "},
                                {"bold": True, "text": "TechBak Imports"},
                                {"text": "."}
                            ]}
                        ]
                    }
                },
                {
                    "id": "blk_s2",
                    "type": "text",
                    "content": {
                        "richText": [
                            {"type": "p", "children": [
                                {"text": "Vou coletar algumas informações para conectar você com nosso time de atendimento. 😊"}
                            ]}
                        ]
                    }
                }
            ]
        },
        {
            "id": "grp_nome",
            "title": "Nome do cliente",
            "graphCoordinates": {"x": 750, "y": 0},
            "blocks": [
                {
                    "id": "blk_n1",
                    "type": "text",
                    "content": {
                        "richText": [
                            {"type": "p", "children": [{"text": "Qual é o seu nome?"}]}
                        ]
                    }
                },
                {
                    "id": "blk_n2",
                    "type": "text input",
                    "options": {
                        "variableId": "var_nome",
                        "labels": {"placeholder": "Digite seu nome...", "button": "Enviar"},
                        "isLong": False
                    }
                }
            ]
        },
        {
            "id": "grp_motivo",
            "title": "Motivo do contato",
            "graphCoordinates": {"x": 1100, "y": 0},
            "blocks": [
                {
                    "id": "blk_m1",
                    "type": "text",
                    "content": {
                        "richText": [
                            {"type": "p", "children": [{"text": "Como podemos te ajudar hoje?"}]}
                        ]
                    }
                },
                {
                    "id": "blk_m2",
                    "type": "choice input",
                    "items": [
                        {"id": "it1", "content": "📦 Rastreamento de pedido"},
                        {"id": "it2", "content": "🔧 Suporte técnico"},
                        {"id": "it3", "content": "💰 Financeiro / Pagamento"},
                        {"id": "it4", "content": "❓ Outra dúvida"}
                    ],
                    "options": {
                        "buttonAlignment": "left",
                        "isMultipleChoice": False,
                        "isSearchable": False
                    }
                }
            ]
        },
        {
            "id": "grp_aguardar",
            "title": "Abrindo ticket",
            "graphCoordinates": {"x": 1450, "y": 0},
            "blocks": [
                {
                    "id": "blk_a1",
                    "type": "text",
                    "content": {
                        "richText": [
                            {"type": "p", "children": [
                                {"text": "⏳ Aguarde um momento, estou abrindo seu atendimento..."}
                            ]}
                        ]
                    }
                }
            ]
        },
        {
            "id": "grp_webhook",
            "title": "Webhook FastAPI",
            "graphCoordinates": {"x": 1800, "y": 0},
            "blocks": [
                {
                    "id": "blk_w1",
                    "type": "Webhook",
                    "options": {
                        "url": "http://fastapi:8000/tickets/transbordo",
                        "method": "POST",
                        "headers": [{"id": "h1", "key": "Content-Type", "value": "application/json"}],
                        "isCustomBody": True,
                        "body": "{\"remoteJid\": \"{{Contact ID}}\", \"nome\": \"{{nome_cliente}}\"}",
                        "responseVariableMapping": []
                    }
                }
            ]
        },
        {
            "id": "grp_fim",
            "title": "Confirmacao",
            "graphCoordinates": {"x": 2150, "y": 0},
            "blocks": [
                {
                    "id": "blk_f1",
                    "type": "text",
                    "content": {
                        "richText": [
                            {"type": "p", "children": [
                                {"text": "✅ Pronto, "},
                                {"bold": True, "text": "{{nome_cliente}}"},
                                {"text": "! Um atendente foi notificado e vai te responder em breve."}
                            ]}
                        ]
                    }
                },
                {
                    "id": "blk_f2",
                    "type": "text",
                    "content": {
                        "richText": [
                            {"type": "p", "children": [
                                {"text": "🕐 Horário de atendimento: segunda a sexta, das 8h às 18h."}
                            ]}
                        ]
                    }
                }
            ]
        }
    ],
    "edges": [
        {"id": "e0", "from": {"eventId": START_EVENT_ID}, "to": {"groupId": "grp_saudacao"}},
        {"id": "e1", "from": {"groupId": "grp_saudacao", "blockId": "blk_s2"}, "to": {"groupId": "grp_nome"}},
        {"id": "e2", "from": {"groupId": "grp_nome", "blockId": "blk_n2"}, "to": {"groupId": "grp_motivo"}},
        {"id": "e3", "from": {"groupId": "grp_motivo", "blockId": "blk_m2", "itemId": "it1"}, "to": {"groupId": "grp_aguardar"}},
        {"id": "e4", "from": {"groupId": "grp_motivo", "blockId": "blk_m2", "itemId": "it2"}, "to": {"groupId": "grp_aguardar"}},
        {"id": "e5", "from": {"groupId": "grp_motivo", "blockId": "blk_m2", "itemId": "it3"}, "to": {"groupId": "grp_aguardar"}},
        {"id": "e6", "from": {"groupId": "grp_motivo", "blockId": "blk_m2", "itemId": "it4"}, "to": {"groupId": "grp_aguardar"}},
        {"id": "e7", "from": {"groupId": "grp_aguardar", "blockId": "blk_a1"}, "to": {"groupId": "grp_webhook"}},
        {"id": "e8", "from": {"groupId": "grp_webhook", "blockId": "blk_w1"}, "to": {"groupId": "grp_fim"}}
    ],
    "variables": [
        {"id": "var_nome", "name": "nome_cliente"},
        {"id": "var_cid", "name": "Contact ID"},
        {"id": "var_cname", "name": "Contact Name"},
        {"id": "var_cphone", "name": "Contact Phone Number"}
    ]
}

payload = json.dumps({"typebot": flow}).encode()
req = urllib.request.Request(
    f"http://localhost:3001/api/v1/typebots/{TYPEBOT_ID}",
    data=payload,
    method="PATCH",
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
)
try:
    with urllib.request.urlopen(req) as r:
        body = r.read().decode()
        print("STATUS:", r.status)
        print("RESP:", body[:500])
except urllib.error.HTTPError as e:
    print("HTTP ERROR:", e.code)
    print(e.read().decode()[:500])
