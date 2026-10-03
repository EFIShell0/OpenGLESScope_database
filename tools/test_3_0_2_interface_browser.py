from pathlib import Path
from playwright.sync_api import sync_playwright
import json,re
root=Path(__file__).resolve().parents[1]
source=(root/'tools/test_3_0_0_live_browser.py').read_text()
exec(source.split('with sync_playwright() as p:')[0],globals())
rows=[]
for i in range(63):
 id=f'{i+1:064x}'
 rows.append({'id':id,'submitted_at':f'2026-10-02T10:{i%60:02d}:00.000Z','gpu_name':f'Test GPU {i+1}','vendor':['Qualcomm','Arm','Imagination'][i%3],'manufacturer':'Reference Manufacturer','model':f'Model {i%7}','opengles_version':'OpenGL ES 3.2','egl_version':'1.5','application_version':'2.2.22','application_version_code':2222,'android_release':'15','driver_version':f'{i+1}.0','driver_mode':'System'})
row_map={x['id']:{**x,'gpu':{'name':x['gpu_name'],'vendor':x['vendor']},'device':{'manufacturer':x['manufacturer'],'model':x['model'],'androidRelease':'15'},'application':{'version':'2.2.22','versionCode':2222},'driver':{'mode':'System','version':x['driver_version']},'opengles':{'version':'OpenGL ES 3.2','glslVersion':'OpenGL ES GLSL ES 3.20','extensions':[]},'egl':{'initializedVersion':'1.5','clientApis':'OpenGL_ES','vendor':'EGL Vendor','extensions':[],'clientExtensions':[]},'technicalReport':{'limits':[],'extensions':[],'eglExtensions':[],'eglClientExtensions':[],'compressedFormats':[],'shaderBinaryFormats':[],'programBinaryFormats':[],'precision':[],'queryDiagnostics':[],'eglConfigs':[{'EGL_CONFIG_ID':7,'EGL_RED_SIZE':8,'EGL_GREEN_SIZE':8,'EGL_BLUE_SIZE':8,'EGL_SAMPLES':4}],'display':{}},'reportText':'OpenGL ES test report'} for x in rows}
seed={'schemaVersion':2,'normalizerVersion':16,'databaseVersion':'3.0.27','currentProducer':'OpenGLESScope 3.0.7','reports':rows,'nextCursor':None}
head={'databaseReleaseVersion':'3.0.27','workerReleaseVersion':'3.0.27','reportCount':len(rows),'latestReportId':rows[0]['id'],'latestSubmittedAt':rows[0]['submitted_at'],'syncToken':'63:seed'}
seed_js=r"""<script>(()=>{const previous=window.fetch,seed=SEED,detail=DETAIL,sync=SYNC;window.fetch=async function(input,options){const u=String(input);if(/\/v1\/reports\/[a-f0-9]{64}(?:\?|$)/.test(u)){const id=u.match(/\/v1\/reports\/([a-f0-9]{64})/)[1];return new Response(JSON.stringify(detail[id]||{}),{status:detail[id]?200:404,headers:{'content-type':'application/json'}})}if(u.includes('/v1/reports?'))return new Response(JSON.stringify(seed),{status:200,headers:{'content-type':'application/json'}});if(u.includes('/v1/sync'))return new Response(JSON.stringify(sync),{status:200,headers:{'content-type':'application/json'}});return previous(input,options)}})();</script>""".replace('SEED',json.dumps(seed)).replace('DETAIL',json.dumps(row_map)).replace('SYNC',json.dumps(head))
app_source=(root/'assets/app.v3027.js').read_text()
needle='<script>'+app_source+'</script>'
assert needle in html
html=html.replace(needle,seed_js+needle,1)
for name in ['scroll-system.v3027.js']:
 content='<script>'+(root/'assets'/name).read_text()+'</script>'
 html,n=re.subn(r'<script\b[^>]*src="[^"]*'+re.escape(name)+r'(?:\?[^"]*)?"[^>]*>\s*</script>',lambda _:content,html)
 assert n==1,(name,n)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
 for width,height in [(1440,900),(390,844)]:
  ctx=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
  page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)+' '+str(getattr(e,'stack',''))))
  page.set_content(html,wait_until='domcontentloaded',timeout=20000)
  page.wait_for_function("document.body.classList.contains('startup-layout-ready')",timeout=20000)
  assert page.locator('#privacyNotice').count()==0
  page.wait_for_function("document.querySelector('#content .reports-table tbody')?.rows.length===25",timeout=10000)
  assert page.locator('#mainNav .nav-button').count()==16
  assert page.locator('#content .report-favorite').count()==25
  assert page.locator('#submittedToggle').count()==1
  assert page.locator('#vendorToggle').count()==1
  assert page.locator('#typeToggle').count()==1
  page.locator('#submittedToggle').click()
  assert page.locator('#submittedToggle').get_attribute('aria-expanded')=='true'
  assert page.locator('#content .submitted-reveal').first.get_attribute('aria-hidden')=='false'
  page.locator('#vendorToggle').click()
  assert page.locator('#content .vendor-reveal').first.get_attribute('aria-hidden')=='false'
  page.locator('#typeToggle').click()
  assert page.locator('#content .type-reveal').first.get_attribute('aria-hidden')=='false'
  page.locator('#content [data-copy-report-id]').first.click()
  assert page.locator('#detailView').is_hidden()
  page.locator('#content .report-favorite').first.click()
  assert page.locator('#detailView').is_hidden()
  page.locator('#reportNext').click()
  assert page.locator('#reportPageInput').input_value()=='2'
  page.locator('#reportPageInput').fill('999')
  page.locator('#reportPageInput').press('Enter')
  assert page.locator('#reportPageInput').input_value()=='2'
  page.locator('#reportPageSize').select_option('50')
  page.wait_for_function("document.querySelector('#content .reports-table tbody').rows.length===50")
  page.locator('#mainNav button[data-view="devices"]').click()
  assert page.locator('#content .version-statistics.device-statistics').count()==1
  assert page.locator('#content .cohort-table tbody tr').count()==25
  page.locator('#deviceSort').select_option('reports')
  page.locator('#devicesNext').click()
  assert page.locator('#devicesPageInput').input_value()=='2'
  page.locator('#devicesPageInput').fill('0')
  page.locator('#devicesPageInput').press('Enter')
  assert page.locator('#devicesPageInput').input_value()=='2'
  page.locator('#mainNav button[data-view="versions"]').click()
  assert page.locator('#content .version-statistics').count()==1
  page.locator('#versionGroup').select_option('pair')
  assert page.locator('#content .cohort-table thead th').count()==7
  page.locator('#versionsNext').click()
  assert page.locator('#versionsPageInput').input_value()=='2'
  page.locator('#mainNav button[data-view="opengles"]').click()
  assert page.locator('#content .version-statistics').count()==1
  assert 'GLSL ES' in page.locator('#content').inner_text()
  page.locator('#mainNav button[data-view="egl"]').click()
  assert page.locator('#content .version-statistics').count()==1
  assert 'EGL runtime' in page.locator('#content').inner_text()
  page.locator('#mainNav button[data-view="eglconfigs"]').click()
  page.wait_for_function("document.querySelector('#eglConfigSearch')!==null",timeout=20000)
  assert 'EGL_CONFIG_ID' in page.locator('#content').inner_text()
  page.locator('#eglConfigSearch').fill('EGL_RED_SIZE')
  page.wait_for_function("document.querySelector('#eglConfigSearch')?.value==='EGL_RED_SIZE'",timeout=15000)
  page.locator('#mainNav button[data-view="trends"]').click()
  assert page.locator('#trendGranularity').count()==1
  page.locator('#trendGranularity').select_option('day')
  assert '2026-10-02' in page.locator('#content').inner_text()
  page.locator('#trendGranularity').select_option('week')
  assert page.locator('#content .version-statistics').count()==1
  for view in ['reports','devices','versions','opengles','egl','extensions','limits','formats','precision','eglconfigs','display','diagnostics','statistics','trends','encyclopedia','compare']:
   page.locator(f'#mainNav button[data-view="{view}"]').click()
   page.wait_for_timeout(90)
   assert page.locator('#mainNav button.active').get_attribute('data-view')==view,view
  page.locator('#mainNav button[data-view="reports"]').click()
  page.evaluate("window.dispatchEvent(new Event('offline'))")
  page.wait_for_function("document.querySelector('#networkStatusShell')?.dataset.state==='offline'",timeout=2500)
  assert 'offline' in page.locator('#networkStatusTitle').inner_text().lower()
  page.evaluate("window.dispatchEvent(new Event('online'))")
  page.wait_for_function("document.querySelector('#networkStatusShell')?.dataset.state==='restored'",timeout=5000)
  page.evaluate("document.dispatchEvent(new Event('openglesscope:connection-error'))")
  page.wait_for_timeout(200)
  assert page.locator('#networkStatusShell').get_attribute('data-state')!='unavailable'
  page.evaluate("document.dispatchEvent(new Event('openglesscope:connection-ok'))")
  page.wait_for_function("document.querySelector('#networkStatusShell')?.dataset.state==='restored'",timeout=2500)
  assert page.evaluate('window.__requestNetworkCalls')==0
  assert not errors,(width,errors)
  print('CHROMIUM UI PARITY PASS',width,height,'63 report entries; disclosure/copy/favorite isolated; 10/25/50 pages; devices/versions cohorts; offline/restore/error notifications; privacy')
  ctx.close()
 browser.close()
