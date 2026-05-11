require('dotenv').config();

const {
    default: makeWASocket,
    useMultiFileAuthState,
    DisconnectReason
} = require('@whiskeysockets/baileys');
const { Boom } = require('@hapi/boom');
const pino = require('pino');
const { handleMessage } = require('./botLogic');

const MAX_RETRIES = 5;
let retries = 0;

async function connectToWhatsApp() {
    const { state, saveCreds } = await useMultiFileAuthState('auth_info');

    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: true,
        logger: pino({ level: 'silent' }),
        browser: ['TechBak Bot', 'Chrome', '1.0.0'],
    });

    sock.ev.on('connection.update', (update) => {
        const { connection, lastDisconnect, qr } = update;

        if (qr) {
            console.log('\n--- ESCANEIE O QR CODE ABAIXO ---');
        }

        if (connection === 'close') {
            const code = (lastDisconnect?.error instanceof Boom)
                ? lastDisconnect.error.output?.statusCode
                : null;

            const loggedOut = code === DisconnectReason.loggedOut;

            if (loggedOut) {
                console.log('Sessão encerrada (logout). Remova a pasta auth_info e reinicie.');
                return;
            }

            if (retries < MAX_RETRIES) {
                retries++;
                const delay = retries * 3000;
                console.log(`Conexão fechada. Tentativa ${retries}/${MAX_RETRIES} em ${delay / 1000}s...`);
                setTimeout(connectToWhatsApp, delay);
            } else {
                console.error(`Falha após ${MAX_RETRIES} tentativas. Encerrando.`);
                process.exit(1);
            }
        }

        if (connection === 'open') {
            retries = 0;
            console.log('BOT CONECTADO COM SUCESSO!');
        }
    });

    sock.ev.on('creds.update', saveCreds);

    sock.ev.on('messages.upsert', async ({ messages, type }) => {
        if (type !== 'notify') return;
        for (const m of messages) {
            if (m.key.fromMe || !m.message) continue;
            try {
                await handleMessage(sock, m);
            } catch (err) {
                console.error(`[Erro] Falha ao processar mensagem:`, err.message);
            }
        }
    });
}

console.log('Iniciando o Bot...');
connectToWhatsApp().catch(err => {
    console.error('Erro crítico ao iniciar:', err);
    process.exit(1);
});
