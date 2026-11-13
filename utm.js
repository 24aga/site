/* 24AGÁ · origem do anúncio
   Guarda utm_source / utm_campaign / utm_content da visita (vale por 30 dias) e leva junto
   em todo link para o cadastro (app.24aga.com.br), para o ADM saber qual anúncio trouxe cada contato. */
(function () {
  var KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
  try {
    var q = new URLSearchParams(location.search), keep = {}, has = false;
    KEYS.forEach(function (k) { if (q.get(k)) { keep[k] = q.get(k).slice(0, 80); has = true; } });
    if (q.get('fbclid')) { keep.fbclid = '1'; if (!keep.utm_source) { keep.utm_source = 'meta'; has = true; } }
    if (has) { keep.at = Date.now(); localStorage.setItem('24h.utm', JSON.stringify(keep)); }
  } catch (e) {}
  function utm() { try { var u = JSON.parse(localStorage.getItem('24h.utm') || '{}'); if (u.at && Date.now() - u.at > 30 * 864e5) return {}; return u; } catch (e) { return {}; } }
  function carry(a) {
    try {
      var u = new URL(a.href); if (u.hostname !== 'app.24aga.com.br') return;
      var o = utm(); KEYS.forEach(function (k) { if (o[k] && !u.searchParams.get(k)) u.searchParams.set(k, o[k]); });
      a.href = u.toString();
    } catch (e) {}
  }
  document.addEventListener('click', function (e) { var a = e.target.closest && e.target.closest('a[href*="app.24aga.com.br"]'); if (a) carry(a); }, true);
  window.utm24 = utm;
})();
