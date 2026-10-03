from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile
import threading
import urllib.parse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
summaries=[]
details={}
for i in range(7):
    rid=f'{i+1:064x}'
    row={'id':rid,'submitted_at':f'2026-10-02T10:{i:02d}:00.000Z','schema_version':2,'gpu_name':f'Cached GPU {i+1}','vendor':'Qualcomm','manufacturer':'Test Vendor','model':f'Device {i+1}','opengles_version':'OpenGL ES 3.2','egl_version':'1.5','application_version':'2.2.22','application_version_code':2222}
    summaries.append(row)
    details[rid]={**row,'submittedAt':row['submitted_at'],'gpu':{'name':row['gpu_name'],'vendor':'Qualcomm'},'device':{'manufacturer':'Test Vendor','model':row['model'],'androidRelease':'15'},'application':{'version':'2.2.22','versionCode':2222},'driver':{'mode':'System','version':'1.0'},'opengles':{'version':'OpenGL ES 3.2','extensions':[]},'egl':{'initializedVersion':'1.5','vendor':'Test Vendor','extensions':[]},'technicalReport':{'limits':[],'extensions':[],'eglExtensions':[],'eglClientExtensions':[],'compressedFormats':[],'shaderBinaryFormats':[],'programBinaryFormats':[],'precision':[],'queryDiagnostics':[],'eglConfigs':[],'display':{}},'reportText':'PUBLIC TEST REPORT'}
index={'schemaVersion':2,'normalizerVersion':16,'databaseVersion':'3.0.23','currentProducer':'OpenGLESScope 3.0.4','reports':summaries,'nextCursor':None}
sync={'databaseReleaseVersion':'3.0.23','workerReleaseVersion':'3.0.23','reportCount':7,'latestReportId':summaries[0]['id'],'latestSubmittedAt':summaries[0]['submitted_at'],'syncToken':'7:mock'}
health={'status':'ok','schemaVersion':2,'technicalReportSchema':5,'normalizerVersion':16,'currentProducer':'OpenGLESScope 3.0.4','databaseVersion':'3.0.23'}
def payload(url):
    path=urllib.parse.urlsplit(url).path
    if path=='/v1/reports':return index
    if path=='/v1/health':return health
    if path=='/v1/sync':return sync
    if path.startswith('/v1/reports/'):
        return details.get(path.split('/')[-1],{})
    return {}
