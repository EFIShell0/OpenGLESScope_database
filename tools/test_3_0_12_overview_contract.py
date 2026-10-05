from pathlib import Path
import re
r=Path(__file__).resolve().parents[1]
app=(r/'assets/app.v3028.js').read_text()
css=(r/'assets/site.v3028.css').read_text()
experience=(r/'assets/experience.v3028.js').read_text()
html=(r/'index.html').read_text()
assert "overview:['REPORT OVERVIEW','Overview'" in app
assert "detailWorkspace(state.detailTab,detailStats(p,n,state.detailTab)" in app
section=app[app.index('function renderDetailTab(p)'):app.index("if(state.detailTab==='opengles')",app.index('function renderDetailTab(p)'))]
assert 'detail-overview-grid' in section and 'el.innerHTML=body;return;' in section
assert 'detail-overview-report-id' in section and 'word-break:break-all' in css
assert 'detailReturnScroll=Math.max(0,window.scrollY||0)' in app
assert 'rememberRouteScroll(detailReturnRoute)' in app
assert 'routeScrollPositions.set(returnTo,target)' in app
assert "k==='opengles'?glEsLogo('nav-gles-logo')" in app
assert "k==='egl'?eglLogo('nav-egl-logo')" in app
assert '.nav-button .nav-gles-logo' in css and '.nav-button .nav-egl-logo' in css
assert 'OpenGL® ES™' in app+html and 'EGL™' in app+html
assert "isVerifiedOffline:()=>state.health?.offlineSnapshot===true" in app
assert "if(!reachable()){interrupted=true;banner('offline')}else{markOnline();void sync(true)}" in experience
assert "else if(window.__OGS30__?.isVerifiedOffline?.()){interrupted=true;banner('checking')}" not in experience
for term in ['preloadJson','SHA-256','seedPreloadedReports','cachedReportLoads','async function ensureAllDetails','openglesscope:release-transition']:
 assert term in (app+experience),term
assert (r/'tools/pages.workflow.yml').read_bytes()==(r/'.github/workflows/pages.yml').read_bytes()
print('3.0.28 Overview, Back, white official logos, consistent GL/EGL labels and offline snapshot contract: PASS')
