/* Meta Pixel 24AGÁ: eventos de conversão e engajamento */
!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
const PIXEL_ID = '1773671088100425';
fbq('init', PIXEL_ID);
fbq('track', 'PageView');
const px = (ev, params, custom, opts) => { try { fbq(custom ? 'trackCustom' : 'track', ev, params || {}, opts || {}); } catch (e) {} };
const pxOnce = {};
const once = (k, fn) => { if (pxOnce[k]) return; pxOnce[k] = true; fn(); };
const nicheNow = () => { try { return currentNiche(); } catch (e) { return ''; } };
const planInfo = k => { try { return PLANS24.find(p => p.k === k) || {}; } catch (e) { return {}; } };

// Link do anúncio com ?nicho=estetica|odonto|medico|bemestar abre o site já nesse segmento
(function () {
  try {
    const n = (new URLSearchParams(location.search).get('nicho') || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z]/g, '');
    const map = { estetica:'estetica', odonto:'odonto', odontologia:'odonto', medico:'medico', medicos:'medico', medicina:'medico', bemestar:'bemestar', saude:'bemestar' };
    if (map[n]) localStorage.setItem('24h.niche', map[n]);
  } catch (e) {}
})();

// Link de parceiro: 24aga.com.br/?parceiro=CODIGO (fica guardado por 90 dias)
(function () {
  try {
    const c = (new URLSearchParams(location.search).get('parceiro') || '').trim().toLowerCase().replace(/[^a-z0-9-]/g, '').slice(0, 30);
    if (c) { localStorage.setItem('24h.parceiro', c); localStorage.setItem('24h.parceiro.at', String(Date.now())); }
    else if (Date.now() - Number(localStorage.getItem('24h.parceiro.at') || 0) > 90 * 864e5) localStorage.removeItem('24h.parceiro');
  } catch (e) {}
})();

// Origem do visitante (UTM / clique do anúncio), guardada para ir junto com o lead
(function () {
  try {
    const q = new URLSearchParams(location.search), keep = {};
    ['utm_source','utm_medium','utm_campaign','utm_content','utm_term','fbclid'].forEach(k => { if (q.get(k)) keep[k] = q.get(k); });
    if (Object.keys(keep).length) localStorage.setItem('24h.utm', JSON.stringify(keep));
  } catch (e) {}
})();
function utmTag() {
  try { const u = JSON.parse(localStorage.getItem('24h.utm') || '{}'); return [u.utm_source, u.utm_campaign, u.utm_content].filter(Boolean).join('|'); } catch (e) { return ''; }
}

// Cliques
document.addEventListener('click', e => {
  const t = e.target.closest ? e.target : null; if (!t) return;
  const wa = t.closest('a[href*="wa.me"]');
  if (wa) return px('Contact', { content_name: wa.closest('.exit24') ? 'popup-saida' : wa.id === 'wa-float' ? 'botao-flutuante' : 'whatsapp', content_category: nicheNow() });
  const b = t.closest('[data-a]'); if (!b) return;
  const a = b.dataset.a;
  if (a === 'choosePlan') { const p = planInfo(b.dataset.k); px('InitiateCheckout', { content_name: p.name || b.dataset.k, value: p.price || 0, currency: 'BRL', content_category: nicheNow() }); }
  else if (a === 'pickNiche') px('EscolheuNicho', { nicho: b.dataset.k }, true);
  else if (a === 'startTour') px('TourDemonstracao', { nicho: nicheNow() }, true);
}, true);
document.addEventListener('change', e => { if (e.target && e.target.id === 'ld-p') { const p = planInfo(e.target.value); px('InitiateCheckout', { content_name: p.name, value: p.price || 0, currency: 'BRL' }); } }, true);

// Começou a preencher o cadastro
document.addEventListener('focusin', e => {
  if (e.target && e.target.closest && e.target.closest('#contato form, form#ld, form[data-f="lead"]')) once('form', () => px('ComecouCadastro', { nicho: nicheNow() }, true));
}, true);

