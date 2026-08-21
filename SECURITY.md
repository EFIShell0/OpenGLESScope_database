# Security

OpenGLESScope Database accepts only complete OpenGLESScope technical report submissions over HTTPS.

## Submission validation

The Worker enforces exact schema-v2 / technicalReport-v1 object shapes, bounded strings and arrays, canonical diagnostic states, exact duplicated extension/display consistency, complete collection state and a compatibility floor of OpenGLESScope 0.1.17+.

For current OpenGLESScope 0.1.25 reports, canonical TXT identity is cross-checked against structured application, GPU, driver, OpenGL ES, EGL and Android evidence. Canonical section counts must match structured report arrays. Duplicate limit/diagnostic/extension/format/precision/config identities are rejected. Available limits and precision values require matching Available diagnostics, and non-empty enumeration arrays require successful enumeration evidence. KHR_debug/core debug and EXT_disjoint_timer_query evidence is checked when applicable.

## Privacy

Payload field names are recursively inspected after JSON parsing. Sensitive-name canonicalization removes punctuation and separators before matching. IMEI, Android ID, device serial, MAC/account/authentication identifiers, request-IP fields, advertising identifiers and private-path fields are forbidden report fields. Request IP addresses are not copied into report payloads or D1 report records.

The submission endpoint is intentionally accountless so the Android application can submit without a user account. CORS is a browser policy rather than caller attestation. Production operators may apply Cloudflare edge/rate-limit abuse controls without persisting request IP data as report content.

## Resource bounds and storage

Request bodies are streamed and rejected above 2 MiB before complete JSON materialization. Recursive canonicalization has a depth bound. Stable key-sorted canonical JSON is hashed with SHA-256 for report IDs. D1 statements remain parameter-bound and submission timestamps are server-authored.

Malformed stored JSON returns a generic 500 response without stack disclosure. Structured technical reports are returned without a duplicated normalized copy; compatibility normalization is materialized only for stored data without structured technicalReport evidence.

## HTTP and browser policy

CORS is restricted to the configured GitHub Pages origin. Native Android requests without an Origin header remain supported. API responses, including preflight, use no-store, nosniff, no-referrer, restrictive Permissions-Policy, frame denial, same-origin opener policy, same-site resource policy and a deny-by-default API Content Security Policy. Unsupported methods return 405 with an Allow header.

The frontend has no third-party JavaScript, analytics, remote fonts or advertising. API reads are timeout-bounded and capped at 4 MiB before JSON parsing. Detail fetching is concurrency-bounded and failures remain visible.

The frontend avoids report-derived HTML execution, dynamic code evaluation and silent static-index fallback. Coverage and custom table-scroll geometry use CSP-safe browser primitives.

## Deployment isolation

Production Wrangler configuration is pinned to Cloudflare account `6881527e6e0b9bc4a0c009473428d1bc` and D1 database `2c945dda-e320-4b3a-9fac-a086373db17c`. Production deploy/migration/diagnostic operations fail closed through the account verifier.
