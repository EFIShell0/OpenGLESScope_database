from pathlib import Path
from playwright.sync_api import sync_playwright
import json
import os
root=Path(__file__).resolve().parents[1]
ids=[format(i+1,'064x') for i in range(15)]
rows=[{'id':id,'submitted_at':f'2026-10-02T08:{i:02d}:00.000Z','gpu_name':f'Adreno {700+i}','vendor':'Qualcomm','opengles_version':'OpenGL ES 3.2','egl_version':'1.5','manufacturer':'Test Devices','model':f'Device {i}','application_version':'2.2.22','application_version_code':2222,'driver_version':'Unavailable','driver_mode':'System OpenGL ES/EGL'} for i,id in enumerate(ids)]
releases={'health':{'status':'ok','schemaVersion':2,'technicalReportSchema':5,'normalizerVersion':16,'databaseVersion':'3.0.26','currentProducer':'OpenGLESScope 3.0.6','compatibleProducer':'OpenGLESScope 3.0.6 (versionCode 3006) for new submissions only; existing earlier reports remain readable','snapshotAutomation':{'configured':True,'mode':'async-github-actions-workflow-dispatch'}},'sync':{'databaseReleaseVersion':'3.0.26','workerReleaseVersion':'3.0.26','reportCount':15,'latestReportId':ids[-1],'latestSubmittedAt':rows[-1]['submitted_at'],'syncToken':'mock'},'index':{'schemaVersion':2,'databaseVersion':'3.0.26','normalizerVersion':16,'currentProducer':'OpenGLESScope 3.0.6','reports':rows,'nextCursor':None}}
def detail(i):
 row=rows[i]
 return {'id':row['id'],'submittedAt':row['submitted_at'],'application':{'version':'2.2.22','versionCode':2222},'device':{'manufacturer':'Test Devices','model':row['model'],'androidRelease':'16','sdk':36},'gpu':{'name':row['gpu_name'],'vendor':'Qualcomm'},'driver':{'mode':'System OpenGL ES/EGL','version':'Unavailable'},'opengles':{'version':'OpenGL ES 3.2','glslVersion':'OpenGL ES GLSL ES 3.20','extensions':['GL_KHR_debug']},'egl':{'vendor':'Test EGL','version':'1.5','initializedVersion':'1.5','clientApis':'OpenGL_ES','extensions':['EGL_KHR_create_context'],'clientExtensions':[]},'collection':{'status':'available','complete':True},'technicalReport':{'schemaVersion':5,'extensions':['GL_KHR_debug'],'eglExtensions':['EGL_KHR_create_context'],'eglClientExtensions':[],'eglCapabilities':[],'limits':[],'eglConfigs':[],'compressedFormats':[],'internalFormats':[],'shaderBinaryFormats':[],'programBinaryFormats':[],'precision':[],'queryDiagnostics':[]},'reportText':'Test report snapshot'}
from playwright.sync_api import sync_playwright
import base64,re
html=(root/'index.html').read_text()
html=re.sub(r'<meta[^>]*http-equiv="Content-Security-Policy"[^>]*>', '', html)
for asset in ['openglesscope_logo_horizontal-v017.png','opengles-gl-es-v030.png','egl-logo-white-v028.png']:
 data='data:image/png;base64,'+base64.b64encode((root/'assets'/asset).read_bytes()).decode('ascii')
 html=html.replace('./assets/'+asset,data)
html=re.sub(r'<link\b[^>]*href="[^"]*site\.v3026\.css(?:\?[^\"]*)?"[^>]*>',lambda x:'<style>'+(root/'assets/site.v3026.css').read_text()+'</style>',html)
mock="""<script>window.OPENGLESSCOPE_DATABASE_API='https://openglesscope-database-api.openglesscope.workers.dev';const MOCK_PAYLOAD=PLACEHOLDER;window.fetch=async function(input){const u=String(input);let value;if(u.includes('/v1/health'))value=MOCK_PAYLOAD.health;else if(u.includes('/v1/sync'))value=MOCK_PAYLOAD.sync;else if(u.includes('/v1/reports/'))value=MOCK_PAYLOAD.details[u.split('/').at(-1)];else if(u.includes('/v1/reports'))value=MOCK_PAYLOAD.index;else if(u.includes('data/index.json'))value=MOCK_PAYLOAD.index;else value={};return new Response(JSON.stringify(value),{status:200,headers:{'content-type':'application/json'}})}</script>"""
mock=mock.replace('PLACEHOLDER',json.dumps({**releases,'details':{id:detail(i) for i,id in enumerate(ids)}}))
html,n=re.subn(r'<script\b[^>]*src="[^"]*config\.js[^"]*"[^>]*>\s*</script>',lambda x:mock,html);assert n==1,n
html,n=re.subn(r'<script\b[^>]*src="[^"]*app\.v3026\.js[^"]*"[^>]*>\s*</script>',lambda x:'<script>'+(root/'assets/app.v3026.js').read_text()+'</script>',html);assert n==1,n
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
 for width,height in [(1440,900),(390,844)]:
  page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce')
  errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
  page.set_content(html,wait_until='domcontentloaded',timeout=20000)
  page.wait_for_function("document.querySelector('#metrics .metric .value')?.textContent==='15'",timeout=20000)
  page.wait_for_function("document.querySelector('#liveStatus')?.textContent.includes('15 reports')",timeout=15000)
  page.wait_for_timeout(120)
  content=page.locator('#content').inner_text()
  assert 'Adreno' in content,content[:1000]
  assert 'Database unavailable' not in page.locator('body').inner_text()
  assert 'Worker version mismatch' not in page.locator('body').inner_text()
  assert page.locator('.error-panel').count()==0
  assert page.locator('#mainNav button').count()==16
  report_row=page.locator('#content .report-row').first
  assert report_row.count()==1,'Report row not rendered'
  first_id=report_row.get_attribute('data-id')
  report_row.click()
  page.wait_for_selector('#detailView.active .detail-hero-v126',timeout=12000)
  assert page.locator('#detailView .detail-identity-card').count()==7,'Detail identity cards lost reference geometry'
  assert page.locator('#detailView .detail-identity-card.detail-id-full').inner_text().find(first_id)>=0
  assert page.locator('#copyReportId').count()==1
  assert page.locator('#detailView .detail-tabs .tab-button').count()==11
  assert page.locator('#detailView .detail-actions').count()==1
  page.locator('#detailBack').click()
  page.wait_for_selector('#contentView.active #content .report-row',timeout=12000)
  assert page.locator('#detailView.active').count()==0
  assert not errors,errors
  preview=os.environ.get('BROWSER_PREVIEW_DIR')
  if preview:
   dest=Path(preview);dest.mkdir(parents=True,exist_ok=True)
   page.screenshot(path=str(dest/('OpenGLESScope-Database-3.0.26-'+('desktop' if width>600 else 'mobile')+'.png')),full_page=False)
  print('LIVE HANDSHAKE PASS',width,height,'15 reports and detail/back reference structure; no release mismatch/error panel')
  page.close()
 browser.close()
