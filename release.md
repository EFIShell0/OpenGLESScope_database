# OpenGLESScope Database 0.1.23

OpenGLESScope Database 0.1.23 is a focused Reports-table presentation parity release against VulkanScope Database 0.35.8.

## Reports table

- The Reports header now says **Device** instead of **GPU**, while retaining the same report-backed GPU/device identity content.
- Complete OpenGL ES runtime version strings are presented in compact VulkanScope-style version chips.
- Complete EGL initialized/runtime version strings are presented in the same chip geometry.
- Version chips are single-line and never intentionally stack the version characters vertically. Long values remain accessible through the existing synchronized horizontal table scroller.
- Reports header typography uses the VulkanScope reference color, 12 px size and matching weight.
- Report ID values use the VulkanScope monospace size and normal weight.

## Semantics and compatibility

- No OpenGL ES, EGL, Android Display/HDR or diagnostic state semantics changed.
- Missing or unavailable evidence is not converted to Unsupported.
- Submission schema remains version 2 and technicalReport schema remains version 1.
- Compatible producer floor remains OpenGLESScope 0.1.17+.
- Current producer audit target remains OpenGLESScope 0.1.25.
- Worker normalizer remains version 5.
- No D1 migration or stored-report rewrite is introduced.

## Active assets

- JavaScript: `assets/app.v033.js`
- CSS: `assets/site.v033.css`
- Config cache key: `v=033`

## Validation

- Full database audit
- JavaScript syntax checks
- Worker contract tests
- Static index validation
- ZIP integrity validation
