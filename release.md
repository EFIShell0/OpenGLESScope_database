# OpenGLESScope Database 0.2.3

OpenGLESScope Database 0.2.3 adds the same design-consistent technical Compare filter as VulkanScope Database.

- `Differences only` remains enabled by default.
- New `Technical differences only` is also enabled by default.
- Application version/versionCode and Collection status/complete/source are hidden only from the technical comparison view.
- ABI, Android/device, driver, OpenGL ES, EGL, limits, extensions, formats, precision, EGL Configs, diagnostics and Display/HDR differences remain visible.
- Compare field/difference/section metrics follow the active technical filter.
- Disabling the technical filter restores producer/collection metadata comparison.
- Database and application versioning remain independent; current producer remains OpenGLESScope 0.2.2.
- Worker normalizer remains 8; no D1 migration or stored-report rewrite is required.
