/**
 * Base de conhecimento de suporte técnico.
 * Para adicionar novos problemas: copie um bloco e ajuste id, tags e answer.
 * Tags são palavras-chave em minúsculo SEM acento — a busca normaliza o texto automaticamente.
 */

const entries = [
    {
        id: 'pc_nao_liga',
        tags: ['nao liga', 'nao inicia', 'nao acende', 'nao quer ligar', 'nao da pra ligar', 'nao responde', 'morto', 'apagado'],
        title: 'Computador não liga',
        answer:
            `*Computador não liga* 🖥️\n\n` +
            `Tente estes passos em ordem:\n\n` +
            `1️⃣ Verifique se o cabo de energia está bem encaixado na tomada e no PC\n` +
            `2️⃣ Teste a tomada com outro aparelho para confirmar que tem energia\n` +
            `3️⃣ Se for notebook, tente ligar só no cabo (sem bateria) e depois só na bateria\n` +
            `4️⃣ Pressione o botão power por 10 segundos para forçar desligamento, depois ligue\n` +
            `5️⃣ Se usar estabilizador ou no-break, verifique se está ligado e funcionando\n\n` +
            `Se nada funcionar, pode ser problema no botão power, na fonte ou na placa-mãe — precisará de análise presencial.`,
    },
    {
        id: 'tela_azul',
        tags: ['tela azul', 'bsod', 'blue screen', 'tela azul da morte', 'travou tela azul', 'erro azul'],
        title: 'Tela Azul (BSOD)',
        answer:
            `*Tela Azul (BSOD)* 💙\n\n` +
            `Indica problema de hardware ou driver.\n\n` +
            `1️⃣ Anote o código exibido na tela (ex: SYSTEM_SERVICE_EXCEPTION)\n` +
            `2️⃣ Reinicie — se foi pontual, pode não voltar\n` +
            `3️⃣ Verifique se há atualizações do Windows pendentes\n` +
            `4️⃣ Se ocorreu logo após instalar programa ou driver, desinstale-o\n` +
            `5️⃣ Se for frequente, pode ser RAM com defeito ou HD com setores ruins\n\n` +
            `Se tiver o código da tela azul, informe aqui para uma análise mais precisa.`,
    },
    {
        id: 'lento',
        tags: ['lento', 'devagar', 'travando', 'trava muito', 'demora muito', 'lentidao', 'pesado', 'emperrado', 'travado'],
        title: 'Computador lento / travando',
        answer:
            `*Computador lento ou travando* 🐢\n\n` +
            `1️⃣ Reinicie o computador — parece básico mas resolve muita coisa\n` +
            `2️⃣ Feche programas que não está usando (aba da barra de tarefas com botão direito → Fechar)\n` +
            `3️⃣ Abra o Gerenciador de Tarefas (Ctrl+Shift+Esc) e veja o que está consumindo CPU/memória\n` +
            `4️⃣ Desative programas que abrem com o Windows: Gerenciador de Tarefas → aba Inicializar\n` +
            `5️⃣ Verifique se o HD/SSD está quase cheio — deixe pelo menos 10% livre\n` +
            `6️⃣ Execute o Windows Defender para verificar vírus\n\n` +
            `Se o computador for antigo (mais de 5 anos) pode ser hora de upgrade de memória RAM ou trocar o HD por SSD.`,
    },
    {
        id: 'sem_internet',
        tags: ['sem internet', 'internet caiu', 'sem conexao', 'sem wifi', 'wifi nao conecta', 'nao conecta', 'internet nao funciona', 'sem rede', 'rede caiu', 'nao tem internet', 'internet lenta', 'internet caindo'],
        title: 'Sem internet / Wi-Fi',
        answer:
            `*Sem internet ou Wi-Fi* 🌐\n\n` +
            `1️⃣ Reinicie o modem/roteador: desligue da tomada, aguarde 30 segundos e ligue novamente\n` +
            `2️⃣ No Windows: clique com botão direito no ícone de rede → Solucionar problemas\n` +
            `3️⃣ Esqueça a rede Wi-Fi e reconecte digitando a senha novamente\n` +
            `4️⃣ Teste outro dispositivo (celular) na mesma rede — se também não conecta, o problema é no modem\n` +
            `5️⃣ Se usar cabo, troque ou teste o cabo em outra porta do roteador\n` +
            `6️⃣ Abra o CMD como administrador e execute:\n   • \`ipconfig /flushdns\`\n   • \`netsh winsock reset\`\n   • Reinicie após os comandos`,
    },
    {
        id: 'tela_preta',
        tags: ['tela preta', 'sem imagem', 'monitor apagado', 'monitor nao liga', 'sem sinal', 'no signal', 'nao aparece nada', 'tela nao aparece'],
        title: 'Tela preta / sem imagem',
        answer:
            `*Tela preta / sem imagem* 🖥️\n\n` +
            `1️⃣ Verifique se o monitor está ligado e o cabo (HDMI/VGA/DisplayPort) está bem encaixado nos dois lados\n` +
            `2️⃣ Tente outro cabo ou outra entrada do monitor\n` +
            `3️⃣ Se o PC tem saída de vídeo na placa-mãe E uma placa de vídeo dedicada, tente as duas\n` +
            `4️⃣ Conecte um monitor diferente para saber se o problema é no monitor ou no PC\n` +
            `5️⃣ Se o PC liga (ouve sons, luzes acendem) mas a tela fica preta, pode ser placa de vídeo ou configuração de resolução\n\n` +
            `Se o monitor exibe "Sem sinal" mesmo com o cabo conectado, o problema provavelmente é no computador.`,
    },
    {
        id: 'senha_windows',
        tags: ['esqueci a senha', 'nao lembro a senha', 'senha errada', 'senha do windows', 'nao consigo entrar', 'bloqueado', 'senha incorreta', 'nao acessa windows'],
        title: 'Esqueci a senha do Windows',
        answer:
            `*Esqueci a senha do Windows* 🔑\n\n` +
            `*Se usar conta Microsoft (Outlook/Hotmail):*\n` +
            `Acesse account.live.com/password/reset em outro dispositivo e redefina online.\n\n` +
            `*Se usar conta local:*\n` +
            `1️⃣ Na tela de login, clique em "Esqueci o PIN" ou "Opções de entrada"\n` +
            `2️⃣ Windows 10/11 pode oferecer perguntas de segurança ou envio por e-mail\n` +
            `3️⃣ Se não funcionar, é necessário usar uma mídia de recuperação\n\n` +
            `⚠️ *Não use ferramentas de terceiros desconhecidas* — podem comprometer a segurança.\n\n` +
            `Para redefinição via mídia de recuperação, podemos fazer presencialmente.`,
    },
    {
        id: 'virus',
        tags: ['virus', 'malware', 'infectado', 'hacker', 'ransomware', 'trojan', 'spyware', 'meu pc foi hackeado', 'pc com virus', 'propaganda aparecendo', 'pop up', 'propaganda'],
        title: 'Vírus ou Malware',
        answer:
            `*Vírus ou Malware* 🦠\n\n` +
            `1️⃣ Desconecte da internet para evitar que o malware envie dados\n` +
            `2️⃣ Abra o *Windows Defender* → Verificação Completa (pode demorar horas)\n` +
            `3️⃣ Baixe e execute o *Malwarebytes Free* (malwarebytes.com) — ele pega o que o Defender perde\n` +
            `4️⃣ Após a limpeza, mude todas as senhas importantes de outro dispositivo\n` +
            `5️⃣ Verifique extensões suspeitas no navegador e desinstale programas desconhecidos\n\n` +
            `⚠️ Se os arquivos foram criptografados (ransomware), *não pague o resgate* — traga para nós avaliarmos as opções.`,
    },
    {
        id: 'reiniciando',
        tags: ['reiniciando sozinho', 'reinicia sozinho', 'desliga sozinho', 'desligando sozinho', 'apaga sozinho', 'apagando sozinho', 'reinicia do nada', 'desliga do nada', 'reseta sozinho'],
        title: 'Computador reiniciando/desligando sozinho',
        answer:
            `*Computador reiniciando ou desligando sozinho* 🔄\n\n` +
            `As causas mais comuns são superaquecimento ou problema de hardware:\n\n` +
            `1️⃣ Verifique a temperatura: baixe o *HWMonitor* (grátis) e veja se CPU/GPU passam de 90°C em uso\n` +
            `2️⃣ Limpe o interior do computador — poeira entope as ventoinhas e causa superaquecimento\n` +
            `3️⃣ Verifique se a ventoinha do processador está girando\n` +
            `4️⃣ Cheque se há algum erro no Visualizador de Eventos do Windows (Win+X → Visualizador de Eventos)\n` +
            `5️⃣ Teste a memória RAM com o *MemTest86*\n\n` +
            `Se desligar sem aviso (sem tela azul antes), é provável superaquecimento ou fonte fraca.`,
    },
    {
        id: 'barulho',
        tags: ['barulho', 'fazendo barulho', 'ruido', 'bip', 'beep', 'barulho estranho', 'rangendo', 'chiando', 'ventilador barulhento', 'fan barulho'],
        title: 'Barulho no computador',
        answer:
            `*Barulho no computador* 🔊\n\n` +
            `O tipo de barulho indica a causa:\n\n` +
            `🔵 *Ventoinha barulhenta:* Acumulo de poeira. Limpe com ar comprimido. Se persistir, a ventoinha pode precisar de troca.\n\n` +
            `🔴 *Clique repetido (tipo "clac clac"):* Sinal grave — provavelmente o HD está falhando. *Faça backup imediatamente.*\n\n` +
            `🟡 *Rangido / chiado:* Pode ser a fonte de alimentação com problema.\n\n` +
            `🟠 *Bip ao ligar:* Sequência de bips indica erro de hardware (RAM, placa de vídeo). Conte os bips e informe aqui.\n\n` +
            `Para HD com barulho de clique, não espere — os dados podem ser perdidos a qualquer momento.`,
    },
    {
        id: 'impressora',
        tags: ['impressora', 'impressora nao funciona', 'nao imprime', 'impressora offline', 'impressora travada', 'papel preso', 'atolamento de papel', 'nao reconhece impressora'],
        title: 'Impressora não funciona',
        answer:
            `*Impressora não funciona* 🖨️\n\n` +
            `1️⃣ Verifique se a impressora está ligada e conectada (cabo USB ou Wi-Fi)\n` +
            `2️⃣ Cancele todos os trabalhos na fila de impressão: Painel de Controle → Dispositivos e Impressoras → duplo clique na impressora → cancele tudo\n` +
            `3️⃣ Reinicie o serviço de spooler: Win+R → \`services.msc\` → "Spooler de Impressão" → Reiniciar\n` +
            `4️⃣ Desinstale e reinstale o driver da impressora (site do fabricante)\n` +
            `5️⃣ Verifique se tem papel e tinta/toner\n\n` +
            `Se aparecer "Offline" mesmo conectada, o problema costuma ser o driver ou o spooler.`,
    },
    {
        id: 'teclado_mouse',
        tags: ['teclado nao funciona', 'mouse nao funciona', 'teclado parou', 'mouse parou', 'mouse nao move', 'teclado digitando errado', 'mouse travado', 'nao reconhece teclado', 'nao reconhece mouse'],
        title: 'Teclado ou Mouse não funciona',
        answer:
            `*Teclado ou Mouse não funciona* ⌨️🖱️\n\n` +
            `1️⃣ Desconecte e reconecte o dispositivo em outra porta USB\n` +
            `2️⃣ Teste o mesmo teclado/mouse em outro computador para saber se o problema é no dispositivo ou no PC\n` +
            `3️⃣ Se for wireless: troque as pilhas e verifique o receptor USB\n` +
            `4️⃣ Reinicie o computador com o dispositivo conectado\n` +
            `5️⃣ Verifique no Gerenciador de Dispositivos (Win+X) se há algum ponto de exclamação amarelo\n\n` +
            `Se o teclado digitar caracteres errados (letras em vez de números), verifique se o *Num Lock* ou o layout de idioma está correto.`,
    },
    {
        id: 'sem_audio',
        tags: ['sem som', 'sem audio', 'audio nao funciona', 'som nao funciona', 'nao tem som', 'caixa de som nao funciona', 'headphone nao funciona', 'fone nao funciona', 'som sumiu'],
        title: 'Sem áudio / som não funciona',
        answer:
            `*Sem áudio* 🔇\n\n` +
            `1️⃣ Verifique se o volume não está no mínimo ou mutado (ícone de som na barra de tarefas)\n` +
            `2️⃣ Clique com botão direito no ícone de som → Abrir configurações de som → verifique o dispositivo de saída correto\n` +
            `3️⃣ Se usa caixa de som ou headphone externo, verifique o cabo e se o dispositivo está ligado\n` +
            `4️⃣ Clique com botão direito no ícone de som → Solucionar problemas de som\n` +
            `5️⃣ Atualize ou reinstale o driver de áudio: Gerenciador de Dispositivos → Entradas e saídas de áudio\n\n` +
            `Após atualizar driver de áudio, reinicie o computador.`,
    },
    {
        id: 'windows_update',
        tags: ['windows update', 'nao atualiza', 'erro ao atualizar', 'atualizacao travada', 'windows nao atualiza', 'update falhando', 'windows update erro'],
        title: 'Windows não atualiza',
        answer:
            `*Windows não atualiza* ⚙️\n\n` +
            `1️⃣ Verifique se tem espaço em disco suficiente (mínimo 10 GB livres)\n` +
            `2️⃣ Execute a solução de problemas: Configurações → Windows Update → Solucionar problemas\n` +
            `3️⃣ Abra o CMD como administrador e execute em sequência:\n   • \`net stop wuauserv\`\n   • \`net stop bits\`\n   • \`ren C:\\Windows\\SoftwareDistribution SoftwareDistribution.old\`\n   • \`net start wuauserv\`\n   • \`net start bits\`\n` +
            `4️⃣ Tente o Windows Update novamente\n\n` +
            `Se persistir com código de erro, informe o código aqui para diagnóstico específico.`,
    },
    {
        id: 'superaquecimento',
        tags: ['superaquecendo', 'esquentando muito', 'muito quente', 'temperatura alta', 'pc quente', 'esquenta', 'calor excessivo', 'ventoinha acelerada'],
        title: 'Computador superaquecendo',
        answer:
            `*Computador superaquecendo* 🌡️\n\n` +
            `1️⃣ Verifique a temperatura com o *HWMonitor* — acima de 90°C em repouso é crítico\n` +
            `2️⃣ Limpe as ventoinhas e dissipadores com ar comprimido (faça em ambiente aberto)\n` +
            `3️⃣ Garanta que o computador tem espaço ao redor para ventilação — não coloque em gavetas ou espaços fechados\n` +
            `4️⃣ Verifique se todas as ventoinhas estão girando\n` +
            `5️⃣ A pasta térmica do processador pode estar seca — após 3–4 anos é recomendado reaplicar\n\n` +
            `Superaquecimento crônico reduz a vida útil do hardware e pode causar danos permanentes.`,
    },
    {
        id: 'formatacao',
        tags: ['formatar', 'formatacao', 'reinstalar windows', 'reinstalar o windows', 'formatar pc', 'reset de fabrica', 'resetar pc', 'limpar tudo', 'restaurar windows'],
        title: 'Formatar / Reinstalar Windows',
        answer:
            `*Formatar / Reinstalar o Windows* 💿\n\n` +
            `Antes de tudo:\n` +
            `⚠️ *Faça backup de tudo* — documentos, fotos, downloads, área de trabalho e favoritos do navegador.\n\n` +
            `*Opção 1 — Redefinir o Windows (sem mídia):*\n` +
            `Configurações → Sistema → Recuperação → Redefinir este PC\n` +
            `Escolha "Remover tudo" para uma limpeza completa.\n\n` +
            `*Opção 2 — Instalação limpa (pendrive):*\n` +
            `1️⃣ Baixe a ferramenta de criação de mídia em microsoft.com/software-download/windows11\n` +
            `2️⃣ Crie um pendrive bootável (mínimo 8 GB)\n` +
            `3️⃣ Reinicie pelo pendrive e siga as instruções\n\n` +
            `Se quiser que realizemos a formatação, podemos fazer isso presencialmente.`,
    },
];

function normalize(text) {
    return text
        .toLowerCase()
        .normalize('NFD')
        .replace(/[̀-ͯ]/g, '')
        .replace(/[^a-z0-9\s]/g, ' ');
}

function search(query) {
    const normalized = normalize(query);
    let best = null;
    let bestScore = 0;

    for (const entry of entries) {
        let score = 0;
        for (const tag of entry.tags) {
            if (normalized.includes(tag)) {
                // Tags mais longas têm peso maior (mais específicas)
                score += tag.split(' ').length;
            }
        }
        if (score > bestScore) {
            bestScore = score;
            best = entry;
        }
    }

    return bestScore > 0 ? best : null;
}

module.exports = { search };
