# OpenGLESScope Database Engineering Rules

## Non-negotiable
- Third-party comparison product names are forbidden in every shipped filename, source file, generated artifact, test, audit, UI string, report, database field and metadata. Neutral capability-reference terminology must be used instead.
- Dedicated packaged app-store metadata directory bundles are forbidden from source release archives.
- Root release.md files are forbidden from source release archives; release notes, when needed, are distributed separately from the source ZIP.
- README.md files are forbidden from source release archives; release documentation must use purpose-specific audit, rules or changelog files.
- Source-code comments are forbidden.
- Security, correctness, memory safety, performance and usability are never traded away for convenience.
- No guessed OpenGL ES, EGL, display or HDR capability may be reported.
- Available, unavailable, not-applicable and unknown are distinct states.
- Runtime OpenGL ES and EGL extension names remain exactly as reported by the implementation.
- OpenGL ES version, GLSL ES version, EGL version and Android platform version remain distinct values.
- Android Display/HDR evidence is never reinterpreted as OpenGL ES/EGL capability.
- Every technical category present in a complete submitted report remains accessible in the database UI.
- Parsed or aggregate views never replace or discard the canonical TXT report.
- Aggregate statistics describe only reports actually loaded by the database and never imply global ecosystem coverage.
- Missing extension or runtime-format tokens are shown as not listed/unknown rather than inferred unsupported.
- A queried scalar value is available even when its value is zero or false unless the field is itself a support boolean.
- Query diagnostics are authoritative for Available, Unavailable and Not applicable state.
- The frontend has no third-party JavaScript, analytics, remote fonts, advertisements or remote presentation dependencies.
- Production frontend and Worker API use HTTPS.
- Content Security Policy allows only same-origin resources and the configured OpenGLESScope Worker API.
- Browser-visible assets that materially change use versioned filenames or equivalent cache busting.
- Frontend detail fetching is concurrency-bounded.
- Reports pagination renders no more than 50 rows per page after sorting/filtering.
- Submission time shown by the UI comes only from server-side D1 submitted_at and retains the exact ISO timestamp.
- Device/display data stays private unless the user explicitly submits a complete report.
- Submission excludes personal identifiers, account/authentication data, request IP addresses and private paths.
- No automatic/background report upload exists.

## Submission and Worker
- Application identity is OpenGLESScope with package com.efishell.openglesscope.
- Application and database versions are independent. New report POST requires exactly OpenGLESScope 2.2.22, versionCode 2222, schema 2, technicalReport schema 5; older and future producers are forbidden from submitting. Earlier canonical reports remain read-only and must never be deleted, recast, or hidden. Database release version is independent of producer version.
- Public web URL is https://efishell0.github.io/OpenGLESScope_database/.
- API base is https://openglesscope-database-api.openglesscope.workers.dev.
- Request body is bounded to 2 MiB and is never truncated.
- Complete reports are all-or-nothing submissions.
- Stored report IDs are SHA-256 hashes of stable canonical JSON.
- Pagination uses server-authored submitted_at/id ordering and the submitted_at/id database index.
- Stored payloads remain canonical; compatibility normalization is applied on read when structured technical data is unavailable, so parser fixes do not require rewriting D1 rows.
- The frontend retains a canonical TXT compatibility fallback when structured normalization is unavailable, without inventing state semantics.
- Worker response bodies use no-store, nosniff, no-referrer, restrictive Permissions-Policy and frame denial headers.
- CORS is restricted to the configured GitHub Pages origin.
- Unsupported methods return 405 with an Allow header.
- Recursive submission inspection rejects sensitive field names and excessive nesting.

## Frontend
- Main navigation, report tables and comparison controls are keyboard accessible.
- Long navigation and tables provide horizontal overflow controls and preserve touch/trackpad scrolling.
- Reduced-motion preference disables nonessential transitions.
- Global search covers GPU, vendor, device, driver, OpenGL ES, EGL and loaded technical report fields without scanning or executing raw report text as markup.
- Vendor, GPU and OpenGL ES version filters operate before 50-row pagination.
- Report detail tabs remain visible even when the selected category is empty.
- Detail tabs include Overview, OpenGL ES, EGL, Extensions, Limits, Formats, Precision, EGL Configs, Display/HDR, Diagnostics and Raw report.
- Extension aggregates distinguish reported from not listed; not listed is not mislabeled unsupported.
- Limit and diagnostic aggregates preserve Available, Unavailable, Not applicable and Unknown semantics.
- Compare uses exact report values and does not synthesize missing values.
- HDR artwork is local and used only when the Android-reported HDR type matches known bundled artwork. Unknown HDR names remain text.
- document.title follows the active database destination using the same destination semantics as the reference database: Reports uses the base title, every other main destination prefixes its visible label, and report detail prefixes GPU name plus the active detail-tab label.
- The database header uses the exact application horizontal logo asset. Browser icon assets use the application GL|ES artwork centered in white on an opaque black square; no alternative logo geometry is invented.

## OpenGLESScope 0.1.17 compatibility floor
- Schema version 2 and technicalReport schema version 1 are accepted.
- technicalReport includes limits, OpenGL ES extensions, EGL display extensions, EGL client extensions, compressed formats, shader binary formats, program binary formats, shader precision, query diagnostics, EGL configs and display evidence.
- EGL config presentation preserves every attribute currently emitted by OpenGLESScope 0.1.17.
- Display presentation preserves current mode ID, resolution, refresh rate, supported modes, wide-color evidence, HDR type list and Android-provided luminance metadata.
- Query diagnostics are preserved in structured detail, aggregate views and raw canonical report access.

## OpenGLESScope 0.1.17 compatibility additions
- Compatible submissions retain schema version 2 and technicalReport schema version 1.
- Application version/versionCode are preserved in report detail and server-side summary metadata.
- Runtime extension counts must exactly match the submitted runtime extension arrays, and duplicated technical-report extension sets must match their corresponding top-level sets.
- Nested EGL configuration and Android display evidence are type-validated rather than accepted solely by object presence.
- The canonical TXT snapshot must identify the same producer version and contain the core OpenGL ES, EGL, diagnostics and EGL-config sections.

## Release 0.1.7
- Database version is 0.1.7.
- Database version remains intentionally independent from the OpenGLESScope application version.
- Primary UI accent remains the official OpenGL ES brand tone #BA2A8D.
- Frontend API JSON materialization is capped at 4 MiB per response and timeout-bounded.
- Report summary metadata includes application version and versionCode for newly stored reports.
- Display/HDR evidence supports explicit newest/oldest ordering without changing server-authored submission timestamps.
- State-semantic coverage uses colored progress fills; non-dominant coverage containers remain neutral and only a uniquely dominant state receives additional emphasis.
- Active horizontal navigation remains visible through edge affordances and bring-into-view behavior.
- Release assets use v017 cache-busted filenames.


## Release 0.1.8
- Database version is 0.1.8.
- Production Wrangler configuration pins Cloudflare account ID 6881527e6e0b9bc4a0c009473428d1bc and D1 database ID 2c945dda-e320-4b3a-9fac-a086373db17c.
- The `openglesscope` Wrangler auth profile is directory-local operational state and is never committed.
- The committed account ID is mandatory fail-closed protection against deployment to an unrelated authenticated Cloudflare account.
- Repository ignore rules exclude node_modules, Wrangler local state, environment/secret files, logs, Python caches and OS metadata.
- `node_modules` is never committed. A locally generated package-lock may be committed for reproducibility.
- Wrangler is pinned to 4.124.0 for this release.
- No D1 schema migration is introduced by 0.1.8.
- Frontend cache-busted assets remain v017 because their bytes and behavior are unchanged.


## Release 0.1.10
- Database version is 0.1.10.
- Every main navigation destination has a local semantic SVG icon in addition to its text label; text remains authoritative and icons are presentation-only.
- Top-level custom filters use the same compact control geometry as the quality reference: 36 px minimum control height, 34 px option height, compact 14 px local semantic icons and selected-option checkmarks.
- Filter iconography is local SVG path data with no remote dependency and never changes report semantics.
- Filter listboxes retain the hidden native select as authoritative state and support keyboard, mouse and touch input, Home/End navigation, Escape close and viewport-aware drop-up behavior.
- Mobile filters use a responsive two-column layout and collapse to one column on narrow displays.
- Navigation, detail tabs, pagination, table scrolling, focus-visible indication and reduced-motion behavior are audited together so presentation parity cannot regress one input modality.
- OpenGL ES/EGL terminology and Available/Unavailable/Not applicable/Unknown semantics remain unchanged by visual parity work.
- Production Cloudflare account and D1 identity remain pinned to the OpenGLESScope account and database.


## Release 0.1.10
- Database version is 0.1.10.
- The hero repository card uses a local inline GitHub mark, dedicated icon container and chevron while retaining authoritative text and accessible labeling.
- Root document horizontal overflow is prohibited; only intentional navigation/table containers may scroll horizontally.
- Footer geometry follows the reference-quality compact footer without creating a page-level horizontal scrollbar.
- Hero copy and repository action remain responsive and collapse vertically on narrow layouts.
- Existing navigation/filter iconography, keyboard behavior, report semantics, account pinning and D1 identity remain unchanged.


## Release 0.1.11 GPU artwork and coverage parity
- Database version is 0.1.11.
- Report-backed GPU rows use only bundled local vendor artwork selected from submitted GL vendor/renderer text; artwork is presentation-only and never creates capability evidence.
- Unknown or unmapped vendors retain submitted text unchanged and use the bundled unknown artwork.
- Recent reports, Reports, EGL Configs and report-detail hero expose GPU artwork at the same compact presentation quality as the reference database.
- Coverage progress fills always retain semantic state colors. Percentage text receives semantic color only for the unique dominant state in the same distribution; tied highest and non-dominant percentages remain neutral.
- Extension and runtime-format absence remains Not listed/Unknown evidence and is never converted to Unsupported.
- Visual parity work must not alter counts, denominators, filters, report schema, D1 contents or OpenGL ES/EGL state semantics.


## Release 0.1.12 Compare and coverage parity
- Database version is 0.1.12.
- Compare report selectors emphasize the submitted GPU name with the same bold hierarchy as the VulkanScope Database quality reference while keeping device/model tail text secondary.
- The GPU filter uses the same bold GPU-name hierarchy without changing its native-select authoritative value.
- Compare uses the compact custom differences-only checkbox, summary metrics, section density, table spacing and responsive picker geometry used by the quality reference.
- Coverage meters use the same compact bar-plus-percentage visual hierarchy as the quality reference while preserving explicit OpenGLESScope labels and visible count/denominator evidence.
- Coverage fill color always follows the semantic state. Percentage text receives semantic color only when that state is the unique numerical maximum within the same distribution; ties remain neutral.
- Diagnostic coverage uses the same unique-dominant rule as extension, limit and format coverage; tied maxima never receive dominant emphasis.
- Compare and coverage parity must not change report values, counts, denominators, filtering, OpenGL ES/EGL evidence semantics, D1 schema or stored payloads.
- Browser-visible frontend assets changed by this release use v022 cache-busted filenames.


## Release 0.1.13 filter, report-index and footer parity
- Database version is 0.1.13.
- Reports use the same compact sort/per-page toolbar hierarchy as the VulkanScope Database quality reference, with submission timestamp first, deterministic sorting and no more than 50 rendered rows per page.
- Submission timestamps remain server-authored D1 values and are rendered through a locale-aware formatter that includes date, time, seconds and time-zone information; sorting continues to use the exact timestamp value.
- Top-level status options are view-specific and expose only states that the corresponding OpenGL ES/EGL evidence can justify. Extensions and runtime formats expose Reported/Not listed rather than inventing Unsupported. Limits and diagnostics preserve Available/Unavailable/Not applicable/Unknown. Display exposes only availability of submitted display evidence.
- Display/HDR hides vendor, GPU and OpenGL ES-version filters because Android display evidence is a separate evidence domain; hidden stale graphics filters must not suppress Display/HDR rows.
- Extensions expose an Extension scope selector for OpenGL ES, EGL display and EGL client tokens. Formats expose a runtime-format family selector. Precision exposes a shader-stage selector. These controls are presentation/filtering only and never alter normalized report data.
- Coverage geometry, neutral non-dominant treatment and unique-dominant percentage coloring follow the VulkanScope Database quality reference while retaining the additional OpenGLESScope Not applicable state.
- The footer has the same compact top divider and 72 px alignment geometry as the quality reference and must not create page-level horizontal overflow.
- Browser-visible frontend assets changed by this release use v023 cache-busted filenames.

## Release 0.1.14 Reports-as-home parity
- Database version is 0.1.14.
- The Overview destination is removed from primary navigation. Reports is the first destination and the default database home view for the root URL, invalid/empty hashes and Back/Forward restoration.
- Reports uses the same listing hierarchy as the VulkanScope Database quality reference: server-authored Submitted timestamp first, bold GPU name with secondary device text, local GPU artwork, runtime/vendor/version metadata and report ID remain visible without collapsing technical identity.
- The report index API fetch batch is explicitly 500 rows per cursor page. The frontend follows every returned cursor page until the server returns no next cursor; a repeated cursor is an explicit error rather than a silent partial listing.
- Report rendering remains independently bounded to at most 50 rows per visible page. The user-facing Per page selector offers exactly 10, 25 and 50 rows, defaults to 25, and applies after search/filter/sort so page boundaries remain deterministic.
- Reports sorting retains submission newest/oldest, OpenGL ES newest/oldest, EGL newest/oldest, GPU A/Z, vendor A/Z, Android version newest/oldest and OpenGLESScope version newest/oldest options.
- The report toolbar, range indicator, pagination buttons and responsive mobile layout follow the same density and interaction quality as the VulkanScope Database reference while preserving OpenGLESScope terminology.
- Reports remains the bare browser title `OpenGLESScope Database`; other main destinations continue to prefix their visible destination label.
- Removing Overview is presentation/navigation only and must not alter normalized report data, D1 schema, capability-state semantics, filtering evidence, report-detail access or raw canonical TXT access.
- Browser-visible changed frontend assets use v024 cache-busted filenames.



