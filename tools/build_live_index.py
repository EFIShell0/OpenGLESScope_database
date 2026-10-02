"""Build a bounded, authoritative read-only Pages summary snapshot from the live Worker.

No report body, request IP, tokens or private identifiers are embedded in the artifact.
Snapshot mode verifies the triggering report is visible; failure aborts Pages deployment.
"""
import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

API = 'https://openglesscope-database-api.openglesscope.workers.dev'
ID = re.compile(r'^[0-9a-f]{64}$')
MAX_REPORTS = 100000
MAX_RESPONSE = 4 * 1024 * 1024
ALLOWED = ('id', 'submitted_at', 'schema_version', 'gpu_name', 'vendor', 'opengles_version',
           'egl_version', 'manufacturer', 'model', 'application_version', 'application_version_code')

def fetch(url):
    req = urllib.request.Request(url, headers={'Accept': 'application/json', 'User-Agent': 'OpenGLESScope-Database-3.0.4-snapshot'})
    with urllib.request.urlopen(req, timeout=25) as response:
        if int(response.headers.get('content-length') or 0) > MAX_RESPONSE:
            raise RuntimeError('Oversized index response')
        raw = response.read(MAX_RESPONSE + 1)
        if len(raw) > MAX_RESPONSE:
            raise RuntimeError('Oversized index response')
    return json.loads(raw.decode('utf-8'))

def build(api, expected):
    if not api.startswith('https://') and not api.startswith('http://127.0.0.1:'):
        raise ValueError('Expected HTTPS API (localhost permitted only for fixtures)')
    rows = []
    seen_ids, seen_cursors = set(), set()
    cursor = None
    while True:
        params = {'limit': '500'}
        if cursor:
            key = (cursor.get('submittedAt'), cursor.get('id'))
            if key in seen_cursors or not isinstance(key[0], str) or not ID.fullmatch(str(key[1])):
                raise ValueError('Invalid or repeated Worker cursor')
            seen_cursors.add(key)
            params.update(beforeSubmittedAt=key[0], beforeId=key[1])
        page = fetch(api + '/v1/reports?' + urllib.parse.urlencode(params))
        if page.get('schemaVersion') != 2 or page.get('databaseVersion') != '3.0.4' or page.get('currentProducer') != 'OpenGLESScope 2.2.22' or page.get('normalizerVersion') != 16 or not isinstance(page.get('reports'), list):
            raise ValueError('Incompatible report index schema')
        for source in page['reports']:
            if not isinstance(source, dict) or set(source) - set(ALLOWED) or not ID.fullmatch(str(source.get('id', ''))):
                raise ValueError('Invalid or private report summary')
            if source['id'] in seen_ids:
                raise ValueError('Duplicate report identifier')
            seen_ids.add(source['id'])
            rows.append({key: source[key] for key in ALLOWED if key in source})
        if len(rows) > MAX_REPORTS:
            raise ValueError('Snapshot report count exceeds explicit bound')
        cursor = page.get('nextCursor')
        if not cursor:
            break
        if not page['reports']:
            raise ValueError('Non-advancing report cursor')
    if expected and expected not in seen_ids:
        raise ValueError('Expected accepted report is not yet present in authoritative Worker list')
    return {'schemaVersion': 2, 'databaseVersion': '3.0.4', 'normalizerVersion': 16,
            'currentProducer': 'OpenGLESScope 2.2.22', 'reports': rows,
            'source': 'authoritative-worker-summary-snapshot', 'reportCount': len(rows)}

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('output', type=Path)
    p.add_argument('--api', default=API)
    p.add_argument('--expect-report-id', default='')
    a = p.parse_args()
    if a.expect_report_id and not ID.fullmatch(a.expect_report_id):
        p.error('Expected report ID must be lowercase 64-hex')
    snapshot = build(a.api.rstrip('/'), a.expect_report_id)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(snapshot, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    print('Validated authoritative live summary snapshot:', snapshot['reportCount'], 'reports')
