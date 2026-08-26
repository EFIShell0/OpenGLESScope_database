# OpenGLESScope Database 0.7.3 Build / Release Audit

- Database version: 0.7.3
- Current producer: OpenGLESScope 0.7.2 / versionCode 702
- Submission schema: 2
- Current technicalReport schema: 2
- Normalizer: 10
- D1 schema: unchanged
- Browser assets: app.v073.js / site.v073.css
- Compatibility floor: OpenGLESScope 0.1.17
- Compatibility ceiling: OpenGLESScope 0.7.2

0.7.3 corrects the Compare control-layout regression by isolating dedicated boolean-toggle styling from generic text/search form rules and by restoring the shared compact control hierarchy: report selectors plus boolean toggles in the primary row, Section and Field search in a secondary subfilter row, and Share comparison link as a separate action.

The release gates source/archive hygiene, routing, exact missing-evidence semantics, Compare contract and layout isolation, Statistics/filter behavior, Worker producer validation, repository state and a freshly staged Pages artifact. D1 storage, normalizer 10, canonical report IDs/hashes and historical producer contracts remain unchanged.
