# OpenGLESScope Database Engineering Rules

## Non-negotiable
- Source-code comments are forbidden.
- Security, correctness, memory safety, performance and usability are never traded away for convenience.
- No guessed OpenGL ES, EGL, display or HDR capability may be reported.
- Available, unavailable, not-applicable and unknown are distinct states.
- Runtime OpenGL ES and EGL extension names remain exactly as reported by the implementation.
- OpenGL ES version, GLSL ES version, EGL version and Android platform version remain distinct values.
- Android Display/HDR evidence is never reinterpreted as OpenGL ES/EGL capability.
- Every technical category present in a complete submitted report remains accessible in the database UI.
- Parsed or aggregate views never replace or discard the canonical TXT report.
- Aggregate statistics describe only reports actually loaded by the database and never imply global ecosystem coverage.
- Missing extension or runtime-format tokens are shown as not listed/unknown rather than inferred unsupported.
- A queried scalar value is available even when its value is zero or false unless the field is itself a support boolean.
- Query diagnostics are authoritative for Available, Unavailable and Not applicable state.
- The frontend has no third-party JavaScript, analytics, remote fonts, advertisements or remote presentation dependencies.
- Production frontend and Worker API use HTTPS.
- Content Security Policy allows only same-origin resources and the configured OpenGLESScope Worker API.
- Browser-visible assets that materially change use versioned filenames or equivalent cache busting.
- Frontend detail fetching is concurrency-bounded.
- Reports pagination renders no more than 50 rows per page after sorting/filtering.
- Submission time shown by the UI comes only from server-side D1 submitted_at and retains the exact ISO timestamp.
- Device/display data stays private unless the user explicitly submits a complete report.
- Submission excludes personal identifiers, account/authentication data, request IP addresses and private paths.
- No automatic/background report upload exists.

## Submission and Worker
- Application identity is OpenGLESScope with package com.efishell.openglesscope.
- Application and database versions are independent. The database accepts compatible OpenGLESScope 0.1.x producers rather than requiring version equality.
- Public web URL is https://efishell0.github.io/OpenGLESScope_database/.
- API base is https://openglesscope-database-api.openglesscope.workers.dev.
- Request body is bounded to 2 MiB and is never truncated.
- Complete reports are all-or-nothing submissions.
- Stored report IDs are SHA-256 hashes of stable canonical JSON.
- Pagination uses server-authored submitted_at/id ordering and the submitted_at/id database index.
- Stored payloads are normalized on read so frontend/parser fixes apply without rewriting D1 rows.
- The frontend retains a canonical TXT compatibility fallback when structured normalization is unavailable, without inventing state semantics.
- Worker response bodies use no-store, nosniff, no-referrer, restrictive Permissions-Policy and frame denial headers.
- CORS is restricted to the configured GitHub Pages origin.
- Unsupported methods return 405 with an Allow header.
- Recursive submission inspection rejects sensitive field names and excessive nesting.

## Frontend
- Main navigation, report tables and comparison controls are keyboard accessible.
- Long navigation and tables provide horizontal overflow controls and preserve touch/trackpad scrolling.
- Reduced-motion preference disables nonessential transitions.
- Global search covers GPU, vendor, device, OpenGL ES and EGL summary metadata.
- Vendor, GPU and OpenGL ES version filters operate before 50-row pagination.
- Report detail tabs remain visible even when the selected category is empty.
- Detail tabs include Summary, OpenGL ES, EGL, Extensions, Limits, Formats, Precision, EGL Configs, Display/HDR, Diagnostics and Raw report.
- Extension aggregates distinguish reported from not listed; not listed is not mislabeled unsupported.
- Limit and diagnostic aggregates preserve Available, Unavailable, Not applicable and Unknown semantics.
- Compare uses exact report values and does not synthesize missing values.
- HDR artwork is local and used only when the Android-reported HDR type matches known bundled artwork. Unknown HDR names remain text.
- document.title follows the active database destination using the same destination semantics as the reference database: Reports uses the base title, every other main destination prefixes its visible label, and report detail prefixes GPU name plus the active detail-tab label.
- The database header uses the exact application horizontal logo asset. Browser icon assets use the application GL|ES artwork centered in white on an opaque black square; no alternative logo geometry is invented.

## OpenGLESScope 0.1.17 compatibility floor
- Schema version 2 and technicalReport schema version 1 are accepted.
- technicalReport includes limits, OpenGL ES extensions, EGL display extensions, EGL client extensions, compressed formats, shader binary formats, program binary formats, shader precision, query diagnostics, EGL configs and display evidence.
- EGL config presentation preserves every attribute currently emitted by OpenGLESScope 0.1.17.
- Display presentation preserves current mode ID, resolution, refresh rate, supported modes, wide-color evidence, HDR type list and Android-provided luminance metadata.
- Query diagnostics are preserved in structured detail, aggregate views and raw canonical report access.

## OpenGLESScope 0.1.17 compatibility additions
- Compatible submissions retain schema version 2 and technicalReport schema version 1.
- Application version/versionCode are preserved in report detail and server-side summary metadata.
- Runtime extension counts must exactly match the submitted runtime extension arrays, and duplicated technical-report extension sets must match their corresponding top-level sets.
- Nested EGL configuration and Android display evidence are type-validated rather than accepted solely by object presence.
- The canonical TXT snapshot must identify the same producer version and contain the core OpenGL ES, EGL, diagnostics and EGL-config sections.

## Release 0.1.7
- Database version is 0.1.7.
- Database version remains intentionally independent from the OpenGLESScope application version.
- Primary UI accent remains the official OpenGL ES brand tone #BA2A8D.
- Frontend API JSON materialization is capped at 4 MiB per response and timeout-bounded.
- Report summary metadata includes application version and versionCode for newly stored reports.
- Display/HDR evidence supports explicit newest/oldest ordering without changing server-authored submission timestamps.
- State-semantic coverage uses colored progress fills; non-dominant coverage containers remain neutral and only a uniquely dominant state receives additional emphasis.
- Active horizontal navigation remains visible through edge affordances and bring-into-view behavior.
- Release assets use v017 cache-busted filenames.


## Release 0.1.8
- Database version is 0.1.8.
- Production Wrangler configuration pins Cloudflare account ID 6881527e6e0b9bc4a0c009473428d1bc and D1 database ID 2c945dda-e320-4b3a-9fac-a086373db17c.
- The `openglesscope` Wrangler auth profile is directory-local operational state and is never committed.
- The committed account ID is mandatory fail-closed protection against deployment to an unrelated authenticated Cloudflare account.
- Repository ignore rules exclude node_modules, Wrangler local state, environment/secret files, logs, Python caches and OS metadata.
- `node_modules` is never committed. A locally generated package-lock may be committed for reproducibility.
- Wrangler is pinned to 4.124.0 for this release.
- No D1 schema migration is introduced by 0.1.8.
- Frontend cache-busted assets remain v017 because their bytes and behavior are unchanged.
