# Zeront - Vulnerability Radar (by SecuScan)

Updated: 2026-11-27T09:43:35Z (UTC). Sources: CISA KEV, FIRST EPSS, SecuScan Vietnam scan aggregates.
Websites tracked in Vietnam: 61169. KEV catalog total: 1805. New KEV this week: 19. Warnings sent: 808.

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
| [CVE-2026-103406](https://www.cve.org/CVERecord?id=CVE-2026-103406) | Hewlett Packard Enterprise (HPE) Juniper Session Smart Conductor and Session Smart Router - Hewlett Packard Enterprise (HPE) Juniper Session Smart Conductor and Session Smart Router OS Command Injection Vulnerability | Remote code execution | 2026-11-28 | 2% |
| [CVE-2026-133469](https://www.cve.org/CVERecord?id=CVE-2026-133469) | Vates Xen Orchestra - Vates Xen Orchestra Improper Validation of Specified Type of Input Vulnerability | Actively exploited | 2026-11-28 | 32% |
| [CVE-2025-41450](https://www.cve.org/CVERecord?id=CVE-2025-41450) | Danfoss AK-SM 800A Series - Danfoss AK-SM 800A Series Improper Authentication Vulnerability | Authentication bypass | 2026-12-09 | 4% |
| [CVE-2023-25914](https://www.cve.org/CVERecord?id=CVE-2023-25914) | Danfoss AK-SM 800A Series - Danfoss AK-SM 800A Series Path Traversal Vulnerability | Path traversal | 2026-11-28 | 2% |
| [CVE-2023-25915](https://www.cve.org/CVERecord?id=CVE-2023-25915) | Danfoss AK-SM 800A Series - Danfoss AK-SM 800A Series Improper Input Validation Vulnerability | Actively exploited | 2026-11-28 | 2% |
| [CVE-2026-133324](https://www.cve.org/CVERecord?id=CVE-2026-133324) | Mitel MiCollab - Mitel MiCollab Not Failing Securely Vulnerability | Actively exploited | 2026-11-28 | 1% |
| [CVE-2026-133275](https://www.cve.org/CVERecord?id=CVE-2026-133275) | Mitel MiCollab - Mitel MiCollab Unrestricted Upload of File with Dangerous Type Vulnerability | Actively exploited | 2026-11-28 | 1% |
| [CVE-2026-133311](https://www.cve.org/CVERecord?id=CVE-2026-133311) | Mitel MiCollab - Mitel MiCollab Weak Authentication Vulnerability | Information disclosure | 2026-12-09 | 1% |
| [CVE-2026-133303](https://www.cve.org/CVERecord?id=CVE-2026-133303) | Mitel MiCollab - Mitel MiCollab XML Injection Vulnerability | Actively exploited | 2026-11-28 | 1% |
| [CVE-2026-133323](https://www.cve.org/CVERecord?id=CVE-2026-133323) | Mitel MiCollab - Mitel MiCollab OS Command Injection Vulnerability | Remote code execution | 2026-11-28 | 6% |
| [CVE-2026-132224](https://www.cve.org/CVERecord?id=CVE-2026-132224) | Optimizely Web Experimentation - Optimizely Web Experimentation External Control of Critical State Data Vulnerability | Actively exploited | 2026-11-27 | 1% |
| [CVE-2026-131914](https://www.cve.org/CVERecord?id=CVE-2026-131914) | Idunno AntiCsrf - Idunno AntiCsrf Deserialization of Untrusted Data Vulnerability | Remote code execution | 2026-11-27 | 4% |
| [CVE-2026-132165](https://www.cve.org/CVERecord?id=CVE-2026-132165) | Drupal Core - Drupal Core Remote Code Execution Vulnerability | Remote code execution | 2026-11-27 | 11% |
| [CVE-2026-133968](https://www.cve.org/CVERecord?id=CVE-2026-133968) | Project MONAI MONAI Label - Project MONAI MONAI Label Path Traversal Vulnerability | Remote code execution | 2026-11-26 | 27% |
| [CVE-2026-134624](https://www.cve.org/CVERecord?id=CVE-2026-134624) | N-able MailAssure - N-able MailAssure (SpamExperts) Server-Side Request Forgery (SSRF) Vulnerability | Server-side request forgery | 2026-11-26 | 2% |
| [CVE-2026-129448](https://www.cve.org/CVERecord?id=CVE-2026-129448) | Apache Roller - Apache Roller Deserialization of Untrusted Data Vulnerability | Remote code execution | 2026-11-23 | 24% |
| [CVE-2026-123890](https://www.cve.org/CVERecord?id=CVE-2026-123890) | Broadcom VMware vCenter - VMWare vCenter Authentication Bypass Using an Alternate Path or Channel Vulnerability | Authentication bypass | 2026-11-23 | 5% |
| [CVE-2025-42884](https://www.cve.org/CVERecord?id=CVE-2025-42884) | SAP NetWeaver - SAP NetWeaver Improper Neutralization of Special Elements in Data Query Logic Vulnerability | Query injection | 2026-11-23 | 1% |
| [CVE-2026-76466](https://www.cve.org/CVERecord?id=CVE-2026-76466) | Cisco Expressway Series - Cisco Expressway Series Use of Hard-coded Credentials Vulnerability | Hard-coded credentials | 2026-11-23 | 1% |
| [CVE-2024-10441](https://www.cve.org/CVERecord?id=CVE-2024-10441) | Synology DiskStation Manager (DSM) - Synology DiskStation Manager (DSM) Improper Encoding or Escaping of Output Vulnerability | Remote code execution | 2026-11-21 | 3% |
| [CVE-2026-40217](https://www.cve.org/CVERecord?id=CVE-2026-40217) | BerriAI LiteLLM - BerriAI LiteLLM Unprotected Alternate Channel Vulnerability | Remote code execution | 2026-12-02 | 20% |
| [CVE-2026-90817](https://www.cve.org/CVERecord?id=CVE-2026-90817) | Vanderbilt University Research Electronic Data Capture (REDCap) - Vanderbilt University Research Electronic Data Capture (REDCap) Code Injection Vulnerability | Remote code execution | 2026-11-21 | 19% |
| [CVE-2026-90436](https://www.cve.org/CVERecord?id=CVE-2026-90436) | Apache Axis - Apache Axis Unsafe Reflection Vulnerability | Remote code execution | 2026-11-21 | 3% |
| [CVE-2026-115731](https://www.cve.org/CVERecord?id=CVE-2026-115731) | Perforce Puppet Enterprise - Perforce Puppet Enterprise Deserialization of Untrusted Data Vulnerability | Remote code execution | 2026-12-01 | 13% |
| [CVE-2026-114713](https://www.cve.org/CVERecord?id=CVE-2026-114713) | UnrealIRCd UnrealIRCd - UnrealIRCd Improper Neutralization of Delimiters Vulnerability | Actively exploited | 2026-11-16 | 10% |

## Watchlist - high exploitation probability, not in KEV yet

| CVE | Flaw | EPSS (30-day exploitation probability) |
|---|---|---|
| [CVE-2021-45105](https://www.cve.org/CVERecord?id=CVE-2021-45105) | Apache Software Foundation Apache Log4j2 - Apache Log4j2 does not always protect from infinite recursion in lookup evaluation | 100% |
| [CVE-2023-50387](https://www.cve.org/CVERecord?id=CVE-2023-50387) | n/a n/a -  | 100% |
| [CVE-2021-44832](https://www.cve.org/CVERecord?id=CVE-2021-44832) | Apache Software Foundation Apache Log4j2 - Apache Log4j2 vulnerable to RCE via JDBC Appender when attacker controls configuration | 98% |
| [CVE-2022-21661](https://www.cve.org/CVERecord?id=CVE-2022-21661) | WordPress wordpress-develop - SQL injection in WordPress | 98% |
| [CVE-2021-44790](https://www.cve.org/CVERecord?id=CVE-2021-44790) | Apache Software Foundation Apache HTTP Server - Possible buffer overflow when parsing multipart content in mod_lua of Apache HTTP Server 2.4.51 and earlier | 97% |
| [CVE-2022-37061](https://www.cve.org/CVERecord?id=CVE-2022-37061) | n/a n/a -  | 96% |

Data policy: aggregates only; individual websites are never named. License: MIT. Machine-readable: feed.json (schema zeront-feed/2), feed.xml (RSS), llms.txt.
