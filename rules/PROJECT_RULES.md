# OpenGLESScope Database Engineering Rules

## Non-negotiable
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
- Application and database versions are independent. The database accepts compatible OpenGLESScope 0.1.x producers rather than requiring version equality.
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
- Detail tabs include Summary, OpenGL ES, EGL, Extensions, Limits, Formats, Precision, EGL Configs, Display/HDR, Diagnostics and Raw report.
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
