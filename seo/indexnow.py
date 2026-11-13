"""Avisa Bing (e outros buscadores do IndexNow) sobre páginas novas ou alteradas.
Rode DEPOIS que o site estiver publicado: python3 seo/indexnow.py   (use --todas para reenviar tudo)
Guarda o que já foi enviado em seo/indexnow-enviado.json (endereço → data do sitemap)."""
import os, re, sys, json, urllib.request
D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(D)
KEY = open(os.path.join(D, 'indexnow.key')).read().strip()
sm = open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read()
cur = dict(re.findall(r'<loc>(.*?)</loc><lastmod>(.*?)</lastmod>', sm))
SENT = os.path.join(D, 'indexnow-enviado.json')
sent = json.load(open(SENT)) if os.path.exists(SENT) else {}
todo = list(cur) if '--todas' in sys.argv else [u for u, d in cur.items() if sent.get(u) != d]
if not todo: print('Nada novo para avisar.'); sys.exit()
body = json.dumps({"host": "24aga.com.br", "key": KEY, "keyLocation": f"https://24aga.com.br/{KEY}.txt", "urlList": todo}).encode()
req = urllib.request.Request('https://api.indexnow.org/indexnow', data=body, headers={'Content-Type': 'application/json; charset=utf-8'})
try:
    r = urllib.request.urlopen(req, timeout=30); code = r.status
except urllib.error.HTTPError as e: code = e.code
print('IndexNow respondeu', code, '·', len(todo), 'endereços')
if code in (200, 202):
    sent.update({u: cur[u] for u in todo}); json.dump(sent, open(SENT, 'w'), indent=0)
