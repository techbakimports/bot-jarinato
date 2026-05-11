import asyncio
import xmlrpc.client
from typing import Optional
from app.config import settings


def _normalizar_telefone(jid: str) -> str:
    return ''.join(filter(str.isdigit, jid.replace('@s.whatsapp.net', '').replace('@g.us', '')))


def _sync_buscar_cliente(telefone_digits: str) -> Optional[dict]:
    try:
        common = xmlrpc.client.ServerProxy(f"{settings.odoo_url}/xmlrpc/2/common")
        uid = common.authenticate(settings.odoo_db, settings.odoo_user, settings.odoo_password, {})
        if not uid:
            return None

        models = xmlrpc.client.ServerProxy(f"{settings.odoo_url}/xmlrpc/2/object")

        # Busca pelo sufixo dos últimos 9 dígitos (cobre DDD + número sem código do país)
        sufixo = telefone_digits[-9:]
        domain = ['|',
            ['mobile', 'like', sufixo],
            ['phone',  'like', sufixo],
        ]

        partners = models.execute_kw(
            settings.odoo_db, uid, settings.odoo_password,
            'res.partner', 'search_read',
            [domain],
            {'fields': ['name', 'mobile', 'phone', 'email', 'vat', 'street', 'city'], 'limit': 1},
        )
        if not partners:
            return None

        p = partners[0]
        partner_id = p['id']

        orders = models.execute_kw(
            settings.odoo_db, uid, settings.odoo_password,
            'sale.order', 'search_read',
            [[['partner_id', '=', partner_id], ['state', 'in', ['sale', 'done']]]],
            {'fields': ['name', 'date_order', 'amount_total', 'state'],
             'limit': 5, 'order': 'date_order desc'},
        )

        return {
            'partner_id': partner_id,
            'nome':       p.get('name'),
            'email':      p.get('email') or None,
            'telefone':   p.get('mobile') or p.get('phone') or None,
            'cpf_cnpj':   p.get('vat') or None,
            'endereco':   f"{p.get('street', '')} — {p.get('city', '')}".strip(' —') or None,
            'pedidos': [
                {
                    'numero': o['name'],
                    'data':   str(o['date_order'])[:10],
                    'valor':  o['amount_total'],
                    'status': o['state'],
                }
                for o in orders
            ],
        }
    except Exception:
        return None


async def buscar_cliente_por_telefone(jid: str) -> Optional[dict]:
    if not settings.odoo_url:
        return None
    tel = _normalizar_telefone(jid)
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _sync_buscar_cliente, tel)
