# Security

OpenGLESScope Database accepts only complete OpenGLESScope report submissions over HTTPS.

The Worker enforces the official application/package identity, compatible 0.1.x producer versions, schema versions, bounded arrays/strings, exact extension-count consistency, EGL/display field types, complete collection status and the canonical TXT report structure. Duplicate structured extension sets must match the corresponding top-level runtime sets.

Request bodies are bounded to 2 MiB before JSON materialization. Excessive recursive depth and forbidden sensitive field names are rejected. Stored report IDs use SHA-256 over stable canonical JSON. D1 submission timestamps are server-authored.

CORS is restricted to the configured GitHub Pages origin. Responses use no-store, nosniff, no-referrer, restrictive Permissions-Policy, frame denial, same-origin opener policy and a deny-by-default API Content Security Policy.

The frontend uses only same-origin presentation assets and the configured HTTPS API. API JSON materialization is timeout-bounded and capped at 4 MiB per response. Detail fetching is concurrency-bounded.

Do not add analytics, remote fonts, third-party JavaScript, automatic/background report submission, personal identifiers, authentication data or private file paths to report payloads.
