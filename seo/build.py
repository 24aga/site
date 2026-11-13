"""24AGÁ · gera o site de conteúdo. Rode: python3 seo/build.py
- Páginas de segmento (landing.py), preços/comparativos/ferramentas (content.py) e blog (blog.py + seo/artigos/*.md)
- Schema (JSON-LD) nas páginas feitas à mão, sitemap.xml, robots.txt e llms.txt"""
import os, re, sys, json, html, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import ORG, SITE, faq_ld, crumbs_ld
import landing, content, blog
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.date.today().isoformat()

def write(path, txt):
    f = os.path.join(ROOT, path.strip('/'), 'index.html') if path.endswith('/') else os.path.join(ROOT, path.strip('/'))
    os.makedirs(os.path.dirname(f), exist_ok=True); open(f, 'w', encoding='utf-8').write(txt)

pages = {}
pages.update(landing.build()); pages['/precos/'] = content.precos(); pages.update(content.comparativos()); pages.update(content.ferramentas())
bp, arts = blog.build(); pages.update(bp)
for p, t in pages.items(): write(p, t)

# Schema nas páginas feitas à mão
SOFT = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "24AGÁ", "applicationCategory": "BusinessApplication", "operatingSystem": "Web, Android, iOS",
        "description": "Atendente com inteligência artificial no WhatsApp que responde, agenda e vende 24 horas para clínicas, empresas e restaurantes.",
        "offers": {"@type": "AggregateOffer", "priceCurrency": "BRL", "lowPrice": "0", "highPrice": "1197", "offerCount": "8"}, "url": SITE}
HAND = {'index.html': ('Clínicas', '/'), 'business/index.html': ('Empresas', '/business/'), 'food/index.html': ('Restaurantes', '/food/'), 'salao/index.html': ('Salões', '/salao/'),
        'escritorio/index.html': ('Escritórios', '/escritorio/'), 'imobiliaria/index.html': ('Imobiliárias', '/imobiliaria/'), 'petshop/index.html': ('Pet shops', '/petshop/'), 'links/index.html': ('Links', '/links/')}
for f, (nm, u) in HAND.items():
    fp = os.path.join(ROOT, f); s = open(fp, encoding='utf-8').read()
    s = re.sub(r'<!--seo-ld-->.*?<!--/seo-ld-->\n?', '', s, flags=re.S)
    faq = [(html.unescape(re.sub('<[^>]+>', '', q)).strip(), html.unescape(re.sub('<[^>]+>', '', a)).strip()) for q, a in re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>', s, flags=re.S)]
    ld = [ORG, SOFT] + ([{"@context": "https://schema.org", "@type": "WebSite", "name": "24AGÁ", "url": SITE}] if u == '/' else []) + ([faq_ld(faq)] if faq else []) + ([crumbs_ld([('Início', '/'), (nm, u)])] if u != '/' else [])
    block = '<!--seo-ld-->' + ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld) + '<!--/seo-ld-->\n'
    s = s.replace('</head>', block + '</head>', 1) if '</head>' in s else s.replace('<div id="app">', block + '<div id="app">', 1)
    if u == '/links/' and '<link rel="canonical"' not in s: s = s.replace('<meta name="theme-color"', '<link rel="canonical" href="https://24aga.com.br/links/">\n<meta name="theme-color"', 1)
    open(fp, 'w', encoding='utf-8').write(s)

# sitemap
urls = [('/', '1.0', 'weekly')] + [(u, '0.9', 'monthly') for _, u in HAND.values() if u not in ('/', '/links/')] + [(p, '0.9', 'monthly') for p in landing.build()] + \
       [('/precos/', '0.9', 'monthly'), ('/blog/', '0.8', 'weekly'), ('/ferramentas/', '0.7', 'monthly')] + [(p, '0.7', 'monthly') for p in pages if p.startswith(('/comparativo/', '/ferramentas/')) and p != '/ferramentas/'] + \
       [(f"/blog/{a['slug']}/", '0.6', 'monthly') for a in arts] + [('/links/', '0.4', 'monthly'), ('/privacidade.html', '0.2', 'yearly'), ('/termos.html', '0.2', 'yearly')]
