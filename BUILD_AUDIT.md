# OpenGLESScope Database 0.1.8 build audit

Release focus: repository hygiene and Cloudflare multi-account isolation.

- Production Cloudflare account is pinned in worker/wrangler.jsonc.
- Production D1 UUID is pinned in worker/wrangler.jsonc.
- Binding remains DB and ALLOWED_ORIGIN remains https://efishell0.github.io.
- Wrangler auth-profile credentials/bindings are not committed; the profile is expected to be bound locally to worker/.
- Root .gitignore excludes node_modules, Wrangler local state, environment/secret files, logs, Python caches and OS metadata.
- Wrangler dependency is pinned to 4.124.0.
- No D1 migration or report-schema change is introduced.
- Worker health metadata reports database version 0.1.8.
- Frontend assets are unchanged and retain v017 cache-busted names.
