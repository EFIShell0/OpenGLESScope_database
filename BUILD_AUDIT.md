# OpenGLESScope Database 2.0.2 build audit

- Database: 2.0.2
- Current producer: OpenGLESScope 2.2.22 / 2222
- Submission schema: 2. Technical report schema: 5. Normalizer: 16.
- UI assets: `app.v2002.js`, `site.v2002.css` and `config.js?v=2002`.
- Locked registry catalog: 5,261 OpenGL ES/EGL reference entries. Reference presence is not runtime support.
- Worker and Pages versions must match before deployment. D1 migration 0004 required before worker deployment; no historical payload rewrite.
- Release checks: `python -B tools/quality_gate.py` and clean extracted repeat. Real Cloudflare deployment remains separate verification.

## Browser interaction evidence
- Optional reproducible offline Chromium harness: `python -B tools/test_2_0_2_browser.py` (requires Python Playwright and installed Chromium, or `CHROMIUM_PATH`). The harness supplies only a local mock response/canonical locked catalog, temporarily removes CSP in its isolated test document to inline the exact shipped assets, and does not change release CSP.
- Executed headless Chromium at 1440 x 900 and 390 x 844; rechecked request-scoped Internet diagnostics, no-fetch-before-click and drawer-close clearing: 16 views, 50-row Encyclopedia, page bounds, custom searchable country selector (maximum 50 results), country Toronto/Istanbul zones, manual UTC/seasonal preview, settings toggles, close behavior, live connection/progress controls and zero JavaScript page errors passed. No live Cloudflare/production upload/browser matrix has been claimed.
- Clean-source `python -B tools/quality_gate.py` and clean-extract repeat are independently release-blocking.

## 2.0.2 parity changes
- Single-observation `/v1/sync` consistency, canonical 4 MiB retrieval limit and atomic D1 chunk migration 0004 for oversized inline payloads.
- SHA-256 checked report reads and rejection of missing/altered chunks.
- Snapshot retry bounds, isolated release and snapshot jobs with shared deployment serialization, authoritative expected-ID checks and published Pages verification.
- Release and snapshot workflows execute the clean source gate immediately before staging. Optional snapshot secret is never committed.

- Privacy: only the user-activated Internet request diagnostics disclose the network address seen by Cloudflare; Settings close clears it, and no report or Pages snapshot stores it.
