# OpenGLESScope Database 2.0.2

## 2.0.2

### Added
- Ordered D1 payload chunks for large canonical reports, integrity-checked reads and migration 0004.
- Request-scoped Internet diagnostics on an explicit Settings button; no background IP lookup or persistence.
- Dedicated publication security/negative mutation tests for release and snapshot paths.

### Changed
- Snapshot dispatch retries transient failures with fixed bounds; permanent failures stop immediately.
- Release and snapshot jobs have separate workflows within one serialized Pages publication group.
- Live synchronization derives report count and latest identity in one D1 observation.
- Existing inline reports, 16 workspaces and exact 2.2.22 producer contract remain unchanged.

## 2.0.1 (previous)

### Added
- Reference-derived 250-country searchable selectors with a 50-choice render cap; selected-country IANA time zone preview.
- Regional date/time Preferences (automatic, country, manual, IANA time zone, date and clock format, seasonal display), with a live preview.
- Explicit submission ISO and raw vendor report table presentation toggles; preference state remains opt-in local only.
- Scroll progress, connection state and additional browser/build information.
- Live filter-count feedback and expanded evidence policy/independence disclosures.

### Changed
- Settings grouping, responsive grid, shared tab presentation and animation/reduced-motion treatments.
- Page number validation for report and Encyclopedia pagination.
- Versioned Pages assets and Worker handshake, without changing canonical report storage or producer compatibility.