class Handler(SimpleHTTPRequestHandler):
    directory_path=None
    def __init__(self,*args,**kwargs):
        super().__init__(*args,directory=str(self.directory_path),**kwargs)
    def do_GET(self):
        if self.path.startswith('/v1/'):
            raw=json.dumps(payload(self.path),separators=(',',':')).encode()
            self.send_response(200)
            self.send_header('Content-Type','application/json')
            self.send_header('Content-Length',str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
            return
        super().do_GET()
    def log_message(self,*args):pass

def test():
    with tempfile.TemporaryDirectory(prefix='og309-preload-') as tmp:
        stage=Path(tmp)/'site'
        subprocess.run([sys.executable,str(ROOT/'tools/build_pages_artifact.py'),str(stage)],check=True,cwd=ROOT)
        Handler.directory_path=stage
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            sys.path.insert(0,str(ROOT/'tools'))
            from build_preload_snapshot import build
            snapshot=build(f'http://127.0.0.1:{server.server_port}',stage/'data/preload')
            assert snapshot['reportCount']==7 and snapshot['chunks']
            from subprocess import run
            run([sys.executable,str(ROOT/'tools/audit_database.py'),'--artifact-tree',str(stage)],check=True,cwd=ROOT)
            checksum_path=stage/'data/preload'/snapshot['chunks'][0]['file']
            verified=checksum_path.read_bytes()
            checksum_path.write_bytes(verified.replace(b'PUBLIC TEST REPORT',b'PUBLIC TEST REPORX',1))
            rejection=run([sys.executable,str(ROOT/'tools/audit_database.py'),'--artifact-tree',str(stage)],capture_output=True,text=True,cwd=ROOT)
            assert rejection.returncode!=0 and 'checksum failed' in rejection.stdout, rejection.stdout
            checksum_path.write_bytes(verified)
            source=(ROOT/'tools/test_3_0_0_live_browser.py').read_text(encoding='utf-8')
            ns={'__file__':str(ROOT/'tools/test_3_0_0_live_browser.py')}
            exec(source.split('with sync_playwright() as p:',1)[0],ns)
            raw_chunk=(stage/'data/preload'/snapshot['chunks'][0]['file']).read_text(encoding='utf-8')
            raw_manifest=(stage/'data/preload/manifest.json').read_text(encoding='utf-8')
            bad_chunk='{"schemaVersion":1,"reports":[]}'
            raw_hash=hashlib.sha256(raw_chunk.encode()).hexdigest()
            bad_hash=hashlib.sha256(bad_chunk.encode()).hexdigest()
            catalog=(ROOT/'data/registry-catalog.v2000.json').read_text(encoding='utf-8')
            local_notice=(ROOT/'licenses/openglesscope-application-mit.md').read_text(encoding='utf-8')
            release=(ROOT/'data/release.json').read_text(encoding='utf-8')
            with sync_playwright() as p:
                browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
                for width,height,corrupt in [(1440,900,False),(390,844,False),(1440,900,True)]:
                    context=browser.new_context(viewport={'width':width,'height':height})
                    script=r"""<script>(()=>{
                        window.OPENGLESSCOPE_DATABASE_API='https://openglesscope-database-api.openglesscope.workers.dev';
                        window.__detailCalls=0;
                        const original=ORIGINAL,broken=BROKEN;
                        Object.defineProperty(window.crypto,'subtle',{configurable:true,value:{digest:async(algorithm,buffer)=>{
                            const raw=new TextDecoder().decode(buffer);
                            const hex=raw===original?ORIGINAL_HASH:BROKEN_HASH;
                            return Uint8Array.from(hex.match(/../g).map(x=>parseInt(x,16))).buffer;
                        }}});
                        window.fetch=async input=>{
                          const url=String(input);let payload;
                          if(url.includes('data/preload/manifest.json'))return new Response(MANIFEST,{status:200,headers:{'content-type':'application/json'}});
                          if(url.includes('data/preload/reports.')){await new Promise(resolve=>setTimeout(resolve,180));return new Response(CORRUPT?broken:original,{status:200,headers:{'content-type':'application/json'}});}
                          if(/\/v1\/reports\/[a-f0-9]{64}/.test(url)){
                           window.__detailCalls++;
                           const id=url.match(/\/v1\/reports\/([a-f0-9]{64})/)[1];payload=DETAILS[id]||{};
                          } else if(url.includes('/v1/reports?'))payload=INDEX;
                          else if(url.includes('/v1/health')){if(!CORRUPT)await new Promise(resolve=>setTimeout(resolve,4000));payload=HEALTH;}
                          else if(url.includes('/v1/sync'))payload=SYNC;
                          else if(url.includes('/v1/network-info'))payload={networkInfoVersion:1};
                          else if(url.includes('data/registry-catalog'))payload=CATALOG;
                          else if(url.includes('data/release.json'))payload=RELEASE;
                          else if(url.includes('data/index.json'))payload=INDEX;
                          else if(url.includes('/licenses/'))return new Response(NOTICE,{status:200,headers:{'content-type':'text/plain'}});
                          else payload={};
                          return new Response(JSON.stringify(payload),{status:200,headers:{'content-type':'application/json'}});
                        };
                      })();</script>"""
                    for key,value in [('ORIGINAL_HASH',json.dumps(raw_hash)),('BROKEN_HASH',json.dumps(bad_hash)),('ORIGINAL',json.dumps(raw_chunk)),('BROKEN',json.dumps(bad_chunk)),('MANIFEST',json.dumps(raw_manifest)),('CORRUPT',json.dumps(corrupt)),('DETAILS',json.dumps(details)),('INDEX',json.dumps(index)),('HEALTH',json.dumps(health)),('SYNC',json.dumps(sync)),('RELEASE',release),('CATALOG',catalog),('NOTICE',json.dumps(local_notice))]:
                        script=script.replace(key,value)
                    html=ns['html'].replace(ns['mock'],script)
                    assert html!=ns['html']
                    page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                    page.set_content(html,wait_until='domcontentloaded',timeout=30000)
                    if not corrupt:
                        page.wait_for_function("document.querySelector('#databaseLoadingDetail')?.textContent.includes('Preparing 7 cached reports')",timeout=5000)
                        assert page.locator('#databaseLoading').is_visible()
                        page.wait_for_function("document.body.classList.contains('startup-layout-ready')",timeout=2800)
                        assert page.locator('#networkStatusShell').get_attribute('data-state')=='checking'
                    else:
                        page.wait_for_function("document.body.classList.contains('startup-layout-ready')",timeout=30000)
                    assert page.locator('#privacyNotice').count()==0
                    assert page.locator('#content .reports-table tbody tr').count()==7
                    calls=page.evaluate('window.__detailCalls')
                    assert calls==(7 if corrupt else 0),(width,corrupt,calls)
                    page.locator('#globalSearch').fill('Cached GPU 1')
                    page.wait_for_timeout(210)
                    assert page.locator('#globalSearchClear').is_visible()
                    assert page.locator('#content .reports-table tbody tr').count()==1
                    page.locator('#globalSearchClear').click()
                    page.wait_for_timeout(210)
                    assert page.locator('#content .reports-table tbody tr').count()==7
                    page.locator('#mainNav button[data-view="extensions"]').click()
                    page.wait_for_selector('#extensionRowSearch',timeout=15000)
                    page.locator('#extensionRowSearch').fill('GL_EXT')
                    assert page.locator('.og-search-clear').filter(visible=True).count()>=1
                    assert not errors,errors
                    print('CHROMIUM 3.0.23 PRELOAD',width,height,'corrupt=',corrupt,'detail API calls=',calls,'cache-first before delayed Worker, explicit progress, search X and filtered views PASS')
                    context.close()
                browser.close()
        finally:
            server.shutdown();server.server_close();thread.join(timeout=3)
if __name__=='__main__':test()
