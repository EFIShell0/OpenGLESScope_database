# OpenGLESScope Database

OpenGLESScope Database is the public, report-backed browser for OpenGLESScope OpenGL ES, EGL and Android Display/HDR evidence.

## Current database release

- Database: `0.1.23`
- Compatible producer floor: OpenGLESScope `0.1.17+` within the `0.1.x` producer line
- Current compatibility audit target: OpenGLESScope `0.1.25`
- Submission schema: `2`
- Technical report schema: `1`
- Worker normalizer: `5`
- Frontend JavaScript: `app.v033.js`
- Frontend CSS: `site.v033.css`

Application and database versions are intentionally independent.

## Public endpoints

- Website: `https://efishell0.github.io/OpenGLESScope_database/`
- API: `https://openglesscope-database-api.openglesscope.workers.dev`
- Application repository: `https://github.com/EFIShell0/OpenGLESScope`
- Database repository: `https://github.com/EFIShell0/OpenGLESScope_database`

## Data model

The database preserves the complete structured report and canonical TXT snapshot submitted by the application. OpenGL ES, GLSL ES, EGL and Android platform/display evidence remain separate. Runtime extension tokens are preserved verbatim. Query diagnostics preserve Available, Unavailable, Not applicable and Unknown as distinct states.

Structured detail includes OpenGL ES/EGL identity, exact GL/EGL extension sets, implementation limits, compressed and binary formats, shader precision, query diagnostics, complete EGL configuration attributes and Android Display/HDR evidence. Top-level and technical-report display objects are validated as complete duplicate evidence and must agree.

## Frontend quality floor

The frontend uses no third-party scripts, analytics, remote fonts or advertising dependencies. It provides keyboard-accessible navigation and controls, local application-derived brand/HDR/GPU artwork, responsive horizontal overflow controls, deterministic 10/25/50-row report pagination, exact report comparison, explicit state-semantic coverage and canonical raw-report access.

Live API failures are explicit error states and are never replaced by an empty static index. Detail-fetch failures are surfaced in the hero metrics. Global search covers loaded structured technical fields in addition to report summary metadata. API responses are timeout-bounded and capped at 4 MiB before JSON materialization.

## Submission and privacy

Reports are uploaded only after an explicit application action. Request bodies are streamed with a 2 MiB hard bound and are never truncated. Exact schema shapes are enforced. Personal identifiers, account/authentication fields, request IP data and private paths are forbidden report fields. Sensitive field-name matching canonicalizes punctuation/separators before comparison.

Stored IDs are SHA-256 hashes of stable key-sorted canonical JSON, and submission time is authored only by the server-side D1 database. Current `OpenGLESScope report` TXT headers are cross-checked against structured application version/versionCode/package identity; the compatible legacy producer header is retained for 0.1.17+ reports.

## Cloudflare account isolation

Production Worker configuration is pinned to Cloudflare account `6881527e6e0b9bc4a0c009473428d1bc` and D1 database `2c945dda-e320-4b3a-9fac-a086373db17c`. Production deploy, migration, migration-list and D1 diagnostic npm commands fail closed through the account verifier. Wrangler is pinned to `4.124.0`.

Local credentials, Wrangler state, environment files, dependencies, logs, caches and build output are excluded by `.gitignore`.

Recommended local commands from `worker/`:

```text
npm install
npm run auth:create
npm run auth:activate
npm run auth:status
npm run test:contract
npm run migrate
npm run deploy
```

`auth:create` is normally needed only once for the local profile.



## 0.1.23 Reports table visual parity

0.1.23 aligns the Reports table presentation with VulkanScope Database 0.35.8 without changing OpenGL ES/EGL evidence semantics or the submission schema. The GPU column label is now Device, complete OpenGL ES and EGL runtime version strings use the same compact version-chip geometry as VulkanScope API versions, Report ID uses matching monospace sizing and normal weight, and Reports header typography follows the VulkanScope reference. Version chips remain single-line so EGL and OpenGL ES version values do not wrap vertically; horizontal overflow remains handled by the synchronized table scroller.

