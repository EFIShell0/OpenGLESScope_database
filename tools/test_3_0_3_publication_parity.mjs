import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const root=new URL('../',import.meta.url);
const read=name=>fs.readFileSync(new URL(name,root),'utf8');
const ux=read('assets/experience.v3026.js');
const app=read('assets/app.v3026.js');
const worker=read('worker/src/index.js');
const workflow=read('.github/workflows/pages.yml');
const marker=JSON.parse(read('data/release.json'));
const block=(first,last)=>{const a=ux.indexOf(first),b=ux.indexOf(last,a+first.length);assert.ok(a>=0&&b>a,first);return ux.slice(a,b)};
assert.deepEqual(marker,{schemaVersion:2,databaseVersion:'3.0.26',releaseReady:false,appAsset:'assets/app.v3026.js',cacheKey:'3026'});
assert.ok(ux.includes('setInterval(()=>void sync(false),3000)'));
assert.ok(ux.includes('setInterval(()=>void releases(),10000)'));
assert.ok(ux.includes("document.addEventListener('openglesscope:new-reports',e=>toast(e.detail?.count))"));
assert.ok(ux.includes("head?.databaseReleaseVersion!==VERSION"));
assert.ok(ux.includes('head.reportCount!==loaded'));
assert.ok(ux.includes('await window.__OGS30__?.refreshLive?.()'));
assert.ok(app.includes("new CustomEvent('openglesscope:new-reports'"));
assert.ok(app.includes('setDatabaseLoading('));
assert.ok(app.includes('if(!startupClosed)'));
assert.ok(app.includes('compareStickySentinel'));
assert.ok(app.includes('detail-section-intro'));
assert.ok(worker.includes('ctx.waitUntil(dispatchSnapshotRefresh(env,id,submittedAt)'));
assert.ok(worker.includes('SNAPSHOT_GITHUB_TOKEN'));
assert.ok(workflow.includes('snapshot-refresh:'));
assert.ok(workflow.includes('--expect-report-id "$REPORT_ID"'));
assert.ok(workflow.includes('verify_published_snapshot.py'));
const publishSource=block('async function published(m){','function updateModal(version)');
const navigationSource=block('function navigatePublishedRelease(version){','async function releases(){');
const releaseSource=block('async function releases(){','const legalFiles=');
const url='https://efishell0.github.io/OpenGLESScope_database/index.html#report/abcdef';
const target={schemaVersion:2,releaseReady:true,databaseVersion:'3.0.26',appAsset:'assets/app.v3026.js',cacheKey:'3026'};
const docs={
 './index.html':'<html>app.v3026.js site.v3026.css experience.v3026.js scroll-system.v3026.js OpenGLESScope Database <strong>3.0.26</strong></html>',
 './assets/app.v3026.js':"const DATABASE_VERSION='3.0.26'",
 './assets/site.v3026.css':'--accent:#ba2a8d;',
 './assets/release-bootstrap.v3026.js':"const LOCAL='3.0.26'",
 './assets/browser-compat.v3026.js':'__OPENGLESSCOPE_BROWSER_INFO__',
 './assets/experience.v3026.js':"const VERSION='3.0.26'",
 './assets/scroll-system.v3026.js':'viewportScrollbar'
};
const reads=[];
const store=new Map;
const navigations=[];
const modals=[];
const context={VERSION:'3.0.3',Date,URL,JSON,Promise,Number,String,
 releaseNavigationPending:false,
 newer:(a,b)=>a.split('.').map(Number).some((v,i)=>v!==Number(b.split('.')[i])&&v>Number(b.split('.')[i])),
 releaseMarkerValid:m=>m?.schemaVersion===2&&m?.releaseReady===true&&/^assets\/app\.v\d+\.js$/.test(m.appAsset)&&/^\d+$/.test(m.cacheKey),
 localText:async input=>{const path=input.split('?')[0];reads.push(path);if(!(path in docs))throw Error('missing asset '+path);return docs[path]},
 sessionStorage:{getItem:k=>store.get(k)||null,setItem:(k,v)=>store.set(k,v),removeItem:k=>store.delete(k)},
 location:{href:url,hash:'#report/abcdef',replace:u=>navigations.push(u)},
 updateModal:v=>modals.push(v),
 ready:true,releaseBusy:false,reachable:()=>true,document:{hidden:false},
 };
vm.createContext(context);
vm.runInContext(publishSource+navigationSource+releaseSource,context);
assert.equal(await vm.runInContext('published(target)',vm.createContext({...context,target})),true);
assert.equal(reads.length,7);
reads.length=0;
assert.equal(await vm.runInContext('published(target)',vm.createContext({...context,target:{...target,releaseReady:false}})),false);
assert.equal(reads.length,0);
const original=docs['./assets/scroll-system.v3026.js'];docs['./assets/scroll-system.v3026.js']='stale version';
assert.equal(await vm.runInContext('published(target)',vm.createContext({...context,target})),false);
docs['./assets/scroll-system.v3026.js']=original;
assert.equal(vm.runInContext("navigatePublishedRelease('3.0.26')",context),true);
assert.equal(navigations.length,1);
assert.equal(new URL(navigations[0]).searchParams.get('_release'),'3.0.26');
assert.equal(new URL(navigations[0]).hash,'#report/abcdef');
assert.equal(vm.runInContext("navigatePublishedRelease('3.0.26')",context),false);
assert.equal(navigations.length,1);
context.releaseNavigationPending=false;
assert.equal(vm.runInContext("navigatePublishedRelease('3.0.26')",context),false);
assert.deepEqual(modals,['3.0.26']);
const ctx2={...context,releaseNavigationPending:false,releaseBusy:false,ready:true,localText:async()=>JSON.stringify(target),published:async()=>true,navigatePublishedRelease:v=>navigations.push('releases:'+v)};
vm.createContext(ctx2);
vm.runInContext(releaseSource,ctx2);
await vm.runInContext('releases()',ctx2);
assert.equal(navigations.at(-1),'releases:3.0.26');
console.log('OpenGLESScope Database 3.0.26 fully published auto-navigation / anti-loop / 3-sec live sync / accepted-report snapshot contracts: ALL PASS');
