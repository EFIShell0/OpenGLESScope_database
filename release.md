# OpenGLESScope Database 0.2.4

OpenGLESScope Database 0.2.4 refines Compare state presentation so status badges communicate real capability/query semantics instead of simple field presence.

## Compare cleanup
- Removed redundant `Available` badges from ordinary metadata and scalar values such as application version, ABI, device identity, Android version/API, driver identity and GL/EGL version strings.
- Removed synthetic availability decoration from EGL Config scalar attributes, ordinary runtime-enumerant text and non-state Display/HDR scalar metadata.
- Missing evidence remains explicit `Unknown / Not reported`.
- Limits and shader precision now use their matching query-diagnostic state in Compare.
- Diagnostics retain their authoritative submitted state.
- Wide-color support and HDR-type availability retain semantic state badges because these values describe support/availability directly.
- `Differences only` and `Technical differences only` behavior from 0.2.3 is preserved.

## Compatibility
- Database: 0.2.4
- Normalizer: 8
- Current producer audit target: OpenGLESScope 0.2.2
- Submission schema: 2
- Technical report schema: 1
- No D1 migration or stored-report rewrite.
