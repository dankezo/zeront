/* Zeront popup: fingerprint the current tab and evaluate it against the radar. */

function zerontFingerprint() {
  var out = { server: null, generator: null, signals: [], next: false, wp: false, jquery: null };
  var gen = document.querySelector('meta[name="generator"]');
  if (gen) out.generator = gen.getAttribute('content');
  var html = '';
  try { html = document.documentElement.innerHTML.slice(0, 300000); } catch (e) {}
  if (html.indexOf('/wp-content/') >= 0) { out.wp = true; out.signals.push('/wp-content/'); }
  if (html.indexOf('/_next/') >= 0) { out.next = true; out.signals.push('/_next/'); }
  if (html.indexOf('__next_f') >= 0) out.signals.push('__next_f');
  if (html.indexOf('react-server-dom') >= 0) out.signals.push('react-server-dom');
  var scripts = Array.prototype.slice.call(document.querySelectorAll('script[src]'));
  for (var i = 0; i < scripts.length; i++) {
    var m = scripts[i].src.match(/jquery[-.](\d+\.\d+\.\d+)/i);
    if (m) { out.jquery = m[1]; break; }
  }
  return fetch(location.origin + '/', { method: 'HEAD', credentials: 'omit' })
    .then(function (r) { out.server = r.headers.get('server'); return out; })
    .catch(function () { return out; });
}

var VERDICT_TEXT = {
  match: 'Trong dải phiên bản dính lỗi đang theo dõi',
  signal: 'Có dấu hiệu công nghệ dính lỗi - cần kiểm tra phiên bản',
  patched: 'Đã ở bản vá',
  clear: 'Ngoài dải phiên bản dính lỗi'
};

async function zGetFeed() {
  var store = await chrome.storage.local.get(['feed', 'feedAt']);
  if (store.feed && store.feedAt && (Date.now() - store.feedAt) < 6 * 3600 * 1000) return store.feed;
  for (var i = 0; i < ZERONT_FEEDS.length; i++) {
    try {
      var r = await fetch(ZERONT_FEEDS[i], { cache: 'no-store' });
      if (r.ok) {
        var feed = await r.json();
        await chrome.storage.local.set({ feed: feed, feedAt: Date.now() });
        return feed;
      }
    } catch (e) {}
  }
  return store.feed || null;
}

function esc(s) {
  return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
  });
}

async function main() {
  var feed = await zGetFeed();
  var feedAtEl = document.getElementById('feedAt');
  if (feed && feed.generated_at) feedAtEl.textContent = 'Radar ' + feed.generated_at.slice(0, 10);
  var tabs = await chrome.tabs.query({ active: true, currentWindow: true });
  var tab = tabs[0];
  var hostEl = document.getElementById('host');
  var box = document.getElementById('verdicts');
  var fpEl = document.getElementById('fp');
  if (!tab || !tab.url || !/^https?:/.test(tab.url)) {
    hostEl.textContent = 'Trang này không kiểm tra được';
    box.innerHTML = '<div class="verdict"><div class="t">Mở một trang web http/https rồi bấm lại Zeront.</div></div>';
  } else {
    var url = new URL(tab.url);
    hostEl.textContent = url.hostname;
    try {
      var res = await chrome.scripting.executeScript({ target: { tabId: tab.id }, func: zerontFingerprint });
      var fp = res && res[0] && res[0].result;
      if (!fp) throw new Error('no result');
      var bits = [];
      if (fp.server) bits.push('Máy chủ: <b>' + esc(fp.server) + '</b>');
      if (fp.generator) bits.push('Generator: <b>' + esc(fp.generator) + '</b>');
      if (fp.jquery) bits.push('jQuery: <b>' + esc(fp.jquery) + '</b>');
      if (fp.next) bits.push('<b>Next.js</b>');
      if (fp.wp) bits.push('<b>WordPress</b>');
      fpEl.innerHTML = bits.length ? bits.join(' · ') : 'Không thấy dấu vết công nghệ nào nổi bật.';
      if (feed) {
        var ev = zEvalFingerprint(fp, feed.featured || []);
        var hits = ev.filter(function (e) { return e.verdict === 'match' || e.verdict === 'signal'; });
        if (hits.length) {
          box.innerHTML = hits.map(function (e) {
            return '<div class="verdict ' + e.verdict + '"><div class="t">' + VERDICT_TEXT[e.verdict] + '</div>'
              + '<div class="e">' + esc(e.item.cves.join(', ')) + ' · ' + esc(e.evidence) + '</div>'
              + '<div class="n">' + esc(e.item.match.note_vi) + ' <a href="https://secuscan.dannyphan.me/radar/" target="_blank" rel="noopener">Cách vá</a></div></div>';
          }).join('');
        } else {
          box.innerHTML = '<div class="verdict ok"><div class="t">Chưa thấy dấu hiệu dính các lỗi đang theo dõi</div>'
            + '<div class="n">Đối chiếu ' + (feed.featured || []).length + ' mục radar với dấu vết công khai của trang này.</div></div>';
        }
      }
    } catch (e) {
      box.innerHTML = '<div class="verdict"><div class="t">Trang chặn việc đọc dấu vết (hoặc là trang hệ thống).</div><div class="n">Thử lại trên trang web thông thường.</div></div>';
    }
  }
  var news = document.getElementById('news');
  if (feed && feed.kev_recent) {
    news.innerHTML = feed.kev_recent.slice(0, 4).map(function (v) {
      return '<a href="' + esc(v.link) + '" target="_blank" rel="noopener"><span class="d">' + esc(v.added.slice(5)) + '</span><span class="c">' + esc(v.cve) + '</span><span>' + esc(v.vendor + ' ' + v.product) + '</span></a>';
    }).join('');
  } else {
    news.innerHTML = '<span class="dim">Chưa tải được dữ liệu radar - kiểm tra mạng rồi mở lại.</span>';
  }
}

document.getElementById('optLink').addEventListener('click', function (e) {
  e.preventDefault();
  chrome.runtime.openOptionsPage();
});
main();
