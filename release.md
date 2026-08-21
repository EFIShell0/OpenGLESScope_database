# OpenGLESScope Database 0.1.19

OpenGLESScope Database 0.1.19 is a full correctness, security, compatibility and performance audit release.

## Highlights

- Fixed submission compatibility with the current OpenGLESScope 0.1.23 TXT report header while retaining the 0.1.17+ compatible legacy header.
- Hardened Worker validation to exact JSON object shapes and complete duplicated display evidence.
- Fixed sensitive field-name normalization so punctuation/separators cannot bypass forbidden identifier matching.
- Restricted query diagnostics to canonical Available / Unavailable / Not applicable / Unknown states.
- Fixed limit and diagnostic aggregate denominators and authoritative diagnostic-state handling.
- Fixed Android HDR empty-list semantics: explicit empty is Unavailable; missing evidence is Unknown.
- Removed the misleading empty-static-index fallback for live API outages.
- Added visible report-detail load failure metrics.
- Expanded global search to loaded structured technical data.
- Avoided duplicating structured technicalReport data into a second normalized detail response.
- Improved main-view transition cancellation/accessibility and removed quadratic OpenGL ES/EGL overview membership scans.
- Corrected parsed core-version display to canonical `major.minor` formatting.
- Added repeatable Worker contract tests and refreshed the repository audit for the actual active cache-busted assets.
- Hardened the GitHub Pages pipeline so static-index validation and the full repository audit run before artifact upload, with current Pages action versions and non-cancelling production deployment concurrency.

## Compatibility

- Compatible producer floor: OpenGLESScope 0.1.17+
- Current audit target: OpenGLESScope 0.1.23
- Submission schema: 2
- Technical report schema: 1
- Worker normalizer: 3
- No D1 migration
- No stored-report rewrite

## Validation

- Frontend JavaScript syntax: PASS
- Worker JavaScript syntax: PASS
- Worker contract suite: PASS
- JSON/JSONC parse checks: PASS
- CSP/local asset reference audit: PASS
- Cloudflare account and D1 pin audit: PASS
- Repository audit: PASS

No live production deployment or remote D1 mutation is performed by this release package.