## 0.1.22 OpenGLESScope 0.1.25 and full tab parity audit

0.1.22 aligns the database with OpenGLESScope 0.1.25 query evidence and closes the remaining shared UI-quality gaps found against VulkanScope Database 0.35.8. Reports now include Driver identity; report-detail tabs expose counts and evidence-aware category views; Extensions and Formats distinguish successful empty/not-listed enumeration from unavailable enumeration; Limits aggregate only actual GL limit queries; Precision uses all loaded reports in its denominator; Display/HDR exposes mode count and luminance evidence. Responsive table geometry and coverage meters are CSP-safe while preserving the 0.1.20 scroll/thumb/shadow interaction contract.

The Worker normalizer is version 5. Current 0.1.25 submissions receive duplicate-evidence checks, section-count cross-checks, Available-diagnostic requirements for structured limits/precision, enumeration-evidence consistency, and KHR_debug / EXT_disjoint_timer_query diagnostic validation. The compatibility floor remains 0.1.17+ and no D1 migration is introduced.

## 0.1.21 platform metadata, parity and full audit

0.1.21 closes the remaining shared-quality gap with VulkanScope Database for report identity and platform metadata. Reports now expose the Android release/API level and the installed OpenGLESScope ABI in the main report table, report Summary, report hero context, global search and Compare. Supported device ABIs are also surfaced without changing canonical stored reports. For current 0.1.24 reports the Worker derives ABI evidence from the canonical TXT snapshot because the producer's schema-v2 application object does not yet carry ABI fields; structured Android release/API remains authoritative from the device object. Older compatible reports retain Unknown rather than guessed ABI values.

The Worker read normalizer is version 4. Current 0.1.24 canonical TXT snapshots are cross-checked against structured GPU, driver mode, OpenGL ES and Android identity, require explicit Application ABI and Supported device ABIs lines, and keep the 2 MiB submission bound, exact schema shapes, recursive sensitive-key rejection, origin restriction and hardened response headers. Stored payloads and D1 schema are unchanged.

The published specification provenance is explicit: OpenGL ES 3.2, GLSL ES 3.20 and EGL 1.5 remain the current Khronos core specifications. Runtime extension names continue to be displayed exactly as reported by the implementation; registry freshness never causes an unreported extension to be inferred as supported or unsupported.

## 0.1.20 responsive table interaction parity

0.1.20 repairs the horizontal table affordance across Reports and every other wide table. The custom thumb now reflects the real viewport/content ratio and moves with the table scroll position; it can be dragged with pointer input, controlled with Arrow/Home/End keys, and remains synchronized with touch/trackpad/native horizontal scrolling and resize changes. Left/right edge shadows fade according to the actual hidden content so mobile portrait layouts expose scroll direction without obscuring table data. Controls are hidden when a table does not overflow. Reduced-motion behavior disables nonessential transitions while preserving direct scrolling. No report semantics, Worker schema, D1 schema or stored payload is changed.

## 0.1.19 full audit

The 0.1.19 audit corrected current OpenGLESScope 0.1.23 TXT-header compatibility, exact-object validation, separator-safe sensitive-key matching, duplicated display consistency, diagnostic-state validation, limit/diagnostic denominators, HDR empty-list semantics, technical global search, live-API failure handling, detail-load visibility and response duplication. It also adds a repeatable Worker contract suite and refreshes the static audit to the actual live cache-busted assets.

No D1 migration or stored-report rewrite is introduced by 0.1.19. The Pages workflow validates the static index and runs the full repository audit before uploading the deployment artifact.

See `SECURITY.md`, `rules/PROJECT_RULES.md` and `rules/0.1.19_FULL_DATABASE_AUDIT.md` for the security/correctness contract and detailed audit result.
