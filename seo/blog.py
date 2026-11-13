"""Blog: cada artigo é um arquivo .md em seo/artigos/ (cabeçalho chave: valor, depois --- e o texto).
Formato do texto: ## título, ### subtítulo, - lista, 1. lista numerada, > citação (modelo de mensagem), | tabela |, **negrito**, [link](/url).
A seção "## Perguntas frequentes" com ### pergunta + parágrafo vira FAQ com Schema automaticamente."""
import os, re, glob, html
from shell import *
DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'artigos')
CATS = {'clinicas': 'Clínicas e consultórios', 'saloes': 'Salões e barbearias', 'escritorios': 'Escritórios', 'imobiliarias': 'Imobiliárias',
        'petshops': 'Pet shops', 'restaurantes': 'Restaurantes e delivery', 'lojas': 'Lojas e vendas', 'whatsapp': 'Atendimento no WhatsApp', 'ia': 'Inteligência artificial'}

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', t)
    return t

def md(body):
    out, faq, L, i = [], [], body.strip().split('\n'), 0
    in_faq = False
    while i < len(L):
        ln = L[i].rstrip()
        if not ln.strip(): i += 1; continue
        if ln.startswith('## '):
            in_faq = ln[3:].strip().lower().startswith('perguntas frequentes'); out.append(f'<h2>{inline(ln[3:])}</h2>'); i += 1; continue
        if ln.startswith('### '):
            q = ln[4:].strip()
            if in_faq:
                a = []; i += 1
                while i < len(L) and L[i].strip() and not L[i].startswith('#'): a.append(L[i].strip()); i += 1
                faq.append((q, ' '.join(a))); continue
            out.append(f'<h3>{inline(q)}</h3>'); i += 1; continue
        if ln.startswith('> '):
            q = []
            while i < len(L) and L[i].startswith('>'): q.append(L[i][1:].strip()); i += 1
            out.append('<blockquote>' + inline('\n'.join(q)) + '</blockquote>'); continue
        if ln.startswith('|'):
            rows = []
            while i < len(L) and L[i].startswith('|'):
                c = [x.strip() for x in L[i].strip().strip('|').split('|')]
                if not all(set(x) <= set('-: ') for x in c): rows.append(c)
                i += 1
            h = '<tr>' + ''.join(f'<th>{inline(x)}</th>' for x in rows[0]) + '</tr>'
            out.append('<table>' + h + ''.join('<tr>' + ''.join(f'<td>{inline(x)}</td>' for x in r) + '</tr>' for r in rows[1:]) + '</table>'); continue
        m = re.match(r'^(\d+)\. |^- ', ln)
        if m:
            tag = 'ol' if ln[0].isdigit() else 'ul'; items = []
            while i < len(L) and re.match(r'^(\d+)\. |^- ', L[i]): items.append(re.sub(r'^(\d+)\. |^- ', '', L[i])); i += 1
            out.append(f'<{tag}>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + f'</{tag}>'); continue
        if ln.strip() == '[cta]': out.append('[[CTA]]'); i += 1; continue
        p = []
        while i < len(L) and L[i].strip() and not re.match(r'^(#|>|\||- |\d+\. |\[cta\])', L[i]): p.append(L[i].strip()); i += 1
        out.append('<p>' + inline(' '.join(p)) + '</p>')
    return out, faq

def load():
    arts = []
    for f in sorted(glob.glob(os.path.join(DIR, '*.md'))):
        raw = open(f, encoding='utf-8').read(); head, body = raw.split('\n---\n', 1)
        meta = dict(l.split(':', 1) for l in head.strip().split('\n')); meta = {k.strip(): v.strip() for k, v in meta.items()}
        meta['slug'] = os.path.basename(f)[:-3]; meta['body'] = body; arts.append(meta)
    return sorted(arts, key=lambda a: a['date'], reverse=True)

def words(h): return len(re.sub('<[^>]+>', ' ', h).split())

def build():
    arts, out = load(), {}
    by = {a['slug']: a for a in arts}
    for a in arts:
        parts, faq = md(a['body'])
        bodyh = '\n'.join(parts)
        if faq: bodyh += faq_html(faq)
        n = words(bodyh); mins = max(2, round(n / 200))
        bodyh = bodyh.replace('[[CTA]]', cta_box('blog-' + a['slug'][:30], a.get('seg', '')))
        rel = [by[s.strip()] for s in a.get('related', '').split(',') if s.strip() in by][:3]
        if len(rel) < 3: rel += [x for x in arts if x['cat'] == a['cat'] and x['slug'] != a['slug'] and x not in rel][:3 - len(rel)]
        relh = ('<div class="rel"><h2>Leia também</h2><div class="grid">' + ''.join(f'<a class="card" href="/blog/{r["slug"]}/"><small>{CATS.get(r["cat"], "")}</small><b>{html.escape(r["title"])}</b><p>{html.escape(r["desc"][:120])}…</p></a>' for r in rel) + '</div></div>') if rel else ''
        links = ''.join(f'<p><b>Para o seu negócio:</b> <a href="{u}">{html.escape(t)}</a></p>' for u, t in [x.split('|') for x in a.get('pages', '').split(',') if '|' in x])
        tl = f'<div class="tldr"><b>Resposta rápida</b>{inline(a["tldr"])}</div>' if a.get('tldr') else ''
        path = f'/blog/{a["slug"]}/'
        d = a['date']; dt = f'{d[8:10]}/{d[5:7]}/{d[:4]}'
        ld = [ORG, crumbs_ld([('Início', '/'), ('Blog', '/blog/'), (a['title'], path)]),
              {"@context": "https://schema.org", "@type": "Article", "headline": a['title'], "description": a['desc'], "datePublished": d, "dateModified": a.get('updated', d),
               "author": {"@type": "Organization", "name": "Equipe 24AGÁ", "url": SITE}, "publisher": {"@type": "Organization", "name": "24AGÁ", "logo": {"@type": "ImageObject", "url": SITE + "/icon-512.png"}},
               "mainEntityOfPage": SITE + path, "image": SITE + "/og-24aga.png", "inLanguage": "pt-BR", "wordCount": n}]
        if faq: ld.append(faq_ld(faq))
        art = f'<article class="art">{tl}{bodyh}{links}{cta_box("blog-fim", a.get("seg", ""))}</article>{relh}'
        out[path] = page(path, a['title'] + ' · 24AGÁ', a['desc'], html.escape(a.get('h1', a['title'])), inline(a['intro']), art,
                         crumbs=[('Início', '/'), ('Blog', '/blog/'), (CATS.get(a['cat'], ''), f'/blog/#{a["cat"]}')], ld=ld, meta=f'Equipe 24AGÁ · {dt} · {mins} min de leitura', src='blog', seg=a.get('seg', ''))
    secs = ''
    for k, nm in CATS.items():
        L = [a for a in arts if a['cat'] == k]
        if not L: continue
        secs += f'<h2 id="{k}" style="font:800 22px Montserrat,sans-serif;margin:30px 0 12px">{nm}</h2><div class="grid">' + ''.join(f'<a class="card" href="/blog/{a["slug"]}/"><small>{nm}</small><b>{html.escape(a["title"])}</b><p>{html.escape(a["desc"][:130])}…</p></a>' for a in L) + '</div>'
    ld = [ORG, crumbs_ld([('Início', '/'), ('Blog', '/blog/')]), {"@context": "https://schema.org", "@type": "Blog", "name": "Blog da 24AGÁ", "url": SITE + "/blog/", "inLanguage": "pt-BR",
          "blogPost": [{"@type": "BlogPosting", "headline": a['title'], "url": f"{SITE}/blog/{a['slug']}/", "datePublished": a['date']} for a in arts]}]
    out['/blog/'] = page('/blog/', 'Blog da 24AGÁ · Atendimento no WhatsApp, agenda e vendas com IA', 'Guias práticos e modelos prontos para clínicas, salões, escritórios, imobiliárias, pet shops e restaurantes atenderem e venderem mais pelo WhatsApp.',
                         'Blog da 24AGÁ', 'Guias práticos e modelos prontos para atender melhor, agendar mais e vender pelo WhatsApp.', secs + cta_box('blog-index'), crumbs=[('Início', '/'), ('Blog', None)], ld=ld, src='blog')
    return out, arts
