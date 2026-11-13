"""Páginas de venda por segmento (mesmo modelo de /salao/, /escritorio/, /imobiliaria/, /petshop/)."""
import os, json
from urllib.parse import quote
from shell import ORG, faq_ld, crumbs_ld
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, 'business/index.html'), encoding='utf-8').read()
CSS = src[src.index('<style>'):src.index('</style>') + 8]
CSS = (CSS.replace('--acc:#7C3AED;--acc2:#5B21B6;--lil:#C9B3FF;--dark:#0A0812', '--acc:#1F5BFF;--acc2:#0A2BB8;--lil:#A9C2FF;--dark:#05070D')
       .replace('#9B6BFF', '#6E97FF').replace('rgba(124,58,237,', 'rgba(31,91,255,').replace('rgba(155,107,255,', 'rgba(110,151,255,')
       .replace('--bg:#FAF8FF', '--bg:#F4F7FC').replace('--line:#E8E3F2', '--line:#DFE5EF').replace('--muted:#635C73', '--muted:#5B6678').replace('--ink:#15121F', '--ink:#0B1220')
       .replace('#DDD6EE', '#D5DDF0').replace('#BFB6D3', '#AEB9D3').replace('#E6DEFF', '#DCE6FF').replace('linear-gradient(135deg,#7C3AED,#1F5BFF)', 'linear-gradient(135deg,#3B73FF,#0A2BB8)'))
TAIL = src[src.index('<script src="/precos.js'):]
WA = src[src.index('<a class="waf"'):]; SVG = WA[WA.index('<svg'):WA.index('</a>')]
COMMON_FAQ = [('Preciso trocar meu número de WhatsApp?', 'Não. A 24AGÁ conecta no número que você já usa, por QR Code, e o WhatsApp continua funcionando normal no seu celular.'),
              ('E se eu quiser responder pessoalmente?', 'É só responder pelo próprio WhatsApp ou pelo app: a IA sai daquela conversa na hora. Depois você devolve para ela com um toque.'),
              ('Ela entende áudio?', 'Sim. Ela ouve os áudios dos clientes e responde por texto.'),
              ('Tem fidelidade?', 'Os planos têm período mínimo informado no contrato. O teste grátis não tem compromisso nenhum.')]

def page(d):
    k, seg = d['path'], d['seg']; T = f'https://app.24aga.com.br/teste.html?segmento={seg}'
    cta = lambda ev, txt, cls='btn pri': f'<a class="{cls}" href="{T}" data-ev="{ev}">{txt}</a>'
    sub = '<span>Sem cartão · a IA responde até 100 mensagens grátis</span>'
    chat = ''.join(f'<div class="m {w}">{t}<small>{h}</small></div>' for w, t, h in d['chat'])
    box = lambda L: ''.join(f'<div class="box"><div class="em">{e}</div><b>{b}</b><p>{p}</p></div>' for e, b, p in L)
    faqs = d['faq'] + COMMON_FAQ
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)
    wa = quote(d['wa']); url = f'https://24aga.com.br/{k}/'
    plan = lambda key, nm, cls: f'<a class="btn {cls}" href="{T}&amp;plano={key}&amp;origem={k}-planos" data-ev="plan-{key}">Quero o {nm}</a>'
    t2 = TAIL.replace("'business-' + (a.dataset.ev || 'site')", f"'{k}-' + (a.dataset.ev || 'site')").replace("content_name:'pagina-business'", f"content_name:'pagina-{k}'").replace("content_category:'business'", f"content_category:'{k}'")
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in [ORG, faq_ld(faqs), crumbs_ld([('Início', '/'), (d['name'], f'/{k}/')]),
        {"@context": "https://schema.org", "@type": "Service", "name": d['title'], "serviceType": "Atendente com inteligência artificial no WhatsApp", "provider": {"@type": "Organization", "name": "24AGÁ"}, "areaServed": "BR", "audience": {"@type": "BusinessAudience", "name": d['short']}, "url": url}])
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{d['title']}</title>
<meta name="description" content="{d['desc']}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#05070D">
<meta property="og:type" content="website"><meta property="og:site_name" content="24AGÁ"><meta property="og:locale" content="pt_BR">
<meta property="og:url" content="{url}"><meta property="og:title" content="{d['title']}"><meta property="og:description" content="{d['desc']}">
<meta property="og:image" content="https://24aga.com.br/og-24aga.png"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,700;0,800;0,900;1,800&family=Inter:wght@400;500;600;700&display=swap">
{CSS}
{ld}
</head>
<body>
<nav><div class="in"><a class="lg" href="/{k}/"><img src="/apple-touch-icon.png" alt=""><span><b>24<i>AGÁ</i></b><small>{d['name']}</small></span></a>
  <div style="display:flex;gap:8px"><a class="btn ghost hide" href="#planos">Planos</a>{cta('cta-nav', 'Testar grátis')}</div></div></nav>
