# OpenGLESScope Database 0.1.26 Build Audit

The 0.1.26 source is derived from OpenGLESScope Database 0.1.25 and is compared against VulkanScope Database 0.35.8 for the shared table-header and custom-scroll interaction model.

Validation covers JSON/JSONC parsing, local asset references, CSP presence, source-comment prohibition, frontend and Worker JavaScript syntax, Worker contract tests, schema compatibility invariants, production Cloudflare/D1 pinning, cache-busted asset references, static index metadata, report-table/header parity and ZIP integrity.

The specification audit was refreshed against the Khronos OpenGL ES and EGL registries on 2026-08-21. Current published core baselines remain OpenGL ES 3.2, GLSL ES 3.20 and EGL 1.5.

No dynamic production deployment or live D1 mutation is performed by this build audit.
