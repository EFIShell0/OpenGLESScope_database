from pathlib import Path
from collections import Counter
from html.parser import HTMLParser
import hashlib,re
root=Path(__file__).resolve().parents[1]
html=(root/'index.html').read_text(encoding='utf-8')
css=(root/'assets/site.v3001.css').read_text(encoding='utf-8')
app=(root/'assets/app.v3001.js').read_text(encoding='utf-8')
reference=(root/'rules/SHARED_UI_1_4_12_REFERENCE.css').read_text(encoding='utf-8')
source_hash,brand_hash=(root/'rules/SHARED_UI_BASE_SHA256.txt').read_text().splitlines()
assert hashlib.sha256(reference.encode()).hexdigest()==source_hash
SHARED_TEXT_LENGTH=len(reference)
def geometry_only(value):
    value=re.sub(r'#[0-9a-f]{6}(?![0-9a-f])','COLOR',value,flags=re.I)
    value=re.sub(r'rgba?\([^)]*\)','COLOR',value,flags=re.I)
    return value
class Reader(HTMLParser):
    def __init__(self): super().__init__();self.ids=[];self.classes=[];self.categories=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if 'class' in a:self.classes.extend(a['class'].split())
        if a.get('data-settings-category'):self.categories.append(a['data-settings-category'])
def check(h,c):
    canonical=c[:c.index("\n\n.not-applicable")]
    assert len(canonical)>=SHARED_TEXT_LENGTH
    assert geometry_only(canonical)==geometry_only(reference),'reference selector geometry changed'
    assert hashlib.sha256(canonical.encode()).hexdigest()==brand_hash,'theme checksum mismatch'
    assert '--accent:#ba2a8d' in canonical and '--red:#ff8f98' in canonical,'GL/EGL palette not applied'
    assert '/* GL/EGL-only existing components' not in c,'legacy common interface layer reintroduced'
    x=Reader();x.feed(h)
    assert len(x.ids)==len(set(x.ids)),'duplicate HTML id'
    assert Counter(x.categories)==Counter(['favorites','preferences','internet','information'])
    for name in ['topbar','settings-drawer','settings-category-nav','settings-toggle','settings-regional-group','hero-v127','hero-v127-grid','hero-command-deck','database-loading-panel','page-scroll-controls','viewport-scrollbar','destructive-confirm-dialog','footer-brand-stack']:
        assert name in x.classes,name
    for name in ['mainNav','navScrollLeft','navScrollRight','settingsButton','settingsDrawer','settingsBackdrop','settingsClose','favoriteItems','rememberDevice','settingsPageSize','settingsSubmittedDefault','settingsVendorDefault','settingsRegionalMode','settingsRegionalCountry','settingsRegionalDateFormat','settingsRegionalClock','settingsRegionalTimeZone','settingsRegionalSeason','settingsRegionalPreview','settingsNetworkInfo','settingsRequestNetwork','settingsRequestNetworkResult','settingsBrowserInfo','globalSearch','globalSearchClear','metrics','databaseLoading','contentView','filters','detailView','detailBack','viewportScrollbarThumb']:
        assert name in x.ids,name
    assert 'app.v3001.js' in h and 'site.v3001.css' in h and 'config.js?v=3001' in h
    assert 'vulkanscope_logo_horizontal.png' not in h
    for source in ['.settings-drawer','.hero-v127','.nav-button','.settings-toggle','.viewport-scrollbar','@media(prefers-reduced-motion:reduce)']:
        assert source in c,source
check(html,css)
assert 'filter-bar-heading' not in html
assert '<div class="hero-v127-brand-heading"' not in html
assert 'hero-v127-brand-heading' in html
assert 'class="filter-family report-toolbar-family"' in app
assert 'class="nav-icon"' in app
assert 'const detailRequest=++renderGeneration' in app
assert 'detailRequest!==renderGeneration||state.detailId!==id' in app
assert '<span>Per page</span>' in app
assert '<span>Sort</span>' in app
assert 'reference selector geometry changed' in Path(__file__).read_text()

for label,badh,badc in [
    ('Shared source mutation',html,'altered\n'+css),
    ('settings category deletion',html.replace('data-settings-category="favorites"','data-settings-category="gone"',1),css),
    ('broken navigation id',html.replace('id="navScrollLeft"','id="oldNavScrollLeft"',1),css),
    ('duplicate evidence host',html.replace('id="favoriteItems"','id="settingsButton"',1),css)]:
    try:check(badh,badc)
    except AssertionError:continue
    raise AssertionError('Parity negative mutation escaped: '+label)
assert "const NAV=[" in app
assert all(x in app for x in ['renderReports','renderEncyclopedia','renderGlOverview','renderEglOverview','updateInternetPanel','fetchRequestNetworkInfo'])
assert not list(root.glob('DEPLOY*.md')),'deploy markdown is forbidden inside this release'
print('OpenGLESScope Database 3.0.1 order-sensitive VulkanScope 1.4.12 shared UI / GL-EGL semantics / negative-mutation gate: ALL PASS')
