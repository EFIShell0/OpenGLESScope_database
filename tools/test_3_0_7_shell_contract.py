from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
app=(root/'assets/app.v3023.js').read_text(encoding='utf8')
html=(root/'index.html').read_text(encoding='utf8')
css=(root/'assets/site.v3023.css').read_text(encoding='utf8')
parts={
 'overview tab':"const TABS=[['overview','Overview']",
 'overview route':"DETAIL_ROUTE={overview:'Overview'",
 'legacy route alias':"{summary:'overview'}",
 'canonical tab family':"tabs=[['overview','Overview']",
 'grouped overview':'detail-overview-grid',
 'metadata categories':'Submission identity',
 'identity groups':'GPU & driver',
 'runtime evidence':'OpenGL ES / EGL',
 'display evidence':'Display evidence',
 'grouped cards':'detail-overview-section',
 'hero action placement':'''</div>`;$('#detailContent').innerHTML=hero+`<div class="detail-actions"''',
 'canonical TXT export in Raw tab':'id="downloadRawTabReport"',
 'favorite SVG':'function detailFavoriteMarkup(active)',
 'favorite icon state':'favoriteButton.innerHTML=detailFavoriteMarkup(favorites.has(p.id))',
 'report motion':'function animateReportViewIn(el,token)',
 'report exit':'duration:120,easing:\'cubic-bezier(.4,0,.2,1)\'',
 'report entrance':'duration:210,easing:\'cubic-bezier(.2,.8,.2,1)\'',
 'back align':'function syncDetailBackTop(align=false)',
 'back focus':'back.focus({preventScroll:true})',
 'back restoration':'routeScrollPositions.set(returnTo,target)',
 'back source route':'rememberRouteScroll(detailReturnRoute)',
 'direct Overview without TXT fallback':'el.innerHTML=body;return;}if(state.detailTab',
 'async guard':'detailRequest!==renderGeneration||token!==reportViewTransitionToken||state.detailId!==id',
 'startup finish':'setDatabaseLoading(false,\'Current database is ready\'',
 'startup ready':'document.dispatchEvent(new CustomEvent(\'openglesscope:ready\'))',
}
for label,token in parts.items():assert token in app,(label,token)
assert app.count("['overview','Overview']")>=2
assert "['summary','Summary']" not in app
assert "el.classList.add('finished')" not in app
assert "queuePageScrollUi(true)" not in app
assert 'html{overflow-x:clip!important}body.startup-layout-ready{overflow-x:clip!important;overflow-y:visible!important}' in css
assert '@media(prefers-reduced-motion:reduce)' in css
assert 'class="back-button detail-back-button" id="detailBack"' in html
assert 'database-loading-brand' in html and 'database-loading-track' in html
assert 'id="databaseLoadingProgress"' in html
assert html.count('src="./assets/openglesscope_logo_horizontal-v017.png"')>=1
assert app.count('data-tab=')>=1
assert not re.search(r'detailTab\s*:\s*[\'\"]summary[\'\"]',app)
for label,mutation in [('obsolete Overview label',app.replace("[['overview','Overview']","[['overview','Summary']",1)),('lost favorite SVG',app.replace('function detailFavoriteMarkup(active)','function detailFavoriteMarkupMissing(active)',1)),('missing Back offset',app.replace('function syncDetailBackTop(align=false)','function syncDetailBackTopMissing(align=false)',1))]:
 key={'obsolete Overview label':"const TABS=[['overview','Overview']",'lost favorite SVG':'function detailFavoriteMarkup(active)','missing Back offset':'function syncDetailBackTop(align=false)'}[label]
 assert key not in mutation,label
print('OpenGLESScope Database 3.0.23 Overview, action, Back, loader and navigation source gates: PASS')
