# OpenGLESScope Database 0.1.14

OpenGLESScope Database 0.1.14 makes Reports the database home view and aligns report-list pagination/loading behavior with the VulkanScope Database quality reference.

## Changes

- Removed the Overview navigation destination.
- Reports is now the first navigation item and the root/default view.
- Report index requests use a 500-row server cursor batch and follow every returned cursor until completion.
- Repeated cursors fail explicitly rather than silently truncating the visible database.
- Visible report pages remain capped at 50 rows.
- Per-page choices are 10, 25 and 50, with 25 as the default.
- Search, filters and sorting are applied before visible pagination.
- Submission timestamps remain server-authored and include seconds/timezone in presentation.
- Report toolbar and mobile behavior are aligned with the VulkanScope Database reference.
- No schema or D1 migration change.

## Compatibility

- Schema: 2
- Technical report schema: 1
- Compatible producer: OpenGLESScope 0.1.x
