# OpenGLESScope Database 0.2.8

- Current audited producer: OpenGLESScope 0.3.4 / versionCode 304.
- Adds a narrow compatibility bridge for the released OpenGLESScope 0.3.3 duplicate count-diagnostic regression.
- Only GL_NUM_EXTENSIONS, GL_NUM_COMPRESSED_TEXTURE_FORMATS, GL_NUM_SHADER_BINARY_FORMATS and GL_NUM_PROGRAM_BINARY_FORMATS may appear exactly twice for producer 0.3.3, and only with identical status/detail.
- Arbitrary or conflicting duplicates remain rejected; 0.3.4+ requires strict diagnostic uniqueness.
- Fixes stale /v1/reports currentProducer metadata.
- No D1 migration or stored-report rewrite.
