# OpenGLESScope Database 0.1.7

This release updates the database to the current OpenGLESScope 0.1.17 report contract while keeping application and database release numbers independent.

It tightens Worker schema validation, adds producer-version summary metadata, improves frontend network bounds and error handling, adds Display/HDR submission ordering, strengthens keyboard/overflow navigation and adds state-semantic coverage presentation for limits and diagnostics.

No capability is inferred from GPU branding, a missing extension token or a missing query. The canonical TXT report remains accessible in every report detail.


Branding/title parity in 0.1.7:
- The web header horizontal logo is copied directly from the OpenGLESScope application asset with identical bytes.
- Browser icons use the application GL|ES artwork centered on opaque black.
- Reports uses the base browser title; every other main destination prefixes its navigation label.
- Report detail titles use GPU name, active detail-tab label, then OpenGLESScope Database.
