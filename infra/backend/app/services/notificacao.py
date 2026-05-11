import asyncio
import smtplib
from email.mime.text import MIMEText
from app.config import settings


def _smtp_configurado() -> bool:
    return bool(settings.smtp_host and settings.smtp_user and settings.smtp_password and settings.notif_email_destino)


def _sync_enviar_email(destinatario: str, assunto: str, corpo_html: str):
    msg = MIMEText(corpo_html, 'html', 'utf-8')
    msg['Subject'] = assunto
    msg['From']    = settings.smtp_from
    msg['To']      = destinatario

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(settings.smtp_user, settings.smtp_password)
        smtp.send_message(msg)


async def notificar_novo_ticket(nome_cliente: str, remote_jid: str, ticket_id: str):
    if not _smtp_configurado():
        return

    numero = remote_jid.replace('@s.whatsapp.net', '')
    corpo = f"""
    <div style="font-family:sans-serif;max-width:480px;margin:auto;">
      <h2 style="color:#16a34a;">TechBak — Novo Ticket</h2>
      <p>Um cliente solicitou atendimento humano.</p>
      <table style="width:100%;border-collapse:collapse;margin:16px 0;">
        <tr><td style="padding:6px;color:#6b7280;">Cliente</td>
            <td style="padding:6px;font-weight:600;">{nome_cliente or numero}</td></tr>
        <tr style="background:#f9fafb;">
            <td style="padding:6px;color:#6b7280;">WhatsApp</td>
            <td style="padding:6px;">{numero}</td></tr>
        <tr><td style="padding:6px;color:#6b7280;">Ticket ID</td>
            <td style="padding:6px;font-family:monospace;font-size:12px;">{ticket_id}</td></tr>
      </table>
      <a href="{settings.painel_url}"
         style="display:inline-block;background:#16a34a;color:#fff;padding:10px 20px;
                border-radius:8px;text-decoration:none;font-weight:600;">
        Abrir Painel de Atendimento
      </a>
    </div>
    """

    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(
            None, _sync_enviar_email,
            settings.notif_email_destino,
            f"[TechBak] Novo ticket aguardando — {nome_cliente or numero}",
            corpo,
        )
    except Exception:
        pass  # notificação é best-effort, nunca deve quebrar o fluxo principal
