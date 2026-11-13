# Gerador de SEO da 24AGÁ

Rode `python3 seo/build.py` na pasta do site depois de qualquer mudança. Ele gera:
- páginas de segmento (`landing.py`), preços, comparativos e ferramentas (`content.py`)
- o blog (`blog.py` + um arquivo `.md` por artigo em `seo/artigos/`)
- Schema nas páginas feitas à mão, `sitemap.xml`, `robots.txt` e `llms.txt`

Novo artigo: copie um `.md` de `seo/artigos/`, troque o cabeçalho (title, desc, h1, intro, cat, seg, date, tldr, related, pages) e o texto, e rode o build.
A página inicial tem uma "foto" do HTML dentro de `<div id="app">` para Google e IAs lerem; se o texto da home mudar, gere a foto de novo.
Esta pasta não é publicada (veja `.vercelignore`).

Depois de publicar, rode `python3 seo/indexnow.py` para avisar o Bing das páginas novas (chave em `seo/indexnow.key`, arquivo público na raiz).
