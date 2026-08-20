CREATE TABLE IF NOT EXISTS reports (
  id TEXT PRIMARY KEY,
  submitted_at TEXT NOT NULL,
  schema_version INTEGER NOT NULL,
  gpu_name TEXT NOT NULL,
  vendor TEXT NOT NULL,
  opengles_version TEXT NOT NULL,
  egl_version TEXT NOT NULL,
  manufacturer TEXT NOT NULL,
  model TEXT NOT NULL,
  payload_json TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_reports_submitted_id ON reports(submitted_at DESC,id DESC);
