const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, '..', 'data');
const STATE_FILE = path.join(DATA_DIR, 'sessions.json');

let _states = {};

function _load() {
    try {
        fs.mkdirSync(DATA_DIR, { recursive: true });
        if (fs.existsSync(STATE_FILE)) {
            _states = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
            const count = Object.keys(_states).length;
            if (count > 0) console.log(`[Estado] ${count} sessão(ões) restaurada(s).`);
        }
    } catch (err) {
        console.error('[Estado] Falha ao carregar sessões:', err.message);
        _states = {};
    }
}

function _save() {
    try {
        fs.writeFileSync(STATE_FILE, JSON.stringify(_states, null, 2), 'utf8');
    } catch (err) {
        console.error('[Estado] Falha ao salvar sessões:', err.message);
    }
}

function get(jid) {
    return _states[jid] ?? null;
}

function set(jid, state) {
    _states[jid] = state;
    _save();
}

function remove(jid) {
    delete _states[jid];
    _save();
}

_load();

module.exports = { get, set, remove };
