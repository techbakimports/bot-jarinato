require('dotenv').config();
const stateManager = require('./stateManager');
const { createTicket } = require('./ticketManager');
const { search } = require('./knowledgeBase');

const COMPANY = process.env.COMPANY_NAME || 'TechBak Imports';
const HOURS   = process.env.BUSINESS_HOURS || 'Segunda a Sexta, das 9h às 18h';

async function send(sock, jid, text) {
    await sock.sendMessage(jid, { text });
}

function welcomeText(name) {
    return (
        `Olá, *${name}*! 👋\n\n` +
        `Bem-vindo ao suporte técnico da *${COMPANY}*.\n\n` +
        `Descreva o problema que está enfrentando e vou tentar te ajudar.\n\n` +
        `_Ex: "meu computador não liga", "internet caiu", "tela azul"..._`
    );
}

function feedbackText() {
    return `\nIsso resolveu o problema?\n\n1️⃣  Sim, resolveu!\n2️⃣  Não resolveu — quero abrir um chamado`;
}

function noAnswerText() {
    return (
        `Não encontrei uma solução automática para isso. 🤔\n\n` +
        `O que deseja fazer?\n\n` +
        `1️⃣  Abrir um chamado de suporte\n` +
        `2️⃣  Tentar descrever o problema de outro jeito`
    );
}

// ─────────────────────────────────────────────
// Handlers de estado
// ─────────────────────────────────────────────

async function onWaitingDescription(sock, jid, text, name) {
    const entry = search(text);

    if (entry) {
        stateManager.set(jid, { step: 'WAITING_FEEDBACK', context: { description: text, name } });
        await send(sock, jid, entry.answer + '\n\n' + feedbackText());
    } else {
        stateManager.set(jid, { step: 'WAITING_NO_ANSWER', context: { description: text, name } });
        await send(sock, jid, noAnswerText());
    }
}

async function onWaitingFeedback(sock, jid, text, state) {
    const { description, name } = state.context;

    switch (text.trim()) {
        case '1':
            stateManager.remove(jid);
            await send(sock, jid,
                `Ótimo! Fico feliz que tenha resolvido. 😊\n\n` +
                `Se precisar de mais ajuda, é só chamar!`
            );
            break;

        case '2': {
            const ticketId = createTicket(jid, name, description);
            stateManager.remove(jid);
            await send(sock, jid,
                `✅ *Chamado aberto!*\n\n` +
                `📋 Ticket: *${ticketId}*\n\n` +
                `Nossa equipe entrará em contato em breve.\n` +
                `⏰ Horário de atendimento: ${HOURS}\n\n` +
                `Guarde o número do ticket para acompanhamento.`
            );
            break;
        }

        default:
            await send(sock, jid, `Por favor, digite *1* ou *2*.`);
    }
}

async function onWaitingNoAnswer(sock, jid, text, state) {
    const { description, name } = state.context;

    switch (text.trim()) {
        case '1': {
            const ticketId = createTicket(jid, name, description);
            stateManager.remove(jid);
            await send(sock, jid,
                `✅ *Chamado aberto!*\n\n` +
                `📋 Ticket: *${ticketId}*\n\n` +
                `Nossa equipe entrará em contato em breve.\n` +
                `⏰ Horário de atendimento: ${HOURS}\n\n` +
                `Guarde o número do ticket para acompanhamento.`
            );
            break;
        }

        case '2':
            stateManager.set(jid, { step: 'WAITING_DESCRIPTION' });
            await send(sock, jid,
                `Tudo bem! Tente descrever o problema com outras palavras.\n\n` +
                `_Ex: "o monitor fica preto", "a internet cai toda hora", "aparece uma mensagem de erro"..._`
            );
            break;

        default:
            await send(sock, jid, `Por favor, digite *1* ou *2*.`);
    }
}

// ─────────────────────────────────────────────
// Entrada principal
// ─────────────────────────────────────────────

async function handleMessage(sock, m) {
    const jid  = m.key.remoteJid;
    const text = (m.message?.conversation || m.message?.extendedTextMessage?.text || '').trim();
    const name = m.pushName || 'usuário';

    if (!jid.endsWith('@s.whatsapp.net') || !text) return;

    console.log(`[${name}] ${text}`);

    const state = stateManager.get(jid);

    // Sem estado → primeiro contato
    if (!state) {
        stateManager.set(jid, { step: 'WAITING_DESCRIPTION' });
        await send(sock, jid, welcomeText(name));
        return;
    }

    switch (state.step) {
        case 'WAITING_DESCRIPTION':
            await onWaitingDescription(sock, jid, text, name);
            break;
        case 'WAITING_FEEDBACK':
            await onWaitingFeedback(sock, jid, text, state);
            break;
        case 'WAITING_NO_ANSWER':
            await onWaitingNoAnswer(sock, jid, text, state);
            break;
        default:
            stateManager.remove(jid);
            stateManager.set(jid, { step: 'WAITING_DESCRIPTION' });
            await send(sock, jid, welcomeText(name));
    }
}

module.exports = { handleMessage };
