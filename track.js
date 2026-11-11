/* Meta Pixel 24AGÁ + eventos de conversão */
!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '1773671088100425');
fbq('track', 'PageView');
const px = (ev, params, custom) => { try { fbq(custom ? 'trackCustom' : 'track', ev, params || {}); } catch (e) {} };
const pxOnce = {};
// Clique em qualquer link de WhatsApp = Contact
document.addEventListener('click', e => {
  const a = e.target.closest && e.target.closest('a[href*="wa.me"]');
  if (a) px('Contact', { content_name: a.closest('.exit24') ? 'popup-saida' : 'whatsapp' });
}, true);
// Primeira vez que abre a demonstração = ViewContent
function pxDemo(route) {
  if (pxOnce.demo) return; pxOnce.demo = true;
  px('ViewContent', { content_name: 'demonstracao', content_category: (window.currentNiche ? currentNiche() : '') });
}
