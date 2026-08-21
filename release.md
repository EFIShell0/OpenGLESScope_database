# OpenGLESScope Database 0.1.26

OpenGLESScope Database 0.1.26 is a full-source correctness, security, specification and UI-parity audit with a focused fix for the remaining table-header and horizontal-scroll defects.

## Fixes
- Replaced the SVG custom table scrollbar track/thumb with the HTML track/thumb model used by VulkanScope Database 0.35.8.
- Maps native `scrollLeft` to the exact rendered track travel range and explicitly clamps the visual thumb to both endpoints.
- Keeps the native scrollbar visually hidden while preserving native touch, trackpad and keyboard scrolling.
- Applies VulkanScope-compatible neutral sticky table-header geometry, typography and `#151518` surface to every table, including Display/HDR and technical detail tables.
- Removed a CSS source comment and accidental literal escaped-newline sequence that violated `PROJECT_RULES.md` and caused the previous static audit to fail.
- Uses cache-busted `app.v036.js` and `site.v036.css`.

## Audit
- Rechecked OpenGL ES/EGL state semantics and structured/TXT compatibility behavior.
- Rechecked frontend escaping, CSP, same-origin asset policy, bounded API reads, timeout behavior and concurrency bounds.
- Rechecked Worker body/nesting bounds, sensitive-field rejection, report/cursor validation, parameterized D1 access, CORS and security headers.
- Rechecked production Cloudflare account and D1 pinning.
- Rechecked Khronos registries on 2026-08-21: OpenGL ES 3.2, GLSL ES 3.20 and EGL 1.5 remain the current core baselines.
- No D1 migration or report-schema change is introduced.

## Version separation
- Database: `0.1.26`
- Current producer audit target: OpenGLESScope `0.1.25`
- Compatible producer floor: OpenGLESScope `0.1.17+`
- Worker normalizer: `5`
