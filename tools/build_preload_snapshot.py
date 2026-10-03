from __future__ import annotations
import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from build_live_index import build as fetch_index

API = 'https://openglesscope-database-api.openglesscope.workers.dev'
ID = re.compile(r'^[a-f0-9]{64}$')
MAX_RESPONSE = 4 * 1024 * 1024
MAX_CHUNK = 3 * 1024 * 1024
MAX_REPORTS = 100000

def canonical(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).encode('utf-8')

def get_report(api, item):
    rid = item['id']
    request = urllib.request.Request(api + '/v1/reports/' + urllib.parse.quote(rid), headers={'Accept': 'application/json', 'User-Agent': 'OpenGLESScope-Database-preload/3.0.27'})
    last_error = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                if int(response.headers.get('content-length') or 0) > MAX_RESPONSE:
                    raise RuntimeError('Oversized public report')
                raw = response.read(MAX_RESPONSE + 1)
            if len(raw) > MAX_RESPONSE:
                raise RuntimeError('Oversized public report')
            payload = json.loads(raw.decode('utf-8'))
            if not isinstance(payload, dict) or payload.get('id') != rid or payload.get('submittedAt') != item.get('submitted_at'):
                raise RuntimeError('Report identity or authoritative submission timestamp mismatch')
            if payload.get('collectionStatus') == 'incomplete':
                raise RuntimeError('Incomplete report cannot be preloaded')
            return payload
        except (urllib.error.URLError, TimeoutError, OSError, UnicodeError, ValueError, RuntimeError) as error:
            last_error = error
            if isinstance(error, RuntimeError):
                break
            if attempt < 3:
                time.sleep(0.5 * (attempt + 1))
    raise RuntimeError('Unable to verify authoritative public report for cache: ' + type(last_error).__name__)

def build(api, output, expected='', workers=4):
    if not (api.startswith('https://') or api.startswith('http://127.0.0.1:')):
        raise ValueError('HTTPS API required except localhost fixtures')
    snapshot = fetch_index(api, expected)
    index = snapshot['reports']
    if len(index) > MAX_REPORTS or snapshot['schemaVersion'] != 2 or snapshot['databaseVersion'] != '3.0.27':
        raise RuntimeError('Incompatible report-index preload')
    payloads = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, min(8, workers))) as pool:
        futures = {pool.submit(get_report, api, item): item['id'] for item in index}
        for future in concurrent.futures.as_completed(futures):
            rid = futures[future]
            payloads[rid] = future.result()
    output.mkdir(parents=True, exist_ok=True)
    chunks = []
    group = []
    def flush(group):
        if not group:
            return
        content = canonical({'schemaVersion': 1, 'reports': group})
        if len(content) > MAX_CHUNK:
            raise RuntimeError('Preload chunk exceeds 3 MiB')
        sha = hashlib.sha256(content).hexdigest()
        name = 'reports.' + sha[:16] + '.json'
        (output / name).write_bytes(content)
        chunks.append({'file': name, 'sha256': sha, 'byteLength': len(content), 'reportCount': len(group)})
    for item in index:
        report = payloads[item['id']]
        candidate = group + [report]
        if len(canonical({'schemaVersion': 1, 'reports': candidate})) > MAX_CHUNK:
            flush(group)
            group = [report]
        else:
            group = candidate
    flush(group)
    manifest = {'schemaVersion': 1, 'databaseVersion': '3.0.27', 'sourceSchemaVersion': 2,
                'normalizerVersion': 16, 'generatedAt': dt.datetime.now(dt.timezone.utc).isoformat().replace('+00:00', 'Z'),
                'reportCount': len(index), 'generationMode': 'authoritative-public-report-preload',
                'triggerReportId': expected or None, 'reports': index, 'chunks': chunks}
    (output / 'manifest.json').write_bytes(canonical(manifest))
    (output.parent / 'index.json').write_bytes(canonical(snapshot) + b'\n')
    return manifest

def main():
    p = argparse.ArgumentParser()
    p.add_argument('output', type=Path)
    p.add_argument('--api', default=API)
    p.add_argument('--expect-report-id', default='')
    p.add_argument('--expect-attempts', type=int, default=8)
    p.add_argument('--expect-delay', type=float, default=2)
    p.add_argument('--workers', type=int, default=4)
    a = p.parse_args()
    if a.expect_report_id and not ID.fullmatch(a.expect_report_id):
        p.error('Expected lowercase SHA256 ID')
    output = a.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    for old in output.glob('*.json'):
        old.unlink()
    for attempt in range(max(1,min(12,a.expect_attempts))):
        try:
            manifest = build(a.api.rstrip('/'), output, a.expect_report_id, a.workers)
            print('Verified public report preload:', manifest['reportCount'], 'reports in', len(manifest['chunks']), 'chunks')
            return
        except (ValueError, RuntimeError, urllib.error.URLError, TimeoutError, OSError) as exc:
            if attempt + 1 >= max(1,min(12,a.expect_attempts)):
                raise
            time.sleep(max(.25,min(10,a.expect_delay)))

if __name__ == '__main__':
    main()
