# Security

OpenGLESScope Database accepts only complete OpenGLESScope technical report submissions over HTTPS.

## Submission validation

The Worker enforces:

- Application identity `OpenGLESScope` / `com.efishell.openglesscope`.
- Compatible OpenGLESScope `0.1.17+` producers within the `0.1.x` line.
- Submission schema `2` and technicalReport schema `1`.
- Exact top-level and nested object shapes.
- Bounded arrays, strings and numeric/scalar fields.
- Exact OpenGL ES/EGL extension counts and duplicated extension-set consistency.
- Complete top-level and technical-report display objects with exact duplicate consistency.
- Canonical diagnostic states: Available, Unavailable, Not applicable and Unknown.
- Complete collection state.
- Current and compatible legacy canonical TXT header/section structure.

Current `OpenGLESScope report` TXT metadata is cross-checked against structured version, versionCode and package identity.

## Privacy

Request payload field names are recursively inspected after JSON parsing. Sensitive-name canonicalization removes punctuation and separators before matching, so variants such as `user_id`, `account-id` and `access.token` do not bypass the guard.

IMEI, Android ID, device serial, MAC/account/authentication identifiers, request IP fields and private-path fields are forbidden. Request IP addresses are not copied into report payloads or D1 report records.

The public submission endpoint is intentionally accountless so the Android application can submit without a user account. Schema validation and CORS are not cryptographic proof that a non-browser caller is the official APK. Production operators should apply Cloudflare edge/rate-limit abuse controls when appropriate without persisting request IP data as report content.

## Resource bounds and storage

Request bodies are streamed and rejected above 2 MiB before JSON materialization completes. Recursive canonicalization has a depth bound. Stored report IDs use SHA-256 over stable key-sorted canonical JSON, so JSON key reordering cannot bypass deduplication. D1 statements remain parameter-bound and submission timestamps are server-authored.

Malformed stored JSON returns a generic 500 response without stack disclosure. Structured technical reports are returned without a duplicated normalized copy; compatibility normalization is only materialized for legacy rows that lack structured technicalReport data.

## HTTP and browser policy

CORS is restricted to the configured GitHub Pages origin. Worker responses use no-store, nosniff, no-referrer, restrictive Permissions-Policy, frame denial, same-origin opener policy and a deny-by-default API Content Security Policy. Unsupported API methods return 405 with an Allow header.

The frontend uses only same-origin presentation assets and the configured HTTPS Worker API. It contains no third-party JavaScript, analytics, remote fonts or advertising. API JSON reads are timeout-bounded and capped at 4 MiB before parsing. Detail requests are concurrency-bounded, and failures are surfaced instead of silently removed from the apparent loaded set.

Production Wrangler configuration is pinned to the intended Cloudflare account and D1 database. Production npm operations fail closed through the account verifier when account identity cannot be confirmed.

## 0.1.21 platform metadata handling
Android release/API values are read from the submitted structured device object. Application ABI and supported device ABIs are derived from the canonical TXT snapshot only when structured ABI fields are absent. The database does not infer ABI from GPU names, Android model names or CPU marketing data. Derived runtime metadata is added only to API read responses and does not mutate canonical stored payloads. Current 0.1.24 TXT identity lines are cross-checked with structured GPU, driver mode, OpenGL ES and Android fields before acceptance.
