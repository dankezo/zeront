/* Zeront background service worker.
   Daily job: refresh the radar feed; notify on newly tracked flaws;
   re-check the user's permitted websites against tracked items. */
importScripts('match.js');

var ALARM = 'zeront-daily';

chrome.runtime.onInstalled.addListener(function () {
  chrome.alarms.create(ALARM, { periodInMinutes: 60 * 24, delayInMinutes: 5 });
  zRefreshFeed(true);
});
chrome.alarms.onAlarm.addListener(function (a) {
  if (a.name === ALARM) zRefreshFeed(false);
});

async function zFetchFeed() {
  for (var i = 0; i < ZERONT_FEEDS.length; i++) {
    try {
      var r = await fetch(ZERONT_FEEDS[i], { cache: 'no-store' });
      if (r.ok) return await r.json();
    } catch (e) { /* try next mirror */ }
  }
  return null;
}

async function zRefreshFeed(firstRun) {
  var feed = await zFetchFeed();
  if (!feed) return;
  var store = await chrome.storage.local.get(['feed', 'seenFeatured']);
  var oldIds = store.seenFeatured || [];
  var newItems = (feed.featured || []).filter(function (f) { return oldIds.indexOf(f.id) < 0; });
  await chrome.storage.local.set({
    feed: feed,
    feedAt: Date.now(),
    seenFeatured: (feed.featured || []).map(function (f) { return f.id; })
  });
  if (!firstRun && newItems.length) {
    chrome.notifications.create('zeront-new-' + Date.now(), {
      type: 'basic',
      iconUrl: 'icons/icon128.png',
      title: 'Zeront: có lỗi mới đang theo dõi',
      message: newItems.map(function (f) { return f.cves.join(', ') + ' - ' + f.title_vi; }).join('\n')
    });
  }
  await zCheckSites(feed);
}

async function zCheckSites(feed) {
  var store = await chrome.storage.local.get(['sites']);
  var sites = (store.sites || []).filter(function (s) { return s.granted; });
  var results = {};
  var totalMatches = 0;
  for (var i = 0; i < sites.length; i++) {
    var s = sites[i];
    try {
      var r = await fetch('https://' + s.domain + '/', { cache: 'no-store' });
      var html = await r.text();
      var fp = zFingerprintFromHtml(html, r.headers.get('server'));
      var ev = zEvalFingerprint(fp, feed.featured || []);
      var hits = ev.filter(function (e) { return e.verdict === 'match' || e.verdict === 'signal'; });
      results[s.domain] = { at: Date.now(), hits: hits.map(function (h) { return { id: h.item.id, verdict: h.verdict, evidence: h.evidence }; }) };
      totalMatches += hits.length;
    } catch (e) {
      results[s.domain] = { at: Date.now(), error: true, hits: [] };
    }
  }
  await chrome.storage.local.set({ siteResults: results });
  if (totalMatches > 0) {
    chrome.action.setBadgeText({ text: String(totalMatches) });
    chrome.action.setBadgeBackgroundColor({ color: '#e63946' });
  } else {
    chrome.action.setBadgeText({ text: '' });
  }
}
