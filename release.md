# OpenGLESScope Database 0.1.22

OpenGLESScope Database 0.1.22 is a full producer-contract, aggregate-semantics, UI-quality, security and VulkanScope Database parity release for OpenGLESScope 0.1.25.

## OpenGLESScope 0.1.25 compatibility

- Current producer audit target is OpenGLESScope 0.1.25 while the compatible floor remains 0.1.17+ within the schema-v2 / technicalReport-v1 line.
- Worker normalizer is version 5.
- Current 0.1.25 canonical TXT identity is cross-checked against structured application, GPU, driver, OpenGL ES, EGL and Android evidence.
- Current canonical report section counts must match the structured arrays for limits, extension scopes, runtime formats, shader precision, diagnostics and EGL configs.
- Application ABI and supported device ABI evidence remain read-time metadata derived only from canonical TXT when structured ABI fields are absent.
- 0.1.24 current-header reports and compatible 0.1.17 legacy-header reports remain accepted.

## Query-evidence contract

- Duplicate limit names, diagnostic names, runtime extension tokens, runtime format tokens, shader-precision keys and EGL config IDs are rejected for current 0.1.25 submissions.
- Every structured available limit must have a matching `Available` query diagnostic.
- Every structured shader-precision value must have a matching `Available` diagnostic.
- Non-empty extension or runtime-format enumerations require `Available` enumeration-query evidence.
- OpenGL ES 3.2 / `GL_KHR_debug` debug limits require their corresponding diagnostic evidence.
- `GL_EXT_disjoint_timer_query` reports require both timer query-counter-bit diagnostics introduced by OpenGLESScope 0.1.25.
- Missing evidence is not converted into unsupported capability.

## Aggregate correctness

- Extensions now distinguish successful enumeration with a token not listed from an unavailable enumeration query.
- Formats use the same evidence-aware semantics for compressed texture, shader binary and program binary enumerations.
- Limits aggregate only real GL implementation-limit queries and no longer mix GL/EGL identity or unrelated diagnostic records into the limit universe.
- Precision aggregates use every successfully loaded report as the denominator. Missing or failed precision queries remain Unavailable/Unknown evidence rather than disappearing from coverage.
- Diagnostics retain Available, Unavailable, Not applicable and Unknown as separate states.

## Reports and report detail

- Reports now include Driver identity alongside GPU, vendor, OpenGL ES, EGL, Android, application version and ABI metadata.
- Report-detail tabs expose category counts for Extensions, Limits, Formats, Precision, EGL Configs and Diagnostics.
- Report hero metrics expose submission time, short report ID, driver, OpenGL ES version, normalized-field count, extension count and schema.
- Extensions and Formats detail views show the authoritative enumeration diagnostic beside the runtime token list.
- Limits and Precision detail views combine available values with matching diagnostic state and diagnostic detail.
- Display & HDR exposes mode count, wide-color evidence and Android luminance metadata in the main aggregate table.

## Responsive and CSP-safe presentation

- The responsive table thumb continues to track the real horizontal scroll position and viewport/content ratio.
- Custom scrollbar geometry is represented through SVG attributes rather than inline style mutation.
- Coverage meters use semantic `<progress>` elements rather than CSP-sensitive inline width styles.
- Existing touch, trackpad, pointer drag, keyboard Arrow/Home/End, resize synchronization, edge shadows and reduced-motion behavior are preserved.

## VulkanScope Database parity

Every OpenGLESScope destination was compared with the corresponding interaction and evidence-quality floor in VulkanScope Database 0.35.8. Shared quality is aligned for Reports, runtime overview views, Extensions, Limits, Formats, report detail, Display/HDR, Diagnostics, Compare, navigation, search/filter/sort, responsive tables, error handling and Worker security. Vulkan-only categories such as Vulkan features/properties, memory, queues, WSI surface capabilities and Vulkan Profiles are intentionally not copied into an OpenGL ES/EGL database.

## Security and storage

- Exact schema shapes, 2 MiB streaming request bound, recursion bound and sensitive-key rejection remain enforced.
- CORS remains restricted to the configured GitHub Pages origin while native Android requests without an Origin header remain supported.
- Preflight responses now receive the same no-store, nosniff, frame-denial, opener/resource policy and deny-by-default CSP hardening as other API responses.
- Canonical SHA-256 report IDs and server-authored D1 submission timestamps remain unchanged.
- No D1 migration or stored-report rewrite is introduced.

## Specification provenance

- OpenGL ES: 3.2, specification dated May 5, 2022.
- GLSL ES: 3.20, specification dated August 14, 2023.
- EGL: 1.5, specification updated August 27, 2014.
- Registry provenance rechecked on 2026-08-21.
- Runtime extension tokens remain implementation-reported evidence and are never inferred from registry presence.

## Active assets

- JavaScript: `assets/app.v032.js`
- CSS: `assets/site.v032.css`
- Config cache key: `v=032`
