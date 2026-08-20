# Changelog

## 0.1.9

- Added repository `.gitignore` coverage for Node dependencies, Wrangler local state, environment files, logs, Python caches and OS metadata.
- Pinned the production Worker to the dedicated OpenGLESScope Cloudflare `account_id` so an unrelated authenticated account cannot be used accidentally.
- Pinned the production D1 binding to the dedicated OpenGLESScope D1 UUID.
- Added Wrangler auth-profile helper scripts to `worker/package.json` for one-time profile creation/activation and normal status/deploy/migration workflows.
- Pinned Wrangler to 4.124.0 for reproducible local behavior matching the deployed environment.
- Updated the Worker health response to database version 0.1.9.
- Removed Python bytecode/cache artifacts from the release package.
- Frontend behavior, report schema, D1 schema, title behavior and logo assets are unchanged from 0.1.7.

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


## 0.1.9 UI parity
- Added semantic local SVG icons to every main navigation destination.
- Added compact icon-bearing custom filters with selected-option checkmarks and viewport-aware listboxes.
- Matched filter height, spacing, mobile layout, focus visibility, detail tabs, pagination and table-scroll affordances to the project quality baseline.
- Added Windows-safe fail-closed Cloudflare account verification before production D1 and deploy operations.
