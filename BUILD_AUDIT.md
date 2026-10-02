# OpenGLESScope Database 3.0.7 build audit

## 3.0.7 Overview, action geometry, Back and startup regression
- First report-detail destination uses Overview with shared grouped metadata hierarchy; all existing GL/EGL and Display evidence is retained without claiming unsupported fields. Existing Overview URLs remain canonical; earlier Summary alias remains readable.
- Shared detail hero contains all user report actions including additional canonical TXT export. Favoriting uses the common SVG and visible state labels, independent of report-link activation.
- Restored cancelable 120 ms detail exit/210 ms entry, 105/180 ms tab, 90/150 ms workspace transitions, initial loader closure and reduced-motion behavior.
- Fixed accessible Back placement under the sticky header on mobile/desktop; prevented horizontal clipping from creating a non-sticky nested body scrollbar. Back returns to the previous report list scroll.
- The release adds deterministic shell negative mutation checks and desktop/mobile Chromium regression; no API schema or D1 change.

## 3.0.6 Settings, filter and progress repair
- Settings Internet now has 26 request-scoped observation rows and 34 local browser/runtime rows in the reference two-section layout. No network lookup before an explicit user visit to Internet; observed addresses start mosaicked and clear when Settings closes.
- Removed legacy duplicate Browser Information injected into Information, extra Internet actions and Settings page-size selector; bundled 250 first-party country flags, with source and Pages auditing of the exact inventory.
- Per-view GL/EGL filter applicability and grouped control families prevent other tabs receiving irrelevant or stale state; Android artwork bytes match reference, with no overriding size rule.
- Fixed page progress element/CSS mismatch using the reference span fill.
- New static gate `tools/test_3_0_6_settings_filter_contract.py` and desktop/mobile Chromium interaction regression run; no D1 migration or historical report mutation.

## 3.0.5 publication and report interactions
- New report-detail JSON and canonical TXT downloads use validated report identifiers and preserve producer-authored bytes for TXT.
- Shared report actions retain identical geometric button classes, SVG structure, disabled/busy and success/failure feedback.
- Frontend detects Worker release transitions separately from failures, checks immutable published assets without gating on initial index readiness, and prevents failed/incomplete releases from triggering reload.
- Report text selection/drag suppresses row activation; URL-scoped restoration keeps report and settings navigation at the prior scroll position.
- No D1 migration, report backfill or producer-version adjustment was performed.

## 3.0.3 VulkanScope 1.4.12 UI-shell reuse
- Chromium browser regression at 1440×900 and 390×844: 16 destinations, country/clock preferences, filtered selects, invalid pagination, Settings toggles, explicit Settings Internet-only request diagnostics, and clearing after close passed without page errors.
- `tools/test_3_0_0_live_browser.py` exercises actual shipped scripts in isolated Chromium using deterministic mocked API and legally packaged license content; requiring Chromium in core source tests would obstruct environments without a browser. Prior 2.0.5 browser regression tests are also retained.
- Shared header SVG/chrome, Settings drawer categories, hero-v127 grid, loading stage, scrolling controls, destructive confirmation and footer were transplanted from the exact VulkanScope Database 1.4.12 source.
- The VulkanScope 1.4.12 shared CSS is FIRST, SHA-pinned and equal in its non-color geometry; red/maroon palette values are remapped to OpenGLESScope magenta while bounded GL/EGL-specific selectors remain at the end. The old duplicated generic GL style layer was removed.
- The original GL/EGL application logic, data filtering and schema are retained; 16 tabs including native GL/EGL sections remain functional.
- Wrangler 4.146.0 security pin is carried over from the verified 2.0.2 maintenance update.
- No DEPLOY markdown is packaged, per distribution policy.
- Static snapshot verification accepts the 3.0.3 release identity, preserving the separate accepted-report + Pages publication verification flow.


- Database: 3.0.7
- Current producer: OpenGLESScope 2.2.22 / 2222
- Submission schema: 2. Technical report schema: 5. Normalizer: 16.
- UI assets: `app.v3007.js`, `site.v3007.css` and `config.js?v=3007`.
- Locked registry catalog: 5,261 OpenGL ES/EGL reference entries. Reference presence is not runtime support.
- Worker and Pages versions must match before deployment. Check the existing D1 migration list; migration 0004 is required only on databases that have not applied it. No historical payload rewrite.
- Release checks: `python -B tools/quality_gate.py` and clean extracted repeat. Real Cloudflare deployment remains separate verification.

## Browser interaction evidence
- Optional reproducible offline Chromium harness: `python -B tools/test_3_0_0_live_browser.py` (requires Python Playwright and installed Chromium, or `CHROMIUM_PATH`). The harness supplies only a local mock response/canonical locked catalog, temporarily removes CSP in its isolated test document to inline the exact shipped assets, and does not change release CSP.
- Executed headless Chromium at 1440 x 900 and 390 x 844; rechecked request-scoped Internet diagnostics, no-fetch-before-click and drawer-close clearing: 16 views, 50-row Encyclopedia, page bounds, custom searchable country selector (maximum 50 results), country Toronto/Istanbul zones, manual UTC/seasonal preview, settings toggles, close behavior, live connection/progress controls and zero JavaScript page errors passed. No live Cloudflare/production upload/browser matrix has been claimed.
- Clean-source `python -B tools/quality_gate.py` and clean-extract repeat are independently release-blocking.

