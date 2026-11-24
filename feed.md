# Zeront - Vulnerability Radar (by SecuScan)

Updated: 2026-11-24T10:59:48Z (UTC). Sources: CISA KEV, FIRST EPSS, SecuScan Vietnam scan aggregates.
Websites tracked in Vietnam: 61169. KEV catalog total: 1792. New KEV this week: 11. Warnings sent: 808.

## Tracked in Vietnam (verified affected counts)

### nginx HTTP/2 - 'nginx2root' privilege escalation (CVE-2026-123007, CVE-2026-123633)
- Affected in Vietnam (verified, aggregate): 830 sites
- nginx 1.9.5 to 1.31.8 with HTTP/2 enabled
- Every case was verified before outreach; warnings have been sent to the affected site owners.
- Fix: Upgrade nginx to 1.30.7 or later, or disable HTTP/2.

### React Server Components - unauthenticated remote code execution (CVE-2026-126187)
- Affected in Vietnam (verified, aggregate): 10 sites
- react-server-dom-webpack / parcel / turbopack on React 19.0.0 before fixes 19.0.9, 19.1.10, 19.2.9, 19.3.1
- Recorded in the 23 Nov 2026 morning scan. Exploitation conditions are narrow (only specific React Server Components data patterns) - each site needs individual checking.
- Fix: Upgrade the react-server-dom-* packages to the fixed release for your React branch.

## New in CISA KEV (last 21 days)

