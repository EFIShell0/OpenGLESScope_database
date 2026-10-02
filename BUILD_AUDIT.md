# OpenGLESScope Database 2.0.3 build audit

## 2.0.3 VulkanScope 1.4.12 UI-shell reuse
- Chromium browser regression at 1440×900 and 390×844: 16 destinations, country/clock preferences, filtered selects, invalid pagination, Settings toggles, explicit request-only network diagnostics, and clearing after close passed without page errors.
- `tools/test_2_0_3_browser.py` and `tools/test_2_0_3_full_browser_regression.py` are provided as offline/mock-browser regressions; requiring Chromium in the core source gate would obstruct environments without a browser.
- Shared header SVG/chrome, Settings drawer categories, hero-v127 grid, loading stage, scrolling controls, destructive confirmation and footer were transplanted from the exact VulkanScope Database 1.4.12 source.
- Common VulkanScope 1.4.12 CSS is embedded verbatim after GL/EGL-only pre-existing styles, with a bounded branding and compatibility override tail.
- The original GL/EGL application logic, data filtering and schema are retained; 16 tabs including native GL/EGL sections remain functional.
- Wrangler 4.146.0 security pin is carried over from the verified 2.0.2 maintenance update.
- No DEPLOY markdown is packaged, per distribution policy.
- Static snapshot verification accepts the 2.0.3 release identity, preserving the separate accepted-report + Pages publication verification flow.


- Database: 2.0.3
- Current producer: OpenGLESScope 2.2.22 / 2222
- Submission schema: 2. Technical report schema: 5. Normalizer: 16.
- UI assets: `app.v2003.js`, `site.v2003.css` and `config.js?v=2003`.
- Locked registry catalog: 5,261 OpenGL ES/EGL reference entries. Reference presence is not runtime support.
- Worker and Pages versions must match before deployment. D1 migration 0004 required before worker deployment; no historical payload rewrite.
- Release checks: `python -B tools/quality_gate.py` and clean extracted repeat. Real Cloudflare deployment remains separate verification.

## Browser interaction evidence
- Optional reproducible offline Chromium harness: `python -B tools/test_2_0_3_browser.py` (requires Python Playwright and installed Chromium, or `CHROMIUM_PATH`). The harness supplies only a local mock response/canonical locked catalog, temporarily removes CSP in its isolated test document to inline the exact shipped assets, and does not change release CSP.
- Executed headless Chromium at 1440 x 900 and 390 x 844; rechecked request-scoped Internet diagnostics, no-fetch-before-click and drawer-close clearing: 16 views, 50-row Encyclopedia, page bounds, custom searchable country selector (maximum 50 results), country Toronto/Istanbul zones, manual UTC/seasonal preview, settings toggles, close behavior, live connection/progress controls and zero JavaScript page errors passed. No live Cloudflare/production upload/browser matrix has been claimed.
- Clean-source `python -B tools/quality_gate.py` and clean-extract repeat are independently release-blocking.

## 2.0.2 security and snapshot changes (retained)
- Single-observation `/v1/sync` consistency, canonical 4 MiB retrieval limit and atomic D1 chunk migration 0004 for oversized inline payloads.
- SHA-256 checked report reads and rejection of missing/altered chunks.
- Snapshot retry bounds, isolated release and snapshot jobs with shared deployment serialization, authoritative expected-ID checks and published Pages verification.
- Release and snapshot workflows execute the clean source gate immediately before staging. Optional snapshot secret is never committed.

- Privacy: only the user-activated Internet request diagnostics disclose the network address seen by Cloudflare; Settings close clears it, and no report or Pages snapshot stores it.

## Existing Git checkout hygiene
The original release archive has no `worker/package-lock.json`, `.gitattributes` or historical `rules/0.2.6_OPENGLESSCOPE_0.3.3_FULL_DATABASE_AUDIT.md`. These optional existing-checkout files are excluded from the deterministic *source ZIP* census, without deletion from the user’s Git checkout. The Wrangler 4.146.0 package declaration and offline Worker security check remain mandatory. A freshly regenerated npm lock must be audited in the deployment environment; no unverified lock data is invented.
