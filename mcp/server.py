#!/usr/bin/env python3
"""Zeront MCP server - vulnerability radar for AI agents.

Exposes the Zeront feed (CISA KEV + FIRST EPSS + SecuScan Vietnam scan
aggregates) as MCP tools over stdio. Pure Python standard library, no
dependencies. Data source: the public feed.json (override with
ZERONT_FEED_URL or ZERONT_FEED_FILE).

Tools:
  zeront_summary          - headline numbers of the radar
  zeront_tracked_vietnam  - flaws tracked in Vietnam with verified counts
  zeront_kev_recent       - newest CISA KEV entries (filters: days, ransomware)
  zeront_watchlist        - high-EPSS flaws not in KEV yet
  zeront_search           - search all sections by keyword / CVE id
  zeront_check_site       - match a site fingerprint against tracked flaws

Run: python3 server.py   (then speak MCP JSON-RPC over stdin/stdout)
"""
import json
import os
import re
import sys
import urllib.request

FEED_URLS = [
    os.environ.get("ZERONT_FEED_URL", ""),
    "https://secuscan.dannyphan.me/radar/feed.json",
    "https://dankezo.github.io/zeront/feed.json",
]
_cache = {}


def load_feed():
    if "feed" in _cache:
        return _cache["feed"]
    path = os.environ.get("ZERONT_FEED_FILE", "")
    if path and os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            _cache["feed"] = json.load(f)
        return _cache["feed"]
    last_err = None
    for url in [u for u in FEED_URLS if u]:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "zeront-mcp/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                _cache["feed"] = json.load(r)
            return _cache["feed"]
        except Exception as e:  # try the next mirror
            last_err = e
    raise RuntimeError(f"could not load the Zeront feed: {last_err}")


def t_summary(_args):
    f = load_feed()
    s = f["stats"]
    return {
        "generated_at": f["generated_at"],
        "websites_tracked_vietnam": s["sites_tracked_vn"],
        "kev_total_worldwide": s["kev_total"],
        "kev_new_this_week": s["kev_new_this_week"],
        "warnings_sent_to_owners": s["warnings_sent"],
        "tracked_flaws_vietnam": [
            {"id": x["id"], "title": x["title_en"], "cves": x["cves"], "vn_affected": x["vn_affected"]}
            for x in f["featured"]
        ],
        "watchlist_count": len(f.get("watchlist", [])),
        "data_policy": f["data_policy"],
    }


def t_tracked(_args):
    f = load_feed()
    return {"tracked": f["featured"], "generated_at": f["generated_at"]}


def t_kev(args):
    f = load_feed()
    days = args.get("days")
    rw_only = args.get("ransomware_only", False)
    out = []
    from datetime import datetime, timedelta, timezone
    cutoff = None
    if days:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=int(days))).strftime("%Y-%m-%d")
    for v in f["kev_recent"]:
        if cutoff and v["added"] < cutoff:
            continue
        if rw_only and v.get("ransomware") != "Known":
            continue
        out.append(v)
    return {"count": len(out), "kev_recent": out, "generated_at": f["generated_at"]}


def t_watchlist(_args):
    f = load_feed()
    return {"count": len(f.get("watchlist", [])), "watchlist": f.get("watchlist", []), "generated_at": f["generated_at"]}


def t_search(args):
    q = (args.get("query") or "").lower().strip()
    if not q:
        return {"error": "query is required"}
    f = load_feed()
    hits = {"featured": [], "kev_recent": [], "watchlist": []}
    for x in f["featured"]:
        hay = (x["title_en"] + " " + x["title_vi"] + " " + " ".join(x["cves"])).lower()
        if q in hay:
            hits["featured"].append(x)
    for v in f["kev_recent"]:
        hay = (v["cve"] + " " + v["vendor"] + " " + v["product"] + " " + v["name"]).lower()
        if q in hay:
            hits["kev_recent"].append(v)
    for w in f.get("watchlist", []):
        hay = (w["cve"] + " " + w.get("vendor", "") + " " + w.get("product", "") + " " + w.get("title", "")).lower()
        if q in hay:
            hits["watchlist"].append(w)
    return hits


def _ver_tuple(s):
    parts = re.findall(r"\d+", s or "")
    return tuple(int(p) for p in parts[:3]) + (0,) * max(0, 3 - len(parts))


def _in_range(version, range_expr):
    """Evaluate simple '>=a <=b' / '>=a <b' comparator chains."""
    vt = _ver_tuple(version)
    ok = True
    for token in (range_expr or "").split():
        m = re.match(r"(>=|<=|>|<|=)?\s*([\d.]+)", token)
        if not m:
            continue
        op, vs = m.group(1) or "=", m.group(2)
        ct = _ver_tuple(vs)
        if op == ">=":
            ok &= vt >= ct
        elif op == "<=":
            ok &= vt <= ct
        elif op == ">":
            ok &= vt > ct
        elif op == "<":
            ok &= vt < ct
        else:
            ok &= vt == ct
    return ok