// Abriu a demonstração
function pxDemo() { once('demo', () => px('ViewContent', { content_name: 'demonstracao', content_category: nicheNow() })); }

// Engajamento: tempo no site, rolagem e seções vistas (bom para públicos e otimização)
setTimeout(() => once('t30', () => px('Engajado30s', { nicho: nicheNow() }, true)), 30000);
setTimeout(() => once('t90', () => px('Engajado90s', { nicho: nicheNow() }, true)), 90000);
addEventListener('scroll', () => {
  const h = document.documentElement, pct = (scrollY + innerHeight) / Math.max(1, h.scrollHeight);
  if (pct > .5) once('s50', () => px('Rolou50', {}, true));
  if (pct > .9) once('s90', () => px('Rolou90', {}, true));
  [['planos','ViuPlanos'], ['contato','ViuCadastro'], ['followup','ViuFollowup']].forEach(([id, ev]) => {
    const el = document.getElementById(id); if (!el) return;
    const r = el.getBoundingClientRect(); if (r.top < innerHeight * .6 && r.bottom > 0) once(id, () => px(ev, { nicho: nicheNow() }, true));
  });
}, { passive: true });

// Cadastro enviado: Lead com dados para a Meta reconhecer a pessoa (ela criptografa antes de enviar)
function pxLead(lead) {
  try {
    const d = (lead.whatsapp || '').replace(/\D/g, '');
    const ph = d.startsWith('55') ? d : '55' + d;
    const nm = (lead.name || '').trim().toLowerCase().split(/\s+/);
    const norm = s => (s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z]/g, '');
    fbq('init', PIXEL_ID, { ph, fn: norm(nm[0]), ln: norm(nm.slice(1).join('')), ct: norm(lead.city), country: 'br' });
  } catch (e) {}
  const p = planInfo(lead.plan);
  const eventID = 'lead-' + Date.now() + '-' + Math.random().toString(36).slice(2, 8);
  px('Lead', { content_name: p.name || lead.plan, content_category: lead.niche, value: p.price || 0, currency: 'BRL' }, false, { eventID });
  return eventID;
}

// Aviso de cookies: aparece uma vez, some ao clicar em Aceitar
(function () {
  let ok = false; try { ok = localStorage.getItem('24h.cookies') === 'ok'; } catch (e) {}
  if (ok) return;
  const show = () => {
    if (document.getElementById('ck24')) return;
    const st = document.createElement('style');
    st.textContent = '#ck24{position:fixed;left:16px;bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:75;max-width:420px;background:#05070D;color:#EEF2FA;border:1px solid #1C2438;border-radius:14px;padding:14px 16px;display:flex;gap:14px;align-items:center;box-shadow:0 16px 40px rgba(0,0,0,.35);font:14px/1.45 Inter,system-ui,sans-serif}#ck24 a{color:#8FB0FF}#ck24 button{flex:none;background:#1F5BFF;color:#fff;border:0;border-radius:10px;padding:10px 18px;font:600 14px Inter,system-ui,sans-serif;cursor:pointer}@media (max-width:980px){#ck24{left:12px;right:12px;max-width:none}body:has(#ck24) .waf{display:none}body[data-mode="demo"] #ck24{bottom:calc(80px + env(safe-area-inset-bottom,0px))}}@media print{#ck24{display:none}}';
    document.head.appendChild(st);
    const d = document.createElement('div'); d.id = 'ck24'; d.setAttribute('role', 'region'); d.setAttribute('aria-label', 'Aviso de cookies');
    d.innerHTML = '<span>Usamos cookies para melhorar sua experiência e medir nossos anúncios. Saiba mais na <a href="privacidade.html">Política de Privacidade</a>.</span><button type="button">Aceitar</button>';
    d.querySelector('button').onclick = () => { try { localStorage.setItem('24h.cookies', 'ok'); } catch (e) {} d.remove(); };
    document.body.appendChild(d);
  };
  if (document.body) show(); else document.addEventListener('DOMContentLoaded', show);
})();
