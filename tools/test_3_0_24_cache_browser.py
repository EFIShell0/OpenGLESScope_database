"""Chromium integration: independently verified SHA256 bytes + 73-report cache.
Not part of quality_gate on CI, because hosted Actions do not install Playwright/Chromium.
"""
from pathlib import Path
import json, subprocess, sys, tempfile, threading, time, urllib.parse, hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
all_summaries=[];all_details={}
for i in range(75):
    rid=f'{i+1:064x}'
    row={'id':rid,'submitted_at':f'2026-10-03T12:{i//60:02d}:{i%60:02d}.000Z',
         'schema_version':2,'gpu_name':f'Cached GPU {i+1}','vendor':'Qualcomm',
         'manufacturer':'Verified Test','model':f'Device {i+1}',
         'opengles_version':'OpenGL ES 3.2','egl_version':'1.5',
         'application_version':'3.0.4','application_version_code':3004}
    all_summaries.append(row)
    all_details[rid]={**row,'submittedAt':row['submitted_at'],
        'gpu':{'name':row['gpu_name'],'vendor':'Qualcomm'},
        'device':{'manufacturer':'Verified Test','model':row['model'],'androidRelease':'15'},
        'application':{'version':'3.0.4','versionCode':3004},
        'driver':{'mode':'System','version':'Unavailable'},
        'opengles':{'version':'OpenGL ES 3.2','extensions':['GL_KHR_debug']},
        'egl':{'initializedVersion':'1.5','vendor':'Test Vendor','extensions':[]},
        'collection':{'status':'available','complete':True},
        'technicalReport':{'schemaVersion':5,'limits':[],'extensions':['GL_KHR_debug'],
           'eglExtensions':[],'eglClientExtensions':[],'compressedFormats':[],
           'shaderBinaryFormats':[],'programBinaryFormats':[],'precision':[],
           'queryDiagnostics':[],'eglConfigs':[],'display':{}},
        'reportText':'PUBLIC VERIFICATION SNAPSHOT\n'+('RUNTIME ONLY '+str(i)+'\n')*4300}

health={'status':'ok','schemaVersion':2,'technicalReportSchema':5,'normalizerVersion':16,
        'currentProducer':'OpenGLESScope 3.0.4','databaseVersion':'3.0.24'}
def idx(n):return {'schemaVersion':2,'normalizerVersion':16,'databaseVersion':'3.0.24',
                   'currentProducer':'OpenGLESScope 3.0.4','reports':all_summaries[:n],
                   'nextCursor':None}
def sync(n):return {'databaseReleaseVersion':'3.0.24','workerReleaseVersion':'3.0.24',
                    'reportCount':n,'latestReportId':all_summaries[n-1]['id'],
                    'latestSubmittedAt':all_summaries[n-1]['submitted_at'],'syncToken':f'{n}:test'}
class Handler(SimpleHTTPRequestHandler):
    stage=None
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(self.stage),**kwargs)
    def do_GET(self):
        path=urllib.parse.urlsplit(self.path).path
        if path.startswith('/v1/'):
            if path=='/v1/reports': data=idx(73)
            elif path=='/v1/health': data=health
            elif path=='/v1/sync': data=sync(73)
            elif path.startswith('/v1/reports/'):
                data=all_details.get(path.rsplit('/',1)[-1],{})
            else:data={}
            raw=json.dumps(data,separators=(',',':'),ensure_ascii=False).encode()
            self.send_response(200);self.send_header('content-type','application/json')
            self.send_header('content-length',str(len(raw)));self.end_headers();self.wfile.write(raw)
            return
        if '/data/preload/reports.' in path:time.sleep(.15)
        return super().do_GET()
    def log_message(self,*args):pass

