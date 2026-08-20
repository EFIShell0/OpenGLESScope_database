# Build audit

OpenGLESScope Database 0.1.7 was audited as a static frontend plus Cloudflare Worker/D1 release.

## Passed gates

- Frontend JavaScript syntax: PASS
- Worker JavaScript syntax: PASS
- JSON and JSONC parsing: PASS
- HTML local asset resolution: PASS
- Content Security Policy presence: PASS
- Cache-busted production asset references: PASS
- OpenGLESScope 0.1.17-shaped JSON Schema validation: PASS
- Worker health metadata: PASS
- Worker valid POST: PASS
- Worker summary producer-version metadata: PASS
- Worker detail normalization: PASS
- Cross-extension-set consistency rejection: PASS
- CORS rejection: PASS
- 405 Allow behavior: PASS
- Sensitive/source-comment rules: PASS
- Legacy/reference project token scan: PASS
- Static fallback index build: PASS

The database version is independent from the application version.


Branding/title parity in 0.1.7:
- The web header horizontal logo is copied directly from the OpenGLESScope application asset with identical bytes.
- Browser icons use the application GL|ES artwork centered on opaque black.
- Reports uses the base browser title; every other main destination prefixes its navigation label.
- Report detail titles use GPU name, active detail-tab label, then OpenGLESScope Database.

## Branding and title verification
- Application horizontal logo SHA-256: ac879ea07e27b82c82e0562e5ec5c7d1867f8d779ca9d2072fbcd7d2a3121cf9.
- Database horizontal logo SHA-256: ac879ea07e27b82c82e0562e5ec5c7d1867f8d779ca9d2072fbcd7d2a3121cf9.
- Header logo parity: PASS, byte-identical.
- Favicon PNG: 64x64 opaque black background with the application GL|ES artwork in white.
- Apple touch icon: 180x180 opaque black background with the same GL|ES artwork.
- Reports title: OpenGLESScope Database.
- Overview title: Overview - OpenGLESScope Database.
- Main destination title rule: <Visible tab label> - OpenGLESScope Database.
- Report detail title rule: <GPU> - <Visible detail tab label> - OpenGLESScope Database.
- Detail title is refreshed after the full report loads and whenever the detail tab changes.