<header class="hero"><div class="in"><div>
  <span class="eyebrow">{d['eyebrow']}</span><h1>{d['h1']}</h1><p class="lead">{d['lead']}</p>
  <div class="ctas">{cta('cta-hero', 'Começar teste grátis →')}<a class="btn ghost" href="https://wa.me/5566999087424?text={wa}" target="_blank" rel="noopener" data-ev="wa-hero">Falar com a gente</a></div>
  <div class="trust"><span>✅ Teste grátis, sem cartão</span><span>✅ Funciona no seu WhatsApp</span><span>✅ Você aprova o que ela pode dizer</span></div>
</div>
<div class="phone"><div class="scr"><div class="wh"><div class="av">24</div><div><b>{d['who']}</b><small>online · responde na hora</small></div></div>
  <div class="ms">{chat}<div class="m i" style="background:#2A3942;align-self:center;font-size:11px;color:#9EB3BB">{d['alert']}</div></div></div></div>
</div></header>
<section><div class="in center"><span class="k">Para quem é</span><h2>Feita para {d['short']}</h2>
  <p class="sub">Se os seus clientes chamam no WhatsApp para perguntar preço, horário ou marcar, a 24AGÁ resolve, com a língua do seu negócio.</p>
  <div class="segs">{''.join(f'<span>{x}</span>' for x in d['tags'])}</div><div class="cta-in">{cta('cta-paraquem', '🚀 Testar grátis no meu negócio')}{sub}</div></div></section>
<section style="padding-top:0"><div class="in"><div class="center"><span class="k">O problema</span><h2>{d.get('probh', 'Cada mensagem sem resposta é um cliente indo para o concorrente')}</h2></div>
  <div class="grid3">{box(d['probs'])}</div><div class="cta-in">{cta('cta-problema', '🚀 Parar de perder clientes · teste grátis')}{sub}</div></div></section>
<section style="padding-top:0"><div class="in"><div class="center"><span class="k">O que ela faz</span><h2>Uma atendente que não falta, não cansa e não esquece</h2></div>
  <div class="grid3">{box(d['feats'])}</div><div class="cta-in">{cta('cta-recursos', '🚀 Quero essa atendente · grátis')}{sub}</div></div></section>
<section style="padding-top:0"><div class="in"><div class="band"><div><b>24h</b><span>atendendo todo dia, inclusive feriados</span></div><div><b>&lt; 30s</b><span>para responder cada cliente</span></div><div><b>100%</b><span>das mensagens respondidas</span></div><div><b>0</b><span>cliente esquecido sem retorno</span></div></div></div></section>
<section style="padding-top:0"><div class="in"><div class="center"><span class="k">Como funciona</span><h2>Pronta em poucos dias, sem trocar seu número</h2></div>
  <div class="steps"><div class="step"><div class="em">📲</div><b>Conecta seu WhatsApp</b><p>Você lê um QR Code com o celular do negócio. O WhatsApp continua funcionando normal.</p></div>
  <div class="step"><div class="em">🧠</div><b>A IA aprende o seu negócio</b><p>Serviços, preços, horários e regras. Você aprova tudo o que ela pode dizer.</p></div>
  <div class="step"><div class="em">🚀</div><b>Ela começa a atender</b><p>Você acompanha pelo app no celular e assume qualquer conversa quando quiser.</p></div></div>
  <div class="cta-in">{cta('cta-como', '🚀 Conectar meu WhatsApp e testar grátis')}{sub}</div></div></section>
