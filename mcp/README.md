# Zeront MCP server

Model Context Protocol server that exposes the Zeront vulnerability
radar as tools for any MCP-capable agent (Claude Code, Cursor, Windsurf,
and other MCP clients). Pure Python 3 standard library - no pip installs.

## Tools

| Tool | What it returns |
|---|---|
| `zeront_summary` | Headline numbers: sites tracked in Vietnam, KEV totals, warnings sent |
| `zeront_tracked_vietnam` | Flaws tracked in Vietnam with verified aggregate affected counts + fixes |
| `zeront_kev_recent` | Newest CISA KEV entries; filters `days`, `ransomware_only` |
| `zeront_watchlist` | High-EPSS (over 0.90) flaws not in KEV yet, verified via CVE.org |
| `zeront_search` | Search everything by CVE id, vendor, product or keyword |
| `zeront_check_site` | Match a site fingerprint (`server_header`, `page_signals`) against tracked flaws |

Data comes from the public feed
(`https://secuscan.dannyphan.me/radar/feed.json`, mirrored at
`https://dankezo.github.io/zeront/feed.json`). Override with the
`ZERONT_FEED_URL` or `ZERONT_FEED_FILE` environment variables.

## Setup

Claude Code:

```bash
claude mcp add zeront -- python3 /path/to/zeront/mcp/server.py
```

Generic MCP client configuration (JSON):

```json
{
  "mcpServers": {
    "zeront": {
      "command": "python3",
      "args": ["/path/to/zeront/mcp/server.py"]
    }
  }
}
```

## Honesty rules baked into the data

- Vietnam figures are aggregates from real scans; individual websites
  are never named.
- A `zeront_check_site` match means the fingerprint fits a tracked
  flaw's pattern (version range or page signal). It is not proof the
  site can be exploited - the tool returns the certainty level and the
  conditions so the agent can say exactly that.