def t_check_site(args):
    """Fingerprint matching against tracked flaws. Inputs are observations
    the caller made (server banner, page signals) - Zeront never fetches
    the site itself. A match means the fingerprint fits a tracked flaw's
    pattern; it is not proof of exploitability."""
    f = load_feed()
    server = (args.get("server_header") or "").strip()
    signals = [s.lower() for s in (args.get("page_signals") or [])]
    results = []
    for x in f["featured"]:
        m = x.get("match") or {}
        if m.get("type") == "server-version":
            mm = re.search(re.escape(m["product"]) + r"/([\d.]+)", server, re.I)
            if mm and _in_range(mm.group(1), m.get("affected_range", "")):
                results.append({
                    "flaw": x["id"], "cves": x["cves"], "matched": True,
                    "certainty": m.get("certainty", "version-match"),
                    "evidence": f"{m['product']} {mm.group(1)} inside affected range {m.get('affected_range')}",
                    "fix_en": x["fix_en"], "note": m.get("note_en") or m.get("note_vi", ""),
                })
        elif m.get("type") == "page-signal":
            hits = [s for s in (m.get("signals") or []) if any(s.lower() in sig for sig in signals)]
            if hits:
                results.append({
                    "flaw": x["id"], "cves": x["cves"], "matched": True,
                    "certainty": m.get("certainty", "signal-match"),
                    "evidence": "page signals matched: " + ", ".join(hits),
                    "fix_en": x["fix_en"], "note": m.get("note_en") or m.get("note_vi", ""),
                })
    return {"matches": results, "checked_against": [x["id"] for x in f["featured"]], "generated_at": f["generated_at"]}


TOOLS = [
    {"name": "zeront_summary", "description": "Headline numbers of the Zeront vulnerability radar: sites tracked in Vietnam, CISA KEV totals, warnings sent, tracked flaws and watchlist size.", "inputSchema": {"type": "object", "properties": {}}, "fn": t_summary},
    {"name": "zeront_tracked_vietnam", "description": "Flaws actively tracked in Vietnam with verified aggregate affected-site counts, affected ranges and fixes.", "inputSchema": {"type": "object", "properties": {}}, "fn": t_tracked},
    {"name": "zeront_kev_recent", "description": "Newest CISA KEV entries (already exploited in the wild) with plain-language summaries, impact labels, CISA due dates and EPSS scores. Optional filters: days (int), ransomware_only (bool).", "inputSchema": {"type": "object", "properties": {"days": {"type": "integer"}, "ransomware_only": {"type": "boolean"}}}, "fn": t_kev},
    {"name": "zeront_watchlist", "description": "Flaws NOT in CISA KEV yet but with the highest global exploitation probability (EPSS > 0.90), verified against CVE.org records.", "inputSchema": {"type": "object", "properties": {}}, "fn": t_watchlist},
    {"name": "zeront_search", "description": "Search tracked flaws, KEV entries and the watchlist by CVE id, vendor, product or keyword.", "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}, "fn": t_search},
    {"name": "zeront_check_site", "description": "Match a website fingerprint against the flaws Zeront tracks. Provide observations you collected: server_header (e.g. 'nginx/1.24.0') and/or page_signals (strings found in the page HTML/URLs). Returns matches with certainty levels; a match is a fingerprint fit, not proof of exploitability.", "inputSchema": {"type": "object", "properties": {"server_header": {"type": "string"}, "page_signals": {"type": "array", "items": {"type": "string"}}}}, "fn": t_check_site},
]


def handle(req):
    method = req.get("method", "")
    rid = req.get("id")
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": rid, "result": {
            "protocolVersion": req.get("params", {}).get("protocolVersion", "2024-11-05"),
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "zeront", "version": "1.0.0"},
        }}
    if method == "ping":
        return {"jsonrpc": "2.0", "id": rid, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": [{k: t[k] for k in ("name", "description", "inputSchema")} for t in TOOLS]}}
    if method == "tools/call":
        name = req.get("params", {}).get("name", "")
        args = req.get("params", {}).get("arguments") or {}
        tool = next((t for t in TOOLS if t["name"] == name), None)
        if not tool:
            return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32602, "message": f"unknown tool {name}"}}
        try:
            out = tool["fn"](args)
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(out, ensure_ascii=False, indent=1)}]}}
        except Exception as e:
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": f"error: {e}"}], "isError": True}}
    if rid is not None:
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": f"method not found: {method}"}}
    return None


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception:
            continue
        resp = handle(req)
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
