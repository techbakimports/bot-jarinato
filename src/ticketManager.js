const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, '..', 'data');
const TICKETS_FILE = path.join(DATA_DIR, 'tickets.json');

function _loadTickets() {
    try {
        if (fs.existsSync(TICKETS_FILE)) {
            return JSON.parse(fs.readFileSync(TICKETS_FILE, 'utf8'));
        }
    } catch {}
    return [];
}

function generateId() {
    return `TKT-${Date.now().toString(36).toUpperCase()}`;
}

function createTicket(jid, name, description) {
    const tickets = _loadTickets();
    const ticket = {
        id: generateId(),
        jid,
        name,
        description,
        createdAt: new Date().toISOString(),
        status: 'aberto',
    };
    tickets.push(ticket);
    fs.mkdirSync(DATA_DIR, { recursive: true });
    fs.writeFileSync(TICKETS_FILE, JSON.stringify(tickets, null, 2), 'utf8');
    return ticket.id;
}

// Simula consulta de pedido — substitua por integração real com seu sistema
function lookupOrder(orderNumber) {
    const statusOptions = [
        { status: 'Em separação', detail: 'Seu pedido está sendo preparado no estoque.' },
        { status: 'Aguardando pagamento', detail: 'Aguardamos a confirmação do pagamento.' },
        { status: 'Em trânsito', detail: 'Seu pedido está a caminho.' },
        { status: 'Saiu para entrega', detail: 'O pedido saiu para entrega hoje.' },
        { status: 'Entregue', detail: 'Pedido entregue com sucesso.' },
    ];
    const index = orderNumber.split('').reduce((acc, c) => acc + c.charCodeAt(0), 0) % statusOptions.length;
    return statusOptions[index];
}

module.exports = { createTicket, lookupOrder };
