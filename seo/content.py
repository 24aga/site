"""Preços, comparativos e ferramentas grátis."""
from shell import *

def precos():
    plans = [('essencial', 'Essencial', 'Negócios pequenos', 300, ['Atendente com IA no WhatsApp 24h', 'Agenda, lembretes e confirmação', 'Follow-up automático', 'Pix na conversa']),
             ('profissional', 'Profissional', 'Equipes de 2 a 5 pessoas', 800, ['Tudo do Essencial', 'Agenda por profissional', 'Campanhas e clientes sumidos', 'Avaliações no Google']),
             ('premium', 'Premium', 'Negócios maiores ou com filiais', 2000, ['Tudo do Profissional', 'Várias unidades e equipes', 'Relatórios por unidade', 'Acompanhamento semanal no 1º mês'])]
    dflt = {'essencial': (397, 1500), 'profissional': (697, 2500), 'premium': (1197, 3800)}
    food = [('resto_gratis', 'Cardápio grátis', 0, 0, 'Cardápio digital com pedidos no seu WhatsApp, para começar'), ('resto_delivery', 'Delivery', 97, 197, 'Cardápio digital próprio, pedidos no WhatsApp, sem comissão por pedido'), ('resto_ia', 'Delivery + IA Start', 197, 197, 'IA que anota pedidos no WhatsApp · até 500 conversas'),
            ('resto_ia_pro', 'Delivery + IA Pro', 297, 197, 'Até 1.500 conversas · cupons, entregas por bairro'), ('resto_ia_max', 'Delivery + IA Max', 497, 297, 'Até 4.000 conversas · para alto volume')]
    rows = ''.join(f'<tr><td><b>{n}</b><br><small>{who}</small></td><td><span data-p24="{k}:m">R$ {dflt[k][0]}/mês</span></td><td><span data-p24="{k}:s">R$ {dflt[k][1]:,}</span></td><td>até {c:,} conversas/mês<br><small>{" · ".join(f)}</small></td></tr>'.replace(',', '.') for k, n, who, c, f in plans)
    frows = ''.join(f'<tr><td><b>{n}</b></td><td><span data-p24="{k}:m">{"Grátis" if not m else f"R$ {m}/mês"}</span></td><td><span data-p24="{k}:s">{"Sem custo" if not s else f"R$ {s}"}</span></td><td>{d}</td></tr>' for k, n, m, s, d in food)
    faq = [('Tem teste grátis?', 'Sim. Clínicas, empresas, salões, escritórios, imobiliárias e pet shops testam grátis, sem cartão: a IA responde até 100 mensagens. Restaurantes têm o cardápio digital grátis.'),
           ('O que é a implantação?', 'É o valor pago uma vez para configurar tudo: conexão do WhatsApp, cadastro de serviços e preços, regras da IA e treinamento da equipe.'),
           ('Tem fidelidade?', 'Os planos têm período mínimo informado no contrato. O teste grátis não tem compromisso.'),
           ('Paga comissão por venda ou pedido?', 'Não. A mensalidade é fixa. Não cobramos porcentagem sobre agendamentos, vendas ou pedidos.'),
           ('Como funciona o pagamento?', 'Implantação por Pix ou cartão e mensalidade fixa todo mês. Você acompanha tudo pelo app.'),
           ('O que conta como conversa?', 'Cada cliente atendido pela IA no período conta como uma conversa, não importa quantas mensagens troquem.')]
    body = f'''<div class="art"><div class="tldr"><b>Resumo</b>Clínicas e negócios com agenda: de <b>R$ 397 a R$ 1.197 por mês</b>, mais implantação única. Restaurantes: cardápio digital grátis para começar e planos a partir de <b>R$ 97 por mês</b>, sem comissão por pedido. Sem taxa por venda ou agendamento. <span data-p24-badge hidden></span></div>
<h2>Clínicas, empresas, salões, escritórios, imobiliárias e pet shops</h2>
<table><tr><th>Plano</th><th>Mensalidade</th><th>Implantação</th><th>Inclui</th></tr>{rows}</table>
<h2>Restaurantes e delivery (24AGÁ Food)</h2>
<table><tr><th>Plano</th><th>Mensalidade</th><th>Implantação</th><th>Para quem</th></tr>{frows}</table>
<p>Compare com o custo de uma recepcionista na <a href="/comparativo/recepcionista-ou-atendente-ia/">página do comparativo</a> ou calcule quanto as faltas custam na <a href="/ferramentas/calculadora-de-faltas/">calculadora grátis</a>.</p>
{cta_box('precos')}<h2>Perguntas frequentes</h2>{faq_html(faq)}</div>'''
    ld = [ORG, faq_ld(faq), crumbs_ld([('Início', '/'), ('Preços', '/precos/')]),
          {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "24AGÁ", "applicationCategory": "BusinessApplication", "operatingSystem": "Web, Android, iOS",
           "description": "Atendente com inteligência artificial no WhatsApp que responde, agenda e vende 24 horas.",
           "offers": [{"@type": "Offer", "name": n, "price": str(dflt[k][0]), "priceCurrency": "BRL"} for k, n, *_ in plans] + [{"@type": "Offer", "name": n, "price": str(m), "priceCurrency": "BRL"} for k, n, m, s, d in food]}]
    return page('/precos/', 'Preços da 24AGÁ · Atendente com IA no WhatsApp a partir de R$ 97/mês', 'Planos e valores da 24AGÁ: atendente com IA no WhatsApp para clínicas, empresas e restaurantes. Mensalidade fixa, sem comissão. Teste grátis.',
                'Preços e planos', 'Mensalidade fixa, sem comissão por venda ou pedido. Teste grátis antes de decidir.', body, crumbs=[('Início', '/'), ('Preços', None)], ld=ld, src='precos',
                scripts='<script src="/precos.js?v=2"></script>')

