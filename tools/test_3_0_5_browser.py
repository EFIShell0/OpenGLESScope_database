from pathlib import Path
from playwright.sync_api import sync_playwright
import json,os
root=Path(__file__).resolve().parents[1]
source=(root/'tools/test_3_0_2_interface_browser.py').read_text(encoding='utf-8')
exec(source.rsplit('\nwith sync_playwright() as p:',1)[0],globals())
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH') or '/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
 for width,height in [(1440,900),(390,844)]:
  context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce',accept_downloads=True)
  page=context.new_page();errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(html,wait_until='domcontentloaded',timeout=30000)
  page.wait_for_function("document.body.classList.contains('startup-layout-ready') && window.__OGS30__?.getCount?.()===63",timeout=22000)
  assert page.locator('#privacyNotice').count()==0
  page.wait_for_selector('#content .report-row')
  page.evaluate("window.scrollTo({top:360,behavior:'instant'})")
  page.wait_for_function('window.scrollY > 100',timeout=3000)
  page.locator('#content .report-row').nth(7).scroll_into_view_if_needed()
  before=page.evaluate('window.scrollY')
  page.locator('#content .report-row').nth(7).click()
  page.wait_for_selector('#downloadReportJson')
  assert page.locator('#downloadRawReport').count()==1
  with page.expect_download(timeout=12000) as raw:
   page.locator('#downloadRawReport').click()
  raw_file=raw.value
  assert raw_file.suggested_filename.startswith('OpenGLESScope-raw-report-')
  raw_path=Path('/tmp')/f'ogles-305-{width}.txt';raw_file.save_as(raw_path)
  assert raw_path.read_text(encoding='utf-8')=='OpenGL ES test report'
  with page.expect_download(timeout=12000) as export:
   page.locator('#downloadReportJson').click()
  json_file=export.value
  assert json_file.suggested_filename.endswith('.json') and json_file.suggested_filename.startswith('OpenGLESScope-')
  json_path=Path('/tmp')/f'ogles-305-{width}.json';json_file.save_as(json_path)
  payload=json.loads(json_path.read_text(encoding='utf-8'))
  assert payload['id']==page.locator('.detail-report-id').inner_text()
  page.locator('#detailContent [data-tab="raw"]').click()
  page.wait_for_selector('#downloadRawTabReport')
  assert page.locator('.raw-report-scroll').inner_text().strip()=='OpenGL ES test report'
  with page.expect_download(timeout=12000) as raw_again:
   page.locator('#downloadRawTabReport').click()
  assert raw_again.value.suggested_filename==raw_file.suggested_filename
  page.locator('#copyReportLink').click()
  assert page.locator('#copyReportLink span').inner_text() in ('Copied','Copy failed')
  page.locator('#detailBack').click()
  page.wait_for_function("document.querySelector('#detailView')?.classList.contains('active')===false")
  page.wait_for_timeout(200)
  after=page.evaluate('window.scrollY')
  assert abs(after-before)<120,(width,before,after)
  page.evaluate("() => {const node=document.querySelector('.report-row .gpu-name-text');const range=document.createRange();range.selectNodeContents(node);const sel=window.getSelection();sel.removeAllRanges();sel.addRange(range)}")
  page.locator('#content .report-row').first.click(force=True)
  page.wait_for_timeout(160)
  assert not page.locator('#detailView').is_visible(),'Selected text activated report'
  page.evaluate('window.getSelection().removeAllRanges()')
  page.evaluate("() => {window.__OGS30__?.getCount?.(); const original=window.fetch;window.fetch=async(url,opts)=>{if(String(url).includes('/v1/sync'))return new Response(JSON.stringify({databaseReleaseVersion:'3.0.23',reportCount:63,latestReportId:document.querySelector('.report-row').dataset.id,latestSubmittedAt:'2026-10-02T10:00:00.000Z',syncToken:'63:transition'}),{status:200,headers:{'content-type':'application/json'}});return original(url,opts)}}")
  assert page.evaluate('window.__OGS30__.refreshLive()') is False
  page.wait_for_function("document.querySelector('#networkStatusShell')?.dataset.state==='checking'",timeout=3000)
  assert not page.locator('#databaseUpdateModal').is_visible()
  assert not errors,(width,errors)
  print('CHROMIUM 3.0.23 PASS',width,height,'canonical TXT and JSON downloads, route scroll return, selection guard, staged Worker release banner, zero errors',flush=True)
  context.close()
 browser.close()