def run():
    with tempfile.TemporaryDirectory(prefix='ogs-cache24-browser-') as tmp:
        stage=Path(tmp)/'site'
        subprocess.run([sys.executable,'-B',str(ROOT/'tools/build_pages_artifact.py'),str(stage)],check=True,cwd=ROOT)
        Handler.stage=stage
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        base=f'http://127.0.0.1:{server.server_port}'
        try:
            sys.path.insert(0,str(ROOT/'tools'))
            from build_preload_snapshot import build
            cached=build(base,stage/'data/preload')
            assert cached['reportCount']==73 and len(cached['chunks'])>=2,cached
            subprocess.run([sys.executable,'-B',str(ROOT/'tools/audit_database.py'),
                            '--artifact-tree',str(stage),'--require-preload'],check=True,cwd=ROOT)
            source=(ROOT/'tools/test_3_0_0_live_browser.py').read_text(encoding='utf-8')
            ns={'__file__':str(ROOT/'tools/test_3_0_0_live_browser.py')}
            exec(source.split('with sync_playwright() as p:',1)[0],ns)
            chunks={}
            for part in cached['chunks']:
                data=(stage/'data/preload'/part['file']).read_bytes()
                assert hashlib.sha256(data).hexdigest()==part['sha256']
                chunks[part['file']]={'raw':data.decode('utf-8'),'sha':part['sha256']}
            manifest=(stage/'data/preload/manifest.json').read_text(encoding='utf-8')
            with sync_playwright() as p:
                browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
                for n,width,height in [(73,1440,900),(75,390,844)]:
                    context=browser.new_context(viewport={'width':width,'height':height})
                    page=context.new_page(); errors=[]
                    page.on('pageerror',lambda e:errors.append(str(e)))
                    injected=r"""<script>(()=>{
                        window.OPENGLESSCOPE_DATABASE_API='https://openglesscope-database-api.openglesscope.workers.dev';
                        const CHUNKS=MOCK_CHUNKS,MANIFEST=MOCK_MANIFEST,INDEX=MOCK_INDEX,DETAILS=MOCK_DETAILS;
                        window.__reportDetailCalls=[];
                        Object.defineProperty(window.crypto,'subtle',{configurable:true,value:{digest:async(algorithm,buffer)=>{
                          const raw=new TextDecoder('utf-8').decode(buffer);
                          const verified=Object.values(CHUNKS).find(x=>x.raw===raw);
                          const sha=verified?verified.sha:'0'.repeat(64);
                          return Uint8Array.from(sha.match(/../g).map(x=>parseInt(x,16))).buffer;
                        }}});
                        window.fetch=async input=>{
                          const u=String(input);
                          let data={};
                          if(u.includes('data/preload/manifest.json'))return new Response(MANIFEST,{status:200,headers:{'content-type':'application/json'}});
                          if(u.includes('data/preload/reports.')){
                            const name=u.match(/reports\.[a-f0-9]{16}\.json/)?.[0];
                            const chunk=CHUNKS[name];if(!chunk)return new Response('Not found',{status:404});
                            await new Promise(resolve=>setTimeout(resolve,100));
                            return new Response(chunk.raw,{status:200,headers:{'content-type':'application/json'}});
                          }
                          if(/\/v1\/reports\/[a-f0-9]{64}/.test(u)){
                            const id=u.match(/\/v1\/reports\/([a-f0-9]{64})/)[1];
                            window.__reportDetailCalls.push(id);data=DETAILS[id]||{};
                          } else if(u.includes('/v1/reports?'))data=INDEX;
                          else if(u.includes('/v1/health'))data=MOCK_HEALTH;
                          else if(u.includes('/v1/sync'))data=MOCK_SYNC;
                          else if(u.includes('/v1/network-info'))data={networkInfoVersion:1};
                          else if(u.includes('data/release.json'))data=MOCK_RELEASE;
                          else if(u.includes('data/index.json'))data=INDEX;
                          else if(u.includes('registry-catalog'))data=MOCK_CATALOG;
                          else if(u.includes('/licenses/'))return new Response(MOCK_NOTICE,{status:200,headers:{'content-type':'text/plain'}});
                          return new Response(JSON.stringify(data),{status:200,headers:{'content-type':'application/json'}});
                        };
                    })();</script>"""
                    defs=[('MOCK_CHUNKS',chunks),('MOCK_MANIFEST',manifest),('MOCK_INDEX',idx(n)),
                          ('MOCK_DETAILS',all_details),('MOCK_HEALTH',health),('MOCK_SYNC',sync(n)),
                          ('MOCK_RELEASE',json.loads((stage/'data/release.json').read_text())),
                          ('MOCK_CATALOG',json.loads((ROOT/'data/registry-catalog.v2000.json').read_text())),
                          ('MOCK_NOTICE',(ROOT/'licenses/openglesscope-application-mit.md').read_text())]
                    for key,value in defs:injected=injected.replace(key,json.dumps(value,ensure_ascii=False))
                    html=ns['html'].replace(ns['mock'],injected)
                    assert html!=ns['html']
                    page.set_content(html,wait_until='domcontentloaded',timeout=40000)
                    page.wait_for_function("document.body.classList.contains('startup-layout-ready')",timeout=30000)
                    page.wait_for_function(f"window.__OGS30__?.getCount?.()==={n}",timeout=30000)
                    page.wait_for_timeout(500)
                    calls=page.evaluate('window.__reportDetailCalls')
                    assert len(calls)==n-73,(n,len(calls),calls[:2],errors[:3])
                    assert len(set(calls))==len(calls),('Repeated report body request',calls)
                    assert not errors,errors
                    print(f'CHROMIUM SHA-VERIFIED CACHE {width}x{height}: published=73, live={n}, individual API calls={len(calls)} PASS')
                    context.close()
                browser.close()

        finally:
            server.shutdown();server.server_close();thread.join(timeout=3)
if __name__=='__main__':run()