## Release 0.1.15 report-detail interaction parity
- Database version is 0.1.15.
- Report-detail tabs use the VulkanScope Database reference geometry: 8 px gap, 7 px tab-strip padding, 7 px by 8 px tab-button padding, 12 px text and 750 font weight.
- Report-detail tab changes preserve one persistent detail body and use a 105 ms exit plus 180 ms entrance transition with the reference easing curves.
- Active detail tabs use roving tabindex, ARIA tab state, keyboard Arrow/Home/End navigation and scroll-into-view behavior.
- Reduced-motion preference disables nonessential detail-tab transitions.
- Raw report uses a contained 12 px / 1.55 monospace presentation, 16 px padding, 16 px radius, 68 vh maximum height and internal scrolling.
- OpenGL ES branding and capability semantics remain authoritative; Vulkan-specific terminology or driver semantics are not introduced.
- No D1 schema migration or report-payload rewrite is introduced.
- Browser-visible changed frontend assets use v025 cache-busted filenames.


## Release 0.1.16 hero information parity
- Database version is 0.1.16.
- The hero follows the VulkanScope Database information hierarchy while preserving OpenGL ES terminology: eyebrow `OPENGL ES CAPABILITY INTELLIGENCE`, title `OpenGL ES Hardware Database`, and the deep report-backed implementation description.
- Hero search copy follows the compact reference wording but only names query domains actually present in OpenGLESScope data.
- The five hero metrics are Reports, GPU models, OpenGL ES extensions, Normalized fields and Producer/query baseline. Vulkan-specific `Device extensions` terminology is forbidden.
- GPU models are counted from report summaries; OpenGL ES extensions are unique exact runtime tokens from loaded canonical report detail; normalized fields count primitive values in the normalized technical-report view without inventing missing data.
- Producer/query baseline is server-authored by the health endpoint and states the OpenGLESScope/OpenGL ES/GLSL ES/EGL query baseline.
- Hero metric population may fetch report detail only through the existing concurrency-bounded detail loader; no unbounded fetch fan-out is introduced.
- Existing Available, Unavailable, Not applicable and Unknown semantics, D1 schema, canonical TXT access, report-detail behavior and OpenGL ES branding remain unchanged.
- Browser-visible changed frontend assets use v026 cache-busted filenames.

## Release 0.1.17 EGL branding
- Database version is 0.1.17.
- The official bundled EGL logo asset is used wherever the database presents the EGL runtime destination as branded navigation: the primary EGL navigation button, the EGL main-view heading and the report-detail EGL tab.
- EGL Configs remains a distinct technical configuration destination and keeps its semantic configuration icon; the official EGL brand mark is not used to imply that configuration enumeration is a separate EGL product or capability.
- EGL logo presentation is local-only, transparent-background, aspect-ratio preserving and sized to the same compact visual hierarchy as the existing navigation and detail-tab artwork.
- Text labels remain authoritative for accessibility and navigation semantics; the EGL artwork is decorative and uses empty alternative text.
- EGL branding changes are presentation-only and must not alter report values, extension/config evidence, filters, counts, D1 schema, stored payloads or canonical TXT data.
- Browser-visible frontend assets changed by this release use v027 cache-busted filenames.


## Release 0.1.18 OpenGL ES and EGL brand-mark parity
- Database version is 0.1.18.
- Every branded EGL runtime surface uses the bundled official EGL silhouette rendered as a white monochrome mark on the dark database UI; the previous red EGL presentation is forbidden.
- The OpenGL ES runtime destination uses the exact bundled white `GL|ES` artwork from the OpenGLESScope application rather than a generic OpenGL ES glyph.
- Brand marks are used consistently in the primary navigation, corresponding main-view heading, report-detail tab button and matching runtime section heading.
- EGL Configs remains a separate technical configuration destination and retains its semantic configuration icon rather than the EGL product mark.
- Brand artwork is local-only, keeps its source aspect ratio, is decorative for accessibility, and never replaces the authoritative visible text label.
- Branding changes are presentation-only and must not alter OpenGL ES/EGL evidence, counts, filters, report payloads, canonical TXT data, D1 schema or stored records.
- Browser-visible changed frontend assets use v028 cache-busted filenames.

## Release 0.1.19 full database audit and hardening
- Database version is 0.1.19 and the compatibility floor remains OpenGLESScope 0.1.17 with schema version 2 and technicalReport schema version 1.
- The current OpenGLESScope TXT header beginning with `OpenGLESScope report` is accepted and cross-checked against structured application version, versionCode and package identity; the legacy `OpenGLESScope <version>` header remains accepted for compatible 0.1.17+ stored/submitted reports.
- Submission objects use exact schema shapes. Unknown top-level or nested JSON fields are rejected rather than silently persisted.
- Sensitive field-name canonicalization removes separators and punctuation before matching, so forms such as `user_id`, `account-id` and `access.token` cannot bypass the forbidden-identifier guard.
- Query diagnostic status is restricted to Available, Unavailable, Not applicable and Unknown.
- Top-level and technicalReport display objects must be complete and exactly equivalent; duplicated display evidence is not allowed to disagree.
- Structured technicalReport detail responses are not duplicated into a second normalized copy. Worker normalization is materialized only as a compatibility fallback when structured technicalReport data is absent.
- A live API failure is an explicit unavailable/error state. An empty static index must never be used to make an API outage appear to be a valid zero-report database.
- Failed detail loads are surfaced through a visible report-load-failure metric; aggregate results describe only successfully loaded reports.
- Global search includes loaded application, device, GPU, driver, OpenGL ES, EGL and normalized technical fields in addition to summary metadata.
- Limit aggregates use query diagnostics as authoritative state evidence, use every successfully loaded report in the denominator and count missing query evidence as Unknown. A value is shown in aggregate value distribution only when the authoritative state is Available.
- Diagnostic aggregates use every successfully loaded report in the denominator and count absent diagnostic evidence as Unknown.
- An explicitly reported empty Android HDR type list is Unavailable, not Unknown and never Unsupported. A missing/non-array HDR list remains Unknown.
- Display/HDR state filtering exposes Available, Unavailable and Unknown only; it does not invent OpenGL ES/EGL support semantics from Android display evidence.
- Main-view transitions use cancellation, `aria-busy`, GPU-friendly transforms and reduced-motion handling consistent with report-detail transition quality.
- The parsed OpenGL ES core version is rendered canonically as `<major>.<minor>` with no presentation separator error.
- Repeated report-detail membership checks use report-ID sets rather than quadratic scans on OpenGL ES/EGL overview aggregation.
- Worker contract tests cover current 0.1.23 submission compatibility, legacy 0.1.17 header compatibility, schema-floor rejection, exact-object rejection, duplicated-display consistency, diagnostic-state validation, media type validation, CORS, report ID validation, 405 Allow behavior and the 2 MiB streamed-body bound.
- No D1 schema migration is introduced by 0.1.19; existing D1 rows remain unchanged.
- Browser-visible changed JavaScript uses `app.v029.js`; unchanged current CSS remains `site.v028.css`; the white EGL artwork uses `egl-logo-white-v029.png` generated from the current application EGL asset while preserving its alpha geometry exactly.
- GitHub Pages deployment uses a separate validated build job, runs the static-index validator and full repository audit before artifact upload, uses the current Pages action family, and does not cancel an in-progress production Pages deployment.


## Release 0.1.20 responsive table interaction parity
- Database version is 0.1.20.
- Every horizontally overflowing report, aggregate, compare and detail table uses one synchronized horizontal-scroll state for native scrolling, arrow controls, the custom track/thumb and edge affordances.
- The custom table thumb position must reflect the actual horizontal table offset and its width must reflect the visible fraction of table content. A decorative fixed thumb is forbidden.
- The table-scroll track supports pointer dragging and keyboard Left/Right Arrow, Home and End operation.
- Left and right table edge shadows are derived from actual hidden content and animate only as a presentation affordance; they never cover or change report semantics.
- Custom table controls are hidden when the table does not horizontally overflow.
- Dynamically rendered report-detail tables receive the same scrolling behavior as main-view tables and no table is enhanced more than once.
- Resize changes recalculate scrollbar geometry, overflow state, button state and edge-shadow state.
- Reduced-motion preference disables nonessential table-edge/thumb/button transitions while preserving immediate scrolling and keyboard operation.
- OpenGL ES, EGL, Display/HDR, query-diagnostic, aggregate, compare, canonical TXT and submission semantics are unchanged by this UI release.
- No D1 schema migration or stored-report rewrite is introduced.
- Browser-visible changed frontend assets use v030 cache-busted filenames.


## Release 0.1.21 platform metadata and full parity audit
- Database version is 0.1.21.
- Reports, Summary, Compare and global search expose Android release/API, application ABI and supported device ABIs when evidence exists.
- Android release/API is authoritative from the structured device object.
- For current schema-v2 producers that do not structurally carry ABI, application ABI and supported device ABIs may be derived only from exact canonical TXT header lines; missing evidence is Unknown and is never inferred from hardware identity.
- Android-version sorting uses loaded authoritative report detail and must not depend on nonexistent summary columns.
- Current OpenGLESScope 0.1.24 canonical TXT identity lines are cross-checked against structured GPU, driver mode, OpenGL ES and Android identity, and bounded ABI evidence is required for 0.1.24+ current-header submissions.
- Current-header complete canonical TXT reports use a 1000-byte minimum; the legacy 0.1.17+ compatibility header retains its historical lower bound.
- Worker normalizer version is 4 and derived runtime metadata never mutates the stored canonical payload.
- Published specification provenance is OpenGL ES 3.2 (May 5, 2022), GLSL ES 3.20 (August 14, 2023) and EGL 1.5 (August 27, 2014), audited against the Khronos registries on 2026-08-21.
- Runtime extension tokens remain implementation-reported evidence and are never inferred from registry presence.
- Shared frontend, Worker, security, error, responsive-table, keyboard, reduced-motion, title, pagination and Cloudflare deployment behavior is audited against VulkanScope Database 0.35.8; Vulkan-only technical categories are not copied into OpenGLESScope.
- Main-navigation and detail-tab bring-into-view scrolling honors reduced-motion preference.
- No D1 schema migration or stored-report rewrite is introduced.
- Browser-visible changed JavaScript uses `app.v031.js`; unchanged CSS remains `site.v030.css`.

## Release 0.1.22 OpenGLESScope 0.1.25 and full tab parity audit
- Database version is 0.1.22 and the compatible producer floor remains OpenGLESScope 0.1.17+ with submission schema 2 and technicalReport schema 1.
- OpenGLESScope 0.1.25 is the current producer audit target and Worker normalizer version is 5.
- Current 0.1.25 canonical TXT identity must agree with structured application, GPU, driver, OpenGL ES, EGL and Android evidence, and canonical technical-section counts must agree with structured array lengths.
- Current-producer limit names, diagnostic names, runtime extension tokens, runtime-format tokens, shader-precision keys and EGL config IDs are duplicate-free.
- Every available structured limit and shader-precision value has matching Available query-diagnostic evidence.
- Non-empty OpenGL ES/EGL extension and runtime-format enumerations require Available enumeration-query evidence; an unavailable enumeration is never translated to Not listed or Unsupported.
- OpenGL ES 3.2 or GL_KHR_debug evidence requires the debug-limit diagnostics emitted by the producer. GL_EXT_disjoint_timer_query evidence requires both query-counter-bit diagnostics emitted by OpenGLESScope 0.1.25.
- Reports expose Driver alongside GPU/vendor/OpenGL ES/EGL/Android/application/ABI identity and preserve deterministic sort/filter/pagination behavior.
- Extensions, Limits, Formats and Precision aggregate every successfully loaded report with diagnostic-authoritative Available, Unavailable, Not applicable and Unknown semantics where applicable.
- Limits aggregates contain actual GL implementation-limit query names only; GL/EGL identity, enumeration and shader-precision diagnostic names do not contaminate the limit universe.
- Report-detail tabs expose natural category counts and retain query evidence next to Extensions, Formats, Limits and Precision values.
- Display/HDR exposes current mode, refresh, supported-mode count, wide-color evidence, HDR types and Android luminance metadata without reinterpreting those fields as GL/EGL capability.
- Coverage meters and custom horizontal-scroll geometry use CSP-safe primitives and retain the 0.1.20 synchronized pointer/keyboard/touch/trackpad/resize/edge-shadow contract.
- CORS preflight responses receive the normal hardened API response headers.
- Shared Reports, OpenGL ES/EGL overview, Extensions, Limits, Formats, report detail, Display/HDR, Diagnostics, Compare, responsive, title, search/filter/sort, error and Worker-security behavior is audited against VulkanScope Database 0.35.8; Vulkan-specific categories are not copied into OpenGLESScope.
- No D1 migration or stored-report rewrite is introduced.
- Browser-visible changed frontend assets use `app.v032.js` and `site.v032.css`; config cache key is `v=032`.


## Release 0.1.23 Reports table visual parity
- Database version is 0.1.23.
- The Reports table labels its GPU/device identity column Device, matching the VulkanScope Database reference without changing the underlying GPU/device evidence.
- Complete OpenGL ES and EGL runtime version strings are rendered in compact version chips matching VulkanScope API-version geometry.
- Reports version chips remain single-line; long values use the existing synchronized horizontal table overflow path rather than vertical character wrapping.
- Reports table header color, size and weight match the VulkanScope Database 0.35.8 reference.
- Report ID values match the VulkanScope monospace size and normal font weight.
- These are presentation-only changes. OpenGL ES, EGL, Display/HDR, query diagnostics, complete-report gating, filtering, sorting, pagination, canonical TXT access, Worker validation and submission semantics remain unchanged.
- No D1 schema migration or stored-report rewrite is introduced.
- Browser-visible changed frontend assets use `app.v033.js` and `site.v033.css`; config cache key is `v=033`.

