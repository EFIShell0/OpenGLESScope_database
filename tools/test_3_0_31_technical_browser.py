from pathlib import Path
from playwright.sync_api import sync_playwright
import json,os
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/test_3_0_2_interface_browser.py').read_text(encoding='utf-8')
ns={'__file__':str(ROOT/'tools/test_3_0_2_interface_browser.py')}
exec(source.rsplit('\nwith sync_playwright() as p:',1)[0],ns)
rows=ns['rows'][:2]
report=ns['row_map']
report={r['id']:report[r['id']] for r in rows}
report[rows[0]['id']]['technicalReport'].update({
 'extensions':['GL_EXT_parity_probe'],
 'compressedFormats':['GL_COMPRESSED_RGBA_ASTC_4x4_KHR'],
 'limits':[{'name':'GL_MAX_TEXTURE_SIZE','value':4096}],
 'precision':[{'shader':'GL_VERTEX_SHADER','type':'GL_HIGH_FLOAT','rangeMin':127,'rangeMax':127,'precision':23}],
 'queryDiagnostics':[{'name':'GL_EXTENSIONS','status':'Available'},{'name':'compressedFormats','status':'Available'},{'name':'GL_MAX_TEXTURE_SIZE','status':'Available'},{'name':'GL_VERTEX_SHADER/GL_HIGH_FLOAT','status':'Available'}]
})
report[rows[1]['id']]['technicalReport'].update({
 'extensions':[], 'compressedFormats':[], 'limits':[], 'precision':[],
 'queryDiagnostics':[{'name':'GL_EXTENSIONS','status':'Available'},{'name':'compressedFormats','status':'Available'},{'name':'GL_MAX_TEXTURE_SIZE','status':'Unavailable'},{'name':'GL_VERTEX_SHADER/GL_HIGH_FLOAT','status':'Unavailable'}]
})
seed={'schemaVersion':2,'normalizerVersion':16,'databaseVersion':'3.0.31','currentProducer':'OpenGLESScope 3.0.7','reports':rows,'nextCursor':None}
head={'databaseReleaseVersion':'3.0.31','workerReleaseVersion':'3.0.31','reportCount':2,'latestReportId':rows[0]['id'],'latestSubmittedAt':rows[0]['submitted_at'],'syncToken':'2:probe'}
seed_js=r'''<script>(()=>{const previous=window.fetch,seed=SEED,detail=DETAIL,sync=SYNC;window.fetch=async function(input,options){const u=String(input);if(/\/v1\/reports\/[a-f0-9]{64}(?:\?|$)/.test(u)){const id=u.match(/\/v1\/reports\/([a-f0-9]{64})/)[1];return new Response(JSON.stringify(detail[id]||{}),{status:detail[id]?200:404,headers:{'content-type':'application/json'}})}if(u.includes('/v1/reports?'))return new Response(JSON.stringify(seed),{status:200,headers:{'content-type':'application/json'}});if(u.includes('/v1/sync'))return new Response(JSON.stringify(sync),{status:200,headers:{'content-type':'application/json'}});return previous(input,options)}})();</script>'''.replace('SEED',json.dumps(seed)).replace('DETAIL',json.dumps(report)).replace('SYNC',json.dumps(head))
html=ns['html'].replace(ns['seed_js'],seed_js)
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH') or '/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
 for width,height in [(1440,900),(390,844)]:
  context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
  page=context.new_page()
  errors=[]
  page.on('pageerror',lambda error:errors.append(str(error)))
  page.set_content(html,wait_until='domcontentloaded',timeout=30000)
  page.wait_for_function("document.body.classList.contains('startup-layout-ready')",timeout=20000)
  for view,token,columns in [('extensions','GL_EXT_parity_probe',['Reported','Reported %','Not listed','Not listed %']),('limits','GL_MAX_TEXTURE_SIZE',['Query available','Query unavailable','Unavailable %']),('formats','GL_COMPRESSED_RGBA_ASTC_4x4_KHR',['Reported','Reported %','Not listed']),('precision','GL_VERTEX_SHADER',['Query available','Query unavailable','Unavailable %'])]:
   page.locator(f'#mainNav button[data-view="{view}"]').click()
   page.wait_for_function("(token)=>document.querySelector('#content')?.textContent.includes(token)",arg=token,timeout=15000)
   assert page.locator('#contentView').get_attribute('data-main-view')==view,(width,view,'view marker')
   for col in columns:assert col in page.locator('#content').inner_text(),(width,view,col)
   cells=page.locator('#content .coverage-value')
   assert cells.count()>0,(width,view,'no percent meters')
   fifty=page.locator('#content .coverage .coverage-value').filter(has_text='50.0%')
   assert fifty.count()>0,(width,view,'50% missing')
   fill=fifty.first.locator('xpath=../div[contains(@class,"coverage-bar")]/div[contains(@class,"coverage-fill")]')
   assert fill.count()==1,(width,view,'fill missing')
   assert fill.get_attribute('style')=='width:50%',(width,view,fill.get_attribute('style'))
   height_px=page.locator('#content .coverage-bar').first.evaluate('(el)=>Math.round(el.getBoundingClientRect().height)')
   assert height_px==7,(width,view,'bar-height',height_px)
   assert page.locator('#content .subfilters').first.evaluate('(el)=>getComputedStyle(el).display')=='grid',(width,view,'filter geometry')
   assert not errors,(width,view,errors)
  assert page.locator('#precisionNext').is_disabled()
  context.close()
  print('CHROMIUM 3.0.31 TECHNICAL PARITY PASS',width,height)
 browser.close()
