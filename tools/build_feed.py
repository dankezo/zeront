#!/usr/bin/env python3
"""Zeront feed builder.

Pulls the CISA KEV catalog (public), merges SecuScan aggregate scan
figures (data/aggregates.json) and the hand-tracked featured items
(data/featured.json), and writes:

  feed.json  - machine-readable feed for agents and developers
  feed.xml   - RSS 2.0 feed
  data.js    - window.ZERONT_DATA for the radar page

Data policy: aggregates only. No individual website is ever named.
Run: python3 tools/build_feed.py
"""
import json
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
RECENT_DAYS = 21
MAX_RECENT = 25


def fetch_kev():
    req = urllib.request.Request(KEV_URL, headers={"User-Agent": "zeront-feed-builder/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def cve_link(cve):
    return f"https://www.cve.org/CVERecord?id={cve}"


def main():
    now = datetime.now(timezone.utc)
    aggregates = json.loads((ROOT / "data" / "aggregates.json").read_text(encoding="utf-8"))
    featured = json.loads((ROOT / "data" / "featured.json").read_text(encoding="utf-8"))

    try:
        kev = fetch_kev()
        kev_source = "live"
    except Exception as e:  # fall back to the committed seed so the page never breaks
        print(f"KEV fetch failed ({e}); falling back to data/kev_seed.json", file=sys.stderr)
        kev = None
        kev_source = "seed"

    kev_recent = []
    kev_total = None
    kev_released = None
    if kev:
        vulns = kev.get("vulnerabilities", [])
        kev_total = len(vulns)
        kev_released = kev.get("dateReleased")
        cutoff = (now - timedelta(days=RECENT_DAYS)).strftime("%Y-%m-%d")
        recent = [v for v in vulns if v.get("dateAdded", "") >= cutoff]
        recent.sort(key=lambda v: v.get("dateAdded", ""), reverse=True)
        for v in recent[:MAX_RECENT]:
            kev_recent.append({
                "cve": v["cveID"],
                "vendor": v.get("vendorProject", ""),
                "product": v.get("product", ""),
                "name": v.get("vulnerabilityName", ""),
                "added": v.get("dateAdded", ""),
                "due": v.get("dueDate", ""),
                "ransomware": v.get("knownRansomwareCampaignUse", "Unknown"),
                "desc": (v.get("shortDescription", "") or "")[:240],
                "link": cve_link(v["cveID"]),
            })
    else:
        seed = json.loads((ROOT / "data" / "kev_seed.json").read_text(encoding="utf-8"))
        for v in seed:
            kev_recent.append({
                "cve": v["cve"], "vendor": v["vendor"], "product": v["product"],
                "name": v["name"], "added": v["added"], "due": v["due"],
                "ransomware": v["ransomware"], "desc": v["desc"][:240],
                "link": cve_link(v["cve"]),
            })

    week_cutoff = (now - timedelta(days=7)).strftime("%Y-%m-%d")
    kev_new_week = sum(1 for v in kev_recent if v["added"] >= week_cutoff)

    feed = {
        "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generator": "zeront (by SecuScan)",
        "kev_source": kev_source,
        "kev_catalog_released": kev_released,
        "data_policy": "Aggregates only. Individual websites are never named or scored in public data.",
        "stats": {
            "sites_tracked_vn": aggregates["sites_tracked"],
            "warnings_sent": aggregates["warnings_sent"],
            "replies_received": aggregates["replies_received"],
            "kev_total": kev_total,
            "kev_new_this_week": kev_new_week,
            "aggregates_updated": aggregates["updated"],
        },
        "featured": featured,
        "kev_recent": kev_recent,
        "sources": [
            {"name": "CISA Known Exploited Vulnerabilities Catalog", "url": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog"},
            {"name": "NVD - National Vulnerability Database", "url": "https://nvd.nist.gov/"},
            {"name": "SecuScan aggregate scan figures (Vietnam)", "url": "https://secuscan.dannyphan.me/"},
        ],
    }

    (ROOT / "feed.json").write_text(json.dumps(feed, ensure_ascii=False, indent=1), encoding="utf-8")
    (ROOT / "data.js").write_text("window.ZERONT_DATA = " + json.dumps(feed, ensure_ascii=False) + ";\n", encoding="utf-8")

    # RSS 2.0
    items = []
    for f in featured:
        for cve in f["cves"]:
            items.append({
                "title": f"[Tracked in Vietnam] {cve} - {f['title_en']}",
                "link": cve_link(cve),
                "desc": f"{f['affected_en']} Fix: {f['fix_en']} Confirmed affected sites in Vietnam (aggregate): {f['vn_affected']}.",
                "date": f["tracked_since"],
            })
    for v in kev_recent:
        items.append({
            "title": f"{v['cve']} - {v['vendor']} {v['product']}: {v['name']}",
            "link": v["link"],
            "desc": v["desc"],
            "date": v["added"],
        })
    rss_items = []
    for it in items:
        try:
            dt = datetime.strptime(it["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            pub = format_datetime(dt)
        except Exception:
            pub = format_datetime(now)
        rss_items.append(
            "  <item>\n"
            f"   <title>{escape(it['title'])}</title>\n"
            f"   <link>{escape(it['link'])}</link>\n"
            f"   <guid>{escape(it['link'])}</guid>\n"
            f"   <pubDate>{pub}</pubDate>\n"
            f"   <description>{escape(it['desc'])}</description>\n"
            "  </item>"
        )
    rss = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0"><channel>\n'
        " <title>Zeront - Vulnerability Radar by SecuScan</title>\n"
        " <link>https://secuscan.dannyphan.me/radar/</link>\n"
        " <description>New exploited vulnerabilities (CISA KEV), tracked flaws in Vietnam with aggregate impact figures, and fixes. Aggregates only - individual websites are never named.</description>\n"
        " <language>vi</language>\n"
        f" <lastBuildDate>{format_datetime(now)}</lastBuildDate>\n"
        + "\n".join(rss_items)
        + "\n</channel></rss>\n"
    )
    (ROOT / "feed.xml").write_text(rss, encoding="utf-8")
    print(f"OK: featured={len(featured)} kev_recent={len(kev_recent)} kev_total={kev_total} source={kev_source}")


if __name__ == "__main__":
    main()
