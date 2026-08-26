# OpenGLESScope Database 0.7.4 Build / Release Audit

- Database version: 0.7.4
- Current producer: OpenGLESScope 0.7.2 / versionCode 702
- Submission schema: 2
- Technical report schema: 2 for OpenGLESScope 0.7.0+
- Normalizer: 10
- Browser assets: app.v074.js / site.v074.css
- D1 migration: not required

## Presentation audit
0.7.4 re-audits shared database presentation against VulkanScope Database 0.39.8. Compare now uses a bounded compact primary picker, a single secondary Section / Field search row, a separate share action and immediately adjacent summary/results. Navigation, hero spacing, card-grid sizing, custom-select geometry, table-scroll controls, page-button states and responsive filter geometry use the shared interaction dimensions while OpenGL ES/EGL branding and magenta styling remain product-specific.

Clear filters is hidden when there is no visible active filter or global search. Desktop Compare control groups are bounded to 760 CSS px; tablet and phone layouts use deterministic two-column and one-column fallbacks.

## Release-gate audit
The following gates passed on the source tree:
- repository repair/check
- static index rebuild before source audit
- source audit
- audit-hygiene regression tests
- frontend and Worker JavaScript syntax checks
- route contract
- Compare semantics contract
- Statistics/filter contract
- shared UI parity contract
- Worker contract
- allow-listed Pages staging
- staged Pages artifact audit

`tools/build_index.py` is pinned to databaseVersion 0.7.4 and currentProducer OpenGLESScope 0.7.2. `tools/repair_repository.py --apply` removes stale assets/workflows, README.md, root release.md and transient dependency/cache/build directories so local audit preparation no longer requires separate manual cleanup commands.