<section id="planos" style="padding-top:0"><div class="in"><div class="center"><span class="k">Planos</span><h2>Menos que um funcionário. Trabalha 24 horas.</h2><div style="margin:6px 0 0"><span data-p24-badge hidden style="display:inline-block;background:#DC2626;color:#fff;font-weight:800;font-size:13px;letter-spacing:.04em;padding:6px 12px;border-radius:999px"></span></div><p class="sub">Um ou dois clientes a mais por mês já pagam a mensalidade. Veja todos os detalhes em <a href="/precos/">preços</a>.</p></div>
  <div class="plans">
    <div class="plan"><h3>Essencial</h3><div class="pr" data-p24="essencial:m">R$ 397<small>/mês</small></div><p class="who">Negócios pequenos · implantação <span data-p24="essencial:s">R$ 1.500</span></p><ul><li>Atendente com IA no WhatsApp 24h</li><li>Até 300 conversas por mês</li><li>Agenda, lembretes e confirmação</li><li>Follow-up automático</li><li>Pix na conversa</li></ul>{plan('essencial', 'Essencial', 'dark')}</div>
    <div class="plan top"><h3>Profissional</h3><div class="pr" data-p24="profissional:m">R$ 697<small>/mês</small></div><p class="who">Equipes de 2 a 5 pessoas · implantação <span data-p24="profissional:s">R$ 2.500</span></p><ul><li>Tudo do Essencial</li><li>Até 800 conversas por mês</li><li>Agenda por profissional</li><li>Campanhas e clientes sumidos</li><li>Avaliações no Google</li></ul>{plan('profissional', 'Profissional', 'pri')}</div>
    <div class="plan"><h3>Premium</h3><div class="pr" data-p24="premium:m">R$ 1.197<small>/mês</small></div><p class="who">Negócios maiores ou com filiais · implantação <span data-p24="premium:s">R$ 3.800</span></p><ul><li>Tudo do Profissional</li><li>Até 2.000 conversas por mês</li><li>Várias unidades e equipes</li><li>Relatórios por unidade</li><li>Acompanhamento semanal no 1º mês</li></ul>{plan('premium', 'Premium', 'dark')}</div>
  </div><div class="trial"><div><b>Teste grátis antes de decidir</b><p>A IA responde até 100 mensagens e ouve até 5 áudios dos seus clientes. Sem cartão.</p></div>{cta('cta-trial', 'Começar teste grátis →', 'btn')}</div></div></section>
<section style="padding-top:0"><div class="in"><div class="center"><span class="k">Dúvidas</span><h2>Perguntas frequentes</h2></div><div class="faq">{faq}</div>
  <div class="cta-in">{cta('cta-duvidas', '🚀 Ainda com dúvida? Teste grátis, sem cartão')}{sub}</div>
  <p class="sub center" style="margin-top:20px">Leia também: {' · '.join(f'<a href="{u}">{n}</a>' for u, n in d.get('read', []))}</p></div></section>
