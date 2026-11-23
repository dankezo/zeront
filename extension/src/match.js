/* Zeront shared matching logic: deterministic, no AI, no network.
   Used by the popup (page context) and the background service worker. */
var ZERONT_FEEDS = [
  'https://secuscan.dannyphan.me/radar/feed.json',
  'https://dankezo.github.io/zeront/feed.json'
];

function zParseVer(s) {
  return String(s || '').split('.').map(function (x) { var n = parseInt(x, 10); return isNaN(n) ? 0 : n; });
}
function zCmpVer(a, b) {
  var pa = zParseVer(a), pb = zParseVer(b), n = Math.max(pa.length, pb.length);
  for (var i = 0; i < n; i++) {
    var d = (pa[i] || 0) - (pb[i] || 0);
    if (d !== 0) return d < 0 ? -1 : 1;
  }
  return 0;
}
function zInRange(v, range) {
  return String(range || '').split(/\s+/).filter(Boolean).every(function (part) {
    var m = part.match(/^(>=|<=|>|<|=)?(\d+(?:\.\d+)*)$/);
    if (!m) return false;
    var op = m[1] || '=', c = zCmpVer(v, m[2]);
    if (op === '>=') return c >= 0;
    if (op === '<=') return c <= 0;
    if (op === '>') return c > 0;
    if (op === '<') return c < 0;
    return c === 0;
  });
}
/* fp: {server, generator, signals:[], next:bool, wp:bool}
   Returns [{item, verdict: 'match'|'signal'|'patched'|'clear', evidence}] */
function zEvalFingerprint(fp, featured) {
  var out = [];
  (featured || []).forEach(function (f) {
    var m = f.match;
    if (!m) return;
    if (m.type === 'server-version') {
      if (fp.server && fp.server.toLowerCase().indexOf(m.product.toLowerCase()) >= 0) {
        var re = new RegExp(m.product + '\\/(\\d+\\.\\d+\\.\\d+)', 'i');
        var vm = fp.server.match(re);
        if (vm) {
          var v = vm[1];
          if ((m.patched_versions || []).indexOf(v) >= 0) out.push({ item: f, verdict: 'patched', evidence: fp.server });
          else if (zInRange(v, m.affected_range)) out.push({ item: f, verdict: 'match', evidence: fp.server });
          else out.push({ item: f, verdict: 'clear', evidence: fp.server });
        }
      }
    } else if (m.type === 'page-signal') {
      var hits = (m.signals || []).filter(function (s) {
        return (fp.signals || []).indexOf(s) >= 0 || (s === '/_next/' && fp.next);
      });
      if (hits.length) out.push({ item: f, verdict: 'signal', evidence: hits.join(', ') });
    }
  });
  return out;
}
/* Fingerprint from raw homepage HTML + Server header (background checks). */
function zFingerprintFromHtml(html, server) {
  var h = String(html || '').slice(0, 300000);
  var signals = [];
  if (h.indexOf('/wp-content/') >= 0) signals.push('/wp-content/');
  if (h.indexOf('/_next/') >= 0) signals.push('/_next/');
  if (h.indexOf('__next_f') >= 0) signals.push('__next_f');
  if (h.indexOf('react-server-dom') >= 0) signals.push('react-server-dom');
  var gen = null;
  var gm = h.match(/<meta[^>]+name=["']generator["'][^>]+content=["']([^"']+)["']/i);
  if (gm) gen = gm[1];
  return { server: server || null, generator: gen, signals: signals, next: signals.indexOf('/_next/') >= 0, wp: signals.indexOf('/wp-content/') >= 0 };
}
