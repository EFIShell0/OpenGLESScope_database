# OpenGLESScope Database

OpenGLESScope Database is the public, report-backed browser for OpenGLESScope OpenGL ES, EGL and Android Display/HDR evidence.

## Current database release

- Database: `0.2.8`
- Compatible producer floor: OpenGLESScope `0.1.17+` within compatible `0.x` schema-2 / technical-report-1 releases
- Current producer: OpenGLESScope `0.3.3` / versionCode `303`
- Submission schema: `2`
- Technical report schema: `1`
- Worker normalizer: `9`
- Frontend JavaScript: `app.v041.js`
- Frontend CSS: `site.v036.css`

Application and database versions are intentionally independent.

## Compare

Compare provides `Differences only` and a design-consistent `Technical differences only` filter. Technical mode is enabled by default and removes application-version/versionCode and collection-state/source noise while retaining ABI, Android/device, driver, OpenGL ES, EGL and all capability/query evidence. The filter is presentation-only and never rewrites stored reports.

## Public endpoints

- Website: `https://efishell0.github.io/OpenGLESScope_database/`
- API: `https://openglesscope-database-api.openglesscope.workers.dev`
- Application repository: `https://github.com/EFIShell0/OpenGLESScope`
- Database repository: `https://github.com/EFIShell0/OpenGLESScope_database`

## Data and security model

The database preserves the complete structured report and canonical TXT snapshot. Runtime extension tokens and query diagnostics remain exact. API failures are explicit. Report submission remains explicit, bounded and schema-validated; personal/account/authentication identifiers and request-IP persistence remain forbidden.