<section style="padding-top:0"><div class="in"><div class="final"><h2>{d['final']}</h2><p class="sub" style="color:#D5DDF0;margin:0 auto 22px">Comece o teste grátis agora. Leva 2 minutos.</p>{cta('cta-final', 'Começar teste grátis →')}</div></div></section>
<footer>24AGÁ · Atendente com IA no WhatsApp · <a href="/links/">Outros negócios</a> · <a href="/blog/">Blog</a> · <a href="/ferramentas/">Ferramentas grátis</a> · <a href="/precos/">Preços</a><br>ROITY BUSINESS SOLUTIONS LTDA · CNPJ 53.472.596/0001-99 · <a href="/privacidade.html">Política de Privacidade</a> · <a href="/termos.html">Termos de Uso</a></footer>
<a class="trialbar" href="{T}" data-ev="cta-barra-fixa">🚀 Testar grátis no meu negócio</a>
<a class="waf" href="https://wa.me/5566999087424?text={wa}" target="_blank" rel="noopener" aria-label="Falar no WhatsApp" data-ev="wa-float">{SVG}</a>
{t2}'''

H = lambda e, b, p: (e, b, p)
S = [
 dict(path='odontologia', seg='odonto', name='Odontologia', short='clínicas odontológicas e dentistas',
  title='Atendente com IA no WhatsApp para Dentistas e Clínicas Odontológicas · 24AGÁ', desc='Atendente com IA para consultórios e clínicas odontológicas: responde o WhatsApp 24h, agenda avaliações, confirma consultas e retoma orçamentos de implante e ortodontia. Teste grátis.',
  eyebrow='Para dentistas e clínicas odontológicas', h1='Avaliação marcada, <em>orçamento retomado</em>, cadeira cheia.',
  lead='A atendente com IA responde o WhatsApp do consultório em segundos, explica os tratamentos com os textos que você aprovou, marca a avaliação e confirma na véspera. Quem recebeu orçamento de implante ou aparelho e sumiu é chamado de volta, com cuidado.',
  who='OdontoVida', chat=[('c', 'Oi, quanto custa clareamento?', '21:40'), ('i', 'Oi, Rafaela! O valor do clareamento é definido na avaliação, porque depende do caso. A avaliação é gratuita. Tenho quinta às 10h ou sábado às 9h. Qual prefere?', '21:40'), ('c', 'Sábado 9h', '21:41'), ('i', 'Reservado: sábado às 9h ✅ A Dra. Paula confirma e eu te aviso por aqui.', '21:41')],
  alert='🔔 Aviso para o consultório: avaliação para aprovar',
  probs=[H('🦷', 'Orçamento que esfria', 'Implante, ortodontia e lentes: o paciente pede o valor, recebe o plano e some. Sem retorno, a venda se perde.'), H('📞', 'Recepção dividida', 'Telefone, balcão e WhatsApp ao mesmo tempo. A mensagem espera, e o paciente marca em outro consultório.'), H('🕳️', 'Cadeira vazia', 'Falta sem aviso numa agenda cheia de horários longos é prejuízo que não volta.')],
  feats=[H('💬', 'Responde em segundos, 24h', 'Explica cada tratamento com textos aprovados pelo dentista, sem diagnóstico.'), H('🗓️', 'Agenda avaliações', 'Mostra horários livres e reserva. Você aprova com um toque.'), H('✅', 'Confirma e reduz faltas', 'Confirmação na véspera com um toque e lembrete no dia.'), H('🔁', 'Retoma orçamentos', 'Follow-up de quem recebeu proposta de implante, aparelho ou lentes.'), H('🚨', 'Urgência vai para a equipe', 'Dor forte, inchaço ou sangramento: ela passa na hora para o consultório.'), H('📊', 'Mostra o resultado', 'Avaliações marcadas, propostas e faturamento no painel.')],
  tags=['🦷 Clínicas odontológicas', '😁 Ortodontia', '🔩 Implantes', '✨ Estética dental', '👶 Odontopediatria', '🏥 Redes e franquias'],
  faq=[('A IA fala o preço dos tratamentos?', 'Só o que você cadastrar. Para tratamentos que dependem de avaliação, ela explica isso e oferece o horário da avaliação.'), ('Ela dá orientação clínica?', 'Não. Ela nunca dá diagnóstico nem indica medicação. Sinais de urgência vão direto para a equipe.'), ('Funciona com vários dentistas?', 'Sim. Cada profissional tem a sua agenda, e a IA marca com quem estiver livre ou com o preferido do paciente.')],
  read=[('/blog/como-reduzir-faltas-na-clinica/', 'Como reduzir faltas'), ('/blog/como-responder-preco-no-whatsapp/', 'Como responder preço no WhatsApp')], final='Seu consultório atendendo e agendando 24 horas.', wa='Olá! Quero conhecer a 24AGÁ para o meu consultório odontológico.'),
 dict(path='estetica', seg='estetica', name='Estética', short='clínicas de estética e harmonização',
  title='Atendente com IA no WhatsApp para Clínicas de Estética e Harmonização · 24AGÁ', desc='Atendente com IA para clínicas de estética e harmonização facial: responde leads do Instagram em segundos, agenda avaliações e faz follow-up de quem pediu valor. Teste grátis.',
  eyebrow='Para estética e harmonização facial', h1='Quem viu o seu anúncio <em>recebe resposta na hora</em>.',
  lead='O lead do Instagram pergunta o valor do botox às 22h. A atendente com IA responde em segundos, explica com os textos que a clínica aprovou, oferece a avaliação e reserva. Quem pediu valor e sumiu recebe um follow-up gentil.',
  who='Clínica Vitalle', chat=[('c', 'Vi o anúncio. Quanto é o botox?', '22:14'), ('i', 'Oi, Camila! 😊 A toxina é a partir de R$ 1.200, e a quantidade é definida na avaliação com a Dra. Helena. Tenho terça 15h ou quinta 10h. Qual fica melhor?', '22:14'), ('c', 'Terça 15h', '22:15'), ('i', 'Pré-reservado para terça às 15h ✅ A confirmação chega em instantes.', '22:15')],
  alert='🔔 Aviso para a clínica: avaliação para aprovar · origem: anúncio',
  probs=[H('💸', 'Anúncio pago, lead sem resposta', 'Você paga pelo clique, o lead chama à noite e só recebe resposta no dia seguinte. Já marcou em outra clínica.'), H('💬', '"Quanto custa?" o dia inteiro', 'A mesma pergunta repetida, enquanto a equipe tenta atender quem está na cadeira.'), H('👻', 'Pediu valor e sumiu', 'A maioria não agenda na primeira conversa. Sem follow-up, o investimento no anúncio vai embora.')],
  feats=[H('⚡', 'Responde o lead na hora', 'Em segundos, 24 horas, com o tom da sua clínica.'), H('📝', 'Textos aprovados', 'Ela só explica procedimentos com as informações que você aprovou. Nada de prometer resultado.'), H('🗓️', 'Agenda avaliações', 'Oferece horários livres e reserva. Você aprova com um toque.'), H('🔁', 'Follow-up que converte', '1 hora, 1 dia e 3 dias depois, e para quando a pessoa responde.'), H('📈', 'Sabe de qual anúncio veio', 'Cada contato chega com a origem: você vê qual campanha agenda mais.'), H('🚨', 'Reação vai para a equipe', 'Inchaço, dor ou alergia após procedimento: passa na hora para a clínica.')],
  tags=['💉 Harmonização facial', '✨ Estética facial e corporal', '🧴 Dermatologia estética', '💆 Spas', '🔬 Biomedicina estética', '💄 Micropigmentação'],
  faq=[('A IA promete resultado de procedimento?', 'Não. Ela segue regras fixas: não promete resultado, não dá diagnóstico e não indica se um procedimento serve para a pessoa. Isso é na avaliação.'), ('Dá para saber qual anúncio trouxe o paciente?', 'Sim. A origem (anúncio, Instagram, Google) aparece em cada contato e nos relatórios.'), ('E fotos de antes e depois?', 'Assuntos com fotos e dúvidas clínicas vão para a equipe, que responde pessoalmente.')],
  read=[('/blog/como-responder-preco-no-whatsapp/', 'Como responder preço no WhatsApp'), ('/blog/modelos-de-follow-up-no-whatsapp/', 'Modelos de follow-up')], final='Sua clínica de estética respondendo cada lead em segundos.', wa='Olá! Quero conhecer a 24AGÁ para a minha clínica de estética.'),
 dict(path='medicos', seg='medico', name='Médicos', short='médicos, consultórios e especialistas',
  title='Atendente com IA no WhatsApp para Consultórios Médicos · 24AGÁ', desc='Atendente com IA para consultórios médicos e especialistas: responde o WhatsApp 24h, agenda consultas, confirma presença e encaminha urgências para a equipe. Teste grátis.',
  eyebrow='Para consultórios médicos e especialistas', h1='Consultas agendadas no WhatsApp, <em>com segurança</em>.',
  lead='A atendente com IA responde os pacientes em segundos, passa valores e convênios que você cadastrou, oferece horários e confirma na véspera. Ela nunca dá orientação médica: sinais de urgência vão direto para a equipe.',
  who='Consultório Dr. André', chat=[('c', 'Boa noite, vocês atendem Unimed?', '20:55'), ('i', 'Boa noite, Paulo! Atendemos particular, e emitimos recibo para reembolso. A consulta é R$ 350. Tenho segunda 8h ou quarta 16h.', '20:55'), ('c', 'Quarta 16h', '20:56'), ('i', 'Pré-reservado: quarta às 16h ✅ A secretária confirma em instantes.', '20:56')],
  alert='🔔 Aviso para o consultório: consulta para aprovar',
  probs=[H('☎️', 'Telefone que não para', 'A secretária atende o balcão, o telefone e o WhatsApp. Alguém sempre espera.'), H('🕳️', 'Falta na agenda', 'Consulta marcada e paciente que não vem, sem avisar. Horário perdido.'), H('🌙', 'Mensagem fora do horário', 'O paciente chama à noite e no domingo. Na segunda, já marcou com outro médico.')],
  feats=[H('💬', 'Responde em segundos, 24h', 'Valores, convênios, endereço e preparo, com os textos que você aprovou.'), H('🗓️', 'Agenda consultas', 'Oferece horários livres e reserva. A secretária ou o médico aprova.'), H('✅', 'Confirma presença', 'Confirmação com um toque na véspera e lembrete no dia.'), H('🩺', 'Nunca orienta', 'Não dá diagnóstico, dose ou conduta. Urgência: orienta o SAMU 192 e avisa a equipe.'), H('🔁', 'Chama para retorno', 'Lembra o paciente do retorno no tempo que você definir.'), H('📊', 'Mostra o resultado', 'Consultas marcadas, faltas evitadas e origem dos pacientes.')],
  tags=['🩺 Clínicos e especialistas', '👩‍⚕️ Ginecologia', '🧴 Dermatologia', '🧠 Psiquiatria', '🦴 Ortopedia', '💻 Teleconsulta'],
  faq=[('A IA dá orientação médica?', 'Nunca. Ela é treinada para não dar diagnóstico, dose ou conduta. Sinais de urgência são encaminhados para atendimento imediato e para a equipe.'), ('E os dados dos pacientes?', 'Ficam guardados com segurança, e só a sua equipe tem acesso pelo app.'), ('Funciona com teleconsulta?', 'Sim. Você cadastra a teleconsulta como serviço e ela agenda normalmente.')],
  read=[('/blog/ia-no-whatsapp-e-seguro-para-clinicas/', 'IA no WhatsApp é segura para clínicas?'), ('/blog/mensagem-de-confirmacao-de-consulta-modelos/', 'Mensagens de confirmação')], final='Seu consultório atendendo 24 horas, com segurança.', wa='Olá! Quero conhecer a 24AGÁ para o meu consultório.'),
 dict(path='advocacia', seg='escritorio', name='Advocacia', short='advogados e escritórios de advocacia',
  title='Atendente com IA no WhatsApp para Advogados e Escritórios de Advocacia · 24AGÁ', desc='Atendente com IA para escritórios de advocacia: responde o WhatsApp 24h, faz a triagem do caso, marca reuniões e nunca dá parecer jurídico. Teste grátis.',
  eyebrow='Para advogados e escritórios de advocacia', h1='Triagem feita, <em>reunião marcada</em>, sem você parar o processo.',
  lead='A atendente com IA responde no WhatsApp do escritório em segundos, entende a área do caso (trabalhista, família, previdenciário, cível…), anota um resumo e marca a reunião. Ela nunca dá parecer jurídico: quem orienta é você.',
  who='Silva Advocacia', chat=[('c', 'Boa noite. Meu INSS foi negado, vocês pegam esse tipo de caso?', '22:30'), ('i', 'Boa noite, Marta. Atendemos direito previdenciário, sim. A análise do seu caso é feita pela Dra. Lúcia numa reunião. Prefere presencial ou online?', '22:30'), ('c', 'Online', '22:31'), ('i', 'Tenho amanhã às 11h ou sexta às 15h. Qual fica melhor?', '22:31'), ('c', 'Sexta 15h', '22:31'), ('i', 'Marcado: sexta às 15h, online ✅', '22:32')],
  alert='🔔 Aviso para o escritório: reunião marcada · área: previdenciário',
  probs=[H('⏳', 'Interrupção o dia todo', 'Cada mensagem tira você da peça que está escrevendo.'), H('🌙', 'O caso aparece fora do horário', 'Demissão, separação, prisão: o problema aparece à noite. Fica com o cliente quem responde primeiro.'), H('🗂️', 'Contato que não é para você', 'Muita conversa de área que o escritório não atende. A triagem toma tempo.')],
  feats=[H('💬', 'Responde em segundos, 24h', 'Com educação, sigilo e o tom do seu escritório.'), H('🧭', 'Faz a triagem', 'Identifica a área e anota um resumo, sem pedir documento pelo WhatsApp.'), H('🗓️', 'Marca reuniões', 'Presencial ou online, nos horários livres de cada advogado.'), H('⚖️', 'Nunca dá parecer', 'Não diz se a pessoa tem direito ou quanto vai receber.'), H('🚨', 'Urgência vai para você', 'Audiência, prazo ou prisão: ela te avisa no celular na hora.'), H('📊', 'Mostra o resultado', 'Reuniões marcadas e origem dos clientes no painel.')],
  tags=['👷 Trabalhista', '👪 Família e sucessões', '🧓 Previdenciário', '🏛️ Cível e consumidor', '🚔 Criminal', '🏢 Empresarial'],
  faq=[('A IA dá orientação jurídica?', 'Não. Ela é treinada para nunca dar parecer, nem dizer se a pessoa tem direito. Ela entende o assunto e marca a reunião.'), ('E as regras de publicidade da advocacia?', 'A IA só responde quem procurou o escritório e segue as informações que você aprovar. Revise os textos com base nas normas da OAB que valem para você.'), ('E o sigilo?', 'Ela pede só um resumo curto e nunca pede documentos pelo WhatsApp. Só o escritório acessa as conversas.')],
  read=[('/blog/atendimento-de-escritorio-de-advocacia-no-whatsapp/', 'Atendimento de escritório no WhatsApp'), ('/comparativo/recepcionista-ou-atendente-ia/', 'Recepcionista ou IA?')], final='Seu escritório atendendo 24 horas, sem perder o foco.', wa='Olá! Quero conhecer a 24AGÁ para o meu escritório de advocacia.'),
 dict(path='contabilidade', seg='escritorio', name='Contabilidade', short='escritórios de contabilidade',
  title='Atendente com IA no WhatsApp para Escritórios de Contabilidade · 24AGÁ', desc='Atendente com IA para contadores: responde clientes e novos contatos no WhatsApp 24h, organiza pedidos, marca reuniões e não dá parecer tributário. Teste grátis.',
  eyebrow='Para escritórios de contabilidade', h1='Menos WhatsApp na sua mesa. <em>Mais clientes novos</em>.',
  lead='A atendente com IA responde quem quer abrir empresa, trocar de contador ou tirar uma dúvida. Ela entende o pedido, anota e marca a reunião com a sua equipe. Nada de parecer tributário pelo WhatsApp: isso fica com o contador.',
  who='Contabilidade Prisma', chat=[('c', 'Oi, quero abrir um MEI e depois virar ME. Vocês fazem?', '19:48'), ('i', 'Oi, Diego! Fazemos sim. Para entender o seu caso, o Rodrigo faz uma conversa rápida de 30 min. Tenho amanhã 9h ou 14h, online ou no escritório.', '19:48'), ('c', '14h online', '19:49'), ('i', 'Marcado: amanhã às 14h, online ✅', '19:49')],
  alert='🔔 Aviso para o escritório: reunião marcada · abertura de empresa',
  probs=[H('📲', 'O WhatsApp vira uma fila', 'Guia, boleto, dúvida, pedido de documento: tudo no mesmo número, o dia inteiro.'), H('🧲', 'Cliente novo esperando', 'Quem quer abrir empresa ou trocar de contador chama vários escritórios. Quem responde primeiro, fecha.'), H('⏰', 'Fim de mês caótico', 'Na época de fechamento, ninguém tem tempo de responder com calma.')],
  feats=[H('💬', 'Responde em segundos, 24h', 'Atende novos contatos e clientes com o tom do seu escritório.'), H('🧭', 'Organiza o pedido', 'Abertura, troca de contador, imposto de renda: anota e direciona.'), H('🗓️', 'Marca reuniões', 'Online ou presencial, com quem estiver livre.'), H('🧾', 'Nunca dá parecer', 'Não calcula imposto nem dá orientação tributária pelo WhatsApp.'), H('🔁', 'Retoma propostas', 'Chama de volta quem pediu orçamento de honorários e sumiu.'), H('📊', 'Mostra o resultado', 'Novos clientes e origem de cada contato.')],
  tags=['🧾 Escritórios contábeis', '🏪 Abertura de empresas', '📑 Imposto de renda', '💼 BPO financeiro', '🏢 Departamento pessoal', '📈 Consultoria'],
  faq=[('A IA responde dúvida de imposto?', 'Não. Ela não dá parecer tributário. Ela entende o pedido e passa para a equipe ou marca a reunião.'), ('Funciona para atender clientes atuais também?', 'Sim. Ela responde dúvidas simples que você cadastrar (prazos, documentos, horários) e encaminha o resto.'), ('Dá para separar quem é cliente novo?', 'Sim. Os contatos ficam organizados em etapas no funil, com etiquetas.')],
  read=[('/blog/atendimento-de-escritorio-de-advocacia-no-whatsapp/', 'Atendimento de escritórios no WhatsApp'), ('/blog/modelos-de-follow-up-no-whatsapp/', 'Modelos de follow-up')], final='Seu escritório contábil atendendo 24 horas.', wa='Olá! Quero conhecer a 24AGÁ para o meu escritório de contabilidade.'),
 dict(path='barbearia', seg='salao', name='Barbearias', short='barbearias',
  title='Atendente com IA no WhatsApp para Barbearias · Agenda cheia 24h · 24AGÁ', desc='Atendente com IA para barbearias: responde o WhatsApp 24h, agenda corte e barba com cada barbeiro, lembra o cliente e chama de volta quem sumiu. Teste grátis.',
  eyebrow='Para barbearias', h1='Cadeira cheia, <em>sem largar a máquina</em> para responder.',
  lead='A atendente com IA responde os clientes da barbearia em segundos, passa os valores, mostra os horários de cada barbeiro e marca. Lembra no dia e chama de volta quem não aparece há tempo.',
  who='Barbearia Dom', chat=[('c', 'Fala! Tem horário hoje pra corte e barba?', '18:42'), ('i', 'Fala, Lucas! Hoje tenho 19h com o Léo ou 20h com o Bruno. Corte + barba sai R$ 70. Qual fica melhor?', '18:42'), ('c', '19h com o Léo', '18:42'), ('i', 'Fechado: hoje às 19h com o Léo ✅', '18:43')],
  alert='🔔 Aviso para a barbearia: novo horário marcado',
  probs=[H('✂️', 'Mão na máquina, celular apitando', 'Atendendo, não dá para responder. O cliente vai para a barbearia da esquina.'), H('🕳️', 'Horário vago', 'Falta sem aviso e encaixe que ninguém soube. Cadeira parada é dinheiro perdido.'), H('👻', 'Cliente que não volta', 'Cortava a cada 3 semanas e sumiu. Ninguém chamou.')],
  feats=[H('💬', 'Responde em segundos, 24h', 'Passa valores e tira dúvidas no jeito da sua barbearia.'), H('💈', 'Agenda por barbeiro', 'O cliente escolhe o barbeiro e o horário livre.'), H('✅', 'Lembra e confirma', 'Lembrete no dia com confirmação de um toque.'), H('🔁', 'Traz o cliente de volta', 'Chama quem passou do tempo de corte.'), H('⭐', 'Pede avaliação no Google', 'Depois do corte, pede a avaliação. Sua barbearia sobe no Google.'), H('📊', 'Mostra o faturamento', 'Horários marcados pela IA e faturamento no painel.')],
  tags=['💈 Barbearias', '✂️ Barbeiros autônomos', '🧔 Barba e bigode', '👦 Corte infantil', '🎨 Pigmentação', '🏆 Barbearias premium'],
  faq=[('O cliente escolhe o barbeiro?', 'Sim. A IA pergunta a preferência e mostra só os horários daquele barbeiro.'), ('Dá para encaixar cliente de última hora?', 'Sim. Ela mostra os horários livres do dia e marca na hora.'), ('Funciona com plano de assinatura?', 'Você cadastra os planos como serviço e a IA explica e agenda normalmente.')],
  read=[('/blog/agenda-de-salao-e-barbearia-pelo-whatsapp/', 'Agenda de salão e barbearia pelo WhatsApp'), ('/ferramentas/calculadora-de-faltas/', 'Calculadora de faltas')], final='Sua barbearia agendando 24 horas.', wa='Olá! Quero conhecer a 24AGÁ para a minha barbearia.'),
]
def build():
    out = {}
    for d in S: out[f"/{d['path']}/"] = page(d)
    return out