## Release 0.1.24 navigation, filters, HDR units and table-scroll parity
- Database version is 0.1.24.
- The main navigation control geometry matches the VulkanScope Database 0.35.8 reference while retaining OpenGLESScope branding and OpenGL ES/EGL semantics.
- Reports toolbar custom-select geometry matches the VulkanScope Database 0.35.8 reference.
- Reports Driver mode text remains single-line where the reference presentation keeps the corresponding system-driver label intact; table overflow is handled horizontally rather than breaking that label.
- Android Display/HDR luminance values show the physical unit cd/m² when a luminance value is available; unavailable evidence remains unavailable and no value is inferred.
- Horizontally overflowing tables expose one custom synchronized horizontal scrollbar; the native table scrollbar is visually hidden while touch, trackpad, wheel and programmatic horizontal scrolling remain functional.
- Browser-visible changed frontend assets use v034 cache-busted filenames.
- No report schema, Worker normalization, D1 schema, capability semantics or canonical report evidence is changed by this release.


## Release 0.1.25 VulkanScope presentation parity
- Database version is 0.1.25.
- Table header typography, weight, sizing, sticky behavior and surface treatment use the VulkanScope Database table-header geometry across all database tables.
- Reports vendor presentation may add a UI-only canonical vendor/family identifier such as `Qualcomm / Adreno (0x5143)` when the runtime GL vendor/renderer text unambiguously matches the maintained display mapping. This is presentation metadata only: it must not be stored as queried OpenGL ES evidence, used to infer capabilities, or alter the submitted report.
- OpenGL ES and EGL version chips keep VulkanScope geometry while using the OpenGLESScope magenta interface accent family.
- The synchronized horizontal scrollbar thumb must clamp exactly to the beginning and end of its track when the underlying table is at its minimum or maximum horizontal scroll position.
- Browser-visible changed frontend assets use cache-busted `site.v035.css` and `app.v035.js`.

## Release 0.1.26 full UI, security and specification audit
- Database version is 0.1.26 and remains independent from the current OpenGLESScope producer version, which remains 0.1.25 for this database release.
- Every database table uses the same neutral sticky header geometry as the VulkanScope reference: 12 px header text, the reference header foreground, the reference `#151518` header surface and consistent cell geometry across Reports, Display/HDR, OpenGL ES, EGL and all other tabular destinations.
- The custom horizontal table scrollbar uses a real HTML track and thumb. Thumb width is derived from `clientWidth / scrollWidth`, thumb travel is derived from the exact track width minus thumb width, and the thumb is explicitly clamped to the track start/end when the table is at its left/right boundary.
- Native table scrollbars remain visually hidden while touch, trackpad, wheel-with-Shift, keyboard, pointer dragging and edge buttons retain access to the same native scroll position.
- OpenGL ES 3.2, GLSL ES 3.20 and EGL 1.5 remain the current Khronos core specification baselines. Published specification dates remain OpenGL ES 3.2 May 5 2022, GLSL ES 3.20 August 14 2023 and EGL 1.5 August 27 2014.
- Runtime OpenGL ES, GLSL ES and EGL version strings remain implementation evidence and are never rewritten to match the engineering baseline.
- Vendor IDs, GPU names and display metadata remain presentation/index data and are never promoted into unsupported capability inference.
- Frontend rendering remains escaped/same-origin, CSP-restricted and free of third-party script, analytics, remote font and remote presentation dependencies.
- Worker request bounds, recursive sensitive-field rejection, parameterized D1 access, strict report-ID/cursor validation, CORS restriction, no-store/nosniff/no-referrer/frame denial/Permissions-Policy protections and fail-closed Cloudflare account pinning remain mandatory.
- Browser-visible changed frontend assets use v036 cache-busted filenames.


## Release 0.2.0
- Database version is 0.2.0 and remains independent from the OpenGLESScope application version.
- Current validated producer is OpenGLESScope 0.2.1 with versionCode 201.
- Producer parsing is semantic across compatible 0.x releases instead of being hard-coded to 0.1.x patch versions.
- The compatibility floor remains OpenGLESScope 0.1.17; major-version 1.x and malformed/prerelease producer strings are rejected until a future schema compatibility decision is made explicitly.
- OpenGLESScope 0.2.1 submissions must retain schema version 2, technicalReport schema version 1, complete structured/TXT parity, current ABI metadata, runtime identity evidence, enumeration counts and query diagnostics.
- For OpenGLESScope 0.2.1 and newer compatible 0.x producers, Android desired maximum, maximum-average and minimum luminance values in canonical TXT evidence must either be Unavailable or include the cd/m² unit and numerically match structured display evidence.
- Display/HDR luminance values remain Android-reported metadata and are never reinterpreted as measured panel luminance or OpenGL ES capability.
- Current Khronos registry baselines remain OpenGL ES 3.2, GLSL ES 3.20 and EGL 1.5; registry audit date is 2026-08-21.
- Frontend health/metrics expose the compatible-producer contract so a producer-version rejection is diagnosable instead of appearing as an unexplained generic schema failure.
- Superseded JavaScript and CSS release assets are removed from the packaged release after reference validation; only browser-referenced current assets remain.
- Existing HTTPS, CORS, CSP, body-size, nesting-depth, sensitive-field, D1 identity, pagination, canonical hashing and no-background-upload protections remain mandatory.


## Release 0.2.1 Android security-patch Reports parity
- Database version is 0.2.1 and remains independent from the OpenGLESScope application version.
- The Reports Android column uses the VulkanScope presentation contract: the Android release/SDK remains the primary value and an available Android security patch is rendered directly below as `Patch YYYY-MM-DD` using the existing `table-sub` typography.
- Android security-patch evidence is optional for backwards compatibility. Reports that did not submit a security patch remain without a patch subline; the Database must never infer, synthesize or guess a patch level from Android release, SDK, GPU, device model or submission date.
- Submission schema 2 may carry optional `device.securityPatch` in canonical `YYYY-MM-DD` form. Existing schema-2 producers without the field remain valid.
- Runtime metadata may also recover an explicitly reported `Android security patch` or `Security patch` TXT line, but only as display metadata; conflicting or malformed submitted structured fields are rejected rather than normalized into fabricated evidence.
- Security-patch data is device/platform metadata only and must not affect OpenGL ES, EGL, Display/HDR or extension capability inference.
- Existing report-ID hashing, body-size bounds, sensitive-field rejection, CORS/CSP/security headers, D1 identity pinning, pagination and no-background-upload behavior remain unchanged.
- Browser-visible changed JavaScript uses `app.v038.js`; unchanged CSS remains `site.v036.css`; config cache key is `v=038`.


## Release 0.2.2 Android security-patch producer enforcement
- Database version is 0.2.2 and current validated producer is OpenGLESScope 0.2.2 with versionCode 202.
- OpenGLESScope 0.2.2 and newer compatible producers must submit canonical `device.securityPatch` in `YYYY-MM-DD` form and matching canonical TXT lines `Android security patch:` and `Security patch:`.
- Older compatible reports remain backward compatible and are not assigned fabricated patch evidence.
- Reports renders explicit patch evidence as `Patch YYYY-MM-DD` beneath Android release/SDK using the established VulkanScope parity treatment.
- Patch metadata is Android platform evidence only and never participates in graphics capability inference.
- Existing schema, canonical hashing, report-size bounds, recursive sensitive-field rejection, CORS/CSP/security headers, D1 parameterization and origin restrictions remain mandatory.


## Release 0.2.3 technical-differences compare filter
- Compare retains `Differences only` and adds `Technical differences only` with the same existing compare-toggle geometry, interaction and brand-state treatment.
- `Technical differences only` is enabled by default and removes producer/report-generation metadata noise while retaining graphics, Android platform and implementation evidence.
- Application version/versionCode and Collection status/complete/source are non-technical Compare metadata. Application ABI and supported-device ABI are technical platform evidence and remain visible.
- Device manufacturer/model/product, Android release/API/security patch, driver mode/version, GL/EGL identity, extensions, limits, formats, precision, EGL Configs, diagnostics and Display/HDR evidence remain technical.
- Filtering is presentation-only and must not mutate schema 2, technical report 1, stored payloads, report text, SHA-256 report identity or Worker normalization.
- Compare A/B field counts, difference count and section count follow the active technical field universe.

## Release 0.2.4 Compare semantic-state cleanup
- Database version is 0.2.4 and remains independent from the OpenGLESScope producer version.
- Compare does not decorate ordinary identity, metadata or scalar values with an Available badge merely because a value exists.
- Application version/versionCode, ABI strings, device identity, Android release/API, driver identity, GL/EGL identity, EGL Config scalar attributes, runtime enumerant text and ordinary Display/HDR scalar metadata render as values without synthetic availability decoration.
- Missing Compare-side evidence remains explicit Unknown / Not reported and is never silently replaced with an empty value.
- Query-diagnostic state remains authoritative and visible for Limits, Shader precision and Diagnostics rows.
- Display/HDR support-state fields retain semantic badges where the field itself represents support or availability, including wide-color support and HDR-type availability.
- Compare status badges therefore communicate actual support/query/availability semantics rather than simple object presence.
- Technical differences filtering from 0.2.3 remains presentation-only and its field/difference/section counts continue to follow the active field universe.
- No report schema, Worker normalizer, stored payload, canonical TXT, SHA-256 report identity, D1 schema or capability inference changes are introduced.
- Browser-visible changed JavaScript uses `app.v041.js`; unchanged CSS remains `site.v036.css`.


## Release 0.2.5
- Database version is 0.2.5.
- Current producer audit target is OpenGLESScope 0.3.2 / versionCode 302.
- Compatible producer floor remains OpenGLESScope 0.1.17+ within compatible 0.x schema-2 / technical-report-1 releases.
- Registry audit date is 2026-08-23.
- Production Worker compatibility date is 2026-08-23.
- No D1 migration or stored-report rewrite is introduced.
- Runtime format strings, including compressed texture, shader binary and program binary formats, remain submitted evidence and are never inferred by the Database.


## Release 0.2.7 OpenGLESScope 0.3.3 complete-report compatibility
- Database version is 0.2.7 and remains independent from the OpenGLESScope application version.
- Current producer audit target is OpenGLESScope 0.3.3 / versionCode 303.
- OpenGLESScope 0.3.3 canonical TXT evidence uses `Core version:` plus `Core version provenance:`; provenance must identify either the direct GL_MAJOR_VERSION / GL_MINOR_VERSION query or parsing from GL_VERSION exactly as emitted by the producer.
- Older compatible producers retain the historical `Parsed core version:` validation path; backward compatibility must not require fabricated new provenance lines.
- OpenGLESScope 0.3.3 versionCode must be 303. A mismatched current producer identity is rejected fail-closed.
- Submission schema 2 and technicalReport schema 1 remain unchanged. The expanded 0.3.3 queryDiagnostics array is accepted as explicit evidence and must not be silently truncated.
- Current Khronos baselines remain OpenGL ES 3.2, GLSL ES 3.20 and EGL 1.5; registry audit date is 2026-08-24.
- Production Worker compatibility date is 2026-08-24.
- No D1 migration, report rewrite, hash rewrite or capability inference is permitted for this release.
## Release 0.2.7 Cloudflare compatibility-date deploy correctness
- Database version is 0.2.7.
- `worker/wrangler.jsonc` compatibility_date must never be later than the date accepted by the Cloudflare Workers API at deployment time.
- Local timezone rollover must not be used to advance compatibility_date before Cloudflare accepts that date.
- When the local calendar is ahead of Cloudflare/API UTC acceptance, use the latest non-future accepted compatibility date and update it later only after deployment validation.
- Release verification must fail if compatibility_date is the known rejected future date for the audited deployment window.


## Release 0.2.8

- Database version is 0.2.8.
- Current audited producer is OpenGLESScope 0.3.4 / versionCode 304.
- Duplicate query diagnostic names remain invalid and must be rejected.
- `/v1/health` and `/v1/reports` must report the same current producer metadata.
- No D1 migration or stored-report rewrite is required.
- Compatibility exception for producer 0.3.3 only: duplicate diagnostics are permitted only for GL_NUM_EXTENSIONS, GL_NUM_COMPRESSED_TEXTURE_FORMATS, GL_NUM_SHADER_BINARY_FORMATS, and GL_NUM_PROGRAM_BINARY_FORMATS, exactly twice, with identical status and detail. This bridges the released 0.3.3 producer regression without weakening 0.3.4+ uniqueness.

## Release 0.2.9 VulkanScope-quality OpenGLESScope 0.4.1 parity
- Database version is 0.2.9 and current audited producer is OpenGLESScope 0.4.1 / versionCode 401.
- Compatible producer floor remains OpenGLESScope 0.1.17+ within compatible 0.x schema-2 / technical-report-1 releases.
- Compare includes Common evidence only in addition to Differences only and Technical differences only.
- Cross-producer detection uses both application version and versionCode. One-sided absence remains Unknown / Not reported and is never inferred Unsupported.
- Compare metrics expose A fields, B fields, Common fields, One-sided fields, Visible differences and Visible sections.
- Canonical report hash route is `#reports/<64-hex-id>/Overview`; validated section routes and canonical two-report Compare routes are first-class navigation contracts.
- Browser-visible current assets are `app.v042.js` and `site.v042.css`; stale versioned app/CSS assets are forbidden in release packages.
- Source audit, repository-state, route, Compare, Worker, audit-hygiene and staged Pages artifact tests are mandatory release gates.
- GitHub Pages deploys only an explicit allow-listed `_site` artifact. Worker source, tools, rules, workflows and transient files must not leak into Pages.
- Schema 2, technicalReport 1, normalizer 9, D1 schema, stored report IDs/hashes and the 2 MiB submission limit remain unchanged.
- Production Worker compatibility date remains 2026-08-23 until a newer date is deployment-validated by Cloudflare.

