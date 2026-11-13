"""24AGÁ · moldura comum das páginas de conteúdo (preços, comparativos, ferramentas, blog)."""
import html, json
from urllib.parse import quote
SITE = 'https://24aga.com.br'
WA = '5566999087424'
TRIAL = 'https://app.24aga.com.br/teste.html'
esc = html.escape

CSS = """
:root{--ink:#0B1220;--mut:#5B6678;--line:#DFE5EF;--bg:#F4F7FC;--card:#fff;--acc:#1F5BFF;--acc2:#0A2BB8;--dark:#05070D;--soft:#EAF0FF;--ok:#16A34A}
*{box-sizing:border-box}html,body{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased;overflow-x:clip}
a{color:var(--acc)}img{max-width:100%}
.in{max-width:1080px;margin:0 auto;padding:0 18px}.nr{max-width:760px}
nav.top{position:sticky;top:0;z-index:20;background:rgba(5,7,13,.92);backdrop-filter:blur(10px)}
nav.top .in{display:flex;align-items:center;justify-content:space-between;height:60px;gap:10px}
.lg{display:flex;align-items:center;gap:9px;color:#fff;text-decoration:none}.lg img{width:30px;height:30px;border-radius:8px}
.lg b{font:800 19px Montserrat,sans-serif}.lg b i{font-style:normal;color:#6E97FF}
.nl{display:flex;gap:16px;align-items:center}.nl a{color:#C9D3EA;text-decoration:none;font-size:14px;font-weight:600}.nl a:hover{color:#fff}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;border:0;border-radius:12px;padding:13px 20px;font:700 15px Inter,sans-serif;text-decoration:none;cursor:pointer}
.btn.pri{background:var(--acc);color:#fff;box-shadow:0 10px 26px rgba(31,91,255,.3)}.btn.gh{background:#fff;color:var(--ink);border:1px solid var(--line)}
.nl .btn{padding:9px 14px;font-size:14px;color:#fff}
header.hd{background:radial-gradient(70% 90% at 85% 0%,rgba(31,91,255,.45),transparent 60%),var(--dark);color:#fff;padding:46px 0 50px}
.crumbs{font-size:13px;color:#9FB0D3;margin-bottom:12px}.crumbs a{color:#9FB0D3;text-decoration:none}
h1{font:900 clamp(30px,5vw,46px)/1.08 Montserrat,sans-serif;letter-spacing:-.02em;margin:0 0 12px}
header.hd p{font-size:18px;line-height:1.55;color:#D5DDF0;margin:0;max-width:680px}
.meta{margin-top:14px;font-size:13px;color:#9FB0D3}
main{padding:36px 0 30px}
.art{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:30px clamp(18px,4vw,40px)}
.art h2{font:800 26px/1.2 Montserrat,sans-serif;margin:30px 0 10px;letter-spacing:-.01em}.art h3{font-size:19px;margin:22px 0 8px}
.art p,.art li{font-size:17px;line-height:1.7;color:#25304A}.art ul,.art ol{padding-left:22px}.art li{margin:4px 0}
.art blockquote{margin:16px 0;padding:14px 16px;background:var(--soft);border-left:4px solid var(--acc);border-radius:10px;font-size:16px;line-height:1.6;white-space:pre-line}
.art table{display:block;overflow-x:auto;width:100%;border-collapse:collapse;margin:16px 0;font-size:15px}.art th,.art td{border:1px solid var(--line);padding:10px;text-align:left;vertical-align:top}.art th{background:var(--soft)}
.tldr{background:var(--soft);border-radius:14px;padding:16px 18px;margin:0 0 18px;font-size:16px;line-height:1.6}.tldr>b:first-child{display:block;margin-bottom:4px}
.cta{margin:28px 0;background:linear-gradient(135deg,var(--acc),var(--acc2));color:#fff;border-radius:18px;padding:22px;display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap}
.cta b{font:800 20px Montserrat,sans-serif;display:block}.cta span{color:#DCE6FF;font-size:15px}.cta .btn{background:#fff;color:var(--acc2)}
.faq details{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin-bottom:8px}.faq summary{font-weight:700;cursor:pointer}.faq p{margin:8px 0 0;color:var(--mut);line-height:1.6}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}
.card{display:block;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px;text-decoration:none;color:var(--ink)}.card:hover{border-color:var(--acc)}
.card small{color:var(--acc);font-weight:700;font-size:12px;letter-spacing:.06em;text-transform:uppercase}.card b{display:block;font-size:18px;margin:6px 0}.card p{margin:0;color:var(--mut);font-size:15px;line-height:1.5}
.rel{margin-top:30px}.rel h2{font:800 22px Montserrat,sans-serif}
footer.ft{border-top:1px solid var(--line);padding:30px 18px 90px;text-align:center;color:var(--mut);font-size:13.5px;line-height:1.8}footer.ft a{color:var(--mut)}
.fl{display:flex;flex-wrap:wrap;justify-content:center;gap:6px 16px;margin-bottom:10px}
.waf{position:fixed;right:16px;bottom:16px;width:54px;height:54px;border-radius:50%;background:#25D366;display:grid;place-items:center;box-shadow:0 10px 30px rgba(0,0,0,.25);z-index:30}.waf svg{width:27px;height:27px;fill:#fff}
@media (max-width:760px){.nl a:not(.btn){display:none}}
"""

