# OpenGLESScope Database 0.7.0

OpenGLESScope Database 0.7.0 is the companion release for OpenGLESScope 0.7.0 and its expanded EGL/runtime technical report.

- Current validated producer: OpenGLESScope 0.7.0 / versionCode 700.
- Submission envelope remains schema 2.
- Current producer technicalReport advances to schema 2; compatible historical producers retain technicalReport schema 1.
- Normalizer version advances to 10.
- Adds fail-closed validation for EGL runtime context/display/surface binding evidence.
- Adds validation, Report Detail and Compare support for expanded EGL Config fields and exact unavailable-attribute evidence.
- EGL extension-backed config fields require their exact prerequisite extension token.
- Preserves Common evidence only, technical-differences filtering and cross-producer comparison warnings.
- Keeps one-sided absent evidence Unknown / Not reported; Database does not manufacture Unsupported results.
- Removes synthetic PCI/Vulkan-style vendor-ID presentation; submitted GL_VENDOR/GL_RENDERER evidence remains authoritative.
- Uses current cache-busted frontend assets `app.v070.js` and `site.v070.css`.
- Preserves schema-2 canonical SHA-256 report identity, D1 schema/data, 2 MiB bounds, sensitive-field rejection, CORS/CSP and explicit submission semantics.
- No D1 migration or stored-report rewrite is required.
