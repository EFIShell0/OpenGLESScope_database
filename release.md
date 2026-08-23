# OpenGLESScope Database 0.2.6

OpenGLESScope Database 0.2.6 restores exact compatibility with OpenGLESScope 0.3.3 while preserving the schema-2 / technicalReport-1 storage contract and existing report corpus.

## Changes

- Current producer audit target is OpenGLESScope 0.3.3 / versionCode 303.
- Accepts the 0.3.3 canonical TXT core-version evidence: `Core version:` plus `Core version provenance:`.
- Preserves backward compatibility with older compatible producers that use the historical `Parsed core version:` line.
- Requires the 0.3.3 version/versionCode identity pair and rejects mismatches fail-closed.
- Preserves the expanded 0.3.3 query-diagnostic array without schema changes or truncation.
- Registry audit date and Cloudflare Worker compatibility date are 2026-08-24.
- Worker normalizer metadata is 9.
- No D1 migration or stored-payload rewrite is required.

## Version

- Database: 0.2.6
- Submission schema: 2
- Technical report schema: 1
- Current producer: OpenGLESScope 0.3.3 / versionCode 303
- OpenGL ES baseline: 3.2
- GLSL ES baseline: 3.20
- EGL baseline: 1.5
