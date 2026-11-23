# Zeront — Competitive Landscape & Marketability Assessment

Date: 2026-11-23. Researched from live sources (URLs cited inline). Blunt by request.

## 1. Who else publishes a KEV / exploited-vulnerability dashboard or feed?

KEV republishing is a **crowded, commodity space**. The data itself is free (CISA KEV is CC0), so mirrors are everywhere:

- **CISA KEV (the source)** — free JSON/CSV feed, the catalog everyone copies (1,790 entries as of 2026-11-23). Audience: US federal agencies (legally bound to it) and everyone downstream. https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- **VulnCheck KEV** — the strongest free competitor. Its own KEV catalog claims ~80% more entries than CISA KEV, listed on average 27 days earlier, with citations for why each CVE is listed. The full Exploit & Vulnerability Intelligence product is commercial (quote-only; free Community tier exists). 23,000+ community members. Also ships an API, an MCP server, a published Claude Code agent skill, and a browser extension. https://www.g2.com/products/vulncheck-exploit-and-vulnerability-intelligence/pricing · https://seemplicity.ai/blog/seemplicity-leverages-vulncheckkev/ · https://providers.apievangelist.com/providers/vulncheck/
- **GreyNoise** — internet-wide sensor network classifying scanner IPs, with CVE context per IP. Free Community tier (50 searches/week); paid tiers are contact-sales (third-party listings put entry paid plans near $9,999/yr). Has an official MCP server and llms.txt-formatted docs. Audience: SOC/enterprise analysts, not website owners. https://apis.io/providers/greynoise/ · https://www.anchorterminal.com/tools/greynoise
- **watchTowr** — enterprise attack-surface management + automated red teaming; re-tests a customer's estate within an hour of a new threat. Quote-only pricing (a Singapore SME reseller cites S$750–3,000/month). Audience: banks, government, large enterprises. Not a public feed at all. https://cyberreviewed.com/reviews/watchtowr/
- **Patchstack** — the closest SMB/website-owner competitor. WordPress/Drupal vulnerability database plus a plugin that detects vulnerable components on **your own sites** and alerts you. Free Personal plan covers 3 sites (detection + alerts); protection is $5/site/month; Developer plan $69/month for 25 sites. But: CMS-plugin-based, WordPress/Drupal only, English, no local scan data, no agent feed. https://docs.patchstack.com/faq-troubleshooting/pricing-plans/does-patchstack-have-a-free-version/
- **OpenCVE** — open-source + SaaS vulnerability intelligence platform. Users subscribe to vendors/products and get alerts (email/webhook/Slack) when matching CVEs appear or change; enriches with KEV/EPSS; AI enrichment on the Cloud tier. Free plan + paid cloud tiers. Audience: technical security teams who can name their stack in CPE terms. https://www.opencve.io/
- **Hobbyist/SEO KEV mirrors** — kev.vallis.info (daily KEV summary in 14 languages), immunitysec.com (KEV dashboard syncing every 6 hours, with EPSS), securitybriefing.net (weekly KEV briefing with CVSS+EPSS tables), hackthehammer.com (KEV statistics). Free, English-first, no original data, no per-user matching. https://kev.vallis.info/en/index.html · https://www.immunitysec.com/vulnerabilities/kev/ · https://securitybriefing.net/cyber-alerts/cisa-kev-weekly-briefing-2026-11-18/

## 2. Agent-oriented vulnerability feeds — this space is NOT empty

Anyone claiming "first vulnerability feed for AI agents" would be wrong:

- **Helix Threat Watch (helix.ml)** — the closest direct analogue to Zeront's agent play. Publishes per-category **llms.txt**, JSON Feed, RSS and a changes.json update stream, with an explicit "Use with your AI" section: poll hourly with ETag, match `stacks` / `affectedVersions` / `cveIds` against systems you manage, alert only on a match; each incident has an `agentBrief` markdown field. English-only, curated incidents (vulnerabilities + breaches + supply chain), no own-scan data, no extension, no localization. https://www.helixml.tech/threat-watch/c/patch/llms.txt
- **MCP servers for CVE/KEV/NVD are multiplying**: NIST NVD MCP Server (CVE search/retrieval for agents), `vulnerability-exposure-mcp` (checks domains/IPs/software versions against NVD, KEV, EPSS, Shodan, GreyNoise and more), `exploitwatch-mcp` (CVE triage: `lookup_cve`, `check_kev`, `get_epss`), and a Rust "CVE MCP Server" with 34 tools and a self-updating daily intel store. All free/open-source, all aimed at technical users who run an MCP client. https://glama.ai/mcp/servers/Cyreslab-AI/nist-nvd-mcp-server · https://pypi.org/project/vulnerability-exposure-mcp/1.0.0/ · https://pypi.org/project/exploitwatch-mcp · https://glama.ai/mcp/servers/Liohtml/cve-mcp-server
- **VulnCheck and GreyNoise both ship official MCP servers** (VulnCheck also a Claude Code skill), so even the big vendors are already in the agent channel. https://providers.apievangelist.com/providers/vulncheck/ · https://apis.io/providers/greynoise/
- One caution from 2026 research: llms.txt files were abused as an agent instruction channel (unclaimed package names in vendor llms.txt files executed inside corporate networks). Zeront's llms.txt is data-only (no install/run commands), which is the safe pattern — worth stating explicitly in marketing. https://sprk3.com/blog/llms-txt-directive-file-abandoned-package-supply-chain

