import argparse
import concurrent.futures
import hashlib
import urllib.parse
import json
import re
import sys
import time
import urllib.request
from urllib.parse import urlencode

ID=re.compile(r'^[0-9a-f]{64}$')
PUBLISHED='https://efishell0.github.io/OpenGLESScope_database/data/index.json'
MAX_INDEX=64*1024*1024

def fetch(id):
    q=urlencode({'report':id,'audit':int(time.time())})
    request=urllib.request.Request(PUBLISHED+'?'+q,headers={'Accept':'application/json','Cache-Control':'no-cache','User-Agent':'OpenGLESScope-Database-snapshot-verifier'})
    with urllib.request.urlopen(request,timeout=20) as response:
        if int(response.headers.get('content-length') or 0)>MAX_INDEX:
            raise RuntimeError('Published snapshot is oversized')
        raw=response.read(MAX_INDEX+1)
        if len(raw)>MAX_INDEX:raise RuntimeError('Published snapshot is oversized')
    payload=json.loads(raw.decode('utf-8'))
    if not isinstance(payload,dict) or payload.get('schemaVersion')!=2 or payload.get('databaseVersion')!='3.0.30' or not isinstance(payload.get('reports'),list):
        raise RuntimeError('Published artifact is not current schema-2 release')
    return any(isinstance(row,dict) and row.get('id')==id for row in payload['reports'])

def verify_preload(attempts=12, interval=3):
    """Verify the *published* authoritative cache, not merely the source tree or index."""
    base=PUBLISHED.rsplit('/index.json',1)[0]
    last='unavailable'
    def bounded_json(url, max_bytes=4*1024*1024):
        request=urllib.request.Request(url,headers={'Accept':'application/json','Cache-Control':'no-cache','User-Agent':'OpenGLESScope-Database-published-cache-verifier/3.0.30'})
        with urllib.request.urlopen(request,timeout=25) as response:
            raw=response.read(max_bytes+1)
        if len(raw)>max_bytes:raise RuntimeError('Published cache object exceeds size budget')
        return raw,json.loads(raw.decode('utf-8'))
    for attempt in range(max(1,attempts)):
        try:
            nonce=int(time.time()*1000)
            _,index=bounded_json(PUBLISHED+'?preload-audit='+str(nonce),64*1024*1024)
            _,manifest=bounded_json(base+'/preload/manifest.json?preload-audit='+str(nonce),8*1024*1024)
            if index.get('databaseVersion')!='3.0.30' or manifest.get('databaseVersion')!='3.0.30':
                raise RuntimeError('Published index/cache release mismatch')
            summaries=index.get('reports'); cached=manifest.get('reports'); parts=manifest.get('chunks')
            if not isinstance(summaries,list) or not isinstance(cached,list) or not isinstance(parts,list) or summaries!=cached:
                raise RuntimeError('Published index and cache manifest disagree')
            if manifest.get('reportCount')!=len(summaries):raise RuntimeError('Published manifest report count mismatch')
            ids={r['id']:r['submitted_at'] for r in summaries}
            if len(ids)!=len(summaries):raise RuntimeError('Duplicate report identifier in published index')
            def check_chunk(meta):
                file=meta['file'];digest=meta['sha256'];n=meta['byteLength']
                if not re.fullmatch(r'reports\.[a-f0-9]{16}\.json',str(file)) or not re.fullmatch(r'[a-f0-9]{64}',str(digest)) or file!='reports.'+digest[:16]+'.json':
                    raise RuntimeError('Published cache chunk naming invalid')
                raw,obj=bounded_json(base+'/preload/'+urllib.parse.quote(file)+'?preload-audit='+str(nonce),3145728)
                if len(raw)!=n or hashlib.sha256(raw).hexdigest()!=digest:raise RuntimeError('Published cache checksum mismatch')
                rows=obj.get('reports')
                if obj.get('schemaVersion')!=1 or not isinstance(rows,list) or len(rows)!=meta['reportCount']:
                    raise RuntimeError('Published cache chunk schema mismatch')
                return [(entry['id'],entry['submittedAt']) for entry in rows]
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
                groups=list(pool.map(check_chunk,parts))
            seen={}
            for group in groups:
                for rid,timestamp in group:
                    if rid not in ids or rid in seen or ids[rid]!=timestamp:raise RuntimeError('Published cache report identity mismatch')
                    seen[rid]=1
            if len(seen)!=len(ids):raise RuntimeError('Published cache missing one or more report bodies')
            print('Published verified preload:',len(ids),'reports in',len(parts),'SHA-256 checked chunks')
            return True
        except Exception as error:
            last=type(error).__name__+': '+str(error)[:160]
            if attempt+1<max(1,attempts):time.sleep(interval)
    raise RuntimeError('Published cache verification failed: '+last)

def verify(id,attempts=12,interval=10):
    if not ID.fullmatch(id):raise ValueError('Expected a lowercase 64-hex report ID')
    last=''
    for n in range(attempts):
        try:
            if fetch(id):return True
            last='Report not yet visible in published Pages index'
        except Exception as e:last=type(e).__name__+': '+str(e)[:180]
        if n+1<attempts:time.sleep(interval)
    raise RuntimeError('Published snapshot verification failed: '+last)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--expect-report-id',default='')
    parser.add_argument('--verify-preload',action='store_true')
    args=parser.parse_args()
    if not args.expect_report_id and not args.verify_preload: parser.error('expected report ID or --verify-preload required')
    if args.expect_report_id:
        verify(args.expect_report_id)
        print('Published Pages snapshot contains the exact accepted report ID: PASS')
    if args.verify_preload:verify_preload()
