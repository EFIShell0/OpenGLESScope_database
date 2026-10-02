from pathlib import Path
from collections import Counter
from html.parser import HTMLParser
import hashlib,re
root=Path(__file__).resolve().parents[1]
html=(root/'index.html').read_text(encoding='utf-8')
css=(root/'assets/site.v2004.css').read_text(encoding='utf-8')
app=(root/'assets/app.v2004.js').read_text(encoding='utf-8')
reference=(root/'rules/VULKANSCOPE_DATABASE_1.4.12_UI_PARITY_SHA256.txt').read_text(encoding='utf-8')
expected=re.search(r'SHA-256: ([a-f0-9]{64})',reference).group(1)
start='/* Common VulkanScope Database 1.4.12 design/interaction specification: retained source, no recreated approximations. */\n'
end='\n/* GL/EGL schema and branding adaptations only. */'
class Reader(HTMLParser):
    def __init__(self): super().__init__();self.ids=[];self.classes=[];self.categories=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if 'class' in a:self.classes.extend(a['class'].split())
        if a.get('data-settings-category'):self.categories.append(a['data-settings-category'])
def check(h,c):
    assert start in c and end in c
    shared=c.split(start,1)[1].split(end,1)[0]
    assert hashlib.sha256(shared.encode('utf-8')).hexdigest()==expected,'VulkanScope UI source block changed'
    x=Reader();x.feed(h)
    assert len(x.ids)==len(set(x.ids)),'duplicate HTML id'
    assert Counter(x.categories)==Counter(['favorites','preferences','internet','information'])
    for name in ['topbar','settings-drawer','settings-category-nav','settings-toggle','settings-regional-group','hero-v127','hero-v127-grid','hero-command-deck','database-loading-panel','page-scroll-controls','viewport-scrollbar','destructive-confirm-dialog','footer-brand-stack']:
        assert name in x.classes,name
    for name in ['mainNav','navLeft','navRight','settingsButton','settingsDrawer','settingsBackdrop','settingsClose','favoriteItems','rememberDevice','settingsPageSize','settingsSubmittedDefault','settingsVendorDefault','settingsRegionalMode','settingsRegionalCountry','settingsRegionalDateFormat','settingsRegionalClock','settingsRegionalTimeZone','settingsRegionalSeason','settingsRegionalPreview','settingsNetworkInfo','settingsRequestNetwork','settingsRequestNetworkResult','settingsBrowserInfo','globalSearch','globalSearchClear','metrics','databaseLoading','contentView','filters','detailView','detailBack','viewportScrollbarThumb']:
        assert name in x.ids,name
    assert 'app.v2004.js' in h and 'site.v2004.css' in h and 'config.js?v=2004' in h
    assert 'vulkanscope_logo_horizontal.png' not in h
    for source in ['.settings-drawer','.hero-v127','.nav-button','.settings-toggle','.viewport-scrollbar','@media(prefers-reduced-motion:reduce)']:
        assert source in c,source
check(html,css)
for label,badh,badc in [
    ('Vulkan source mutation',html,css.replace(start,start+'altered\n',1)),
    ('settings category deletion',html.replace('data-settings-category="favorites"','data-settings-category="gone"',1),css),
    ('broken navigation id',html.replace('id="navLeft"','id="oldNavLeft"',1),css),
    ('duplicate evidence host',html.replace('id="favoriteItems"','id="settingsButton"',1),css)]:
    try:check(badh,badc)
    except AssertionError:continue
    raise AssertionError('Parity negative mutation escaped: '+label)
assert "const NAV=[" in app
assert all(x in app for x in ['renderReports','renderEncyclopedia','renderGlOverview','renderEglOverview','updateInternetPanel','fetchRequestNetworkInfo'])
assert not list(root.glob('DEPLOY*.md')),'deploy markdown is forbidden inside this release'
print('OpenGLESScope Database 2.0.4 exact VulkanScope 1.4.12 shared UI / GL-EGL semantics / negative-mutation gate: ALL PASS')
