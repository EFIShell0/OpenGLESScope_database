# OpenGLESScope Database 0.1.25

OpenGLESScope Database 0.1.25 is a focused UI-parity correction against VulkanScope Database 0.35.8.

## Changes

- Matched the main navigation tab/button geometry to VulkanScope.
- Matched Reports toolbar filter control geometry to VulkanScope.
- Kept Driver mode labels such as `System driver` on one line instead of breaking them inside the cell.
- Added `cd/m²` to available Display/HDR luminance values.
- Removed the extra visible native horizontal table scrollbar so overflowing tables show the same single synchronized custom scrollbar pattern as VulkanScope.
- Added cache-busted `app.v035.js` and `site.v035.css`.

## Unchanged

Report schema, Worker normalization, D1 storage, OpenGL ES/EGL evidence semantics, Android Display/HDR evidence semantics and canonical report preservation are unchanged.


## 0.1.25 presentation parity
- Unified table-header typography and surface treatment with VulkanScope across all database tables.
- Added UI-only canonical vendor/family/ID labels for recognized GL vendor/renderer identities (for example `Qualcomm / Adreno (0x5143)`).
- Rethemed OpenGL ES and EGL version chips with the OpenGLESScope accent while preserving VulkanScope geometry.
- Fixed synchronized horizontal scrollbar endpoint clamping so the thumb reaches the exact end of the track.
- Updated cache-busted frontend assets to `app.v035.js` and `site.v035.css`.
