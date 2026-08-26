# OpenGLESScope Database 0.7.0 Build / Release Audit

## Release identity

- Database version: 0.7.0
- Current producer: OpenGLESScope 0.7.0 / versionCode 700
- Submission schema: 2
- Current technicalReport schema: 2
- Historical compatible technicalReport schema: 1
- Normalizer: 10
- Current browser assets: app.v070.js / site.v070.css
- D1 migration: none

## Executed source gates

- `python3 tools/audit_database.py --source-tree .`: PASS
- `python3 tools/repair_repository.py --check`: CLEAN
- `python3 tools/test_audit_hygiene.py`: ALL PASS
- `node --check assets/app.v070.js`: PASS
- `node --check worker/src/index.js`: PASS
- `node tools/test_routes.mjs`: ALL PASS
- `node tools/test_compare_contract.mjs`: ALL PASS
- `node worker/tests/contract.mjs`: ALL PASS

The Worker contract suite verifies the current 0.7.0/700 submission path, historical compatible producers, technicalReport-2 enforcement, required EGL runtime evidence, EGL binding consistency, duplicate rejection, extension-prerequisite validation, producer/version rejection, 2 MiB body bounds, CORS/media-type behavior, sensitive-field rejection, canonical schema behavior and existing report/detail routes.

## Pages artifact gate

A fresh allow-listed Pages artifact was generated with `tools/build_pages_artifact.py` and audited with `python3 tools/audit_database.py --artifact-tree <artifact>`. Result: PASS.

The staged artifact contains only the approved Pages HTML/config/schema/data/assets. Worker source, tools, rules, workflows, dependency trees and repository transients are excluded.

## Security and provenance

- GL_VENDOR / GL_RENDERER remain submitted runtime evidence; synthetic PCI/Vulkan-style vendor identifiers are not used.
- D1 access remains parameterized and canonical report identity remains SHA-256 based.
- Existing 2 MiB bounds, recursive sensitive-field rejection, CORS/CSP and fail-closed current-producer validation remain active.
- One-sided Compare absence remains Unknown / Not reported and is not fabricated as Unsupported.
- No D1 migration, stored-report rewrite or report-hash rewrite is introduced.

All Database release gates required by the 0.7.0 project rules passed on the source tree before packaging.
