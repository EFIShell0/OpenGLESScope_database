# OpenGLESScope Database 0.2.1

OpenGLESScope Database 0.2.1 aligns the Reports Android column with VulkanScope: explicit Android security-patch evidence is shown below the Android release/SDK as `Patch YYYY-MM-DD` using the same secondary text treatment.

The schema-2 device object now permits an optional canonical `securityPatch` field. Existing reports and producers that do not contain this field remain valid. The Database never derives or guesses a patch level from SDK, Android version, device identity or submission date.

No OpenGL ES/EGL capability semantics, D1 schema, report-ID hashing or stored-report rewrite is introduced.