def comparativos():
    out = {}
    faq1 = [('Chatbot e atendente com IA são a mesma coisa?', 'Não. O chatbot comum segue um menu fixo de botões. A atendente com IA entende o que a pessoa escreve (até áudio), responde com as informações do seu negócio e executa ações como agendar.'),
            ('A IA pode inventar informação?', 'Uma atendente com IA bem configurada só usa as informações aprovadas pelo negócio e passa para a equipe quando não sabe. Na 24AGÁ, você aprova o que ela pode dizer.'),
            ('Qual é mais barato?', 'Chatbots de menu costumam ser mais baratos, mas perdem clientes que não se encaixam nos botões. Compare pelo resultado: quantos contatos viram agendamento ou venda.')]
    body1 = f'''<div class="art"><div class="tldr"><b>Resumo</b>O chatbot de menu ("digite 1 para…") resolve perguntas previsíveis. A atendente com IA entende qualquer mensagem, inclusive áudio, e conduz até o agendamento ou a venda. Para quem vende pelo WhatsApp, a IA converte mais porque conversa como gente.</div>
<h2>A diferença na prática</h2>
<table><tr><th></th><th>Chatbot de menu</th><th>Atendente com IA</th></tr>
<tr><td>Como o cliente fala</td><td>Escolhe opções numeradas</td><td>Escreve ou manda áudio, do jeito dele</td></tr>
<tr><td>Pergunta fora do roteiro</td><td>Trava ou repete o menu</td><td>Entende e responde, ou chama a equipe</td></tr>
<tr><td>Agendamento</td><td>Formulário ou link externo</td><td>Oferece horários livres e reserva na conversa</td></tr>
<tr><td>Tom</td><td>Robótico</td><td>Natural, no jeito do seu negócio</td></tr>
<tr><td>Follow-up</td><td>Mensagem fixa</td><td>Personalizada com o que a pessoa pediu</td></tr>
<tr><td>Configuração</td><td>Desenhar cada fluxo</td><td>Cadastrar serviços, preços e regras</td></tr></table>
<h2>Quando o chatbot de menu ainda faz sentido</h2><p>Para segunda via de boleto, status de pedido com número ou triagem muito simples, um menu resolve. Quando a conversa envolve dúvida, preço, objeção e agendamento, que é o caso de clínicas, salões, escritórios, imobiliárias e lojas, o menu perde gente.</p>
<h2>O que observar antes de escolher</h2><ul><li>A IA usa só as informações que você aprova?</li><li>Ela passa para uma pessoa quando precisa, avisando no seu celular?</li><li>Ela agenda na sua agenda real, sem conflito?</li><li>Funciona no seu número atual de WhatsApp?</li><li>Você vê o resultado em reais (agendamentos e vendas geradas)?</li></ul>
<p>Veja também: <a href="/blog/como-escolher-atendente-ia-whatsapp/">checklist para escolher uma atendente com IA</a>.</p>
{cta_box('comp-chatbot')}<h2>Perguntas frequentes</h2>{faq_html(faq1)}</div>'''
    out['/comparativo/chatbot-ou-atendente-ia/'] = page('/comparativo/chatbot-ou-atendente-ia/', 'Chatbot ou atendente com IA no WhatsApp? Diferenças e qual escolher', 'Comparativo entre chatbot de menu e atendente com inteligência artificial no WhatsApp: como cada um atende, agenda, vende e quando usar.',
        'Chatbot ou atendente com IA?', 'As diferenças que importam para quem atende e vende pelo WhatsApp.', body1, crumbs=[('Início', '/'), ('Comparativos', None)], ld=[ORG, faq_ld(faq1), crumbs_ld([('Início', '/'), ('Chatbot ou atendente com IA', '/comparativo/chatbot-ou-atendente-ia/')])], src='comp-chatbot')
    faq2 = [('A IA substitui a recepcionista?', 'Ela assume o repetitivo do WhatsApp: responder, passar preço, agendar, confirmar e lembrar. A recepção fica livre para quem está no balcão. Muitos negócios mantêm a pessoa e usam a IA para não perder ninguém fora do horário.'),
            ('Quanto custa uma recepcionista?', 'Além do salário, entram encargos, benefícios, férias e 13º. Use a calculadora da página para colocar os valores da sua cidade.'),
            ('A IA atende à noite e no fim de semana?', 'Sim, 24 horas, todos os dias. É justamente quando muita gente chama.')]
    calc = '''<div class="art" style="margin-top:14px"><h2 style="margin-top:0">Faça a conta do seu negócio</h2>
<p><label>Salário da recepcionista (R$): <input id="s" type="number" value="1800" style="width:120px"></label></p>
<p><label>Encargos e benefícios (% sobre o salário): <input id="e" type="number" value="70" style="width:80px"></label></p>
<p><label>Mensalidade do plano 24AGÁ (R$): <input id="p" type="number" value="397" style="width:100px"></label></p>
<blockquote id="r"></blockquote></div>
<script>function c(){var s=+document.getElementById('s').value||0,e=+document.getElementById('e').value||0,p=+document.getElementById('p').value||0,t=s*(1+e/100),f=n=>n.toLocaleString('pt-BR',{style:'currency',currency:'BRL',maximumFractionDigits:0});document.getElementById('r').textContent='Recepcionista: cerca de '+f(t)+' por mês (horário comercial).\\n24AGÁ: '+f(p)+' por mês (24 horas, todos os dias).\\nDiferença: '+f(t-p)+' por mês, '+f((t-p)*12)+' por ano.';}document.querySelectorAll('#s,#e,#p').forEach(i=>i.addEventListener('input',c));c();</script>'''
    body2 = f'''<div class="art"><div class="tldr"><b>Resumo</b>A recepcionista atende em horário comercial e custa salário mais encargos. A atendente com IA responde o WhatsApp 24 horas, por uma mensalidade fixa. O melhor resultado costuma vir das duas juntas: a IA no WhatsApp e a pessoa no presencial.</div>
<h2>Comparação lado a lado</h2>
<table><tr><th></th><th>Recepcionista</th><th>Atendente com IA (24AGÁ)</th></tr>
<tr><td>Horário</td><td>Comercial</td><td>24h, 7 dias</td></tr><tr><td>Tempo de resposta</td><td>Depende da fila do balcão</td><td>Segundos</td></tr>
<tr><td>Várias conversas ao mesmo tempo</td><td>Uma por vez</td><td>Todas ao mesmo tempo</td></tr><tr><td>Lembretes e confirmação</td><td>Manual, quando dá tempo</td><td>Automáticos</td></tr>
<tr><td>Atendimento humano e empático no presencial</td><td>Sim</td><td>Não substitui</td></tr><tr><td>Faltas, férias, troca de pessoa</td><td>Acontece</td><td>Não se aplica</td></tr>
<tr><td>Custo</td><td>Salário + encargos + benefícios</td><td>Mensalidade fixa</td></tr></table>
<h2>O melhor dos dois</h2><p>A IA cuida do WhatsApp: responde na hora, agenda, confirma e chama de volta quem sumiu. A recepcionista cuida de quem está na sua frente, sem o celular apitando. Quando um assunto precisa de gente, a IA passa a conversa para a equipe com todo o histórico.</p>
{cta_box('comp-recepcao')}<h2>Perguntas frequentes</h2>{faq_html(faq2)}</div>{calc}'''
    out['/comparativo/recepcionista-ou-atendente-ia/'] = page('/comparativo/recepcionista-ou-atendente-ia/', 'Recepcionista ou atendente com IA? Custo, horário e quando usar cada uma', 'Compare recepcionista e atendente com inteligência artificial no WhatsApp: custo, horário, tempo de resposta e como usar as duas juntas. Com calculadora.',
        'Recepcionista ou atendente com IA?', 'Custo, horário e o que cada uma faz melhor. Com calculadora para o seu caso.', body2, crumbs=[('Início', '/'), ('Comparativos', None)], ld=[ORG, faq_ld(faq2), crumbs_ld([('Início', '/'), ('Recepcionista ou atendente com IA', '/comparativo/recepcionista-ou-atendente-ia/')])], src='comp-recepcao')
    return out

