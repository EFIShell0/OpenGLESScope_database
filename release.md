# OpenGLESScope Database 0.1.9

This maintenance release hardens repository hygiene and Cloudflare multi-account isolation.

The production Worker configuration is pinned to the dedicated OpenGLESScope Cloudflare account and D1 database. Wrangler auth profiles remain local to each machine and directory; the committed `account_id` is the fail-closed account guard. Repository ignore rules exclude dependencies, local Wrangler state, credentials, environment files, logs and generated caches.

No D1 migration is required from 0.1.7. Frontend behavior, report schema, title behavior and branding assets are unchanged.


## 0.1.9 UI parity
- Added semantic local SVG icons to every main navigation destination.
- Added compact icon-bearing custom filters with selected-option checkmarks and viewport-aware listboxes.
- Matched filter height, spacing, mobile layout, focus visibility, detail tabs, pagination and table-scroll affordances to the project quality baseline.
- Added Windows-safe fail-closed Cloudflare account verification before production D1 and deploy operations.
