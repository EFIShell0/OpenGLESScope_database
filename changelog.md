# Changelog

## 0.1.17

- Added official EGL branding to the EGL navigation destination, EGL view heading and report-detail EGL tab.
- Kept EGL Configs configuration-specific rather than misusing the EGL brand mark as a capability/state indicator.
- Added v027 cache-busted frontend assets.
- No D1, report-schema or report-semantic changes.

# 0.1.16

- Matched the VulkanScope Database hero information hierarchy with OpenGL ES-native wording.
- Renamed the hero to **OpenGL ES Hardware Database** and aligned its implementation-data description and search copy.
- Replaced the previous generic hero cards with **Reports**, **GPU models**, **OpenGL ES extensions**, **Normalized fields**, and **Producer/query baseline**.
- Added a server-authored OpenGLESScope/OpenGL ES/GLSL ES/EGL query baseline and retained bounded detail loading for aggregate metrics.
- Preserved report semantics, D1 schema, raw canonical report access, and the 0.1.15 report-detail interaction parity work.

# 0.1.15
- Matched VulkanScope report-detail tab animation, control geometry, keyboard behavior and Raw report presentation.
- Added v025 frontend cache busting without schema or D1 changes.

# 0.1.14

- Removed the Overview destination and made Reports the default/root database view.
- Matched VulkanScope Database report-list hierarchy and responsive toolbar behavior.
- Kept the report-index cursor batch at 500 rows and now follows all returned cursor pages without an arbitrary 200-page truncation cap.
- Added repeated-cursor detection so a broken pagination chain fails explicitly instead of silently presenting a partial database.
- Kept user-selectable visible page sizes at exactly 10, 25, and 50 rows with a hard 50-row maximum.
- Preserved deterministic filter/sort-before-pagination behavior and exact server-authored submission timestamps.
- Added v024 cache-busted frontend assets.
- No D1 migration or report-schema change.

# Changelog

## 0.1.13

- Report-index sort/per-page/date parity.
- View-specific state filters.
- Extension, format and precision subfilters.
- Display/HDR filter isolation.
- Coverage and footer visual parity.

## 0.1.11
- Added GPU vendor artwork parity and dominant-percentage coverage styling based on the VulkanScope Database reference.
- Preserved OpenGL ES/EGL runtime-evidence semantics.

## 0.1.10
- Added the full GitHub repository mark/icon treatment to the hero repository action.
- Matched repository-card geometry, hover treatment and chevron behavior to the reference-quality database UI.
- Prevented unintended root-level horizontal overflow while preserving intentional table and navigation scrolling.
- Tightened responsive hero and footer geometry.
- Preserved report semantics, Worker schema, D1 schema and Cloudflare account isolation.

## 0.1.10

- Added repository `.gitignore` coverage for Node dependencies, Wrangler local state, environment files, logs, Python caches and OS metadata.
- Pinned the production Worker to the dedicated OpenGLESScope Cloudflare `account_id` so an unrelated authenticated account cannot be used accidentally.
- Pinned the production D1 binding to the dedicated OpenGLESScope D1 UUID.
- Added Wrangler auth-profile helper scripts to `worker/package.json` for one-time profile creation/activation and normal status/deploy/migration workflows.
- Pinned Wrangler to 4.124.0 for reproducible local behavior matching the deployed environment.
- Updated the Worker health response to database version 0.1.10.
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


## 0.1.10 UI parity
- Added semantic local SVG icons to every main navigation destination.
- Added compact icon-bearing custom filters with selected-option checkmarks and viewport-aware listboxes.
- Matched filter height, spacing, mobile layout, focus visibility, detail tabs, pagination and table-scroll affordances to the project quality baseline.
- Added Windows-safe fail-closed Cloudflare account verification before production D1 and deploy operations.


## 0.1.13
- Matched Compare control density, GPU-name emphasis and differences-only control to the VulkanScope Database quality reference.
- Matched coverage bar/percentage hierarchy while preserving explicit OpenGL ES/EGL state labels and count denominators.
- Fixed diagnostic dominant-percentage coloring so only a unique maximum is emphasized and ties remain neutral.
- Added v022 cache-busted frontend assets.