## Release 0.7.0 full correctness, security, EGL and reporting audit
- Database version is 0.7.0 and current audited producer is OpenGLESScope 0.7.0 / versionCode 700.
- Submission schema remains 2. Current producer technicalReport schema is 2; compatible historical producers retain technicalReport schema 1.
- Normalizer version is 10 and existing D1 schema/report IDs/hashes remain unchanged.
- Current technicalReport 2 requires bounded EGL runtime/context/surface evidence and expanded EGL Config evidence.
- EGL extension-specific config values require exact prerequisite extension tokens; absence must not be inferred as Unsupported.
- Compare retains Common evidence only, technical-differences filtering, cross-producer warnings and Unknown / Not reported one-sided semantics.
- Raw GL_VENDOR / GL_RENDERER evidence is authoritative; synthetic PCI/Vulkan-style vendor identifiers are forbidden.
- Browser-visible current assets are app.v070.js and site.v070.css; stale versioned frontend assets are forbidden.
- Source audit, repository-state, routes, Compare, Worker, audit-hygiene and staged Pages artifact tests are mandatory release gates.
- Existing HTTPS/CORS/CSP, 2 MiB bounds, sensitive-field rejection, canonical hashing, D1 parameterization, pagination and no-background-upload protections remain mandatory.

## Release 0.7.1 statistics, routing, cohort-filter and permalink parity
- Database version is 0.7.1. Current audited producer remains OpenGLESScope 0.7.0 / versionCode 700; submission schema 2, technicalReport 2, normalizer 10, D1 schema and stored report identities remain unchanged.
- Statistics is a first-class main view and uses only loaded report evidence. Percentages describe the loaded and currently filtered submission cohort and must never be described as device-population or market share.
- Distribution charts use first-party local SVG/CSS only. Remote chart libraries, remote scripts, remote fonts, analytics and trackers remain forbidden.
- Interactive distribution slices may apply exact cohort filters only for values that exist in submitted report evidence. Missing values remain Unknown and are never inferred Unsupported.
- Extension statistics rank exact runtime tokens. Because extensions overlap within one report, extension percentages are enumeration prevalence in the loaded cohort and are not exclusive-share charts.
- Global cohort filters cover GL vendor, GPU renderer, OpenGL ES version, EGL version, driver mode/version, Android version, application ABI, OpenGLESScope version and exact extension token.
- Display & HDR isolates itself from irrelevant GPU, OpenGL ES, EGL, driver, ABI, application-version and extension-token filters. Android filtering may remain because it is direct platform evidence.
- Clear filters must reset active global cohort filters and search without mutating any stored report or query evidence.
- Canonical main-view hash routing includes `#statistics`. The historical `#trends` alias may navigate to Statistics but canonical generated links use `#statistics`.
- Canonical report links remain `#reports/<64-lowercase-hex-id>/<validated-section>` and canonical comparison links remain `#compare/<64-lowercase-hex-id>/<64-lowercase-hex-id>`.
- Report and Compare Share/Copy controls generate only canonical first-party permalinks and do not rewrite report IDs, payloads or D1 rows.
- Compare includes section filtering and field-name search in addition to Differences only, Technical differences only and Common evidence only. These filters are presentation-only and never alter comparison-state semantics.
- Browser-visible current assets are app.v071.js and site.v071.css; stale versioned frontend assets are forbidden.
- Source audit, repository-state, route, Compare, Statistics/filter, Worker, audit-hygiene and staged Pages artifact tests are mandatory release gates.

## Release 0.7.2 OpenGLESScope 0.7.1 producer parity and clean archive
- Database version is 0.7.2 and current audited producer is OpenGLESScope 0.7.1 / versionCode 701.
- Compatible producer floor remains OpenGLESScope 0.1.17. The accepted ceiling is 0.7.1; 0.7.0 and 0.7.1 use technicalReport schema 2 while compatible historical producers retain their released technicalReport schema 1 contract.
- OpenGLESScope 0.7.1 application metadata requires installed application ABI and Android-supported device ABIs. Historical producer schemas are not retroactively rewritten.
- Runtime metadata prefers structured 0.7.1 ABI fields and retains report-text fallback for historical reports.
- Worker validation must not require mutable state/control values that OpenGLESScope intentionally excludes from implementation capability reporting.
- The 0.7.1 application ABI fields must exactly agree with the canonical TXT report ABI metadata.
- Existing Statistics, cohort filters, Display/HDR isolation, canonical routing, sharing, Compare filters and Unknown / Not reported semantics remain unchanged.
- D1 schema, normalizer 10, stored report hashes/IDs and historical payloads remain unchanged; no migration is required.
- Browser-visible current assets are app.v072.js and site.v072.css; stale versioned frontend assets are forbidden.
- README.md, root release.md, dedicated packaged app-store metadata directories and forbidden third-party comparison product naming are absent from the source release archive.
- Source audit, repository-state, route, Compare, Statistics/filter, Worker, audit-hygiene and staged Pages artifact tests are mandatory release gates.
## Release 0.7.3 Compare layout correctness and OpenGLESScope 0.7.2 producer parity
- Database version is 0.7.3 and current audited producer is OpenGLESScope 0.7.2 / versionCode 702.
- Compare control layout follows the shared VulkanScope interaction hierarchy: report A/B selectors and boolean comparison toggles occupy the primary compact picker row; Section and Field search occupy a separate subfilter row; Share comparison link is a separate action.
- Compare checkbox inputs must never inherit generic search/text-input sizing, padding, border or column-label styles. The native checkbox remains visually hidden and its dedicated visible check control owns the interactive presentation.
- Compare toggles remain compact inline controls at desktop widths and become bounded responsive grid rows on narrow screens; they must never stretch into tall empty cards.
- Differences only, Technical differences only and Common evidence only retain their existing semantics. Layout corrections must not alter evidence state, missing-value handling, field identity or canonical comparison routing.
- Current producer 0.7.2 uses the same schema 2 / technicalReport 2 application and ABI contract as 0.7.1, with exact versionCode 702. Historical compatible producers retain their released contracts.
- D1 schema, normalizer 10, stored report IDs/hashes and existing payloads remain unchanged; no migration is required.
- Browser-visible current assets are app.v073.js and site.v073.css; stale versioned frontend assets are forbidden.
- README.md, root release.md, dedicated packaged app-store metadata directories and forbidden third-party comparison product naming remain absent from the source release archive.
- Source audit, repository-state, routing, Compare, Statistics/filter, Worker, audit-hygiene and staged Pages artifact tests are mandatory release gates.


## Release 0.7.4 full shared presentation parity and release-gate hardening
- Database version is 0.7.4 and current audited producer remains OpenGLESScope 0.7.2 / versionCode 702. Submission schema 2, technicalReport schema 2, normalizer 10, D1 schema, stored report IDs and report payloads are unchanged.
- Shared database presentation geometry follows VulkanScope Database 0.39.8 for components that have the same interaction role. OpenGL ES/EGL branding, color accents, labels and API-specific evidence remain OpenGLESScope-specific.
- Compare uses the same interaction hierarchy as the shared reference: report A/B selectors plus three boolean toggles form the compact primary picker; Section and Field search form one bounded secondary filter row; Share comparison link is a separate action; summary metrics and comparison sections follow immediately without artificial vertical whitespace.
- Desktop Compare primary and secondary control groups are bounded to 760 CSS px. Narrow viewports use the reference two-column responsive grid and collapse to one column at 430 CSS px without stretching toggles, labels or search fields into empty cards.
- Compare secondary controls are generated through the shared subfilter-control contract. Generic label/input/select sizing must not override dedicated checkbox or subfilter geometry.
- Shared navigation, brand sizing, hero spacing, card grid, custom-select geometry, table-scroll controls, page-button interactions and responsive filter behavior must match the corresponding VulkanScope Database interaction geometry unless an OpenGL ES/EGL-specific control requires a documented exception.
- Clear filters is hidden when no visible cohort filter and no global search query is active. The control appears only when there is something it can clear.
- Browser-visible current assets are app.v074.js and site.v074.css. Stale versioned frontend assets are forbidden.
- `tools/build_index.py` must emit databaseVersion 0.7.4 and currentProducer OpenGLESScope 0.7.2. The source audit runs after the static-index build in CI so stale builder metadata cannot pass local source checks and fail only on GitHub Actions.
- `tools/repair_repository.py --apply` removes stale versioned frontend assets, extra workflows, README.md, root release.md and transient node_modules, .wrangler, __pycache__, .gradle, build and .idea directories. `--check` fails if any of those entries remain.
- Shared UI parity tests, routes, Compare semantics, Statistics/filter contract, Worker contract, source audit, audit-hygiene, repository-state and staged Pages artifact audit are mandatory release gates.
- README.md, root release.md, dedicated packaged app-store metadata directories and forbidden third-party comparison product naming remain absent from the source release archive.


## Release 0.7.5 current EGL binding evidence compatibility
- Database version is 0.7.5 and the current audited producer remains OpenGLESScope 0.7.2 / versionCode 702. Submission schema 2, technicalReport schema 2, normalizer 10, D1 schema, stored payloads and report IDs remain unchanged.
- A complete OpenGLESScope 0.7.0+ report may preserve an explicit EGL current-binding failure as evidence. `currentContext`, `currentDisplay`, `currentDrawSurface` and `currentReadSurface` are evidence booleans, not a requirement that every binding query succeed.
- The Worker must accept a complete report when one or more current-binding booleans are false only when the canonical `EGL current bindings` diagnostic is `Unavailable`. When all four booleans are true, that diagnostic must be `Available`. Other diagnostic states or contradictory evidence are rejected fail-closed.
- Canonical TXT `Current EGL bindings:` values must exactly agree with the four structured booleans. A TXT/structured mismatch remains invalid.
- Explicit binding failures remain visible to Diagnostics, Compare and quality analysis and are never converted to Supported, Not applicable or Unknown.
- The 2 MiB body bound, exact schemas, sensitive-field rejection, extension/query provenance gates, canonical hashing, CORS/CSP/security headers and all historical producer compatibility remain unchanged.
- Source archive hygiene remains mandatory: no README.md, root release.md, packaged store-metadata, transient dependency/cache/build directories or forbidden third-party comparison naming.

## Release 0.7.6 OpenGLESScope 0.7.3 HDR provenance compatibility
- Database version is 0.7.6 and the current audited producer is OpenGLESScope 0.7.3 / versionCode 703.
- Submission schema remains 2, technicalReport schema remains 2, normalizer remains 10 and D1 storage/report IDs remain unchanged. No migration or stored-report rewrite is permitted or required.
- Producer 0.7.3 display objects require `hdrCapabilityStatus` with exactly `available`, `unavailable` or `unknown`; historical producers through 0.7.2 remain accepted under their released display shape without this field.
- For 0.7.3, Available requires at least one HDR type; Unavailable and Unknown require an empty HDR-type list. The Database must not infer Unsupported from an empty list.
- Top-level and technicalReport display objects remain exact duplicates for the producer contract, and canonical TXT `HDR capability status` must match the structured status.
- Current Pages assets are app.v076.js and site.v076.css only. Stale versioned frontend assets are forbidden.
- Current OpenGL ES 3.2 / GLSL ES 3.20 / EGL 1.5 baselines, privacy bounds, exact report hashing, route/Compare/Statistics behavior and Worker security controls remain unchanged.


## Release 0.7.7 OpenGLESScope 1.2.1 technicalReport-v3 end-to-end compatibility
- Database version is 0.7.7 and current audited producer is OpenGLESScope 1.2.1 / versionCode 1201.
- Top-level report schema remains 2. technicalReport schema 3 is accepted only for the 1.2.1 producer and extends v2 with bounded internal-format sample evidence.
- Historical compatible producers retain their released v1/v2 validation shape. The Database must not mutate, reinterpret or silently promote old reports to v3.
- Producer parsing uses canonical three-component semantic versions and enforces the audited floor 0.1.17 and ceiling 1.2.1; unsupported future producers are rejected.
- Each internal-format row requires exact target, canonical internal-format name, evidence state, bounded detail, at most 64 unique positive sample counts and at most 64 matching NV sample-property rows. Duplicate target/format rows are rejected.
- Worker validation requires matching `glGetInternalformativ/<target>/<format>` diagnostic state for every v3 internal-format row. Registry/extension presence is never substituted for runtime evidence.
- The frontend normalizer, Formats view, report detail and Compare map preserve internal-format evidence.
- Worker body/report bounds, origin pinning, forbidden sensitive-key recursion, canonical stable hashing, D1 identity pin, CSP/security headers, pagination bounds and historical compatibility remain mandatory.
- Release verification follows the same evidence classes as the application: source syntax, semantic contract tests, negative malformed-evidence tests, UI/route/compare/statistics tests, package hygiene, deterministic archive reproduction and clean-extract rerun.
- Android/device execution is not a Database evidence class; Cloudflare production deployment is NOT EXECUTED unless separately recorded.

## Release 0.8.0 OpenGLESScope 1.3.0 technicalReport-v4 EGL registry parity
- Accept OpenGLESScope 1.3.0 only as versionCode 1300 with submission schema 2 and technicalReport schema 4.
- Preserve v1/v2/v3 historical producer validation; never reinterpret missing historical fields as Unsupported.
- Validate `eglCapabilities` with a closed bounded schema, canonical evidence states and unique capability names.
- Preserve v4 EGL evidence end-to-end through Worker storage, detail API, EGL UI, search and Compare.
- Do not infer EGL/OpenGL ES runtime capability from registry presence, token names, GPU marketing identity or API version alone.
- Retain the fixed-origin, 2 MiB, sensitive-key, stable-hash, nesting, D1 identity and response-security contracts.
- Run the complete source + staged Pages + deterministic package gate and repeat it after clean extraction before release.

