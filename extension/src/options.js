/* Zeront options: manage the user's own websites + per-domain permissions. */
function esc(s) {
  return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
  });
}
async function getSites() {
  var s = await chrome.storage.local.get(['sites', 'siteResults']);
  return { sites: s.sites || [], results: s.siteResults || {} };
}
async function render() {
  var data = await getSites();
  var box = document.getElementById('sites');
  if (!data.sites.length) { box.innerHTML = '<p>Chưa có website nào.</p>'; return; }
  box.innerHTML = data.sites.map(function (s) {
    var r = data.results[s.domain];
    var hit = r && r.hits && r.hits.length;
    var status = hit
      ? '<span class="tag hit">' + r.hits.length + ' dấu hiệu cần xem</span>'
      : (r ? '<span class="tag on">Đã kiểm tra - ổn</span>' : '<span class="tag">Chưa kiểm tra</span>');
    var perm = s.granted
      ? '<span class="tag on">Tự kiểm tra mỗi ngày: BẬT</span>'
      : '<button class="ghost" data-grant="' + esc(s.domain) + '">Bật kiểm tra mỗi ngày</button>';
    return '<div class="site"><span class="d">' + esc(s.domain) + '</span><span class="st">' + status + perm
      + '<button class="warn" data-del="' + esc(s.domain) + '">Xóa</button></span></div>';
  }).join('');
  box.querySelectorAll('[data-grant]').forEach(function (b) {
    b.addEventListener('click', async function () {
      var domain = b.getAttribute('data-grant');
      var origins = ['https://' + domain + '/*', 'http://' + domain + '/*'];
      var ok = await chrome.permissions.request({ origins: origins });
      if (ok) {
        var d = await getSites();
        d.sites.forEach(function (s) { if (s.domain === domain) s.granted = true; });
        await chrome.storage.local.set({ sites: d.sites });
      }
      render();
    });
  });
  box.querySelectorAll('[data-del]').forEach(function (b) {
    b.addEventListener('click', async function () {
      var domain = b.getAttribute('data-del');
      var d = await getSites();
      var sites = d.sites.filter(function (s) { return s.domain !== domain; });
      await chrome.storage.local.set({ sites: sites });
      try { await chrome.permissions.remove({ origins: ['https://' + domain + '/*', 'http://' + domain + '/*'] }); } catch (e) {}
      render();
    });
  });
}
document.getElementById('addForm').addEventListener('submit', async function (e) {
  e.preventDefault();
  var input = document.getElementById('domain');
  var domain = input.value.trim().toLowerCase().replace(/^https?:\/\//, '').replace(/\/.*$/, '');
  if (!domain || domain.indexOf('.') < 0) { input.focus(); return; }
  var d = await getSites();
  if (!d.sites.some(function (s) { return s.domain === domain; })) {
    d.sites.push({ domain: domain, granted: false });
    await chrome.storage.local.set({ sites: d.sites });
  }
  input.value = '';
  render();
});
render();
