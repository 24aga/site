/* 24AGÁ · PREÇOS — fonte única: tela "Preços" do painel ADM (tabelas pricing e pricing_config).
   Usado nas páginas (Clinic, Business, Food), cadastros, checkout, portal do parceiro e painel.
   Mostra a oferta: "Oferta especial · 30% OFF", preço "de" riscado e o preço "por" (o que é cobrado).
   Marcação automática no HTML:
     <span data-p24="profissional:m"></span>  → mensalidade com de/por  (… /mês)
     <span data-p24="profissional:s"></span>  → implantação com de/por
     <span data-p24-badge></span>             → selo "Oferta especial · 30% OFF" (some se a oferta estiver desligada)
   Se o banco não responder, ficam os valores padrão abaixo. */
(function () {
  const API = 'https://eqfrpmahzvrzzjrcsvbk.supabase.co/rest/v1/';
  const KEY = 'sb_publishable_8sDRdldsSdIWFkdzFy0CLw_gkyqv594';
  const DEF = {
    essencial: { name: 'Essencial', area: 'clinic_business', monthly: 397, setup: 1500, conv_limit: 300 },
    profissional: { name: 'Profissional', area: 'clinic_business', monthly: 697, setup: 2500, conv_limit: 800 },
    premium: { name: 'Premium', area: 'clinic_business', monthly: 1197, setup: 3800, conv_limit: 2000 },
    resto_delivery: { name: 'Delivery', area: 'food', monthly: 97, setup: 197, conv_limit: 0 },
    resto_ia: { name: 'Delivery + IA Start', area: 'food', monthly: 197, setup: 197, conv_limit: 500 },
    resto_ia_pro: { name: 'Delivery + IA Pro', area: 'food', monthly: 297, setup: 197, conv_limit: 1500 },
    resto_ia_max: { name: 'Delivery + IA Max', area: 'food', monthly: 497, setup: 297, conv_limit: 4000 },
  };
  const P = window.P24 = { plans: JSON.parse(JSON.stringify(DEF)), cfg: { show_offer: true, discount_pct: 30, badge: 'Oferta especial' }, loaded: false };
  const isInt = v => Math.abs(v - Math.round(v)) < 0.005;
  P.money = v => 'R$ ' + Number(v).toLocaleString('pt-BR', isInt(+v) ? { maximumFractionDigits: 0 } : { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const D = () => Math.min(90, Math.max(0, Number(P.cfg.discount_pct ?? 30)));
  // preço "de" calculado para o desconto mostrado ser exato (ex.: 30% OFF → preço ÷ 0,7)
  P.orig = v => { const o = Number(v) / (1 - D() / 100); return isInt(+v) ? Math.round(o) : Math.round(o * 100) / 100; };
  P.pct = () => Math.round(D());
  P.offer = () => !!P.cfg.show_offer && D() > 0;
  P.get = k => P.plans[k] || null;
  // "de R$ 906 por R$ 697" em HTML (suffix: "/mês" etc.)
  P.html = (v, suffix = '') => !Number(v) ? `<b>Grátis</b>` : P.offer()
    ? `<s class="p24-de" style="opacity:.6;font-weight:500;font-size:${suffix ? 'max(16px,.55em)' : '.95em'};margin-right:${suffix ? 6 : 4}px;white-space:nowrap">${P.money(P.orig(v))}</s><b class="p24-por" style="white-space:nowrap">${P.money(v)}</b>${suffix}`
    : `<b class="p24-por">${P.money(v)}</b>${suffix}`;
  P.text = v => P.offer() && Number(v) ? `de ${P.money(P.orig(v))} por ${P.money(v)}` : P.money(v);
  P.badge = () => P.offer() ? `${P.cfg.badge} · ${P.pct()}% OFF` : '';
  P.fill = (root = document) => {
    root.querySelectorAll('[data-p24]').forEach(el => {
      const [k, f] = el.dataset.p24.split(':'), p = P.get(k); if (!p) return;
      el.innerHTML = f === 's' ? P.html(p.setup) : P.html(p.monthly, el.dataset.suffix != null ? el.dataset.suffix : '<small>/mês</small>');
    });
    root.querySelectorAll('[data-p24-badge]').forEach(el => { el.textContent = P.badge(); el.hidden = !P.offer(); });
  };
  const h = { apikey: KEY, Authorization: 'Bearer ' + KEY };
  P.ready = Promise.all([
    fetch(API + 'pricing?select=*&active=eq.true&order=position', { headers: h }).then(r => r.ok ? r.json() : null),
    fetch(API + 'pricing_config?select=*&id=eq.1', { headers: h }).then(r => r.ok ? r.json() : null),
  ]).then(([rows, cfg]) => {
    if (Array.isArray(rows) && rows.length) rows.forEach(r => { P.plans[r.key] = { name: r.name, area: r.area, monthly: Number(r.monthly), setup: Number(r.setup), conv_limit: r.conv_limit }; });
    if (Array.isArray(cfg) && cfg[0]) P.cfg = cfg[0];
    P.loaded = true;
  }).catch(() => {}).then(() => { try { P.fill(); } catch (e) {} document.dispatchEvent(new Event('p24')); return P; });
})();