## Release 0.9.0 OpenGLESScope 1.4.0 technicalReport-v4 EGL registry parity
- Database version is 0.9.0 and the current audited producer is OpenGLESScope 1.4.0 / versionCode 1400. Submission schema remains 2 and technicalReport schema remains 4.
- Historical OpenGLESScope 1.3.0 / 1300 technicalReport-v4 and all older version-scoped v1/v2/v3 contracts remain accepted exactly as released; missing historical fields are never reinterpreted as Unsupported.
- Producer 1.4.0 must preserve the corrected EGL creation/runtime boundary: `EGL context creation request` is explicit evidence and `EGL_CONTEXT_MINOR_VERSION`, `EGL_CONTEXT_OPENGL_RESET_NOTIFICATION_STRATEGY`, `EGL_CONTEXT_FLAGS_KHR` and `EGL_CONTEXT_OPENGL_NO_ERROR_KHR` are `Not applicable` runtime-query evidence rather than fabricated `eglQueryContext` results.
- OpenGL ES 3.2 producer reports require explicit `GL_RESET_NOTIFICATION_STRATEGY` diagnostic evidence. When `GL_KHR_robustness` is enumerated, robust-access evidence is mandatory and pre-3.2 producers use the registered `_KHR` reset-strategy query name.
- When OpenGLESScope 1.4.0 enumerates `GL_QCOM_motion_estimation`, `GL_NV_shading_rate_image`, `GL_NV_primitive_shading_rate` or `GL_ARM_shader_framebuffer_fetch`, the corresponding audited query diagnostics must exist; extension enumeration alone is insufficient.
- Worker and producer limits remain aligned: 2 MiB body/report text, 8,192 limits, 16,384 enumeration items/diagnostics, 256 EGL capabilities, 256 internal-format rows, 64 precision rows and 4,096 EGL configs. Duplicate evidence identities fail closed.
- Registry/reference presence, GPU/device identity and API version never substitute for runtime evidence. Available/Unavailable/Not applicable/Unknown remain distinct terminal states.
- Fixed-origin CORS, CSP/security headers, recursive sensitive-key rejection, bounded nesting/body parsing, canonical stable hashing, exact D1 identity, pagination limits and no-redirect producer fetch behavior remain mandatory.
- Release gates include Worker contract tests for 1.4.0 acceptance and malformed/missing 1.4.0 evidence rejection, historical compatibility, frontend route/Compare/Statistics/UI tests, source/package hygiene, exact staged Pages allow-list, deterministic archive reproduction and clean-extract re-verification.
- Production Cloudflare deployment is not claimed by local source/package verification.



## Release 0.9.1 OpenGLESScope 1.4.1 compiler-hotfix producer compatibility
- Database version is 0.9.1 and current producer is OpenGLESScope 1.4.1 / versionCode 1401. Submission schema remains 2 and technicalReport schema remains 4.
- OpenGLESScope 1.4.1 is semantically identical to 1.4.0 for report/query/schema purposes; the application release only fixes real C++/Kotlin compiler errors. The Database must therefore accept exact 1.4.1/1401 evidence while preserving exact 1.4.0/1400 as a historical current-schema producer.
- All 1.4.0 EGL legality, robustness, QCOM/NV/ARM query-evidence, build-metadata, bounds, uniqueness, canonical-state and security requirements apply unchanged to 1.4.1.
- Future producer versions remain fail-closed until explicitly audited. 1.4.2 and above must not be silently treated as 1.4.1.
- Pages current-producer metadata, Worker health metadata, static index metadata, versioned assets, contract tests, deterministic packaging and clean-extract quality gate must agree on 0.9.1 / OpenGLESScope 1.4.1.

## Release 1.0.0 OpenGLESScope 1.5.0 full-quality producer compatibility
- Database version is 1.0.0 and the current audited producer is exact OpenGLESScope 1.5.0 / versionCode 1500. Submission schema remains 2 and technicalReport remains schema 4.
- Historical OpenGLESScope 1.4.1 / 1401 and all earlier version-scoped report contracts remain accepted exactly as released; future producers remain fail-closed until audited.
- Current 1.5.0 canonical TXT evidence includes submission/technical schema metadata, complete EGL pbuffer mipmap/multisample evidence and complete EGL Config extension/unavailable-attribute evidence. The Worker rejects a 1.5.0 payload whose text silently drops those structured evidence classes.
- All 1.4.x EGL legality, GL robustness/QCOM/NV/ARM evidence, bounds, uniqueness, security, canonical hashing and sensitive-field rules remain mandatory.
- Frontend/static/Worker metadata must agree on Database 1.0.0 and current producer OpenGLESScope 1.5.0. Browser-visible current assets are app.v101.js and site.v101.css only; stale versioned assets are forbidden.
- Complete source audit, Worker contract tests, route/Compare/Statistics/UI tests, staged Pages audit, deterministic packaging and clean-extract rerun are mandatory before release.



## Release 1.0.1 OpenGLESScope 1.5.1 compiler-hotfix compatibility
- Database version is 1.0.1 and the current audited producer is exact OpenGLESScope 1.5.1 / versionCode 1501. Submission schema remains 2 and technicalReport remains schema 4.
- OpenGLESScope 1.5.1 is a compiler-only Kotlin syntax correction. Its GL/EGL query, report, security and resource semantics remain those of 1.5.0; the Database must therefore preserve 1.5.0 / 1500 as a separate historical exact producer contract rather than reinterpret it as 1.5.1.
- Future 1.5.2+ producers remain rejected until explicitly audited. Current health/list/static metadata identify 1.5.1 as current and the bounded compatibility ceiling as 1.5.1.
- Browser assets are cache-busted as `app.v101.js`, `site.v101.css` and `config.js?v=101`; stale current-version asset references are forbidden.
- Source and staged Pages audits, Worker contract tests, deterministic package reproduction and clean-extract full-gate rerun are mandatory.

## Release 1.0.2 OpenGLESScope 1.6.0 shared-application parity compatibility
- Database version is 1.0.2 and the current audited producer is exact OpenGLESScope 1.6.0 / versionCode 1600. Submission schema remains 2 and technicalReport remains schema 4.
- OpenGLESScope 1.6.0 changes shared application/network/updater/icon behavior but does not change the GL/EGL report schema. The Database must preserve the complete 1.5.1 evidence requirements for the new exact producer identity rather than weaken validation.
- OpenGLESScope 1.5.1 / 1501, 1.5.0 / 1500 and all earlier version-scoped producer contracts remain accepted exactly as released. Future 1.6.1+ producers remain fail-closed until explicitly audited.
- Current health/list/static metadata identify OpenGLESScope 1.6.0 and the bounded compatibility ceiling is 1.6.0. D1 schema, normalizer 12, canonical report hashing and stored report IDs remain unchanged.
- Browser assets are cache-busted as `app.v102.js`, `site.v102.css` and `config.js?v=102`; stale current-version assets are forbidden.
- Source and staged Pages audits, Worker contract tests, route/Compare/Statistics/UI tests, deterministic package reproduction and clean-extract full-gate rerun are mandatory.

## Release 1.0.3 OpenGLESScope 1.7.0 visual-interaction parity compatibility
- Database version is 1.0.3 and the current audited producer is exact OpenGLESScope 1.7.0 / versionCode 1700. Submission schema remains 2 and technicalReport remains schema 4.
- OpenGLESScope 1.7.0 changes application visual/interaction structure and bounds Encyclopedia rendering but does not change GL/EGL report semantics. Database validation for 1.7.0 therefore preserves the complete 1.6.0 evidence contract under a new exact producer identity.
- OpenGLESScope 1.6.0 / 1600 and all earlier version-scoped producer contracts remain accepted exactly as released. Future 1.7.1+ producers remain fail-closed until explicitly audited.
- Current health/list/static metadata identify OpenGLESScope 1.7.0 and the bounded compatibility ceiling is 1.7.0. D1 schema, normalizer 12, canonical report hashing and stored report IDs remain unchanged.
- Browser assets are cache-busted as `app.v103.js`, `site.v103.css` and `config.js?v=103`; stale current-version asset references are forbidden.
- Source and staged Pages audits, Worker contract tests, route/Compare/Statistics/UI tests, deterministic package reproduction and clean-extract full-gate rerun are mandatory.

## Release 1.0.4 OpenGLESScope 1.8.0 common dialog and security-behavior parity compatibility
- Database version is 1.0.4 and the current audited producer is exact OpenGLESScope 1.8.0 / versionCode 1800. Submission schema remains 2 and technicalReport remains schema 4.
- OpenGLESScope 1.8.0 changes shared application dialogs, semantic action controls, Info/About presentation and updater/submission failure handling without changing GL/EGL report evidence semantics. Database validation therefore preserves the complete 1.7.0 schema-4 evidence contract under the new exact producer identity.
- OpenGLESScope 1.7.0 / 1700 and all earlier version-scoped producer contracts remain accepted exactly as released. Future 1.8.1+ producers remain fail-closed until explicitly audited.
- Current health/list/static metadata identify OpenGLESScope 1.8.0 and the bounded compatibility ceiling is 1.8.0. D1 schema, normalizer 12, canonical report hashing and stored report IDs remain unchanged.
- Browser assets are cache-busted as `app.v104.js`, `site.v104.css` and `config.js?v=104`; stale current-version asset references are forbidden.
- Source and staged Pages audits, Worker contract tests, route/Compare/Statistics/UI tests, deterministic package reproduction and clean-extract full-gate rerun are mandatory.
## Release 1.0.5 OpenGLESScope 1.9.0 UI/storage parity compatibility
- Database version is 1.0.5 and the current audited producer is exact OpenGLESScope 1.9.0 / versionCode 1900. Submission schema remains 2 and technicalReport remains schema 4.
- OpenGLESScope 1.9.0 changes API-neutral UI/icon and in-app shared-storage import/export behavior without changing GL/EGL report evidence semantics. Database validation therefore preserves the complete 1.8.0 schema-4 evidence contract under the new exact producer identity.
- OpenGLESScope 1.8.0 / 1800 and all earlier version-scoped producer contracts remain accepted exactly as released. Future 1.9.1+ producers remain fail-closed until explicitly audited.
- Current health/list/static metadata identify OpenGLESScope 1.9.0 and the bounded compatibility ceiling is 1.9.0. D1 schema, normalizer 12, canonical report hashing and stored report IDs remain unchanged.
- Browser assets are cache-busted as `app.v105.js`, `site.v105.css` and `config.js?v=105`; stale current-version asset references are forbidden.
- Source and staged Pages audits, Worker contract tests, route/Compare/Statistics/UI tests, deterministic package reproduction and clean-extract full-gate rerun are mandatory.

## Release 1.0.6 OpenGLESScope 1.9.1 compiler-hotfix compatibility
- Database version is 1.0.6 and current producer is exact OpenGLESScope 1.9.1 / versionCode 1901. Submission schema remains 2 and technicalReport remains schema 4.
- OpenGLESScope 1.9.1 is a compiler-only correction over 1.9.0; all GL/EGL evidence, bounds, uniqueness, security, storage and report-text validation semantics remain unchanged.
- Exact OpenGLESScope 1.9.0 / 1900 and all historical producer contracts remain accepted; unsupported 1.9.2+ producers remain fail-closed.
- Browser assets are cache-busted as `app.v106.js`, `site.v106.css` and `config.js?v=106`. Source, Worker, staged Pages, deterministic package and clean-extract gates are mandatory.

## Release 1.0.7 OpenGLESScope 1.9.2 exact UI/filter/Encyclopedia compatibility
- Database version is 1.0.7 and current producer is exact OpenGLESScope 1.9.2 / versionCode 1902. Submission schema remains 2 and technicalReport remains schema 4.
- OpenGLESScope 1.9.2 changes API-neutral filter UI, icon/action mapping and crash-safe local Encyclopedia behavior without changing GL/EGL report evidence semantics. Database validation therefore reuses the complete 1.9.1 schema-4 evidence contract under the new exact producer identity.
- Exact OpenGLESScope 1.9.1 / 1901 and all historical producer contracts remain accepted as released. Unsupported OpenGLESScope 1.9.3+ producers remain fail-closed until explicitly audited.
- Current health/list/static metadata identify OpenGLESScope 1.9.2 and the bounded compatibility ceiling is 1.9.2. D1 schema, normalizer 12, canonical report hashing and stored report IDs remain unchanged.
- Browser assets are cache-busted as `app.v107.js`, `site.v107.css` and `config.js?v=107`; stale current-version asset references are forbidden.
- Source and staged Pages audits, Worker contract tests, route/Compare/Statistics/UI tests, deterministic package reproduction and clean-extract full-gate rerun are mandatory.
## Release 1.0.8 OpenGLESScope 1.9.3 schema-5 query/reporting compatibility
- Database version is 1.0.8 and current producer is exact OpenGLESScope 1.9.3 / versionCode 1903. Submission schema remains 2; technicalReport schema 5 is required only for 1.9.3.
- OpenGLESScope 1.9.3 adds GL runtime context/reset/robust-access evidence and expanded EGL pbuffer `eglQuerySurface` evidence. Database validation must preserve value type, query provenance, and Available / Unavailable / Not applicable distinctions without inference.
- Exact OpenGLESScope 1.9.2 / 1902 remains accepted as technicalReport schema 4; all older audited version-scoped contracts remain unchanged. Future 1.9.4+ producers remain fail-closed.
- Current Worker/static/list/health metadata must agree on 1.0.8 / OpenGLESScope 1.9.3, technicalReport schema 5 and registry audit date 2026-09-17.
- Browser assets are cache-busted as `app.v108.js`, `site.v108.css` and `config.js?v=108`; stale current-version assets are forbidden.
- Source/staged Pages audits, Worker contract tests, route/Compare/Statistics/UI tests, deterministic package reproduction and clean-extract full-gate rerun are mandatory.

## Release 1.0.9 OpenGLESScope 2.0.0 VulkanScope-quality parity compatibility
- Database version is 1.0.9 and current producer is exact OpenGLESScope 2.0.0 / versionCode 2000. Submission schema remains 2 and technicalReport schema remains 5.
- Exact OpenGLESScope 1.9.3 / 1903 technicalReport-v5 compatibility remains historical and must not be weakened. Exact 1.9.2 / 1902 schema-4 and all earlier audited contracts remain version-scoped.
- OpenGLESScope 1.9.4 through 1.x are not implicitly accepted by the 2.0.0 ceiling. They remain fail-closed because no released producer contract exists for those identities. OpenGLESScope 2.0.1+ also remains fail-closed until separately audited.
- The 2.0.0 application parity work changes UI/lifecycle/release-quality behavior, not GL/EGL evidence semantics. Database validation must not fabricate Vulkan concepts or infer capabilities absent from schema-5 evidence.
- Worker, health, list, static index and browser metadata must agree on Database 1.0.9, current producer 2.0.0, registry audit date 2026-09-30 and normalizer 12.
- Browser assets are exactly app.v109.js, site.v109.css and config.js?v=109 for this release. Stale current-version asset references are release-blocking.
- Worker contract tests must prove current 2.0.0 acceptance, historical 1.9.3 acceptance, exact versionCode binding, schema-5 GL/EGL runtime evidence, malformed evidence rejection, sensitive-field rejection and future-producer rejection.


