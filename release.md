# OpenGLESScope Database 0.1.8

This maintenance release hardens repository hygiene and Cloudflare multi-account isolation.

The production Worker configuration is pinned to the dedicated OpenGLESScope Cloudflare account and D1 database. Wrangler auth profiles remain local to each machine and directory; the committed `account_id` is the fail-closed account guard. Repository ignore rules exclude dependencies, local Wrangler state, credentials, environment files, logs and generated caches.

No D1 migration is required from 0.1.7. Frontend behavior, report schema, title behavior and branding assets are unchanged.