INP = 'style="width:130px;padding:8px;border:1px solid #DFE5EF;border-radius:8px;font:inherit"'
def ferramentas():
    out = {}
    f1 = f'''<div class="art"><p>Coloque os números do seu negócio. A conta é feita no seu navegador; nada é enviado.</p>
<p><label>Atendimentos marcados por mês<br><input id="a" type="number" value="200" {INP}></label></p>
<p><label>Faltas sem aviso (%)<br><input id="f" type="number" value="15" {INP}></label></p>
<p><label>Valor médio de cada atendimento (R$)<br><input id="t" type="number" value="150" {INP}></label></p>
<p><label>Se as faltas caíssem para (%)<br><input id="g" type="number" value="8" {INP}></label></p>
<blockquote id="r"></blockquote>
<h2>Como diminuir as faltas</h2><ol><li><b>Confirme com um toque:</b> mande a confirmação na véspera com botão ou resposta simples ("responda 1 para confirmar").</li><li><b>Lembre no dia:</b> um lembrete curto algumas horas antes, com endereço e link do mapa.</li><li><b>Facilite remarcar:</b> quem não pode ir precisa de um caminho fácil para trocar o horário, e não para sumir.</li><li><b>Lista de espera:</b> horário liberado vai para quem queria um encaixe.</li><li><b>Acompanhe o número:</b> meça a taxa de faltas todo mês.</li></ol>
<p>Modelos prontos: <a href="/blog/mensagem-de-confirmacao-de-consulta-modelos/">mensagens de confirmação</a> · <a href="/blog/como-reduzir-faltas-na-clinica/">como reduzir faltas</a>.</p>{cta_box('ferr-faltas', title='A 24AGÁ confirma, lembra e remarca sozinha')}</div>
<script>function c(){{var a=+document.getElementById('a').value||0,f=+document.getElementById('f').value||0,t=+document.getElementById('t').value||0,g=+document.getElementById('g').value||0,m=n=>n.toLocaleString('pt-BR',{{style:'currency',currency:'BRL',maximumFractionDigits:0}});var p=a*f/100*t,q=a*g/100*t;document.getElementById('r').textContent='Hoje você perde cerca de '+m(p)+' por mês ('+Math.round(a*f/100)+' faltas), ou '+m(p*12)+' por ano.\\nCom '+g+'% de faltas, a perda cai para '+m(q)+' por mês.\\nDiferença: '+m(p-q)+' por mês, '+m((p-q)*12)+' por ano.';}}document.querySelectorAll('input').forEach(i=>i.addEventListener('input',c));c();</script>'''
    out['/ferramentas/calculadora-de-faltas/'] = page('/ferramentas/calculadora-de-faltas/', 'Calculadora de faltas: quanto sua clínica ou salão perde por mês', 'Calcule grátis quanto dinheiro as faltas sem aviso custam para sua clínica, consultório, salão ou pet shop, e quanto você recupera reduzindo as faltas.',
        'Calculadora de faltas', 'Descubra quanto as faltas sem aviso custam por mês e por ano.', f1, crumbs=[('Início', '/'), ('Ferramentas', '/ferramentas/'), ('Calculadora de faltas', None)], ld=[ORG, crumbs_ld([('Início', '/'), ('Ferramentas', '/ferramentas/'), ('Calculadora de faltas', '/ferramentas/calculadora-de-faltas/')])], src='ferr-faltas')
    f2 = f'''<div class="art"><p>Veja quanto você paga de comissão para aplicativos de delivery e compare com um cardápio próprio de mensalidade fixa. Use a porcentagem que está no <b>seu</b> contrato.</p>
<p><label>Pedidos por mês no aplicativo<br><input id="n" type="number" value="600" {INP}></label></p>
<p><label>Valor médio do pedido (R$)<br><input id="t" type="number" value="55" {INP}></label></p>
<p><label>Comissão + taxas do aplicativo (%)<br><input id="c" type="number" value="20" {INP}></label></p>
<p><label>Quantos % dos pedidos você levaria para o seu cardápio<br><input id="m" type="number" value="40" {INP}></label></p>
<p><label>Mensalidade do cardápio próprio (R$)<br><input id="p" type="number" value="97" {INP}></label></p>
<blockquote id="r"></blockquote>
<h2>Como levar o cliente para o seu canal</h2><ol><li>Coloque o link do cardápio na bio do Instagram, no status e no Google.</li><li>Mande um cupom só para quem pede pelo seu cardápio.</li><li>Coloque um cartão na embalagem: "da próxima vez, peça direto e ganhe…".</li><li>Responda rápido no WhatsApp: quem demora devolve o cliente para o aplicativo.</li></ol>
<p>Leia: <a href="/blog/cardapio-digital-gratis-sem-comissao/">cardápio digital grátis e sem comissão</a>.</p>{cta_box('ferr-comissao', 'food', title='Crie seu cardápio digital grátis', sub='Pedidos direto no seu WhatsApp, sem comissão.')}</div>
<script>function c(){{var n=+document.getElementById('n').value||0,t=+document.getElementById('t').value||0,c=+document.getElementById('c').value||0,m=+document.getElementById('m').value||0,p=+document.getElementById('p').value||0,f=v=>v.toLocaleString('pt-BR',{{style:'currency',currency:'BRL',maximumFractionDigits:0}});var tot=n*t*c/100,ec=n*m/100*t*c/100-p;document.getElementById('r').textContent='Você paga cerca de '+f(tot)+' por mês em comissão ('+f(tot*12)+' por ano).\\nLevando '+m+'% dos pedidos para o seu cardápio, você economiza cerca de '+f(ec)+' por mês, já descontando a mensalidade.';}}document.querySelectorAll('input').forEach(i=>i.addEventListener('input',c));c();</script>'''
    out['/ferramentas/calculadora-comissao-delivery/'] = page('/ferramentas/calculadora-comissao-delivery/', 'Calculadora de comissão de delivery: quanto o aplicativo leva do seu restaurante', 'Calcule grátis quanto seu restaurante paga de comissão para aplicativos de delivery e quanto economiza com cardápio digital próprio.',
        'Calculadora de comissão de delivery', 'Quanto o aplicativo leva por mês e quanto você economiza com o seu próprio cardápio.', f2, crumbs=[('Início', '/'), ('Ferramentas', '/ferramentas/'), ('Comissão de delivery', None)], ld=[ORG, crumbs_ld([('Início', '/'), ('Ferramentas', '/ferramentas/'), ('Comissão de delivery', '/ferramentas/calculadora-comissao-delivery/')])], src='ferr-comissao', og='og-food.png')
    T = {'confirmacao': ('Confirmação', 'Oi, {c}! Passando para confirmar seu {s} amanhã às {h}, aqui na {n}. Posso confirmar? Responda SIM ou, se precisar, te ajudo a remarcar 😊'),
         'lembrete': ('Lembrete do dia', 'Bom dia, {c}! Hoje às {h} tem o seu {s} na {n}. Te esperamos! Se tiver qualquer imprevisto, me avisa por aqui.'),
         'followup': ('Retomar quem sumiu', 'Oi, {c}! Vi que ficou alguma dúvida sobre o {s}. Separei dois horários livres esta semana. Quer que eu reserve um para você?'),
         'pos': ('Pós-atendimento', 'Oi, {c}! Obrigado por vir à {n} hoje 💙 Como foi o seu {s}? Sua opinião ajuda muito a gente.'),
         'avaliacao': ('Pedir avaliação no Google', 'Oi, {c}! Ficamos felizes em te atender. Se puder, deixe sua avaliação da {n} no Google, leva 1 minuto e ajuda muito: [link]'),
         'aniversario': ('Aniversário', 'Feliz aniversário, {c}! 🎉 A equipe da {n} deseja um ano incrível. Tem um mimo esperando por você no seu próximo {s}.'),
         'retorno': ('Chamar para retorno', 'Oi, {c}! Já faz um tempinho desde o seu último {s} na {n}. Que tal agendar o próximo? Tenho horários nesta semana.')}
    opts = ''.join(f'<option value="{k}">{v[0]}</option>' for k, v in T.items())
    import json as _j
    f3 = f'''<div class="art"><p>Escolha o tipo de mensagem, preencha os campos e copie. Funciona para clínica, salão, escritório, imobiliária, pet shop ou loja.</p>
<p><label>Tipo de mensagem<br><select id="k" {INP.replace('130px', '260px')}>{opts}</select></label></p>
<p><label>Nome do negócio<br><input id="n" value="Clínica Bella" {INP.replace('130px', '260px')}></label></p>
<p><label>Nome do cliente<br><input id="cl" value="Mariana" {INP.replace('130px', '260px')}></label></p>
<p><label>Serviço<br><input id="s" value="atendimento" {INP.replace('130px', '260px')}></label></p>
<p><label>Horário<br><input id="h" value="14h" {INP}></label></p>
<blockquote id="r"></blockquote><button class="btn pri" id="cp" type="button">Copiar mensagem</button>
<h2>Dicas para mensagens que funcionam</h2><ul><li>Use o primeiro nome do cliente.</li><li>Uma pergunta por mensagem, com resposta fácil ("responda SIM").</li><li>No máximo um emoji.</li><li>Sempre ofereça o próximo passo: confirmar, remarcar ou agendar.</li><li>Envie em horário comercial; à noite, só se o cliente puxou a conversa.</li></ul>
<p>Mais modelos: <a href="/blog/mensagem-de-confirmacao-de-consulta-modelos/">confirmação de consulta</a> · <a href="/blog/modelos-de-follow-up-no-whatsapp/">follow-up no WhatsApp</a>.</p>{cta_box('ferr-mensagens', title='A 24AGÁ manda essas mensagens sozinha', sub='Na hora certa, personalizadas, e para quando o cliente responde.')}</div>
<script>var T={_j.dumps({k: v[1] for k, v in T.items()}, ensure_ascii=False)};function c(){{var v=id=>document.getElementById(id).value;document.getElementById('r').textContent=T[v('k')].replace(/\\{{c\\}}/g,v('cl')).replace(/\\{{n\\}}/g,v('n')).replace(/\\{{s\\}}/g,v('s')).replace(/\\{{h\\}}/g,v('h'));}}document.querySelectorAll('input,select').forEach(i=>i.addEventListener('input',c));c();document.getElementById('cp').onclick=function(){{navigator.clipboard.writeText(document.getElementById('r').textContent);this.textContent='Copiado ✓';}};</script>'''
    out['/ferramentas/gerador-de-mensagens-whatsapp/'] = page('/ferramentas/gerador-de-mensagens-whatsapp/', 'Gerador de mensagens para WhatsApp: confirmação, lembrete e follow-up', 'Gere grátis mensagens prontas para WhatsApp: confirmação de horário, lembrete, follow-up, pós-atendimento, avaliação no Google e aniversário.',
        'Gerador de mensagens para WhatsApp', 'Mensagens prontas de confirmação, lembrete, follow-up e pós-atendimento. É só preencher e copiar.', f3, crumbs=[('Início', '/'), ('Ferramentas', '/ferramentas/'), ('Gerador de mensagens', None)], ld=[ORG, crumbs_ld([('Início', '/'), ('Ferramentas', '/ferramentas/'), ('Gerador de mensagens', '/ferramentas/gerador-de-mensagens-whatsapp/')])], src='ferr-mensagens')
    cards = [('/ferramentas/calculadora-de-faltas/', 'Calculadora', 'Calculadora de faltas', 'Quanto as faltas sem aviso custam por mês e por ano.'),
             ('/ferramentas/calculadora-comissao-delivery/', 'Calculadora', 'Comissão de delivery', 'Quanto o aplicativo leva e quanto você economiza com cardápio próprio.'),
             ('/ferramentas/gerador-de-mensagens-whatsapp/', 'Gerador', 'Mensagens para WhatsApp', 'Confirmação, lembrete, follow-up, avaliação e aniversário.'),
             ('/comparativo/recepcionista-ou-atendente-ia/', 'Calculadora', 'Recepcionista ou IA', 'Compare o custo mensal das duas opções.')]
    idx = '<div class="grid">' + ''.join(f'<a class="card" href="{u}"><small>{t}</small><b>{n}</b><p>{d}</p></a>' for u, t, n, d in cards) + '</div>' + cta_box('ferramentas')
    out['/ferramentas/'] = page('/ferramentas/', 'Ferramentas grátis para atendimento no WhatsApp · 24AGÁ', 'Calculadoras e geradores grátis para clínicas, salões, restaurantes e empresas: faltas, comissão de delivery, custo de recepção e mensagens de WhatsApp.',
        'Ferramentas grátis', 'Calculadoras e geradores para atender melhor e perder menos clientes.', idx, crumbs=[('Início', '/'), ('Ferramentas', None)], ld=[ORG, crumbs_ld([('Início', '/'), ('Ferramentas', '/ferramentas/')])], src='ferramentas')
    return out
