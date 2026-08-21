# OpenGLESScope Database 0.1.15

OpenGLESScope Database 0.1.15 aligns report-detail tab interaction and the Raw report presentation with the VulkanScope Database quality reference while preserving OpenGL ES-specific semantics and branding.

## Changes

- Report-detail tabs now match the reference control sizing, spacing, sticky container treatment and active-state geometry.
- Switching report tabs uses the same two-stage content transition: a short 105 ms exit followed by a 180 ms eased entrance.
- Active tabs are brought into view inside horizontally scrollable tab strips.
- Keyboard interaction now supports Arrow Left/Right, Home and End with roving tab focus and ARIA tab semantics.
- Raw report now uses the same contained 12 px monospace layout, 1.55 line height, 68 vh maximum height and overflow behavior as the reference database.
- `prefers-reduced-motion` disables nonessential tab transitions.
- Browser-visible frontend assets are cache-busted to v025.

No report schema, D1 migration, submission semantics, OpenGL ES/EGL state semantics, API endpoint, Cloudflare account binding or stored report data is changed.
