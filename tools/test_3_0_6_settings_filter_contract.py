from pathlib import Path
from html.parser import HTMLParser
from hashlib import sha256
import re
root=Path(__file__).resolve().parents[1]
html=(root/'index.html').read_text(encoding='utf-8')
app=(root/'assets/app.v3024.js').read_text(encoding='utf-8')
style=(root/'assets/site.v3024.css').read_text(encoding='utf-8')
worker=(root/'worker/src/index.js').read_text(encoding='utf-8')
experience=(root/'assets/experience.v3024.js').read_text(encoding='utf-8')
class Reader(HTMLParser):
 def __init__(self): super().__init__();self.ids=[];self.tag='';self.path=[];self.settings=[];self.internet_sections=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.path.append((tag,a))
  if 'id' in a:self.ids.append((a['id'],tag,[x.get('data-settings-panel') for _,x in self.path if x.get('data-settings-panel')]))
  if a.get('data-settings-panel'):self.settings.append(a['data-settings-panel'])
  if tag=='section' and 'settings-section' in a.get('class','') and any(x.get('data-settings-panel')=='internet' for _,x in self.path):self.internet_sections.append(a.get('class',''))
 def handle_endtag(self,tag):
  for i in range(len(self.path)-1,-1,-1):
   if self.path[i][0]==tag:self.path=self.path[:i];return
x=Reader();x.feed(html)
ids=[id for id,_,_ in x.ids]
assert len(ids)==len(set(ids)),[p for p in ids if ids.count(p)>1]
assert x.settings==['internet','favorites','preferences','information']
assert len(x.internet_sections)==2
assert dict((id,(tag,path)) for id,tag,path in x.ids)['settingsBrowserInfo'][1]==['internet']
assert not any(z in ids for z in ['settingsRequestNetwork','settingsRequestNetworkResult','settingsRefresh','settingsPageSize'])
assert "browser.id='settingsBrowserInfo'" not in experience
assert '<span id="pageProgressBar"></span>' in html and '.page-progress span{' in style
assert 'const FILTER_APPLICABILITY_GL=' in app and 'function organizeGlobalFiltersGL()' in app
assert 'filterIsApplicableGL(k)&&!!state[k]' in app
assert 'if(state.view===\'display\')' in app and "display:['androidFilter'" in app
assert 'filterIsApplicableGL' in app and 'FILTER_FAMILIES_GL' in app
assert 'settingsNetworkObservation=null' in app and 'clearInterval(settingsNetworkTimer)' in app
assert "settingsNetworkTimer=setInterval" in app and 'settingsNetworkObservation=info' in app
assert 'settingsAddressVisibility[key]=false' in app and 'network-address-mosaic' in app
assert '.android-app-icon{width:23px;height:18px' not in style
android=re.search(r'const ANDROID_APP_FILTER_ICON=(`.*?`);',app).group(1)
assert sha256(android.encode()).hexdigest()=='035bb9b70d7ef57365a304a9eeb110b139acb51561f04cad7460617d0313824c'
assets=list((root/'assets/country-flags').glob('*.png'))
assert len(assets)==250 and all(p.stat().st_size>100 for p in assets)
for key in ['pseudoIPv4','regionCode','continent','httpProtocol','tlsVersion','tlsCipher','clientTcpRtt','clientQuicRtt','deliveryRate','serverTime']:
 assert key in worker,key
for key in ['pseudoIPv4','continent','httpProtocol','tlsVersion','tlsCipher','clientTcpRtt','clientQuicRtt','deliveryRate','serverTime']:
 assert key in app,key
network_handler=worker[worker.index('const requestNetworkInfo=request=>'):worker.index('\nconst canonicalBytes=')]
assert 'env.DB' not in network_handler and 'reportText' not in network_handler
assert (root/'assets/hdr/hdr10_plus_v1014.png').is_file()
print('OpenGLESScope Database 3.0.24 shared Internet/Browser settings, 250 local country flags, scoped filter visibility, progress and green Android: PASS')
