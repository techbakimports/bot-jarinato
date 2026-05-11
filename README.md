# Projeto: WhatsApp Support Bot (Oficial Meta Cloud API)

Este documento contém o guia de implementação para o bot de atendimento ao usuário utilizando a API oficial da Meta.

## 🚀 Passo a Passo Inicial (Configuração Meta)

1.  **Acesse o Portal**: Vá para [developers.facebook.com](https://developers.facebook.com/).
2.  **Crie o Aplicativo**:
    *   Tipo: **Business** (Negócios).
    *   Nome: `Bot Atendimento Suporte`.
3.  **Adicione o WhatsApp**:
    *   No painel lateral, procure por "WhatsApp" e clique em "Configurar".
4.  **Configuração de API**:
    *   A Meta abrirá uma tela com um **Número de Teste** e um **ID de Telefone**. Guarde esses valores.
    *   Gere um **Token Temporário** (ele dura 24h, depois precisaremos de um permanente).

---

## 🛠️ Estrutura do Código (O que vamos construir)

O bot será construído com **Node.js** seguindo as melhores práticas de segurança e organização:

```text
bot-what/
├── src/
│   ├── services/        # whatsappService.js (Comunicação com API Meta)
│   ├── controller/      # webhookController.js (Recebe e valida mensagens)
│   ├── bot/             # botLogic.js (O "cérebro" do atendimento)
│   └── index.js         # Servidor principal (Express)
├── .env                 # Configurações sensíveis (Tokens e IDs)
└── package.json         # Dependências do projeto
```

## 🔒 Segurança e Robustez

*   **Validação X-Hub**: O servidor verificará se cada mensagem recebida veio realmente da Meta usando um Hash SHA256.
*   **Gestão de Estado**: O bot saberá em qual etapa do atendimento o usuário está (ex: escolhendo opção do menu).
*   **Limpeza**: Código modularizado para fácil manutenção.

---



