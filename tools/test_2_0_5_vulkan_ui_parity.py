from pathlib import Path
from collections import Counter
from html.parser import HTMLParser
import hashlib,re
root=Path(__file__).resolve().parents[1]
html=(root/'index.html').read_text(encoding='utf-8')
css=(root/'assets/site.v2005.css').read_text(encoding='utf-8')
app=(root/'assets/app.v2005.js').read_text(encoding='utf-8')
reference=(root/'rules/VULKANSCOPE_DATABASE_1.4.12_UI_PARITY_SHA256.txt').read_text(encoding='utf-8')
expected=re.search(r'SHA-256: ([a-f0-9]{64})',reference).group(1)
SHARED_BYTES=266528
SHARED_TEXT_LENGTH=266459
class Reader(HTMLParser):
    def __init__(self): super().__init__();self.ids=[];self.classes=[];self.categories=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if 'class' in a:self.classes.extend(a['class'].split())
        if a.get('data-settings-category'):self.categories.append(a['data-settings-category'])
def check(h,c):
    canonical=c[:SHARED_TEXT_LENGTH]
    assert len(canonical)==SHARED_TEXT_LENGTH
    assert hashlib.sha256(canonical.encode('utf-8')).hexdigest()==expected,'VulkanScope stylesheet is not the canonical FIRST layer'
    assert len(c.encode('utf-8'))>SHARED_BYTES
    assert '/* GL/EGL-only existing components' not in c,'legacy common interface layer reintroduced'
    x=Reader();x.feed(h)
    assert len(x.ids)==len(set(x.ids)),'duplicate HTML id'
    assert Counter(x.categories)==Counter(['favorites','preferences','internet','information'])
    for name in ['topbar','settings-drawer','settings-category-nav','settings-toggle','settings-regional-group','hero-v127','hero-v127-grid','hero-command-deck','database-loading-panel','page-scroll-controls','viewport-scrollbar','destructive-confirm-dialog','footer-brand-stack']:
        assert name in x.classes,name
    for name in ['mainNav','navLeft','navRight','settingsButton','settingsDrawer','settingsBackdrop','settingsClose','favoriteItems','rememberDevice','settingsPageSize','settingsSubmittedDefault','settingsVendorDefault','settingsRegionalMode','settingsRegionalCountry','settingsRegionalDateFormat','settingsRegionalClock','settingsRegionalTimeZone','settingsRegionalSeason','settingsRegionalPreview','settingsNetworkInfo','settingsRequestNetwork','settingsRequestNetworkResult','settingsBrowserInfo','globalSearch','globalSearchClear','metrics','databaseLoading','contentView','filters','detailView','detailBack','viewportScrollbarThumb']:
        assert name in x.ids,name
    assert 'app.v2005.js' in h and 'site.v2005.css' in h and 'config.js?v=2005' in h
    assert 'vulkanscope_logo_horizontal.png' not in h
    for source in ['.settings-drawer','.hero-v127','.nav-button','.settings-toggle','.viewport-scrollbar','@media(prefers-reduced-motion:reduce)']:
        assert source in c,source
check(html,css)
assert '<div class="filter-bar-heading">' not in html
assert '<div class="hero-v127-brand-heading"' not in html
assert 'class="hero-v127-brand-heading"' in html
assert 'class="filter-family report-toolbar-family"' in app
assert 'class="nav-icon"' in app
assert 'const detailRequest=++renderGeneration' in app
assert 'detailRequest!==renderGeneration||state.detailId!==id' in app
assert '<span>Per page</span>' in app
assert '<span>Sort</span>' in app
assert 'legacy common interface layer reintroduced' in Path(__file__).read_text()

for label,badh,badc in [
    ('Vulkan source mutation',html,'altered\n'+css),
    ('settings category deletion',html.replace('data-settings-category="favorites"','data-settings-category="gone"',1),css),
    ('broken navigation id',html.replace('id="navLeft"','id="oldNavLeft"',1),css),
    ('duplicate evidence host',html.replace('id="favoriteItems"','id="settingsButton"',1),css)]:
    try:check(badh,badc)
    except AssertionError:continue
    raise AssertionError('Parity negative mutation escaped: '+label)
assert "const NAV=[" in app
assert all(x in app for x in ['renderReports','renderEncyclopedia','renderGlOverview','renderEglOverview','updateInternetPanel','fetchRequestNetworkInfo'])
assert not list(root.glob('DEPLOY*.md')),'deploy markdown is forbidden inside this release'
print('OpenGLESScope Database 2.0.5 order-sensitive VulkanScope 1.4.12 shared UI / GL-EGL semantics / negative-mutation gate: ALL PASS')