## 2.0.2 security and snapshot changes (retained)
- Single-observation `/v1/sync` consistency, canonical 4 MiB retrieval limit and atomic D1 chunk migration 0004 for oversized inline payloads.
- SHA-256 checked report reads and rejection of missing/altered chunks.
- Snapshot retry bounds, isolated release and snapshot jobs with shared deployment serialization, authoritative expected-ID checks and published Pages verification.
- Release and snapshot workflows execute the clean source gate immediately before staging. Optional snapshot secret is never committed.

- Privacy: only opening the Internet Settings panel can request the network address seen by Cloudflare; Settings close clears it, and no report or Pages snapshot stores it.

## Existing Git checkout hygiene
The original release archive has no `worker/package-lock.json`, `.gitattributes` or historical `rules/0.2.6_OPENGLESSCOPE_0.3.3_FULL_DATABASE_AUDIT.md`. These optional existing-checkout files are excluded from the deterministic *source ZIP* census, without deletion from the user’s Git checkout. The Wrangler 4.146.0 package declaration and offline Worker security check remain mandatory. A freshly regenerated npm lock must be audited in the deployment environment; no unverified lock data is invented.

## Release 2.0.5
- Fixed frontend/API release stamp mismatch, audited Android OpenGL® ES™ / EGL™ art and introduced exact-producer POST restriction without D1 migration.

## 3.0.0 native theme/experience release
- The shared reference's layout geometry is retained with OpenGLESScope #BA2A8D branding rather than VulkanScope red.
- Adds native startup gate, bounded same-origin version checks, network status notices, 3-second live sync, new-report toast, privacy/local-storage disclosure and actual locally packaged third-party licenses.
- Existing Worker D1 and exact current producer contract remain unchanged beyond database release identity 3.0.7.
- Visual/browser checks must be distinguished from actual Cloudflare deployment, which is a separate operation.

## 3.0.0 final explicit experience regression
- `python -B tools/test_3_0_0_live_browser.py`: actual inline runtime of all first-party shipped scripts, desktop and mobile, startup hold release, first-visit privacy, viewing and returning from genuine application MIT license without silently acknowledging, session-only consent, source-bound license viewer, seven legal cards, Settings transitions, all 16 destinations, and no unsolicited network address request; zero JavaScript page exceptions. Production Cloudflare is not simulated as proof of remote deployment.
- Startup asset URLs include `?v=3007` consistently in index and release-bootstrap; the source marker remains fail-closed (`releaseReady:false`) until `build_pages_artifact.py` stages and audits the complete `releaseReady:true` Pages artifact.

## 3.0.3 publication and interaction verification
- Actual Chromium at 1440x900 and 390x844: 63 submitted report summaries, five live count metrics, all eleven evidence tabs, reference Compare A/B/swap/search/pin/minimize, and a simulated 64th D1 report updating the count and toast without JavaScript errors.
- Deterministic executable future release checks validate source fail-closed marker, seven actual published assets, reject partial releases, auto-navigate with preserved hash, refuse repeat navigation and protect against stale cache.
- Worker D1-first accepted report dispatch and authenticated snapshot workflow remain unchanged, under contract tests; Pages checks expected new accepted report before publication.
- This release enables automatic future upgrade checks in tabs running 3.0.3 onward. A tab that remains open on 3.0.2 uses the already-loaded old JavaScript and still needs its existing manual Update now action once to enter the new policy.
- Quality gate is run on original and independently clean-extracted package. Browser tests use only mocked content, with no live D1 insert or claimed external Cloudflare deployment.

## 3.0.7 parity repair and independent source review
- Fixed first-load database-loading class remaining set after loader dismissal, which had suppressed the transplanted reference scroll UI on every update.
- Switched Settings Internet and Browser to card/grid row hierarchy rather than single-line/plain-paragraph summaries; network metadata requires the user to open Settings Internet and remains masked by default.
- Used official white EGL v028 (pixel-white transparency), reference HDR10+ v1014, and exact reference green Android filter vector.
- Chart percentages and evidence-state coverage use matching reference geometry without inventing unsupported/available GL/EGL data.
- Preserved all 3.0.3 report, Compare, snapshot, release auto-navigation and schema/producer contracts.

- All fourteen HTTP status documents retain the 1.4.12 error page geometry, independent OpenGLESScope links and strict scriptless CSP; the Browser compatibility script is source-locked except brand text.
- Restricted storage API access no longer raises a Settings Information exception; optional Chromium regression checks actual natural overflow with 15 report summaries and correctly loaded first-party inline PNG/CSS/JS at two viewport sizes.
