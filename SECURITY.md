# OpenGLESScope Database 3.0.10 Security Contract

The Worker accepts only audited OpenGLESScope producers up to exact 2.2.22 / versionCode 2222, schema 2 and the version-scoped technical report contracts (current technicalReport schema 5). Historical read compatibility is preserved without silently accepting unaudited new producers. Runtime GL/EGL data is validated from submission evidence rather than inferred from registry entries.

New submissions have a 2 MiB streaming body limit, fatal UTF-8 decoding, canonical stable JSON SHA-256 identity, 4 MiB canonical retrieval guard, bounded arrays and nesting, strict data-shape and sensitive-key gates, fixed Pages-origin CORS, restrictive no-store/nosniff headers and method-specific 405 Allow responses.

The public Pages artifact contains only audited static assets and first-party public report summaries. New large canonical reports use D1 migration 0004 for ordered, atomic chunks; reads require a contiguous sequence and the original SHA-256 digest. No existing report row is rewritten by the migration. Worker/Pages version checks are fail-closed.

Cloudflare account/D1 identifiers are deployment identity guards, not client secrets. Snapshot dispatch credentials are provided only as Cloudflare Worker secrets, never committed or included in report data. Production deployment, third-party vulnerability advisories and actual Cloudflare responses require independent production verification.

## 3.0.10 storage and snapshot boundaries
- Install D1 migration 0004 before Worker deployment to enable large-payload chunks. D1 batch insertion must remain atomic.
- GitHub snapshot tokens are Worker secrets only. The dispatch path retries only temporary failures, and workflow source always independently verifies both the accepted ID and staged public summary.
- Public Pages snapshots contain allowlisted summary fields only. Raw canonical report content remains served exclusively by report-ID Worker lookup with no-store and integrity verification.

- Internet Settings network diagnostics are requested only on an explicit click and cleared on drawer close. The no-store `/v1/network-info` response is request-scoped, not persisted to reports, favorites, D1 or Pages, and the browser does not use remote geolocation, analytics or IP lookup services.
