#!/usr/bin/env node
'use strict';

/**
 * Fase 2 — Configuração da Comunicação
 *
 * Uso:
 *   node setup.js instance   → cria instância e exibe QR Code para escanear
 *   node setup.js status     → verifica se o WhatsApp está conectado
 *   node setup.js typebot    → configura integração com Typebot
 *   node setup.js webhook    → configura webhook para o FastAPI (Fase 3)
 *   node setup.js all        → executa tudo em sequência (exceto QR Code)
 */

const fs   = require('fs');
const path = require('path');

// ─── Carrega .env ─────────────────────────────────────────────────────────────
function loadEnv() {
  const envPath = path.join(__dirname, '../.env');
  if (!fs.existsSync(envPath)) {
    die('Arquivo infra/.env não encontrado.\nCopie infra/.env.example → infra/.env e preencha os valores.');
  }
  const env = {};
  for (const line of fs.readFileSync(envPath, 'utf8').split('\n')) {
    const t = line.trim();
    if (!t || t.startsWith('#')) continue;
    const idx = t.indexOf('=');
    if (idx === -1) continue;
    env[t.slice(0, idx).trim()] = t.slice(idx + 1).trim();
  }
  return env;
}

const ENV = loadEnv();

const BASE_URL      = (ENV.EVOLUTION_SERVER_URL || 'http://localhost:8080').replace(/\/$/, '');
const API_KEY       = ENV.EVOLUTION_API_KEY       || '';
const INSTANCE_NAME = ENV.EVOLUTION_INSTANCE_NAME || 'techbak';
const TYPEBOT_URL   = ENV.TYPEBOT_VIEWER_URL       || 'http://localhost:3002';
const TYPEBOT_FLOW  = ENV.TYPEBOT_FLOW_ID          || '';
const FASTAPI_URL   = (ENV.FASTAPI_URL            || 'http://localhost:8000').replace(/\/$/, '');

// ─── Utilitários ──────────────────────────────────────────────────────────────
function die(msg) {
  console.error(`\n❌  ${msg}\n`);
  process.exit(1);
}

function ok(msg)   { console.log(`✅  ${msg}`); }
function info(msg) { console.log(`ℹ️   ${msg}`); }
function warn(msg) { console.log(`⚠️   ${msg}`); }
function sep()     { console.log('─'.repeat(60)); }

async function api(method, endpoint, body) {
  const url = `${BASE_URL}${endpoint}`;
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json', 'apikey': API_KEY },
  };
  if (body) opts.body = JSON.stringify(body);

  let res;
  try {
    res = await fetch(url, opts);
  } catch (e) {
    die(`Não foi possível conectar à Evolution API em ${BASE_URL}\n   Verifique se os containers estão rodando: docker compose ps`);
  }

  const text = await res.text();
  try {
    return { status: res.status, body: JSON.parse(text) };
  } catch {
    return { status: res.status, body: text };
  }
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// ─── Exibe QR Code no terminal ────────────────────────────────────────────────
function printQr(qrString) {
  try {
    // qrcode-terminal está no node_modules do projeto pai
    const qr = require(path.join(__dirname, '../../node_modules/qrcode-terminal'));
    console.log('\n📱  Escaneie o QR Code abaixo com o WhatsApp:\n');
    qr.generate(qrString, { small: true });
    console.log('\n   O QR Code expira em ~60 segundos. Se expirar, rode: node setup.js instance\n');
  } catch {
    // Fallback: mostra a string bruta (pode ser decodificada em https://qr-code-generator.com)
    warn('qrcode-terminal não encontrado. Cole o código abaixo em qualquer gerador de QR online:');
    console.log('\n' + qrString + '\n');
  }
}

// ─── Comandos ─────────────────────────────────────────────────────────────────

async function cmdInstance() {
  sep();
  info('Criando instância na Evolution API...');

  // Verifica se já existe
  const list = await api('GET', '/instance/fetchInstances');
  const exists = Array.isArray(list.body) && list.body.some(i => i.instance?.instanceName === INSTANCE_NAME);

  if (!exists) {
    const create = await api('POST', '/instance/create', {
      instanceName:    INSTANCE_NAME,
      qrcode:          true,
      integration:     'WHATSAPP-BAILEYS',
      token:           `${INSTANCE_NAME}_token`,
    });

    if (create.status !== 201 && create.status !== 200) {
      die(`Falha ao criar instância (HTTP ${create.status}):\n${JSON.stringify(create.body, null, 2)}`);
    }
    ok(`Instância "${INSTANCE_NAME}" criada.`);
  } else {
    info(`Instância "${INSTANCE_NAME}" já existe.`);
  }

  // Solicita QR Code
  info('Solicitando QR Code...');
  const conn = await api('GET', `/instance/connect/${INSTANCE_NAME}`);

  if (conn.status !== 200) {
    // Já pode estar conectado
    const state = await api('GET', `/instance/connectionState/${INSTANCE_NAME}`);
    if (state.body?.instance?.state === 'open') {
      ok('WhatsApp já está conectado! Não é necessário escanear o QR Code.');
      return;
    }
    die(`Falha ao obter QR Code (HTTP ${conn.status}):\n${JSON.stringify(conn.body, null, 2)}`);
  }

  const qr = conn.body?.base64 || conn.body?.qrcode || conn.body?.code;
  if (!qr) {
    die(`QR Code não retornado. Resposta: ${JSON.stringify(conn.body, null, 2)}`);
  }

  // Remove prefixo data:image/... se vier como base64 de imagem
  const qrString = qr.replace(/^data:image\/[^;]+;base64,/, '');
  printQr(qrString);

  // Aguarda conexão
  info('Aguardando escaneamento do QR Code...');
  for (let i = 0; i < 30; i++) {
    await sleep(3000);
    const state = await api('GET', `/instance/connectionState/${INSTANCE_NAME}`);
    const s = state.body?.instance?.state;
    if (s === 'open') {
      ok('WhatsApp conectado com sucesso!');
      return;
    }
    process.stdout.write(`   Aguardando... (${(i + 1) * 3}s)\r`);
  }
  warn('Timeout. Rode "node setup.js status" para verificar a conexão depois.');
}

