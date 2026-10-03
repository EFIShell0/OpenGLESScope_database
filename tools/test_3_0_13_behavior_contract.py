from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
a=(ROOT/'assets/app.v3017.js').read_text(encoding='utf-8')
e=(ROOT/'assets/experience.v3017.js').read_text(encoding='utf-8')
c=(ROOT/'assets/site.v3017.css').read_text(encoding='utf-8')
h=(ROOT/'index.html').read_text(encoding='utf-8')
assert "const cached=await preloadPromise;if(cached&&cached.manifest.reportCount>0)" in a
assert "state.details=new Map(cached.details)" in a and "finishStartup();announceLive(`Verified cache:" in a
assert "await loadIndex();await ensureAllDetails();" in a
assert "Preparing ${manifest.reportCount} cached reports" in a
assert "else if(window.__OGS30__?.isVerifiedOffline?.()){interrupted=true;banner('checking')}else{markOnline();void sync(true)}" in e
assert "history.replaceState({view:state.view},'',returnTo)" in a
assert "window.scrollTo({top:target,left:0,behavior:'instant'})" in a
assert "back.focus({preventScroll:true})" in a and "back.scrollIntoView({block:'start',behavior:'instant'})" in a
repair=(ROOT/'tools/repair_repository.py').read_text(encoding='utf-8')
for stem in ['app','site','browser-compat','experience','release-bootstrap','scroll-system']:
 assert "'"+stem+"':" in repair
assert 'id="downloadReportJson"' in a and 'id="downloadRawReport"' not in a
assert 'id="downloadRawTabReport"' in a
for x in ['settings-favorite-item','settings-favorite-open','No favorite reports yet.','Remember on this device']:
 assert x in a+h
for x in ['OpenGLESScope is not affiliated with the Khronos Group','Worker direct npm dependencies','Wrangler 4.146.0','0 third-party runtime libraries','Unpinned transitive']:
 if x=='Unpinned transitive': assert 'not pinned' in e
 else: assert x in e
for x in ['extensionTokenFilter','driverModeFilter','gpuFilter','resolutionFilter','hdrTypeFilter']:
 assert x in a
assert '.coverage-stack{min-width:0;width:100%' in c
assert "packageVersion" not in a
print('3.0.17 cache-first, navigation, favorites, information, filter and TXT parity: PASS')
