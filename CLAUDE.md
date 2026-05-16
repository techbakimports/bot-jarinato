# bot-what

## Objetivo
Bot de atendimento WhatsApp com painel web para atendentes. Integra Baileys (WhatsApp direto) com Evolution API, Typebot (fluxos visuais), FastAPI (backend), Vue.js (painel) e PostgreSQL.

## Stack
- **Bot WhatsApp**: Node.js (CommonJS) + Baileys 7.x
- **Backend API**: Python 3.12 + FastAPI + SQLAlchemy (async)
- **Frontend Painel**: Vue.js 3 + Tailwind CSS (SPA, servido via Nginx)
- **Infra**: Docker Compose (9 serviços)
- **Banco**: PostgreSQL 16 (3 instâncias: evolution, typebot, tickets_db) + Redis 7
- **Integrações**: Evolution API v2.2.3, Typebot builder/viewer, Odoo (opcional), SMTP

## Comandos — Bot (raiz)
```bash
npm start          # Inicia bot Baileys (src/index.js)
```

## Comandos — Infraestrutura
```bash
cd infra
npm run instance   # Cria instância Evolution API + QR WhatsApp
npm run status     # Verifica conexão
npm run typebot    # Configura fluxo Typebot
npm run webhook    # Registra webhook no FastAPI
npm run all        # Executa tudo em sequência

docker compose up -d    # Sobe todos os 9 serviços
docker compose down     # Para tudo
```

## Variáveis de ambiente (infra/.env — 27 variáveis)
```
EVOLUTION_SERVER_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME
TYPEBOT_BUILDER_URL, TYPEBOT_VIEWER_URL, TYPEBOT_SECRET, TYPEBOT_FLOW_ID
SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD
POSTGRES_EVOLUTION_PASSWORD, POSTGRES_TYPEBOT_PASSWORD, POSTGRES_APP_PASSWORD
REDIS_PASSWORD
FASTAPI_URL, JWT_SECRET, PAINEL_URL
ODOO_URL, ODOO_DB, ODOO_USER, ODOO_PASSWORD   # opcional
```

## Arquitetura do atendimento
```
WhatsApp → Baileys (bot) → state machine → ticket JSON local
         → Evolution API → Typebot → POST /tickets/transbordo → FastAPI → PostgreSQL
                                                              → WebSocket → Painel Vue.js
```

## Endpoints FastAPI principais
- `POST /auth/login` — token JWT
- `POST /tickets/transbordo` — cria ticket vindo do Typebot
- `GET /tickets` — lista com filtros
- `POST /tickets/{id}/assumir` — atendente assume
- `WebSocket /ws` — chat live
- `POST /webhook/` — recebe eventos da Evolution API

## Regras
- `auth_info/` contém credenciais WhatsApp da sessão Baileys — nunca commitar (no .gitignore)
- `data/sessions.json` e `data/tickets.json` são fallback local — não são a fonte de verdade em produção
- Os 3 bancos PostgreSQL são isolados: não misturar schemas
- Odoo é integração opcional — o bot funciona sem ela
