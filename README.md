# OpenGLESScope Database

OpenGLESScope Database is the public, report-backed browser for OpenGLESScope OpenGL ES, EGL and Android Display/HDR evidence.

## Current database release

- Database: 0.1.9
- Compatible producer line: OpenGLESScope 0.1.x
- Compatibility audit target: OpenGLESScope 0.1.17
- Submission schema: 2
- Technical report schema: 1
- Worker normalizer: 3

Application and database versions are intentionally independent.

## Public endpoints

- Website: `https://efishell0.github.io/OpenGLESScope_database/`
- API: `https://openglesscope-database-api.openglesscope.workers.dev`
- Application repository: `https://github.com/EFIShell0/OpenGLESScope`
- Database repository: `https://github.com/EFIShell0/OpenGLESScope_database`

## Data model

The database preserves the complete structured report and canonical TXT snapshot submitted by the application. OpenGL ES, GLSL ES, EGL and Android platform/display evidence remain separate. Runtime extension tokens are preserved verbatim. Query state keeps Available, Unavailable, Not applicable and Unknown distinct.

Structured detail includes OpenGL ES/EGL identity, exact GL/EGL extension sets, implementation limits, compressed and binary formats, shader precision, query diagnostics, complete EGL configuration attributes and Android Display/HDR evidence.

## Frontend quality floor

The frontend uses no third-party scripts, analytics, remote fonts or advertising dependencies. It provides keyboard-accessible navigation and controls, cache-busted local assets, responsive table/navigation overflow controls, deterministic 50-row report pagination, exact comparison, explicit state-semantic coverage, Display/HDR ordering and canonical raw-report access.

## Submission and privacy

Reports are uploaded only after an explicit application action. Request bodies are bounded to 2 MiB and are never truncated. Personal identifiers, account/authentication fields, request IP data and private paths are forbidden report fields. IDs are SHA-256 hashes of stable canonical JSON and submission time is authored by the server-side database.

See `SECURITY.md` and `rules/PROJECT_RULES.md` for the security and correctness contract.


Branding/title parity in 0.1.7:
- The web header horizontal logo is copied directly from the OpenGLESScope application asset with identical bytes.
- Browser icons use the application GL|ES artwork centered on opaque black.
- Reports uses the base browser title; every other main destination prefixes its navigation label.
- Report detail titles use GPU name, active detail-tab label, then OpenGLESScope Database.


## Cloudflare account isolation

This release pins the production Worker to Cloudflare account `6881527e6e0b9bc4a0c009473428d1bc` and D1 database `2c945dda-e320-4b3a-9fac-a086373db17c` in `worker/wrangler.jsonc`. Keep the `openglesscope` Wrangler auth profile bound to the `worker` directory. The `account_id` pin is the fail-closed guard that prevents an authenticated profile for another Cloudflare account from deploying this Worker into that account.

Local setup files, credentials, caches and dependencies are excluded by the repository `.gitignore`. `node_modules` must never be committed. `package-lock.json` may be committed after `npm install` generates it locally.

Recommended local commands from `worker/`:

```text
npm install
npm run auth:create
npm run auth:activate
npm run auth:status
npm run migrate
npm run deploy
```

`auth:create` is needed only once per machine/profile. Normal future deployments use the directory-bound profile automatically.


## 0.1.9 UI parity
- Added semantic local SVG icons to every main navigation destination.
- Added compact icon-bearing custom filters with selected-option checkmarks and viewport-aware listboxes.
- Matched filter height, spacing, mobile layout, focus visibility, detail tabs, pagination and table-scroll affordances to the project quality baseline.
- Added Windows-safe fail-closed Cloudflare account verification before production D1 and deploy operations.