## Release 1.0.10 OpenGLESScope 2.1.0 rules/icons/query/performance/UI parity compatibility
- Database version is 1.0.10 and current producer is exact OpenGLESScope 2.1.0 / versionCode 2100. Submission schema remains 2 and technicalReport schema remains 5.
- Historical exact OpenGLESScope 2.0.0 / 2000 schema-5 evidence remains accepted independently; unaudited 1.9.4-1.x identities, 2.0.1-2.0.x identities, and 2.1.1+ remain fail-closed.
- The 2.1.0 application release changes rules enforcement, semantic-icon parity, canonical registry/query validation, extension lookup performance, shared UI behavior, File Manager, Encyclopedia and Settings architecture without inventing new GL/EGL evidence semantics.
- Worker, health, report-list metadata, static index and browser metadata must agree on Database 1.0.10, current producer 2.1.0, registry audit date 2026-09-30 and normalizer 12.
- Browser assets are exactly app.v110.js, site.v110.css and config.js?v=110 for this release. Stale current-version assets are release-blocking.
- Worker contract tests must prove exact 2.1.0 acceptance, exact 2.0.0 historical acceptance, schema-5 evidence consistency, exact versionCode binding, malformed/sensitive evidence rejection and future-producer rejection.
## Release 1.0.11 OpenGLESScope 2.1.1 full-report/UI/Analysis evidence compatibility
- Database version is 1.0.11 and current producer is exact OpenGLESScope 2.1.1 / versionCode 2101. Submission schema remains 2 and technicalReport schema remains 5.
- Exact OpenGLESScope 2.1.0 / 2100 and 2.0.0 / 2000 remain independently validated historical schema-5 producers. Unsupported identities remain fail-closed; no semantic-version range may imply compatibility.
- The 2.1.1 application changes Analysis breadth, evidence disclosure, UI detail, semantic icons and local presentation only. Those changes do not authorize new report fields, fabricated query names or inferred capability support.
- Worker validation remains the source of truth for accepted schema-5 evidence. Registry membership, UI labels, Quality scores, saved minimum profiles, graph relationships and presentation summaries must never be converted into runtime support evidence.
- Worker, health, report-list metadata, static index and browser metadata must agree on Database 1.0.11, current producer OpenGLESScope 2.1.1, registry audit date 2026-09-30 and normalizer 12.
- Browser assets are exactly `app.v111.js`, `site.v111.css` and `config.js?v=111`; stale current frontend assets are release-blocking.
- Contract tests must prove exact 2.1.1 acceptance, exact 2.1.0 and 2.0.0 historical acceptance, schema-5 evidence consistency, exact versionCode binding, malformed/sensitive evidence rejection and 2.1.2+ fail-closed behavior.
- Source audit, route/Compare/Statistics/UI tests, deterministic package reproduction, clean-extract rerun and staged Pages audit are mandatory release evidence.

## Release 1.0.12 OpenGLESScope 2.1.2 toolchain/spec/query/detail compatibility
- Database version is 1.0.12 and current producer is exact OpenGLESScope 2.1.2 / versionCode 2102. Submission schema remains 2 and technicalReport schema remains 5.
- OpenGLESScope 2.1.2 changes Android/build dependencies, platform minimum, splash integration and evidence disclosure only; Database must not invent support from dependency, registry or UI metadata.
- Exact 2.1.1 / 2101, 2.1.0 / 2100, 2.0.0 / 2000 and 1.9.3 / 1903 remain historical schema-5 producers. Unknown 2.1.3+ identities remain fail-closed.
- Worker, health, report-list metadata, static index and browser metadata must agree on Database 1.0.12, current producer OpenGLESScope 2.1.2, registry audit date 2026-09-30 and normalizer 12.
- Browser assets are exactly `app.v112.js`, `site.v112.css` and `config.js?v=112`; stale current frontend assets are release-blocking.
- Contract tests must prove exact 2.1.2 acceptance, exact 2.1.1/2.1.0/2.0.0 historical acceptance, schema-5 evidence consistency, exact versionCode binding, malformed/sensitive evidence rejection and 2.1.3+ fail-closed behavior.

## Release 1.0.13 OpenGLESScope 2.1.3 native compile-hotfix compatibility
- Database version is 1.0.13 and current producer is exact OpenGLESScope 2.1.3 / versionCode 2103. Submission schema remains 2 and technicalReport schema remains 5.
- 2.1.3 is a native compile-correctness hotfix only. Its schema-5 evidence contract is identical to 2.1.2; no capability, registry, report or UI support state may be inferred or rewritten by the Database.
- Exact audited 2.1.2 / 2102, 2.1.1 / 2101, 2.1.0 / 2100 and 2.0.0 / 2000 schema-5 producers remain historical-compatible.
- Worker, health/list metadata, static index and browser metadata must agree on Database 1.0.13, current producer OpenGLESScope 2.1.3 and normalizer 13.
- Contract tests must prove exact 2.1.3 acceptance, exact 2.1.2 historical acceptance, exact versionCode binding, malformed/sensitive evidence rejection and 2.1.4+ fail-closed behavior.
- Frontend cache-busted assets are exactly `app.v113.js`, `site.v113.css` and `config.js?v=113`; stale v112 application/CSS references are forbidden.

## Release 1.0.14 OpenGLESScope 2.1.4 Kotlin/Compose compile-hotfix compatibility
- Database version is 1.0.14 and current producer is exact OpenGLESScope 2.1.4 / versionCode 2104. Submission schema remains 2 and technicalReport schema remains 5.
- OpenGLESScope 2.1.4 is a Kotlin/Compose compile-correctness hotfix only. Its schema-5 evidence contract is identical to 2.1.3; Database normalization must not invent, drop, reclassify or rewrite capability evidence because of the application compile fix.
- Exact 2.1.3 / 2103 remains an audited historical schema-5 producer. 2.1.5+ and any unaudited producer identity remain fail-closed.
- Worker, health/list metadata, static index and browser metadata must agree on Database 1.0.14, current producer OpenGLESScope 2.1.4 and normalizer 14.
- Contract tests must prove exact 2.1.4 acceptance, exact 2.1.3 historical acceptance, exact versionCode binding, schema-5 evidence consistency, malformed/sensitive evidence rejection and 2.1.5+ fail-closed behavior.
- Frontend cache-busted assets are exactly `app.v114.js`, `site.v114.css` and `config.js?v=114`; stale v113 application/CSS/config references are forbidden from current Pages output.
## Release 1.0.15 OpenGLESScope 2.2.0 UI/interaction parity compatibility
- Database version is 1.0.15 and current producer is exact OpenGLESScope 2.2.0 / versionCode 2200. Submission schema remains 2 and technicalReport schema remains 5.
- OpenGLESScope 2.2.0 changes shared UI/interaction presentation only; Database normalization must not invent, drop, reclassify or rewrite capability evidence because of visual/interaction parity work.
- Exact 2.1.4 / 2104 remains an audited historical schema-5 producer. 2.2.1+ and any unaudited producer identity remain fail-closed.
- Worker, health/list metadata, static index and browser metadata must agree on Database 1.0.15, current producer OpenGLESScope 2.2.0 and normalizer 15.
- Frontend cache-busted assets are exactly `app.v115.js`, `site.v115.css` and `config.js?v=115`; stale v114 references are forbidden from current Pages output.



## Release 1.0.16 OpenGLESScope 2.2.1 compile-hotfix compatibility
- Database version is 1.0.16 and current producer is exact OpenGLESScope 2.2.1 / versionCode 2201. Submission schema remains 2 and technicalReport schema remains 5.
- OpenGLESScope 2.2.1 changes Kotlin/Compose compile correctness only; Database normalization must remain schema-5 equivalent to 2.2.0 and must not invent/drop/reclassify evidence.
- Exact 2.2.0 / 2200 remains an audited historical producer. 2.2.2+ and any unaudited producer identity remain fail-closed.
- Worker, health/list metadata, static index, browser metadata and cache-busted assets must agree on Database 1.0.16, current producer 2.2.1 and normalizer 16.
- Current frontend cache-busted assets are exactly `app.v116.js`, `site.v116.css` and `config.js?v=116`; older v115 assets remain historical evidence only and are not shipped as current Pages assets.


## Release 1.1.0 VulkanScope Database 1.4.12 methodology adaptation
- Historical release identity is OpenGLESScope Database 1.1.0. This section supersedes earlier rules only when they reference old *current* release metadata; historical release contracts are immutable audit history.
- `rules/VULKANSCOPE_DATABASE_1.4.12_PROJECT_RULES_REFERENCE.md` is the exact frozen VulkanScope Database source methodology. Its SHA-256 and all ordered level-2 headings are independently checked against `rules/vulkanscope_database_1_4_12_rule_applicability.json`. No VK-specific runtime support, Profiles, Physical Device, Vulkan queue, VkFormat, layer or Vulkan header fields are invented for OpenGL ES/EGL reports.
- Every non-Vulkan-specific engineering principle of that reference is binding: canonical evidence preservation, precise provenance, fail-closed submission, responsive and accessible views, lifecycle-safe bounded transport, browser privacy, explicit freshness, safe staged publication, deterministic packaging, negative-mutation regression, historical immutability and clean-extract rerun.
- The source data model stays OpenGLESScope submission schema 2 / technical report schema 5 / normalizer 16. Actual OpenGL ES and EGL runtime queries, query diagnostics, reported extension token sets, precision, formats, EGL configuration attributes, display/HDR and their Available/Unavailable/Not applicable/Unknown distinctions are authoritative. No Vulkan nomenclature or registry-only support proof is added.
- New submissions accept only explicitly audited released producers and exact semantic-version/versionCode binding through OpenGLESScope 2.2.22 / 2222. OpenGLESScope 2.2.23+, arbitrary future versions, mismatched versionCodes and unknown schema versions remain rejected before storage. Existing historical rows remain readable, comparable and unchanged.
- The 2 MiB streaming request bound, fatal UTF-8 validation, JSON nesting bounds, canonical JSON SHA-256 ID, strict schema and sensitive-field checks, CORS/origin and Content-Security-Policy restrictions, 405 Allow headers, D1 pagination and origin-controlled no-store responses remain mandatory. A failed new-report insert is never represented as accepted, and duplicate content retains its existing ID and submitted time.
- `GET /v1/sync` is a read-only Worker freshness handshake; its latest ID, server timestamp and aggregate count contain public report metadata only. Refresh never mutates an existing detail payload or silently drops a user-selected report/filter. A network failure must be displayed as unknown/offline instead of implying freshness.
- The optional new-report snapshot dispatch is asynchronous only after a successful D1 INSERT with positive `meta.changes`; duplicate uploads never cause dispatch. The GitHub token is stored only in Cloudflare Worker secret `SNAPSHOT_GITHUB_TOKEN`; it is forbidden in source, Pages artifacts, API responses, logs and error messages. Dispatch failures never convert an accepted report into a failed upload.
- GitHub Pages release and snapshot jobs share one `concurrency` group, do not cancel in-progress runs, build the source-controlled staged artifact, verify the triggering report against the authoritative Worker, audit the staged Pages allowlist, and verify the accepted ID in published Pages after snapshot-mode deployment. Local snapshot content is public report summaries, not private report bodies.
- UI live refresh is an explicit user action, with accessible status, disabled duplicate activation, reduced-motion support and separately visible loaded/live counts. Startup uses only validated, public version-matched read-only summaries from `data/index.json` as an explicit offline fallback; a missing report body is never synthesized from a summary. Main navigation, report details, Compare, Statistics, Extensions, GL/EGL disclosure, raw TXT and 50-row maximum report paging retain previously tested behavior. Unknown support is never rewritten as unsupported; temporal identity comes only from the D1 server.
- Source comments, remote CSS imports, unpinned Worker tools, broad external CSP sources, analytics and remote fonts, private/IP fields, transient build directories and unreviewed GitHub workflows remain forbidden. Dependencies and Worker configurations are checked before deployment; production remote deployments are independent of a locally passing gate.
- The release gate MUST verify exact rules reference, application admission and versionCode pairs, invalid UTF-8 rejection, `/v1/sync` no-data/data states, duplicate dispatch suppression, missing-secret safety, snapshot indexing negative cases, frontend accessibility, security preflight, staged allowlist, deterministic ZIP and clean-extract full-gate reproducibility. A documented limitation is not evidence of a test pass.


## Release 2.0.0 full interface parity adaptation
- The immutable VulkanScope Database 1.4.12 rules reference and 116-class applicability census remain required.
- Database release identity is 2.0.0. Submission schema 2, technical-report schema 5 and the audited 2.2.22 / 2222 current producer remain unchanged.
- Primary navigation includes Reports, Devices, Versions, OpenGL ES, EGL, Extensions, Limits, Formats, Precision, EGL Configs, Display & HDR, Diagnostics, Statistics, Trends, Encyclopedia and Compare.
- Vulkan-only memory, queue, physical-device properties and Profiles features are not fabricated; existing GL/EGL semantic destinations remain authoritative.
- Workspace hero, active navigation motion, animated four-tab Settings drawer, startup loader, scroll control, view transitions, table horizontal controls, keyboard accessibility and reduced-motion are mandatory.
- Favorites are explicit report IDs only, session-only by default, persist only after Remember on this device is enabled and never contain report payloads.
- Encyclopedia contains the exact locked reference catalog embedded in OpenGLESScope 2.2.22, generated from gl.xml / egl.xml, not inferred runtime support. Limit visible reference records to 50 per page. Search/filter remains bounded and escaped.
- Devices/Versions/Trends describe the loaded filtered report set only. Trends use server-authored timestamps, never local collection guesses or market-share claims.
- Settings browser/network information is local and is never included in a database report or automatically uploaded.
- Browser feature support is checked by concrete standard feature detection, not user-agent sniffing; fail explicitly where necessary. Destructive local-data clearing uses an accessible in-page cancel/confirm dialog, never browser-default confirm. Favorite toggle state must update row and detail buttons immediately, including accessible pressed state.
- Tests, clean packaging, immutable reference verification, API security and exact producer compatibility are release-blocking.