seen, rows = set(), []
for u, pr, cf in urls:
    if u in seen: continue
    seen.add(u); rows.append(f'<url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{cf}</changefreq><priority>{pr}</priority></url>')
open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(rows) + '\n</urlset>\n')

open(os.path.join(ROOT, 'robots.txt'), 'w').write('''# 24AGÁ · robots.txt
User-agent: *
Allow: /
Disallow: /infra/
Disallow: /supabase/
Disallow: /seo/

# Buscadores de IA são bem-vindos
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot-Extended
Allow: /
User-agent: Bingbot
Allow: /

Sitemap: https://24aga.com.br/sitemap.xml
''')

seg_list = '\n'.join(f"- [{d['name']}]({SITE}/{d['path']}/): {d['desc']}" for d in landing.S)
art_list = '\n'.join(f"- [{a['title']}]({SITE}/blog/{a['slug']}/): {a['desc']}" for a in arts)
open(os.path.join(ROOT, 'llms.txt'), 'w', encoding='utf-8').write(f'''# 24AGÁ

> 24AGÁ é uma atendente com inteligência artificial no WhatsApp, feita no Brasil, que responde clientes 24 horas, tira dúvidas, passa preços, agenda horários, confirma presença, faz follow-up e vende, avisando a equipe no celular quando precisa de uma pessoa. Atende clínicas e consultórios, salões e barbearias, escritórios de advocacia e contabilidade, imobiliárias, pet shops, empresas e lojas, e restaurantes (cardápio digital grátis, pedidos no WhatsApp sem comissão).

Fatos principais:
- Funciona no número de WhatsApp que o negócio já usa (conexão por QR Code ou API oficial da Meta).
- A IA usa só as informações aprovadas pelo negócio; não dá diagnóstico, parecer jurídico ou orientação veterinária, e encaminha urgências para a equipe.
- Agenda na agenda real do negócio, sem conflito, com aprovação da equipe em um toque.
- Confirmação, lembretes, lista de espera, follow-up automático, Pix na conversa, entende áudio.
- App para celular e computador com conversas, agenda, funil de clientes e relatórios em reais.
- Preços: planos Essencial (R$ 397/mês), Profissional (R$ 697/mês) e Premium (R$ 1.197/mês) mais implantação única; restaurantes com cardápio grátis e planos a partir de R$ 97/mês. Sem comissão por venda ou pedido. Teste grátis sem cartão (100 mensagens).
- Empresa: ROITY BUSINESS SOLUTIONS LTDA, CNPJ 53.472.596/0001-99. Contato: WhatsApp +55 66 99908-7424.

## Páginas principais
- [Clínicas e consultórios]({SITE}/): atendente com IA para clínicas, odontologia, estética, médicos e bem-estar.
- [Empresas e lojas]({SITE}/business/): atendente que vende, com catálogo e Pix no WhatsApp.
- [Restaurantes · 24AGÁ Food]({SITE}/food/): cardápio digital grátis, pedidos no WhatsApp sem comissão.
- [Salões]({SITE}/salao/), [Escritórios]({SITE}/escritorio/), [Imobiliárias]({SITE}/imobiliaria/), [Pet shops]({SITE}/petshop/)
- [Preços]({SITE}/precos/)
- [Chatbot ou atendente com IA]({SITE}/comparativo/chatbot-ou-atendente-ia/) · [Recepcionista ou IA]({SITE}/comparativo/recepcionista-ou-atendente-ia/)
- [Ferramentas grátis]({SITE}/ferramentas/)

## Segmentos
{seg_list}

## Blog
{art_list}
''')
print(len(pages), 'páginas geradas ·', len(arts), 'artigos ·', len(rows), 'URLs no sitemap')