| CVE | Flaw | Impact | CISA due | EPSS |
|---|---|---|---|---|
| [CVE-2026-133968](https://www.cve.org/CVERecord?id=CVE-2026-133968) | Project MONAI MONAI Label - Project MONAI MONAI Label Path Traversal Vulnerability | Remote code execution | 2026-11-26 | 4% |
| [CVE-2026-134624](https://www.cve.org/CVERecord?id=CVE-2026-134624) | N-able MailAssure - N-able MailAssure (SpamExperts) Server-Side Request Forgery (SSRF) Vulnerability | Server-side request forgery | 2026-11-26 | 0% |
| [CVE-2026-129448](https://www.cve.org/CVERecord?id=CVE-2026-129448) | Apache Roller - Apache Roller Deserialization of Untrusted Data Vulnerability | Remote code execution | 2026-11-23 | 5% |
| [CVE-2026-123890](https://www.cve.org/CVERecord?id=CVE-2026-123890) | Broadcom VMware vCenter - VMWare vCenter Authentication Bypass Using an Alternate Path or Channel Vulnerability | Authentication bypass | 2026-11-23 | 4% |
| [CVE-2025-42884](https://www.cve.org/CVERecord?id=CVE-2025-42884) | SAP NetWeaver - SAP NetWeaver Improper Neutralization of Special Elements in Data Query Logic Vulnerability | Query injection | 2026-11-23 | 1% |
| [CVE-2026-76466](https://www.cve.org/CVERecord?id=CVE-2026-76466) | Cisco Expressway Series - Cisco Expressway Series Use of Hard-coded Credentials Vulnerability | Hard-coded credentials | 2026-11-23 | 2% |
| [CVE-2024-10441](https://www.cve.org/CVERecord?id=CVE-2024-10441) | Synology DiskStation Manager (DSM) - Synology DiskStation Manager (DSM) Improper Encoding or Escaping of Output Vulnerability | Remote code execution | 2026-11-21 | 3% |
| [CVE-2026-40217](https://www.cve.org/CVERecord?id=CVE-2026-40217) | BerriAI LiteLLM - BerriAI LiteLLM Unprotected Alternate Channel Vulnerability | Remote code execution | 2026-12-02 | 83% |
| [CVE-2026-90817](https://www.cve.org/CVERecord?id=CVE-2026-90817) | Vanderbilt University Research Electronic Data Capture (REDCap) - Vanderbilt University Research Electronic Data Capture (REDCap) Code Injection Vulnerability | Remote code execution | 2026-11-21 | 34% |
| [CVE-2026-90436](https://www.cve.org/CVERecord?id=CVE-2026-90436) | Apache Axis - Apache Axis Unsafe Reflection Vulnerability | Remote code execution | 2026-11-21 | 6% |
| [CVE-2026-115731](https://www.cve.org/CVERecord?id=CVE-2026-115731) | Perforce Puppet Enterprise - Perforce Puppet Enterprise Deserialization of Untrusted Data Vulnerability | Remote code execution | 2026-12-01 | 13% |
| [CVE-2026-114713](https://www.cve.org/CVERecord?id=CVE-2026-114713) | UnrealIRCd UnrealIRCd - UnrealIRCd Improper Neutralization of Delimiters Vulnerability | Actively exploited | 2026-11-16 | 1% |
| [CVE-2026-123039](https://www.cve.org/CVERecord?id=CVE-2026-123039) | Check Point Multiple Products - Check Point Multiple Products Incorrect Permission Assignment for Critical Resource Vulnerability | Actively exploited | 2026-11-16 | 3% |
| [CVE-2026-124194](https://www.cve.org/CVERecord?id=CVE-2026-124194) | Microsoft Office - Microsoft Office Outlook Missing User Interaction for Potentially Unsafe Action Vulnerability | Actively exploited | 2026-11-24 | 25% |
| [CVE-2026-111793](https://www.cve.org/CVERecord?id=CVE-2026-111793) | Openwave Messaging Limited Webtop Media Transcoder - Openwave Messaging Limited Webtop Media Transcoder Incorrect Resource Transfer Between Spheres Vulnerability | Actively exploited | 2026-11-24 | 1% |
| [CVE-2026-20320](https://www.cve.org/CVERecord?id=CVE-2026-20320) | Cisco BroadWorks - Cisco BroadWorks Improper Restriction of XML External Entity Reference Vulnerability | Actively exploited | 2026-11-24 | 2% |
| [CVE-2026-111560](https://www.cve.org/CVERecord?id=CVE-2026-111560) | Barracuda Networks Multiple Products - Barracuda Networks Multiple Products OS Command Injection Vulnerability | Remote code execution | 2026-11-13 | 64% |
| [CVE-2026-116606](https://www.cve.org/CVERecord?id=CVE-2026-116606) | Barracuda Networks Barracuda Email Security Gateway (ESG) - Barracuda Networks Email Security Gateway (ESG) Authentication Bypass Using an Alternate Path or Channel Vulnerability | Authentication bypass | 2026-11-13 | 75% |
| [CVE-2026-125350](https://www.cve.org/CVERecord?id=CVE-2026-125350) | Google Chromium - Google Chromium Use-After-Free Vulnerability | Remote code execution | 2026-11-24 | 7% |
| [CVE-2026-102895](https://www.cve.org/CVERecord?id=CVE-2026-102895) | GPUStack GPUStack - GPUStack Improper Authentication Vulnerability | Remote code execution | 2026-11-12 | 19% |
| [CVE-2026-123158](https://www.cve.org/CVERecord?id=CVE-2026-123158) | OpenBSD OpenSSH - OpenBSD OpenSSH Unexpected Status Code or Return Value Vulnerability | Authentication bypass | 2026-11-12 | 96% |
| [CVE-2026-116779](https://www.cve.org/CVERecord?id=CVE-2026-116779) | SignalWire FreeSwitch - SignalWire FreeSwitch Code Injection Vulnerability | Actively exploited | 2026-11-12 | 44% |
| [CVE-2026-123218](https://www.cve.org/CVERecord?id=CVE-2026-123218) | IBM Aspera Faspex - IBM Aspera Faspex Incorrect Authorization Vulnerability | Privilege escalation | 2026-11-12 | 1% |
| [CVE-2026-19868](https://www.cve.org/CVERecord?id=CVE-2026-19868) | SonicWall SonicOS SSLVPN - SonicWall SonicOS SSLVPN Use of Single-factor Authentication Vulnerability | Actively exploited | 2026-11-20 | 8% |
| [CVE-2024-27834](https://www.cve.org/CVERecord?id=CVE-2024-27834) | Apple Multiple Products - Apple Multiple Products Improper Authentication Vulnerability | Authentication bypass | 2026-11-18 | 2% |

## Watchlist - high exploitation probability, not in KEV yet

| CVE | Flaw | EPSS (30-day exploitation probability) |
|---|---|---|
| [CVE-2025-53771](https://www.cve.org/CVERecord?id=CVE-2025-53771) | Microsoft Microsoft SharePoint Enterprise Server 2016 - Microsoft SharePoint Server Spoofing Vulnerability | 100% |
| [CVE-2026-43284](https://www.cve.org/CVERecord?id=CVE-2026-43284) | Linux Linux - xfrm: esp: avoid in-place decrypt on shared skb frags | 99% |
| [CVE-2026-43500](https://www.cve.org/CVERecord?id=CVE-2026-43500) | Linux Linux - rxrpc: Also unshare DATA/RESPONSE packets when paged frags are present | 94% |
| [CVE-2025-59528](https://www.cve.org/CVERecord?id=CVE-2025-59528) | FlowiseAI Flowise - Flowise has Remote Code Execution vulnerability | 92% |

Data policy: aggregates only; individual websites are never named. License: MIT. Machine-readable: feed.json (schema zeront-feed/2), feed.xml (RSS), llms.txt.