## Release 2.0.1 shared workspace, regional presentation and motion contract
- VulkanScope Database 1.4.12 is the immutable API-neutral shared interaction methodology reference; GL/EGL identity and canonical evidence remain OpenGLESScope-specific.
- All 16 primary navigation workspaces remain functional; keyboard arrows/Home/End and scroll-into-view preserve active destination discoverability. Settings retains four categories with dialog focus containment, restoration and reduced-motion compliance.
- Regional presentation offers Automatic, Country and Manual modes, bounded IANA zone selection, date order, hour cycle and seasonal setting. Presentation never mutates server-authored `submitted_at`, report identity, sorting, age filters or raw TXT.
- Report column defaults explicitly toggle exact submitted ISO timestamp and raw vendor evidence. Unknown evidence remains unknown; no inferred capability or submission time is generated.
- Scroll progress and connection state are visually indicated. Browser connectivity is not treated as proof the Worker can be reached; live synchronization remains explicit and fail-closed.
- Invalid or empty pagination input may not navigate to a non-existent page. Navigation preserves the 50-row upper bound.
- Release requires static UI contracts, locally reproducible real Chromium desktop/mobile/settings/regional/catalog interactions, Worker contract tests, negative mutation checks, deterministic ZIP reproducibility and clean-extract quality gate.


## Release 2.0.2 canonical report and snapshot parity
- VulkanScope Database 1.4.12 remains an immutable methodology reference, not a mandate to invent Vulkan-only GL/EGL fields. The applicable 116 rule classes are preserved.
- The existing OpenGLESScope 2.2.22 / 2222 exact producer contract, submission schema 2, technicalReport schema 5, normalizer 16, current immutable data and 16 workspaces remain unchanged.
- A canonical report is rejected if its UTF-8 representation exceeds a separate 4 MiB retrieval bound. New canonical bodies above the 1,450,000-byte inline threshold are stored in an atomic D1 batch using ordered bounded chunks; the original canonical SHA-256 report identity is retained.
- A complete legacy inline payload is still readable. A chunk sequence with missing, duplicate or reordered indices, malformed values, oversized reconstruction, or a reconstructed SHA-256 that differs from the report ID is rejected, never silently repaired. Deploy migration 0004 before deploying this Worker.
- The live sync handshake reads latest report identity and count from one D1 query to avoid a mismatched multi-query observation. Snapshot dispatch is asynchronous after a successful report insertion only, with at most three bounded requests, short fixed retry waits and retries restricted to transient network, 429 and 5xx failures. Permanent 4xx errors do not retry, authorization secrets never enter client responses, and snapshot delivery failures cannot revoke an accepted D1 row.
- CI snapshot publishing checks the exact triggering ID against the authoritative API, audits the staged artifact and independently checks the published snapshot. Neither Pages freshness nor an absent secret is represented as successful remote publication.
- New release gates explicitly exercise chunking, reassembly, stored-payload corruption, transient dispatch retry, permanent-failure behavior, duplicate suppression, deterministic packaging and a clean-extract rerun.

## Release 2.0.2 request-scoped Internet Settings
- The Internet panel adds an explicit, user-activated network-information request; no IP/geographic information is fetched in the background or included in any canonical report, D1 row, static Pages summary, favorite or local setting.
- The optional Worker `GET /v1/network-info` returns no-store, first-party-CORS request-scoped Cloudflare-observed data; DNS resolvers are explicitly not observable. IP/network fields are only surfaced after an intentional click, inserted through text-only DOM APIs, response-bounded, time-bounded, and cleared when Settings closes.
- Method restriction, cross-origin denial and not-persisted behavior are release-blocking.


## Release 2.0.5 exact VulkanScope 1.4.12 shared UI shell contract
- Base the common HTML/CSS/SVG chrome on the actual VulkanScope Database 1.4.12 release, not visual imitation. Preserve identical structural classes, breakpoints, focus and transition rules for header/navigation, hero-v127, Settings categories, database loading, progress, destructive confirmation, and footer.
- Preserve OpenGLESScope GL/EGL brand identity, authoritative registry, evidence state classes, 16 API-appropriate workspaces, current report identifiers and API schema. Do not render Vulkan-specific fields or fabricated runtime evidence.
- GL/EGL-specific CSS must precede the exact frozen VulkanScope common CSS; only a bounded tail may adapt accents and existing GL/EGL controls. The common CSS block SHA-256 is a release-blocking invariant.
- Browser checks must cover desktop and mobile navigation, all Settings categories, registry pagination, safe regional preferences, explicit-only network diagnostics, report rendering and console-error absence.
- Dependency maintenance inherits the verified Wrangler 4.146.0 exact pin, but no new lockfile may be fabricated from an offline install. npm audit and authenticated Cloudflare deployment remain separately required live gates.
- Snapshot GitHub token is a remote Cloudflare Secret, never ZIP material. The D1 chunk migration and existing reports must be preserved.
- Do not place DEPLOY.md, DEPLOY_<version>.md or equivalent instructions inside distribution ZIP files. Provide deployment commands only in the conversation.

- Before publication, run both `python -B tools/test_2_0_4_browser.py` and `python -B tools/test_2_0_4_full_browser_regression.py` with a local Playwright Chromium. Both desktop and mobile passes are release evidence.

## Database 2.0.5
- Every frontend Worker version check, including health, report index, sync and offline snapshot, uses release 2.0.5 with explicit byte-stamped assertions to prevent stale version literals.
- New POST uploads require exactly OpenGLESScope 2.2.22 (versionCode 2222); existing accepted records remain readable without migration.
- Official OpenGL® ES™ and EGL™ visual labels and artwork are copied from OpenGLESScope 2.2.22 while raw GL/EGL registry tokens and canonical report data are unchanged.
- Common shell/hero/Settings/scrollbar components are retained from VulkanScope Database 1.4.12.
- Never include DEPLOY.md or deployment instructions in source ZIP.
- Empty local `data/index.json` is a build placeholder and must never be presented as a verified offline dataset during Worker unavailability.

## Database 2.0.5 interface parity
- Canonical shared visual design must begin with the exact reference stylesheet, not be appended after stale OpenGLESScope common styles.
- GL/EGL-only CSS is restricted to classes absent from the canonical shared design, and must never redefine common interactive controls.
- Hero/toolbar/detail structural parity requires executable DOM/browser tests, not stylesheet token presence alone.

## Release 3.0.0 native OpenGLESScope full interaction contract
- Version is 3.0.0, independent of the only permitted new-report producer OpenGLESScope 2.2.22 (versionCode 2222). Previously admitted reports remain visible and immutable, D1 migration 0004 is preserved; no new migration.
- VulkanScope Database 1.4.12 is the verified common UI geometry/interaction reference. The shipped visual design preserves its common selectors, breakpoints, transitions, navigation, hero, Settings, page-scroll, modal and loading layouts. Theme hues must be converted from the reference red palette to OpenGLESScope's brand-magenta #BA2A8D. The immutable source stylesheet digest and branded geometry-blind parity test prevent CSS imitation by keyword stuffing. GL/EGL-specific presentation must not invent Vulkan-only evidence.
- The initial startup shell hides unready content, keeps the logo-based loading panel visible, and reveals the shell only after the application reports completion. The browser compatibility gate must fail explicitly and the fail-safe release-bootstrap reveal timeout must prevent indefinite blank pages.
- Settings > Information exposes first-party source provenance, source-specific real local third-party license documents and an upstream OpenGLESScope application MIT notice. Do not manufacture a blanket database licensing claim. Documents are allowlisted, same-origin, UTF-8 decoded, byte-bounded and rendered as textContent; viewers must trap focus, dismiss by Escape/backdrop and honor reduced motion.
- The first-visit privacy notice states that no tracking/analytics cookies are set. A session-only acknowledgement must not write localStorage. Persistent acknowledgment must require explicit choice and remain only in this browser. Optional IP/network diagnostics remain user initiated and request-scoped; no background report uploads.
- Live Worker sync runs every 3 seconds only while the page is visible and connected; connection-offline, Worker-unavailable, checking and restored messages are distinct. Incoming new-report notices use actual API/loaded counts and must not claim a new report until it is present. Request timeouts, byte bounds and concurrency lock remain mandatory.
- Periodic published-release checks must validate data/release.json shape, published readiness, exact release asset names, matching frontend version and linked page before allowing a release transition. Source marker is unpublished; validated Pages artifact marks readiness once all allowlisted assets are staged. No unverified cache-busting reload loops.
- Main navigation retains all 16 GL/EGL semantic destinations, existing report detail tabs, keyboard and responsive controls, page limit 50 and canonical report semantics. Browser, source, negative-mutation, Worker contract, staging, and clean-extract reproducibility tests are release blockers.
- GitHub snapshot secret and production D1 content must not be embedded in ZIP. DEPLOY.md, DEPLOY_<version>.md and equivalent deployment documents must never ship; commands only in chat.


## Database 3.0.1 canonical interaction and semantic-color parity
- Adopt the actual VulkanScope Database 1.4.12 viewport and surface scrollbar algorithms, including thumb dragging, keyboard navigation, arrow endpoints, dynamic content updates and reduced motion. Never hide native root scrollbars unless the custom viewport scrollbar is mounted.
- The canonical shared CSS geometry and matching non-API SVG path shapes are immutable; only OpenGLESScope brand/accent colors and GL/EGL-specific evidence labels/artwork may differ. Semantic error, unsupported, warning, success and neutral colors follow the VulkanScope reference, not brand pink.
- Keep all long evidence tables bounded to 10, 25 or 50 visible rows with validated numeric pagination and explicit total counts; never discard or infer report evidence.
- Horizontal table scrolling must remain accessible by wheel/shift-wheel, scrollbar track, keyboard and mobile touch. The viewport scrollbar is visible for any true vertical overflow; inside settings, select menus, license windows and raw report panes, the reference surface scrollbar is used.
- Existing D1 migrations and stored historical reports remain untouched. New submissions require exactly OpenGLESScope 2.2.22 / versionCode 2222. Any GL/EGL field must remain backed by submitted evidence.
- Run the negative static source-reference checks, Chrome desktop and mobile scrollbar interactions, Worker contract and full quality gate on the original source and clean-extracted deterministic package.
- Never include any DEPLOY*.md document inside a release ZIP.

## Release 3.0.2 interface equivalence and interaction safety
- The reference Reports table and GL/EGL adaptation preserve collapsible Submitted, Vendor and directly reported EGL API columns, exact SHA-256 ID copy, favorites, bounded page sizing and invalid page rejection.
- Devices and Versions show the reference-style chart, selectable aggregation dimension, cohort report counts, and bounded 10/25/50-row tables; missing GL/EGL evidence stays Unknown.
- Network banners use the reference offline, checking, unavailable, restored and automatic retraction lifecycle. Successful Worker probes, not the browser online flag alone, establish Database reachability.
- Connection state updates Internet Settings without querying IP details. Request-visible network information remains explicit opt-in and never enters report payloads or D1.
- First-party brand colors may differ from the reference, while semantic success, warning, failure, unknown and neutral colors retain their distinct roles.
- New cross-page interaction regression tests cover both desktop and mobile layouts, report row action isolation, control geometry and coherent release/Worker handshake.

## Release 3.0.3 publication, details and Compare parity
- The initial loader reports real initial index and bounded detail-fetch progress; it closes at completion. Later three-second live refreshes must never reopen it. The hero report count derives only from loaded D1-submitted reports.
- Report detail retains all eleven GL/EGL semantic destinations and canonical TXT, with reference section hierarchy, real submitted evidence, and no invented Vulkan-only fields.
- Compare A/B identity and summary, Swap, pinned and minimized controls, exact-field filtering and actual difference counts must remain keyboard/touch accessible. Unknown or absent values are never treated as unsupported.
- Once a future release marker is ready, verify index.html, application, stylesheet, bootstrap, browser compatibility, experience and scrollbar assets with byte/time limits before automatic navigation. Preserve hash and prevent stale-cache navigation loops. Existing already-open older frontend scripts cannot be modified remotely and may need their existing one-time update action.
- New accepted D1 reports alone trigger the asynchronous authenticated snapshot workflow. The browser sees live changes by a foreground-only three-second /v1/sync probe, loads verified report data, then updates hero counts and notifies. Snapshot publication must verify the expected accepted report ID, without leaking secrets or rewriting historical records.
- Desktop/mobile browser, Worker contract, deterministic release negative tests and clean-extracted source quality gate are mandatory. No DEPLOY files inside release ZIP.

## Release 3.0.5 common Settings, viewport, evidence-meter and official-asset parity
- Completion of the first report/index startup must remove both startup-layout-hold and database-loading classes before dispatching the ready event; the scrolling controller must not suppress page and inner scrollbars after the loader is hidden. Verify the actual rendered 15+ report case, as well as artificially long content, on desktop and mobile.
- The shared Settings drawer preserves the reference four-tab hierarchy and card/row presentation for Internet and Browser; detailed Worker-visible network identity remains strictly user-initiated, masked by default, bound to a single request and cleared when Settings closes. The GL-specific page-size preference may supplement, not replace, common preferences.
- Circular distribution percentages use reference 120x120 SVG, 46-radius segments, pathLength percentages, legend-list and selected-filter geometry. Evidence availability percentages use the canonical coverage-bar and coverage-fill structure, with a GL-derived denominator and distinct four-state semantics.
- HDR10+ displays the exact reference versioned hdr10_plus_v1014.png asset. White EGL uses the pixel-white transparent official EGL silhouette egl-logo-white-v028.png consistently in main EGL heading, navigation and report-detail/section tabs; the mislabeled red white-v030 artifact is forbidden. The official GL|ES logo remains present throughout OpenGL ES destinations.
- Android filter options use the canonical green #3DDC84 Android SVG path and accessible textual label. Non-Android icons and GPU assets remain unchanged unless required for canonical parity.
- Browser compatibility behavior is byte-for-byte the reference algorithm except OpenGLESScope-specific public names, and all static error pages use the local first-party brand, assets and CSP.
- Preserve all Worker/D1/report schema, 3-second sync and release-ready controls; no D1 migration or producer-version change. The release must pass deterministic clean ZIP, source gate and a real desktop/mobile Settings-scroll + 15-report browser regression.
- Never ship deployment documentation inside ZIPs.