WA_SVG = '<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-3.3-.8-2.8-1.1-4.5-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.4.6-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.2.1.7-.1 1.3z"/></svg>'

FOOT_LINKS = [('/', 'Clínicas'), ('/business/', 'Empresas'), ('/food/', 'Restaurantes'), ('/salao/', 'Salões'), ('/escritorio/', 'Escritórios'),
              ('/imobiliaria/', 'Imobiliárias'), ('/petshop/', 'Pet shops'), ('/precos/', 'Preços'), ('/blog/', 'Blog'), ('/ferramentas/', 'Ferramentas grátis')]

SEG_WA = {'salao': 'para o meu salão', 'escritorio': 'para o meu escritório', 'imobiliaria': 'para a minha imobiliária', 'petshop': 'para o meu pet shop',
          'odonto': 'para o meu consultório odontológico', 'estetica': 'para a minha clínica de estética', 'medico': 'para o meu consultório', 'bemestar': 'para a minha clínica',
          'loja': 'para a minha loja', 'food': 'e o cardápio digital para o meu restaurante'}
def wa_text(seg='', path=''):
    onde = 'Vim pelo blog da 24AGÁ.' if path.startswith('/blog/') else 'Vim pelo site da 24AGÁ.'
    return 'Oi! Quero minha assistente no WhatsApp' + (' ' + SEG_WA[seg] if seg in SEG_WA else '') + '. ' + onde

def trial(src, seg=''):
    if seg == 'food': return f'https://app.24aga.com.br/criar.html?origem={src}'
    if seg == 'loja': return f'{TRIAL}?tipo=loja&origem={src}'
    q = f'?origem={src}' + (f'&segmento={seg}' if seg else '')
    return TRIAL + q

def cta_box(src, seg='', title='Teste a atendente com IA no seu WhatsApp', sub='Grátis, sem cartão. A IA responde até 100 mensagens.'):
    return f'<div class="cta"><div><b>{title}</b><span>{sub}</span></div><a class="btn" href="{esc(trial(src, seg))}" data-ev="cta">Começar teste grátis →</a></div>'

def faq_html(faq):
    return '<div class="faq">' + ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faq) + '</div>'

def page(path, title, desc, h1, intro, body, crumbs=None, ld=None, meta='', og='og-24aga.png', src='site', seg='', head_extra='', scripts=''):
    url = SITE + path
    cr = ''
    if crumbs:
        cr = '<div class="crumbs">' + ' › '.join(f'<a href="{u}">{esc(n)}</a>' if u else esc(n) for n, u in crumbs) + '</div>'
    lds = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or []))
    foot = '<div class="fl">' + ''.join(f'<a href="{u}">{n}</a>' for u, n in FOOT_LINKS) + '</div>'
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#05070D">
<meta property="og:type" content="{'article' if path.startswith('/blog/') and path != '/blog/' else 'website'}">
<meta property="og:site_name" content="24AGÁ">
<meta property="og:locale" content="pt_BR">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}/{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800;900&family=Inter:wght@400;500;600;700&display=swap">
<style>{CSS}</style>
{head_extra}{lds}
</head>
<body>
<nav class="top"><div class="in"><a class="lg" href="/"><img src="/apple-touch-icon.png" alt="24AGÁ"><b>24<i>AGÁ</i></b></a>
<div class="nl"><a href="/blog/">Blog</a><a href="/ferramentas/">Ferramentas</a><a href="/precos/">Preços</a><a class="btn pri" href="{esc(trial(src + '-nav', seg))}">Testar grátis</a></div></div></nav>
<header class="hd"><div class="in nr">{cr}<h1>{h1}</h1><p>{intro}</p>{f'<div class="meta">{meta}</div>' if meta else ''}</div></header>
<main><div class="in nr">{body}</div></main>
<footer class="ft">{foot}24AGÁ · Atendente com IA no WhatsApp · ROITY BUSINESS SOLUTIONS LTDA · CNPJ 53.472.596/0001-99<br><a href="/privacidade.html">Privacidade</a> · <a href="/termos.html">Termos</a></footer>
<a class="waf" href="https://wa.me/{WA}?text={quote(wa_text(seg, path))}" target="_blank" rel="noopener" aria-label="Falar no WhatsApp">{WA_SVG}</a>
<script>
!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init','1773671088100425');fbq('track','PageView');
document.addEventListener('click',function(e){{var a=e.target.closest('a[href*="app.24aga.com.br/teste"]');if(a)try{{fbq('track','StartTrial',{{content_name:'{src}',value:0,currency:'BRL'}})}}catch(x){{}}}},true);
</script>
{scripts}<script src="/utm.js?v=1"></script>
</body>
</html>
'''

ORG = {"@context": "https://schema.org", "@type": "Organization", "name": "24AGÁ", "url": SITE, "logo": SITE + "/icon-512.png",
       "legalName": "ROITY BUSINESS SOLUTIONS LTDA", "taxID": "53.472.596/0001-99",
       "contactPoint": {"@type": "ContactPoint", "telephone": "+55-66-99908-7424", "contactType": "sales", "availableLanguage": "Portuguese"},
       "sameAs": ["https://www.instagram.com/24aga.app/", "https://www.facebook.com/profile.php?id=61596516661834"]}

def faq_ld(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + (u or '')} for i, (n, u) in enumerate(items)]}
