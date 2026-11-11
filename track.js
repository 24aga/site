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
  if (wa) return px('Contact', { content_name: wa.closest('.exit24') ? 'popup-saida' : 'whatsapp', content_category: nicheNow() });
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