async function cmdStatus() {
  sep();
  info(`Verificando estado da instância "${INSTANCE_NAME}"...`);
  const state = await api('GET', `/instance/connectionState/${INSTANCE_NAME}`);

  if (state.status === 404) {
    warn('Instância não encontrada. Rode: node setup.js instance');
    return;
  }

  const s = state.body?.instance?.state;
  if (s === 'open') {
    ok('WhatsApp conectado (open).');
  } else {
    warn(`Estado atual: ${s || 'desconhecido'}. Para reconectar: node setup.js instance`);
  }
}

async function cmdTypebot() {
  sep();
  if (!TYPEBOT_FLOW) {
    die(
      'Variável TYPEBOT_FLOW_ID não definida no .env.\n\n' +
      '   Passos para obter o ID:\n' +
      '   1. Acesse o Typebot Builder: ' + TYPEBOT_URL.replace(':3002', ':3001') + '\n' +
      '   2. Crie um fluxo de boas-vindas/triagem\n' +
      '   3. Vá em Configurações → Geral → copie o "Public ID" do fluxo\n' +
      '   4. Adicione ao .env: TYPEBOT_FLOW_ID=o_id_copiado\n' +
      '   5. Rode este comando novamente.'
    );
  }

  info(`Configurando Typebot na instância "${INSTANCE_NAME}"...`);
  info(`  Viewer URL : ${TYPEBOT_URL}`);
  info(`  Flow ID    : ${TYPEBOT_FLOW}`);

  // Remove configuração antiga (se houver) para evitar conflito
  await api('DELETE', `/typebot/delete/${INSTANCE_NAME}`);

  const r = await api('POST', `/typebot/create/${INSTANCE_NAME}`, {
    enabled:          true,
    url:              TYPEBOT_URL,
    typebot:          TYPEBOT_FLOW,
    triggerType:      'all',          // toda mensagem nova dispara o fluxo
    expire:           20,             // minutos de inatividade antes de reiniciar
    keywordFinish:    '#encerrar',    // palavra que fecha o bot e passa para humano
    delayMessage:     1200,           // ms de delay entre mensagens (simula digitação)
    unknownMessage:   'Desculpe, não entendi. Pode repetir?',
    listeningFromMe:  false,
  });

  if (r.status !== 201 && r.status !== 200) {
    die(`Falha ao configurar Typebot (HTTP ${r.status}):\n${JSON.stringify(r.body, null, 2)}`);
  }

  ok('Typebot configurado! Toda mensagem nova será redirecionada ao fluxo.');
  info('Para pausar o Typebot de um contato específico, use:');
  info('  POST /typebot/changeStatus/{instance}  body: { remoteJid, status: "paused" }');
}

async function cmdWebhook() {
  sep();
  const webhookUrl = `${FASTAPI_URL}/webhook`;
  info(`Configurando webhook para o FastAPI...`);
  info(`  URL destino: ${webhookUrl}`);

  const r = await api('POST', `/webhook/set/${INSTANCE_NAME}`, {
    webhook: {
      enabled:  true,
      url:      webhookUrl,
      byEvents: false,
      base64:   false,
      events: [
        'MESSAGES_UPSERT',      // nova mensagem recebida
        'MESSAGES_UPDATE',      // mensagem atualizada (lida, entregue)
        'SEND_MESSAGE',         // mensagem enviada pelo bot
        'CONNECTION_UPDATE',    // mudança de estado da conexão
      ],
    },
  });

  if (r.status !== 200 && r.status !== 201) {
    die(`Falha ao configurar webhook (HTTP ${r.status}):\n${JSON.stringify(r.body, null, 2)}`);
  }

  ok(`Webhook configurado em ${webhookUrl}`);
  warn('O FastAPI ainda não existe (Fase 3). O webhook ficará ativo mas não encontrará o destino até lá.');
}

// ─── Entry point ──────────────────────────────────────────────────────────────
async function main() {
  const cmd = process.argv[2];

  console.log('\n🤖  TechBak — Configuração da Fase 2');
  console.log(`    Evolution API: ${BASE_URL}`);
  console.log(`    Instância    : ${INSTANCE_NAME}`);
  sep();

  switch (cmd) {
    case 'instance': await cmdInstance(); break;
    case 'status':   await cmdStatus();   break;
    case 'typebot':  await cmdTypebot();  break;
    case 'webhook':  await cmdWebhook();  break;
    case 'all':
      await cmdInstance();
      await cmdTypebot();
      await cmdWebhook();
      break;
    default:
      console.log(`
Comandos disponíveis:
  node setup.js instance   → conecta WhatsApp via QR Code
  node setup.js status     → verifica estado da conexão
  node setup.js typebot    → vincula fluxo do Typebot
  node setup.js webhook    → configura webhook para o FastAPI
  node setup.js all        → instance + typebot + webhook em sequência
`);
  }

  sep();
}

main().catch(e => { console.error(e); process.exit(1); });
