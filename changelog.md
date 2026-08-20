# Changelog

## 0.1.7

- Audited compatibility against OpenGLESScope 0.1.17 while retaining independent database versioning.
- Added application version and versionCode to server-side report summaries through a forward D1 migration.
- Hardened Worker validation for device, OpenGL ES, EGL, display, EGL config, diagnostic and report-text structure.
- Added cross-consistency checks between top-level runtime extension sets and the structured technical report.
- Raised Worker normalizer metadata to version 3.
- Added bounded and timeout-controlled frontend JSON materialization.
- Added active-navigation bring-into-view, navigation edge fades and mouse-wheel horizontal navigation.
- Added explicit newest/oldest ordering to Display & HDR evidence.
- Added state-semantic coverage visualization for implementation limits and diagnostics without coloring non-dominant containers as dominant evidence.
- Added report producer version visibility and global-search coverage.
- Improved failure-state presentation and retry flow.
- Added PNG, ICO and Apple touch icon cache-busted assets for the release.
- Preserved 50-row pagination, bounded concurrent detail fetching, exact comparison and raw canonical TXT access.

- Frontend canonical TXT compatibility fallback is retained for older stored reports when structured normalization is unavailable.


Branding/title parity in 0.1.7:
- The web header horizontal logo is copied directly from the OpenGLESScope application asset with identical bytes.
- Browser icons use the application GL|ES artwork centered on opaque black.
- Reports uses the base browser title; every other main destination prefixes its navigation label.
- Report detail titles use GPU name, active detail-tab label, then OpenGLESScope Database.
