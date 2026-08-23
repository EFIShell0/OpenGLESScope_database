# OpenGLESScope Database 0.2.8 Build Audit

Date: 2026-08-24

## Release gates

- Database identity: 0.2.8.
- Current producer: OpenGLESScope 0.3.4 / versionCode 303.
- Submission schema 2 / technicalReport schema 1 unchanged.
- OpenGLESScope 0.3.4 direct submission contract: PASS (HTTP 201).
- Missing 0.3.3 core-version provenance: rejected (HTTP 400).
- Incorrect 0.3.3 versionCode: rejected (HTTP 400).
- OpenGLESScope 0.3.2 backward-compatibility contract: PASS (HTTP 201).
- Historical compatible producer contracts: PASS.
- Expanded queryDiagnostics remains bounded and schema-compatible.
- Canonical TXT is retained together with structured technical evidence.
- Static database audit: PASS after release packaging validation.
- Worker JavaScript syntax and contract suite: PASS after release packaging validation.
- Frontend JavaScript syntax: PASS after release packaging validation.
- Cloudflare Worker compatibility date: 2026-08-24.
- D1 migration required: no.

The release changes validation/provenance metadata only. Existing D1 rows and canonical stored payloads are not rewritten.

- Cloudflare compatibility date deployability: 2026-08-23, non-future for observed API window.