## Release 3.0.5 publication, navigation and canonical exports
- Publishing a newer Worker while the frontend is still propagating is a release transition, not evidence of lost connectivity. The established checking banner is used; the actual unavailable state requires a failed API request.
- Independent same-origin release checks begin before the full report index becomes ready and navigate automatically only after validating the complete published asset set. Incomplete publication does not trigger a reload; repeated navigation is bounded.
- The exact stored canonical TXT is exported without normalization or markup. JSON export fetches the report by validated public ID and checks returned identity before writing a UTF-8 file. Both actions use the existing report action-button geometry and transient success/failure feedback.
- Report mouse text selection and drag never navigate. Click, keyboard and context behavior remain accessible. Browser Back/Forward and in-app detail return restore route-specific scroll position without changing server-authored report ordering.
- Live report updates must not impersonate a Worker outage during a staged release, nor restart the opening animation. All original producer rules, privacy restrictions, report identity and D1 rows remain unchanged.

## Release 3.0.6 Settings, filters and navigation progress conformity
- Internet Settings use the same two-section card hierarchy as the common interface. Only opening Internet Settings triggers automatic bounded request-scoped observations. Complete current Cloudflare request fields are shown without inventing unseen IPv4/IPv6, DNS, latency or transport data, and each observed IP is mosaicked until individually revealed. No request-specific values are stored in D1, report data or browser persistence; closing Settings clears the observations and stops refresh. Browser information lives inside Internet, not a duplicate Information card.
- Shared report-column Preferences and regional Settings retain the applicable controls. The extra Settings page-size selector and network request/refresh buttons are removed; bounded Reports pagination remains available in its own report toolbar. All first-party country flag images are local and offline-safe.
- The Android filter SVG path and rendered geometry exactly match the common green SVG. No overriding OpenGL-only dimension rule applies.
- The fixed 3-pixel top-of-viewport page progress indicator uses a span as expected by the shared reference CSS. Progress appears only for genuinely scrollable pages and is keyboard-, reduced-motion- and viewport-safe.
- View-specific global filters follow the canonical Hardware, runtime/driver, Platform, Producer, Submission, Evidence state and Display evidence family sequence, translated strictly to the GL/EGL schema. Unavailable or inapplicable controls are hidden and their stale values never filter other destinations; display filters never leak into non-display views. Unknown evidence stays Unknown.
- Production and clean-archive gates cover report-index data integrity, snapshot behavior, Settings and filter interaction, local branded assets, Worker network-info contract and both desktop/mobile scroll progress. No D1 migration or producer-version change. No deployment instructions in ZIP.


## Release 3.0.7 canonical detail, navigation and startup motion conformity
- The first report-detail tab is Overview, using canonical grouped identity, application, Android device, GPU/driver, OpenGL ES/EGL and display-evidence cards. The public report route keeps `/Overview` and accepts the earlier Summary alias without retaining Summary as a visible tab. All submitted values, canonical TXT and existing eleven detail destinations remain accessible.
- The report action group, SVG favorite artwork, labels and action feedback remain inside the detail hero with shared button geometry, while the additional canonical TXT export stays available. The Back button is immediately visible on direct, clicked and history-restored report navigation; it has focus-safe header clearance and returns to the prior reports scroll position.
- Reference-duration 120 ms report exit and 210 ms report entry animation, existing 105/180 ms detail-tab motion and 90/150 ms workspace transitions use a single cancelable navigation lifecycle. Reduced-motion skips nonessential animations. Stale report loads and rapid route changes must never restore a superseded view.
- Initial database progress reflects real report processing, closes through one canonical loading lifecycle, and never reopens on foreground three-second sync. The workspace shell and top header stay correctly sticky: clipping the horizontal overflow must not create a competing body scroll container. Android/mobile layout and OpenGLESScope magenta branding are preserved.
- Release requires exact source geometry audit, static negative-mutation gates, real desktop and mobile Chromium overview, Back, sticky header, loader, tab, action, scroll restoration and prior comparison regression, and clean extracted ZIP quality verification. No report/Worker schema migration and no change to the 2.2.22/2222 submission gate.


## Release 3.0.9 release-state, shader precision and regional controls
- The frontend distinguishes a valid newer Worker response from outage and labels a staged Worker/Pages mismatch Checking; a failed report fetch alone does not prove Internet outage. Independent bounded health probes confirm API reachability. True offline remains explicit.
- Foreground three-second authoritative D1 synchronization and async post-insertion snapshots remain independent. Existing historical records, producer gate 2.2.22/2222, report hash and migration chain are immutable.
- OpenGL ES Shader Precision presents only queried Vertex/Fragment stages, an All shader stages selector, precision type and search. Unknown diagnostics are never guessed supported or unavailable. Rows are 50/page maximum with bounded direct page entry.
- Every enhanced custom filter searches the full native option collection, separates search/scrollable option/pagination areas and pages fifty at a time, including one-page menus. Search clear and keyboard/touch/focus/reduced-motion behavior are required.
- Date/time preferences expose current, standard and daylight offsets for a selected IANA time zone, with no-season-change explanation. All submission instants come solely from Worker-authored submitted_at and retain original ISO.
- Pagination entrance motion is compositor-only, bounded and disabled for reduced motion. Shared design is adapted to real OpenGL ES/EGL evidence; legacy canonical registry symbols and immutable technical audit references must not be silently rewritten.
- Cache-busted browser assets and Worker version are 3.0.9 / 3009. Source quality and clean ZIP reproduction are mandatory; live deployment is separately verified.


## Release 3.0.9 complete shared-rule adoption
- The complete 116-section VulkanScope Database 1.4.12 project-rule corpus is retained as the SHA-pinned, read-only `rules/VULKANSCOPE_DATABASE_1.4.12_PROJECT_RULES_REFERENCE.md`; all 116 source sections are explicitly mapped as adapted to OpenGL ES/EGL in `rules/vulkanscope_database_1_4_12_rule_applicability.json`. These common rules are normative for OpenGLESScope in all API-neutral areas: honest observed evidence, release/build checks, security, CSP, privacy, no background uploads, live/snapshot coordination, cached loading and progress, all responsive page layouts, filters, search clear controls, pagination, scroll, reduced motion, modal access, licensing, accessibility, staged publication and negative testing.
- All reference-specific names, color tokens, API/profile/driver queries, GPU capabilities, expected enumeration counts, producer identities, report schemas, hash rules, D1 bindings and registry entries must be translated to the actually queried OpenGL ES/EGL equivalents. Vulkan-only requirements have no OpenGL ES meaning and cannot be copied as fake data, label, runtime symbol or support state. Original OpenGLESScope application producer, 2.2.22/2222 acceptance gate, report integrity, immutable D1 and GL/EGL terminology supersede incompatible platform-specific instructions.
- Legal/Information panels use the shared Settings information hierarchy, summary metrics, equal seven library cards, license/version chips, keyboard-operable per-license Read actions and the scrollable source-bound accessible Markdown license dialog, with identical desktop/mobile presentation geometry and OpenGLESScope magenta brand variables.
- Source ZIP and source-tree `data/index.json` remain summary-only and must never embed real report bodies or network request metadata. Only the generated GitHub Pages `_site/data/preload/` may contain already-public, authorized GET report responses, produced by an HTTPS read of the currently published Worker after source verification. A manifest lists complete public index, report IDs, authoritative submission timestamps, bounded chunks and full SHA256 checksums. All chunks are bounded, allowlisted and audited cryptographically, must cover each manifest ID once and must exactly match the same-generation published `_site/data/index.json`. No report body is ever stored in version-controlled source, in a new D1 table, or sent by the browser as an upload.
- Startup concurrently checks the live authoritative index and loads the static preload manifest/chunks through browser HTTP cache, checks every chunk SHA256 using Web Crypto, and shows honest `Loading cached reports` progress. A report is reused only when its ID and Worker-authored timestamp match the live index; fetch only missing/new report bodies with concurrency bound four. An invalid cache cannot masquerade as complete: refetch from Worker, or present clearly labeled read-only verified offline data when the Worker genuinely cannot be reached. Foreground sync continues every three seconds without re-opening full-page loading.
- A search or select filter change triggers the reference thin sweep along shared presentation cards, honors reduced-motion, never changes evidence or triggers a redundant network reload, and exposes an accessible clear X when text is nonempty. Clearing dispatches the correct real input event, restores all entries and leaves appropriate focus; all custom option searches inspect the complete underlying option set and page by no more than fifty.
- Run source gate, verified generated Pages preload artifact audit, clean extracted ZIP gate, and desktop/mobile Chromium tests with verified preload resulting in zero detail GETs and intentionally corrupted preload recovering through bounded live GETs. Keep staging/source audit and two workflow sources byte-identical. No deployment instructions in ZIP and no remote deployment claim from local tests.


## Release 3.0.10 shared interaction, mobile and storage parity
- Reference behavior is VulkanScope Database 1.4.12; translate names, branding, domain and GL/EGL evidence without inventing Vulkan APIs.
- Each report-view filter searches all native option text, retains focus during typing, caps options at 50/page, shows explicit validated numeric Page/Go controls, Prev/Next, option count, keyboard cross-page controls and an accessible X clear button. Single-page controls are disabled rather than accepting invalid pages. Settings country/time-zone lists receive the reference searchable treatment.
- Reports, bounded cohort tables, Shader Precision and Registry page controls reject zero, decimals, non-numeric and out-of-range page jumps; sizes stay in 10/25/50 where exposed; retain real data and previous/next behavior.
- Match the validated browser gate exactly apart from first-party text and colors, keep overflow-free mobile geometry and reduced-motion respect.
- Match VulkanScope storage consent: no unsolicited cookie banner; explain storage in Settings Information; preferences and favorites are session-only unless Remember on this device is explicitly enabled. Opting out clears stored favorites and preferences; migrate only previously explicit opt-ins. No tracking/analytics cookie, network metadata persistence or reports in localStorage.
- Complete desktop/mobile Chromium interaction and negative source tests, then source/clean ZIP quality gates. Preserve Worker/D1 schema, immutable report IDs, preload integrity and producer gate 2.2.22/2222.

## Release 3.0.11 Overview, terminology, first-party logos and cache/live integrity
- Report Overview renders a standalone reference six-section card grid and must not use the Raw TXT fallback metadata or wrapper; the full 64-character report identity must wrap within every viewport. Raw TXT remains available only from its dedicated tab and canonical export.
- Report Back must be immediately visible, cancel stale detail load transitions, return to the Reports index and restore the saved listing scroll without redundant reset or layout shift.
- All authored, user-visible labels use OpenGL ES and EGL consistently. Preserve OpenGLESScope as the proper project name, the exact returned GL_VERSION/EGL_VERSION values, registry tokens and immutable raw producer text.
- Top-level OpenGL ES and EGL tabs use their already-packaged official white logos with accessible adjacent tab names, aligned on mobile and desktop and self-hosted under the existing CSP.
- Published preloaded reports are used only after SHA256 and authoritative index timestamp verification; missing/new reports are fetched with concurrency <= 4. Startup explicitly labels verified offline snapshot as read-only and never reports live connectivity until the Worker has passed an independent response check. New reports, report index sync every three seconds, asynchronous verified Pages snapshot, staged release switching and genuine offline/checking/unavailable/restored banners are preserved.
- Worker submission gate and D1 schema are immutable. Clean ZIP and both desktop/mobile Overview/Back/logo/cache/release regressions are required.

## Release 3.0.12 retained branding and renderer evidence
- Existing visible OpenGL® ES™ and EGL™ legal branding is preserved; GL_/EGL_ symbols, producer-authored content and upstream trademark strings are never rewritten.
- GL_VENDOR and GL_RENDERER from reports remain canonical, while a separate presentation layer may modernize the exact legacy Google Inc. display label to Google LLC without claiming that the upstream producer returned it.
- ANGLE is identified as a translation layer, not physical GPU; Vulkan versions embedded in GL_RENDERER are displayed only as ANGLE backend evidence and never conflate with GL_VERSION.
- A physical GPU logo is selected only if an explicit known hardware vendor/model appears in submitted evidence; software renderer names do not inherit hardware branding.
- Overview keys and values use the same shared kv .k and kv .v typography and accessible long-value wrapping as the reference.

## Release 3.0.13 cache-first and report presentation parity
- Do not block display of a complete hash-verified published preload on a live index request. Show the current verified cache with an explicit progress bar first, then reconcile new report IDs against the live authoritative index without rerequesting unchanged report bodies.
- Do not use stale or unverified preload data; preserve integrity, identity and server-authored timestamp checks and a safe read-only offline state. No report body is written to opt-in favorites/preferences storage.
- Preserve the originating main view, table page and scroll position when returning from detail, including when opened from Favorites. Avoid forced viewport scrolling to an in-detail navigation button.
- The canonical producer TXT remains available from Raw report; the shared Overview action row includes Download JSON but does not duplicate a Download TXT shortcut.
- Information and Favorites must use shared dependency inventory and card styles with source-backed, qualified version text. Never invent transitive dependency versions, application capabilities, HDR status or vendor/model data.
- Filter icons reflect the selected OpenGL ES/EGL/device/filter category; percent tracks size consistently across viewport widths and preserve the distinction between reported, not listed, unavailable, not applicable and unknown.
- The latest accepted producer is OpenGLESScope 2.2.22 / versionCode 2222. Accept older complete reports as historical reads and do not invent schema fields or mutate D1 historical data.
