# OpenGLESScope Database 0.1.21

OpenGLESScope Database 0.1.21 is a platform-metadata, security, correctness and VulkanScope Database parity audit release.

## Report metadata
- Reports table now shows Android release/API and Platform / ABI.
- Report Summary now shows Android, Application ABI and Supported device ABIs.
- Report hero context, Compare and global search include the same platform evidence.
- Android values come from the structured `device` object.
- ABI values are derived read-time from the canonical TXT report for current 0.1.24 submissions because the current producer schema does not yet include ABI in the structured application object.
- Missing historical ABI evidence remains Unknown; it is never guessed from CPU/GPU/device names.
- Android-version sorting now uses the loaded authoritative report detail rather than nonexistent summary fields.

## Producer contract and safety
- Worker normalizer version is 4.
- Current OpenGLESScope 0.1.24 canonical TXT reports must match structured GPU, driver mode, OpenGL ES and Android identity.
- Current reports must contain bounded `Application ABI` and `Supported device ABIs` evidence.
- Current-header complete canonical TXT reports are required to be at least 1000 bytes; legacy compatibility headers retain their historical lower bound.
- Exact schema-shape validation, 2 MiB streaming request bounds, recursive sensitive-key rejection, SHA-256 canonical IDs, server-authored timestamps, CORS restriction, no-store/nosniff/no-referrer/frame denial and restrictive Permissions-Policy/CSP remain enforced.

## Khronos specification provenance
- Current OpenGL ES core specification: OpenGL ES 3.2.
- Current OpenGL ES shading-language specification: GLSL ES 3.20.
- Current EGL core specification: EGL 1.5.
- Worker health/list responses expose the published-spec provenance and the 2026-08-21 registry audit date.
- Runtime extension names remain report evidence, not inferred registry support.

## VulkanScope Database parity audit
Shared behavior was compared against VulkanScope Database 0.35.8. OpenGLESScope now matches the reference-quality behavior for bounded detail loading, report identity/platform presentation, global-search coverage, report sorting, responsive horizontal table controls, edge shadows, keyboard/pointer/touch scrolling, title semantics, error states, live API failure behavior, cache-busted JavaScript, hardened Worker responses and Cloudflare account/D1 pinning. Vulkan-only categories are intentionally not copied into an OpenGL ES/EGL database.

## Accessibility and motion
- Main-navigation and detail-tab scroll-into-view behavior now respects `prefers-reduced-motion`.
- Existing table keyboard, pointer, touch and trackpad behavior remains unchanged.

## Assets
- JavaScript: `assets/app.v031.js`
- CSS: `assets/site.v030.css` (unchanged)
- Config cache key: `v=031`

## Storage
No D1 migration and no stored-report rewrite are introduced by 0.1.21.
