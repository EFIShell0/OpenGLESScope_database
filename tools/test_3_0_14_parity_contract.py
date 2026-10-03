from pathlib import Path
R=Path(__file__).resolve().parents[1]
a=(R/'assets/app.v3023.js').read_text(encoding='utf-8')
e=(R/'assets/experience.v3023.js').read_text(encoding='utf-8')
h=(R/'index.html').read_text(encoding='utf-8')
c=(R/'assets/site.v3023.css').read_text(encoding='utf-8')
message='Release, runtime and dependency information for this OpenGLESScope Database build.'
assert h.count(message)==0 and e.count(message)==1
assert "next==='checking'&&reachable()" in e
assert "['offline','unavailable'].includes(network)" in e
assert "back.style.removeProperty('top')" in a and "#detailView .detail-back-button{position:relative!important" in c
assert "const draw=()=>" in a and "input.oninput=()=>{state.encyclopediaQuery=input.value" in a
assert "list.innerHTML=matches.slice(start,start+size)" in a
assert "fresh.focus({preventScroll:true});try{fresh.setSelectionRange" in a
assert 'renderEncyclopedia.ticket=0' in a
assert 'OpenGL® ES™ / EGL™' in a
assert 'const displayBrand=value=>' in a and "put('Driver','Mode',p.driver?.mode)" in a and "esc(displayBrand(p.driver?.mode||'Reported driver'))" in a
assert "put('OpenGL ES','GL_RENDERER',p.gpu?.name)" in a
print('3.0.23 Information, publication banner, Back, responsive registry, stable search and branding: PASS')
