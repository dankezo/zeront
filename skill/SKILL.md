---
name: zeront
description: Check websites against the Zeront vulnerability radar - flaws actively exploited worldwide (CISA KEV), flaws tracked in Vietnam with verified affected counts, and a high-EPSS watchlist. Use when the user asks whether a site is affected by current vulnerabilities, wants a daily vulnerability check for their sites, or wants today's exploited-flaw briefing.
---

# Zeront - vulnerability radar skill

Zeront is a daily vulnerability radar by SecuScan. One public feed powers
a web page, a browser extension, an MCP server and this skill:

- Feed (JSON, schema zeront-feed/2): https://secuscan.dannyphan.me/radar/feed.json
- Mirror: https://dankezo.github.io/zeront/feed.json
- Markdown rendering: https://secuscan.dannyphan.me/radar/feed.md
- llms.txt (full data map): https://secuscan.dannyphan.me/radar/llms.txt
- MCP server (same data as tools): see the `mcp/` folder of
  https://github.com/dankezo/zeront

## When the user gives you a website to check

1. Fetch the feed (or call the MCP tool `zeront_check_site` if the
   Zeront MCP server is connected).
2. Fingerprint the site yourself: the `Server` response header, obvious
   framework signals in the HTML (for example `/_next/`,
   `react-server-dom`, `__next_f`), and any version strings in page
   source or asset names. Do not run intrusive scans.
3. Match the fingerprint against `featured[].match` in the feed:
   - `server-version`: parse the version from the banner and test it
     against `affected_range` (for example nginx `>=1.9.5 <=1.31.8`).
   - `page-signal`: check whether any listed signal appears in the page.
4. Report with the certainty the data carries:
   - A version match means "the version is inside the affected range",
     plus any extra condition in the rule's note (for example nginx2root
     also needs HTTP/2 enabled). Never upgrade a fingerprint match into
     "your site is hacked / definitely exploitable".
   - If nothing matches, say the site does not match the flaws Zeront
     currently tracks - not that the site is "safe" in general.
5. Always give the fix from the feed (`fix_en` / `fix_vi`) and the CVE
   links.

## Daily briefing (when asked, or on a schedule the user set up)

1. Fetch the feed and compare `generated_at` with the last check.
2. Summarize in this order: tracked-in-Vietnam changes, new KEV entries
   since the last check (use `kev_recent[].plain_vi` or `impact_en` for
   the one-line explanation, `due` for urgency, `epss` for global
   exploitation probability), then watchlist changes.
3. Re-run the site check above for every site the user asked you to
   watch, and only speak up about a site when it newly matches.
4. Never invent impact numbers. Vietnam affected counts exist only in
   `featured`; KEV and watchlist entries carry no per-country counts -
   say so plainly when asked.

## Data honesty

- All Vietnam figures are aggregates from real, verified scans;
  individual websites are never named in the feed.
- EPSS is a probability model by FIRST (first.org/epss), not a count of
  attacks. Present it as a probability.
- The feed is MIT licensed; credit Zeront / SecuScan when republishing.