**What Zeront does differently here:** its copy-prompt targets people who will never configure MCP — an SMB owner pastes one prompt into the ChatGPT/Claude they already have. That distribution trick (consumer chatbot as the runtime, a static feed as the data) is genuinely uncommon. The llms.txt file itself is not novel.

## 3. Browser extensions that check YOUR websites

Every extension found works on **the page you are visiting**, not on a registered list of your own sites:

- **CyberPross** — detects technologies and checks known CVEs on the site you are currently visiting. https://chromewebstore.google.com/detail/cyberpross-security-scann/edbncdajlofhbpejdnpjjgjlmbiemeie?hl=en
- **CVEFeed Insights** — highlights CVE IDs in any page you read and shows CVSS/KEV/ransomware tooltips. https://chromewebstore.google.com/detail/cvefeed-insights/khagakknhonbfmjjobgfnbjolcfljkkc
- **VulnCheck Insights** — same pattern (CVE/CPE/PURL enrichment on pages you browse; CPE/PURL needs a premium license). https://chromewebstore.google.com/detail/vulncheck-insights/ialmnppnmajmaeibknkgfihffkobnogp
- Wappalyzer/BuiltWith/Shodan-style extensions — technology/version detection on visited pages only.

No Chrome extension was found that lets a user register their own websites and proactively alerts them when live vulnerability intel matches their stack. The "your sites" alerting job exists only in plugin/SaaS form (Patchstack for WordPress/Drupal, OpenCVE by product subscription). **Zeront's extension concept occupies a real gap — but today it is v0.1.0, sideload-only, with match rules for only the featured tracked flaws, so the gap is claimed, not yet held.**

## 4. Localized / country-specific intel for SMBs

- **kev.vallis.info has a Vietnamese version** — so "KEV in Vietnamese" alone is not a moat. But it is raw machine translation of CISA text and visibly garbled (e.g. an "actor" rendered as a movie actor, stray untranslated fragments), with no local data, no SMB framing, no feed, no extension. https://kev.vallis.info/vi/index.html
- **Inside Vietnam**, vulnerability intel for SMBs comes from state agencies (cyber-security authority warnings) and vendor PR. Bkav, for example, issues press warnings with Vietnam-specific exposure counts (e.g. "nearly 8,000 n8n systems in Vietnam at risk" for CVE-2025-68613) — proof that local counts resonate with Vietnamese media — but these are ad-hoc press releases, not a product, feed, or per-flaw database an SMB or an agent can consume. https://doanhnhan.baophapluat.vn/hang-nghin-he-thong-bao-mat-tai-viet-nam-co-nguy-co-rui-ro-nghiem-trong-90138.html
- No productized, public, machine-readable, Vietnamese-first vulnerability feed with **per-flaw verified local affected counts** was found. That specific asset — real scan aggregates over 61,169 Vietnamese websites, published openly per flaw — appears to be Zeront's alone.

## Comparison table

