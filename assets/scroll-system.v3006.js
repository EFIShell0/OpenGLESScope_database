(()=>{'use strict';
const $=selector=>document.querySelector(selector);
const prefersReducedMotion=()=>window.matchMedia?.('(prefers-reduced-motion: reduce)')?.matches===true;
let pageScrollIdleTimer=0,pageScrollRaf=0,viewportScrollDrag=null;
const markPageScrollActivity=()=>{const wrap=$('#pageScrollControls');if(!wrap)return;wrap.classList.add('is-active');clearTimeout(pageScrollIdleTimer);pageScrollIdleTimer=setTimeout(()=>wrap.classList.remove('is-active'),900)};
const viewportScrollMetrics=()=>{const scrolling=document.scrollingElement||document.documentElement,html=document.documentElement,body=document.body,viewport=Math.max(1,scrolling?.clientHeight||window.innerHeight||html.clientHeight||0),scrollHeight=Math.max(viewport,scrolling?.scrollHeight||0),fallbackDoc=Math.max(viewport,html.scrollHeight||0,body?.scrollHeight||0),max=Math.max(0,scrollHeight-viewport),raw=Number.isFinite(scrolling?.scrollTop)?scrolling.scrollTop:(window.pageYOffset||window.scrollY||0),y=Math.min(max,Math.max(0,raw||0)),remaining=Math.max(0,max-y),doc=Math.max(scrollHeight,fallbackDoc);return{scrolling,viewport,doc,max,y,remaining}};
const syncViewportScrollbar=(metrics=viewportScrollMetrics())=>{const rail=$('#viewportScrollbar'),track=$('#viewportScrollbarTrack'),thumb=$('#viewportScrollbarThumb'),up=$('#viewportScrollbarUp'),down=$('#viewportScrollbarDown');if(!rail||!track||!thumb||!up||!down)return;const{viewport,doc,max,y,remaining}=metrics,scrollable=max>2,atTop=!scrollable||y<=2,atBottom=!scrollable||remaining<=2;rail.classList.toggle('is-scrollable',scrollable);rail.classList.toggle('at-top',atTop);rail.classList.toggle('at-bottom',atBottom);rail.dataset.endpoint=atTop?'top':atBottom?'bottom':'middle';rail.setAttribute('aria-hidden',scrollable?'false':'true');up.disabled=atTop;up.setAttribute('aria-disabled',atTop?'true':'false');down.disabled=atBottom;down.setAttribute('aria-disabled',atBottom?'true':'false');if(!scrollable){thumb.style.height='0px';thumb.style.transform='translateY(0)';thumb.setAttribute('aria-valuenow','0');return}const trackHeight=Math.max(1,track.clientHeight),thumbHeight=Math.max(46,Math.min(trackHeight,trackHeight*(viewport/doc))),travel=Math.max(0,trackHeight-thumbHeight),ratio=max?Math.min(1,Math.max(0,y/max)):0;thumb.style.height=`${thumbHeight}px`;thumb.style.transform=`translateY(${travel*ratio}px)`;thumb.dataset.travel=String(travel);thumb.setAttribute('aria-valuemin','0');thumb.setAttribute('aria-valuemax',String(Math.round(max)));thumb.setAttribute('aria-valuenow',String(Math.round(y)));thumb.setAttribute('aria-valuetext',`${Math.round(ratio*100)}%`)};
const updatePageScrollUi=()=>{const up=$('#pageScrollUp'),down=$('#pageScrollDown'),wrap=$('#pageScrollControls'),progress=$('#pageProgress'),bar=$('#pageProgressBar');if(!up||!down||!wrap)return;if(document.body?.classList.contains('database-loading')){wrap.classList.remove('is-scrollable','is-active');wrap.setAttribute('aria-hidden','true');for(const button of [up,down]){button.classList.remove('is-visible');button.disabled=true;button.tabIndex=-1;button.setAttribute('aria-hidden','true');button.setAttribute('aria-disabled','true')}const rail=$('#viewportScrollbar');rail?.classList.remove('is-scrollable');rail?.setAttribute('aria-hidden','true');if(progress)progress.classList.remove('is-scrollable');if(bar)bar.style.transform='scaleX(0)';return}const metrics=viewportScrollMetrics(),{max,y,remaining}=metrics,scrollable=max>2,setButton=(button,visible,disabled=false)=>{button.classList.toggle('is-visible',visible);button.disabled=!!disabled;button.tabIndex=visible&&!disabled?0:-1;button.setAttribute('aria-hidden',visible?'false':'true');button.setAttribute('aria-disabled',disabled?'true':'false')};wrap.classList.toggle('is-scrollable',scrollable);wrap.setAttribute('aria-hidden',scrollable?'false':'true');const atTop=!scrollable||y<=2,atBottom=!scrollable||remaining<=2;document.documentElement.classList.toggle('at-page-top',atTop);document.documentElement.classList.toggle('at-page-bottom',atBottom);document.body?.classList.toggle('at-page-top',atTop);document.body?.classList.toggle('at-page-bottom',atBottom);setButton(up,scrollable,atTop);setButton(down,scrollable,atBottom);syncViewportScrollbar(metrics);if(progress)progress.classList.toggle('is-scrollable',scrollable);if(bar)bar.style.transform=`scaleX(${scrollable?Math.min(1,Math.max(0,y/max)):0})`};
const queuePageScrollUi=(activity=false)=>{if(activity)markPageScrollActivity();if(pageScrollRaf)return;pageScrollRaf=requestAnimationFrame(()=>{pageScrollRaf=0;updatePageScrollUi()})};
const pageScrollStep=direction=>{markPageScrollActivity();window.scrollBy({top:direction*Math.max(240,window.innerHeight*.72),behavior:prefersReducedMotion()?'auto':'smooth'})};
const initViewportScrollbar=()=>{const rail=$('#viewportScrollbar'),track=$('#viewportScrollbarTrack'),thumb=$('#viewportScrollbarThumb'),up=$('#viewportScrollbarUp'),down=$('#viewportScrollbarDown');if(!rail||!track||!thumb||!up||!down)return;document.documentElement.classList.add('viewport-scrollbar-mounted');document.body?.classList.add('viewport-scrollbar-mounted');const scrollToValue=value=>window.scrollTo({top:Math.max(0,value),behavior:prefersReducedMotion()?'auto':'smooth'});up.addEventListener('click',()=>{if(up.disabled)return;pageScrollStep(-1)});down.addEventListener('click',()=>{if(down.disabled)return;pageScrollStep(1)});track.addEventListener('pointerdown',e=>{if(e.target===thumb)return;const m=viewportScrollMetrics(),rect=track.getBoundingClientRect(),travel=parseFloat(thumb.dataset.travel||'0'),ratio=m.max?m.y/m.max:0,mid=rect.top+travel*ratio+(thumb.offsetHeight/2);pageScrollStep(e.clientY<mid?-1:1)});thumb.addEventListener('pointerdown',e=>{if(e.button!==0)return;e.preventDefault();const m=viewportScrollMetrics(),travel=parseFloat(thumb.dataset.travel||'0');viewportScrollDrag={pointerId:e.pointerId,startY:e.clientY,startScroll:m.y,max:m.max,travel};thumb.setPointerCapture?.(e.pointerId);rail.classList.add('is-dragging')});thumb.addEventListener('pointermove',e=>{const d=viewportScrollDrag;if(!d||d.pointerId!==e.pointerId||d.travel<=0)return;e.preventDefault();const next=d.startScroll+(e.clientY-d.startY)*(d.max/d.travel);window.scrollTo({top:Math.max(0,Math.min(d.max,next)),behavior:'auto'})});const stopDrag=e=>{if(!viewportScrollDrag||e.pointerId!==viewportScrollDrag.pointerId)return;viewportScrollDrag=null;rail.classList.remove('is-dragging');try{thumb.releasePointerCapture?.(e.pointerId)}catch{}};thumb.addEventListener('pointerup',stopDrag);thumb.addEventListener('pointercancel',stopDrag);thumb.addEventListener('keydown',e=>{const m=viewportScrollMetrics(),step=Math.max(48,m.viewport*.1),page=Math.max(240,m.viewport*.72);let target=null;if(e.key==='ArrowUp')target=m.y-step;else if(e.key==='ArrowDown')target=m.y+step;else if(e.key==='PageUp')target=m.y-page;else if(e.key==='PageDown')target=m.y+page;else if(e.key==='Home')target=0;else if(e.key==='End')target=m.max;if(target!==null){e.preventDefault();scrollToValue(Math.max(0,Math.min(m.max,target)))}});queuePageScrollUi(false)};

const SURFACE_SCROLL_SELECTOR='.settings-drawer-body,.custom-select-scroll,.coverage-report-dialog-body,.modal-paged-list,.license-viewer-body,.raw-report-scroll';
const surfaceScrollbarRailMarkup=()=>`<button class="viewport-scrollbar-arrow viewport-scrollbar-up surface-scrollbar-up" type="button" aria-label="Scroll up"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 15l6-6 6 6"/></svg></button><div class="viewport-scrollbar-track surface-scrollbar-track"><div class="viewport-scrollbar-thumb surface-scrollbar-thumb" role="scrollbar" tabindex="0" aria-orientation="vertical" aria-label="Scroll position" aria-valuemin="0" aria-valuemax="0" aria-valuenow="0"></div></div><button class="viewport-scrollbar-arrow viewport-scrollbar-down surface-scrollbar-down" type="button" aria-label="Scroll down"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>`;
const surfaceScrollMetrics=host=>{const viewport=Math.max(1,host?.clientHeight||0),doc=Math.max(viewport,host?.scrollHeight||0),max=Math.max(0,doc-viewport),y=Math.min(max,Math.max(0,Number(host?.scrollTop)||0));return{viewport,doc,max,y,remaining:Math.max(0,max-y)}};
const syncSurfaceScrollbar=host=>{if(!host?.isConnected)return;const rail=host._surfaceScrollbar,track=rail?.querySelector('.surface-scrollbar-track'),thumb=rail?.querySelector('.surface-scrollbar-thumb'),up=rail?.querySelector('.surface-scrollbar-up'),down=rail?.querySelector('.surface-scrollbar-down'),parent=rail?.parentElement;if(!rail||!track||!thumb||!up||!down||!parent)return;const hostRect=host.getBoundingClientRect(),parentRect=parent.getBoundingClientRect(),visible=hostRect.width>0&&hostRect.height>0&&host.getClientRects().length>0,{viewport,doc,max,y,remaining}=surfaceScrollMetrics(host),scrollable=visible&&max>2,atTop=!scrollable||y<=2,atBottom=!scrollable||remaining<=2;const railWidth=Math.max(1,rail.getBoundingClientRect().width||18);rail.style.top=`${Math.round(hostRect.top-parentRect.top)}px`;rail.style.left=`${Math.round(hostRect.right-parentRect.left-railWidth)}px`;rail.style.height=`${Math.round(hostRect.height)}px`;rail.classList.toggle('is-scrollable',scrollable);host.classList.toggle('has-surface-scrollbar',scrollable);parent.classList.toggle('has-surface-scrollbar',scrollable);rail.classList.toggle('at-top',atTop);rail.classList.toggle('at-bottom',atBottom);rail.dataset.endpoint=atTop?'top':atBottom?'bottom':'middle';rail.setAttribute('aria-hidden',scrollable?'false':'true');up.disabled=atTop;up.setAttribute('aria-disabled',atTop?'true':'false');down.disabled=atBottom;down.setAttribute('aria-disabled',atBottom?'true':'false');if(!scrollable){thumb.style.height='0px';thumb.style.transform='translateY(0)';thumb.setAttribute('aria-valuenow','0');return}const trackHeight=Math.max(1,track.clientHeight),thumbHeight=Math.max(Math.min(46,trackHeight),Math.min(trackHeight,trackHeight*(viewport/doc))),travel=Math.max(0,trackHeight-thumbHeight),ratio=max?Math.min(1,Math.max(0,y/max)):0;thumb.style.height=`${thumbHeight}px`;thumb.style.transform=`translateY(${travel*ratio}px)`;thumb.dataset.travel=String(travel);thumb.setAttribute('aria-valuemin','0');thumb.setAttribute('aria-valuemax',String(Math.round(max)));thumb.setAttribute('aria-valuenow',String(Math.round(y)));thumb.setAttribute('aria-valuetext',`${Math.round(ratio*100)}%`)};
let surfaceScrollbarSyncRaf=0;
const queueSurfaceScrollbar=host=>{if(!host)return;requestAnimationFrame(()=>syncSurfaceScrollbar(host))};
const queueAllSurfaceScrollbars=()=>{if(surfaceScrollbarSyncRaf)return;surfaceScrollbarSyncRaf=requestAnimationFrame(()=>{surfaceScrollbarSyncRaf=0;document.querySelectorAll('.surface-scroll-host').forEach(syncSurfaceScrollbar)})};
function enhanceSurfaceScrollbar(host){if(!host||host.dataset.surfaceScrollEnhanced==='1')return;const parent=host.parentElement;if(!parent)return;host.dataset.surfaceScrollEnhanced='1';host.classList.add('surface-scroll-host');parent.classList.add('surface-scroll-owner');if(getComputedStyle(parent).position==='static')parent.classList.add('surface-scroll-owner-static');const rail=document.createElement('div');rail.className='surface-scrollbar';rail.setAttribute('aria-hidden','true');rail.innerHTML=surfaceScrollbarRailMarkup();parent.appendChild(rail);host._surfaceScrollbar=rail;const track=rail.querySelector('.surface-scrollbar-track'),thumb=rail.querySelector('.surface-scrollbar-thumb'),up=rail.querySelector('.surface-scrollbar-up'),down=rail.querySelector('.surface-scrollbar-down'),step=dir=>host.scrollBy({top:dir*Math.max(120,host.clientHeight*.72),behavior:prefersReducedMotion()?'auto':'smooth'}),scrollToValue=value=>host.scrollTo({top:Math.max(0,value),behavior:prefersReducedMotion()?'auto':'smooth'});up.addEventListener('click',()=>{if(!up.disabled)step(-1)});down.addEventListener('click',()=>{if(!down.disabled)step(1)});track.addEventListener('pointerdown',e=>{if(e.target===thumb)return;const m=surfaceScrollMetrics(host),rect=track.getBoundingClientRect(),travel=parseFloat(thumb.dataset.travel||'0'),ratio=m.max?m.y/m.max:0,mid=rect.top+travel*ratio+(thumb.offsetHeight/2);step(e.clientY<mid?-1:1)});let drag=null;thumb.addEventListener('pointerdown',e=>{if(e.button!==0)return;e.preventDefault();const m=surfaceScrollMetrics(host),travel=parseFloat(thumb.dataset.travel||'0');drag={pointerId:e.pointerId,startY:e.clientY,startScroll:m.y,max:m.max,travel};thumb.setPointerCapture?.(e.pointerId);rail.classList.add('is-dragging')});thumb.addEventListener('pointermove',e=>{if(!drag||drag.pointerId!==e.pointerId||drag.travel<=0)return;e.preventDefault();const next=drag.startScroll+(e.clientY-drag.startY)*(drag.max/drag.travel);host.scrollTop=Math.max(0,Math.min(drag.max,next))});const stop=e=>{if(!drag||drag.pointerId!==e.pointerId)return;drag=null;rail.classList.remove('is-dragging');try{thumb.releasePointerCapture?.(e.pointerId)}catch{}};thumb.addEventListener('pointerup',stop);thumb.addEventListener('pointercancel',stop);thumb.addEventListener('keydown',e=>{const m=surfaceScrollMetrics(host),small=Math.max(40,m.viewport*.1),page=Math.max(120,m.viewport*.72);let target=null;if(e.key==='ArrowUp')target=m.y-small;else if(e.key==='ArrowDown')target=m.y+small;else if(e.key==='PageUp')target=m.y-page;else if(e.key==='PageDown')target=m.y+page;else if(e.key==='Home')target=0;else if(e.key==='End')target=m.max;if(target!==null){e.preventDefault();scrollToValue(Math.max(0,Math.min(m.max,target)))}});host.addEventListener('scroll',()=>queueSurfaceScrollbar(host),{passive:true});queueSurfaceScrollbar(host)}
function enhanceKnownSurfaceScrollbars(root=document){if(root.matches?.(SURFACE_SCROLL_SELECTOR))enhanceSurfaceScrollbar(root);root.querySelectorAll?.(SURFACE_SCROLL_SELECTOR).forEach(enhanceSurfaceScrollbar)}


let tablePaginationRaf=0;
function enhanceBoundedEvidenceTables(){
  for(const tbody of document.querySelectorAll('#content .table-wrap table>tbody,#detailContent .table-wrap table>tbody')){
    if(tbody.dataset.boundedTableEnhanced==='1')continue;
    const rows=Array.from(tbody.children).filter(el=>el.tagName==='TR');
    if(rows.length<=25)continue;
    const host=tbody.closest('.table-wrap');
    if(!host||host.closest('.reports-table,.modal-paged-list,.encyclopedia-results'))continue;
    tbody.dataset.boundedTableEnhanced='1';
    let page=1,pageSize=25;
    const surface=host.closest('.table-scroll-shell')||host;
    const pager=document.createElement('div');
    pager.className='pagination bounded-table-pagination';
    pager.setAttribute('aria-label','Table pagination');
    pager.innerHTML=`<div class="report-range" aria-live="polite"></div>
       <label class="report-toolbar-control bounded-page-size"><span>Per page</span><select aria-label="Table rows per page"><option value="10">10</option><option value="25" selected>25</option><option value="50">50</option></select></label>
       <button type="button" class="page-button bounded-prev">← Previous</button>
       <span class="page-jump bounded-table-page-jump"><span class="page-jump-prefix">Page</span><input class="page-jump-input" type="text" inputmode="numeric" pattern="[0-9]*" autocomplete="off" aria-label="Table page number" value="1"><span class="page-jump-of">of <span class="page-jump-max">1</span></span><button type="button" class="page-jump-go" aria-label="Go to table page"><span>Go</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14 M14 7l5 5-5 5"/></svg></button></span>
       <button type="button" class="page-button bounded-next">Next →</button>`;
    surface.insertAdjacentElement('afterend',pager);
    const range=pager.querySelector('.report-range'),size=pager.querySelector('select'),
        prev=pager.querySelector('.bounded-prev'),next=pager.querySelector('.bounded-next'),
        jump=pager.querySelector('.page-jump-input'),maxEl=pager.querySelector('.page-jump-max'),go=pager.querySelector('.page-jump-go');
    const pages=()=>Math.max(1,Math.ceil(rows.length/pageSize));
    const valid=v=>/^[1-9]\d*$/.test(String(v).trim())&&Number.isSafeInteger(Number(v))&&Number(v)<=pages();
    const syncGo=()=>{go.disabled=!valid(jump.value)||Number(jump.value)===page;
      go.setAttribute('aria-disabled',String(go.disabled))};
    function paint(direction=0){
      const count=pages();page=Math.min(count,Math.max(1,page));const first=(page-1)*pageSize,end=Math.min(rows.length,first+pageSize);
      for(let i=0;i<rows.length;i++)rows[i].hidden=i<first||i>=end;
      range.textContent=`Showing ${first+1}–${end} of ${rows.length}`;
      prev.disabled=page<=1;next.disabled=page>=count;
      jump.value=String(page);jump.dataset.pageMax=String(count);jump.maxLength=String(count).length;
      jump.setAttribute('aria-label',`Table page number, 1 to ${count}`);
      maxEl.textContent=String(count);syncGo();
      if(direction&&surface.animate&&!prefersReducedMotion()){
        surface.getAnimations().forEach(a=>a.cancel());surface.animate([
          {opacity:.68,transform:`translate3d(${direction>0?9:-9}px,0,0)`},
          {opacity:1,transform:'translate3d(0,0,0)'}],{duration:180,easing:'cubic-bezier(.2,.8,.2,1)'});
      }
      if(host.scrollLeft)host.scrollLeft=0;
      queuePageScrollUi(false);
    }
    prev.addEventListener('click',()=>{if(page>1){page--;paint(-1)}});
    next.addEventListener('click',()=>{if(page<pages()){page++;paint(1)}});
    size.addEventListener('change',()=>{pageSize=[10,25,50].includes(Number(size.value))?Number(size.value):25;page=1;paint()});
    jump.addEventListener('input',()=>{if(!/^\d*$/.test(jump.value))jump.value=jump.value.replace(/\D/g,'');syncGo()});
    const commit=()=>{if(valid(jump.value)){const target=Number(jump.value),dir=Math.sign(target-page);page=target;paint(dir)}else{jump.value=String(page);syncGo()}};
    jump.addEventListener('keydown',event=>{if(event.key==='Enter'){event.preventDefault();commit();jump.blur()}else if(event.key==='Escape'){event.preventDefault();jump.value=String(page);syncGo();jump.blur()}});
    jump.addEventListener('blur',()=>{jump.value=String(page);syncGo()});
    go.addEventListener('click',()=>{commit();jump.blur()});
    paint();
  }
}
const queueBoundedTables=()=>{
  if(tablePaginationRaf)return;
  tablePaginationRaf=requestAnimationFrame(()=>{tablePaginationRaf=0;enhanceBoundedEvidenceTables()});
};

const init=()=>{
  initViewportScrollbar();
  const up=$('#pageScrollUp'),down=$('#pageScrollDown');
  if(up)up.onclick=()=>pageScrollStep(-1);
  if(down)down.onclick=()=>pageScrollStep(1);
  window.addEventListener('scroll',()=>queuePageScrollUi(true),{passive:true});
  window.addEventListener('resize',()=>{queuePageScrollUi(false);queueAllSurfaceScrollbars()},{passive:true});
  document.addEventListener('visibilitychange',()=>{if(!document.hidden){queuePageScrollUi(false);queueAllSurfaceScrollbars()}},{passive:true});
  const resizeObserver=typeof ResizeObserver==='function'?new ResizeObserver(()=>{queuePageScrollUi(false);queueAllSurfaceScrollbars()}):null;
  for(const selector of ['#content','#detailView','#databaseHero','#settingsDrawer','.shell']){
    const node=$(selector);if(node)resizeObserver?.observe(node);
  }
  const observer=new MutationObserver(changes=>{
    for(const change of changes)for(const node of change.addedNodes)
      if(node.nodeType===1)enhanceKnownSurfaceScrollbars(node);
    queuePageScrollUi(false);queueAllSurfaceScrollbars();queueBoundedTables();
  });
  observer.observe(document.body,{childList:true,subtree:true});
  enhanceKnownSurfaceScrollbars(document);
  queuePageScrollUi(false);queueAllSurfaceScrollbars();queueBoundedTables();
  window.addEventListener('load',()=>{queuePageScrollUi(false);queueAllSurfaceScrollbars();queueBoundedTables()},{once:true});
  document.addEventListener('openglesscope:ready',()=>{queuePageScrollUi(false);queueAllSurfaceScrollbars();queueBoundedTables()});
  document.addEventListener('click',()=>{queueAllSurfaceScrollbars();queuePageScrollUi(false)},{passive:true});
  document.addEventListener('transitionend',()=>{queueAllSurfaceScrollbars();queuePageScrollUi(false)},{passive:true});
  window.OGSScroll301=Object.freeze({refresh:()=>{queuePageScrollUi(false);queueAllSurfaceScrollbars();queueBoundedTables()}});
};
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
