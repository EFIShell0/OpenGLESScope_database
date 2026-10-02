import argparse
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
    if not isinstance(payload,dict) or payload.get('schemaVersion')!=2 or payload.get('databaseVersion')!='3.0.1' or not isinstance(payload.get('reports'),list):
        raise RuntimeError('Published artifact is not current schema-2 release')
    return any(isinstance(row,dict) and row.get('id')==id for row in payload['reports'])

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
    parser.add_argument('--expect-report-id',required=True)
    args=parser.parse_args()
    verify(args.expect_report_id)
    print('Published Pages snapshot contains the exact accepted report ID: PASS')