| Product | What it does | Audience | Price | Zeront has, it lacks | It has, Zeront lacks |
|---|---|---|---|---|---|
| CISA KEV | Authoritative exploited-vuln catalog + feed | US gov + everyone | Free (CC0) | Plain-language VI summaries, local VN affected counts, per-user matching | Authority, completeness, legal mandate |
| VulnCheck | KEV-plus catalog (broader, ~27 days earlier), exploit intel, API, MCP server, extension, Claude skill | Security teams, enterprises | Free Community; commercial by quote | VN scan counts, VI plain language for SMBs, free own-site extension | Far broader/earlier coverage, evidence citations, brand, 23k community, revenue |
| GreyNoise | Internet scanner/IP intelligence with CVE context | SOC analysts | Free tier; paid ~$10k/yr+ | Website-owner focus, per-flaw local counts, VI | Sensor network, MCP server, enterprise integrations |
| watchTowr | ASM + automated red teaming of your estate | Banks, gov, enterprise | Quote-only (reseller: S$750–3,000/mo) | Free, public, SMB-readable | Exploit validation on the customer's own assets, funding, sales channel |
| Patchstack | Detects vulnerable WP/Drupal components on your sites + alerts + virtual patching | WP site owners, agencies | Free (3 sites); $5/site/mo protection | Stack-agnostic (any website), agent feed + copy-prompt, VN data | Working product with users, Web Store/plugin directory presence, actual protection (vPatching) |
| OpenCVE | Subscribe to products, get CVE alerts, KEV/EPSS enrichment | Security teams | Free plan; paid cloud tiers | No-account public feed, plain-language VI, local counts | Mature platform, accounts/projects, alerting infra, AI enrichment |
| Helix Threat Watch | Curated incident feed with llms.txt/JSON/RSS built for AI polling | Technical users, agent builders | Free | VN scan data, VI language, extension, SMB copy-prompt | Broader incident coverage (breaches, supply chain), change-stream (ETag/changes.json) polish |
| CVE MCP servers (NVD MCP, exploitwatch-mcp, vulnerability-exposure-mcp, CVE MCP) | Agent tools to look up/triage CVEs against NVD/KEV/EPSS | Developers, agent users | Free / open source | Zero-setup for non-technical users (copy-prompt), curated daily shortlist with local counts | Real tool-calling (live lookup of any CVE), version-specific checks against a user's actual stack |
| KEV mirrors (kev.vallis.info, immunitysec, briefings) | Republished KEV dashboards/newsletters, some multilingual | Hobbyists, researchers | Free | Original data (VN counts), human-written VI, extension, agent feed | Nothing material — Zeront is ahead of this tier |
| Bkav / VN agency warnings | Ad-hoc press warnings, sometimes with VN exposure counts | Vietnamese public/SMBs via media | Free (PR) | A permanent, queryable, machine-readable per-flaw feed | Media reach, institutional trust, brand recognition in VN |
| **Zeront** | Daily radar page + JSON/RSS/llms.txt feed + own-site Chrome extension + agent copy-prompt, built on KEV + real VN scan aggregates | Vietnamese SMB website owners; AI-agent users | Free (MIT) | — | — |

## Verdict — blunt

**Genuinely novel (the combination, not the ingredients):**
1. **Verified per-flaw affected counts from real scans of one country's web** (61,169 Vietnamese sites; e.g. 830 confirmed for nginx2root), published openly and for free. Nobody above publishes local exposure counts per flaw; Bkav does it only as occasional PR. This is the moat — it is data nobody can copy without running the scans.
2. **Human-written plain Vietnamese for non-technical SMB owners.** The one Vietnamese competitor is garbled machine translation. Zeront's summaries are written for a shop owner, not an analyst.
3. **One feed, three consumer surfaces, all free:** human page, agent surfaces (feed + llms.txt + a copy-prompt that turns the user's existing ChatGPT/Claude into a daily watcher), and a browser extension that matches the user's own sites. Each surface exists somewhere; nobody bundles all three around local SMB data.

**Commodity (do not market these as innovations):** KEV mirroring, EPSS display, RSS/JSON feeds, llms.txt itself, "AI-readable" as a label, CVE highlighting. VulnCheck/GreyNoise/Helix got to the agent channel first or better.

**What a marketer should lead with:** the counted, local, current number — "Right now, 830 websites in Vietnam are confirmed running this flaw" — with the agent hook as the distribution play: "Paste one prompt; your own AI assistant checks your website against the radar every day, free." Lead with the count (proof), close with the agent (novelty).

**Missing before it is credible to market (gaps, in order of damage):**
1. **Zero users and zero social proof.** No installs, testimonials, or third-party citations yet. Every claim is currently self-asserted.
2. **Extension is not on the Chrome Web Store** (developer fee unpaid; sideload ZIP install is a non-starter for the SMB audience it targets) — and its match coverage is only the handful of featured flaws, not the KEV catalog. As shipped, the extension's real-world hit rate will be near zero for most users.
3. **Trust/verifiability of the headline data.** The VN counts are self-reported with no public methodology page, sample evidence, or independent confirmation. VulnCheck shows citations per entry; Zeront shows a number. Skeptical readers (and journalists) will ask how 830 was counted.
4. **Freshness is a one-person pipeline.** Daily updates depend on a single operator's scan process; no public status/history page, no SLA, bus factor = 1. A radar that silently goes stale destroys its own premise.
5. **No alert channel of its own.** No email/Zalo/Telegram push; alerting depends on the user installing an extension or babysitting a chatbot prompt. Patchstack emails you; Zeront currently cannot.
6. **No MCP server.** Static-file polling works, but the agent ecosystem's center of gravity is MCP, and competitors (including free open-source ones) already live there.
7. **Positioning friction:** the radar lives on a subdomain of SecuScan, a paid service — "free public good" messaging will be read as a funnel, because it is one. That's survivable if stated openly, fatal if it looks disguised.
8. **English reach is thin** for the agent story: the agent/extension narrative is the part with global potential, and it is currently told Vietnamese-first.

Bottom line: Zeront is not "another KEV dashboard" — the Vietnam scan data plus the three-surface free distribution is a real, defensible niche. But today it is a promising prototype with a unique dataset, not yet a marketable product: Web Store listing, a methodology/trust page, an alert channel, and the first real users matter more than any new feature.
