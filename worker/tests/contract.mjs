import worker from '../src/index.js';
class Stmt{
  constructor(db,sql){this.db=db;this.sql=sql;this.args=[]}
  bind(...args){this.args=args;return this}
  async run(){
    if(this.sql.startsWith('INSERT OR IGNORE')){
      const [id,submitted_at,schema_version,gpu_name,vendor,opengles_version,egl_version,manufacturer,model,application_version,application_version_code,payload_json]=this.args;
      if(!this.db.rows.has(id))this.db.rows.set(id,{id,submitted_at,schema_version,gpu_name,vendor,opengles_version,egl_version,manufacturer,model,application_version,application_version_code,payload_json});
    }
    return {success:true}
  }
  async first(){
    if(this.sql.startsWith('SELECT submitted_at')){const r=this.db.rows.get(this.args[0]);return r?{submitted_at:r.submitted_at}:null}
    if(this.sql.startsWith('SELECT payload_json')){const r=this.db.rows.get(this.args[0]);return r?{payload_json:r.payload_json,submitted_at:r.submitted_at,id:r.id}:null}
    return null
  }
  async all(){
    const rows=[...this.db.rows.values()].sort((a,b)=>b.submitted_at.localeCompare(a.submitted_at)||b.id.localeCompare(a.id));
    const limit=this.args.at(-1)||100;
    return {results:rows.slice(0,limit).map(({payload_json,...r})=>r)}
  }
}
class DB{constructor(){this.rows=new Map}prepare(sql){return new Stmt(this,sql)}}
const display={name:'Built-in',modeId:1,width:2400,height:1080,refreshRate:120,supportedModes:['2400x1080 @ 120 Hz'],wideColor:true,hdrTypes:[],desiredMaxLuminance:null,desiredMaxAverageLuminance:null,desiredMinLuminance:null};
function payload(version='0.1.23',versionCode=123,header='current'){
  let reportText=header==='current'?`OpenGLESScope report\n==================\nApplication: OpenGLESScope\nApplication version: ${version}\nApplication version code: ${versionCode}\nApplication package: com.efishell.openglesscope\nApplication ABI: arm64-v8a\nDeveloper: Semih Boran\nNickname: EFI Shell\nGitHub: https://github.com/EFIShell0\n`:`OpenGLESScope ${version}\n`;
  reportText+=`\nDEVICE\nManufacturer: Test\n\nOPENGL ES\nGL_VERSION: OpenGL ES 3.2 Test\n\nEGL\nEGL_VERSION: 1.5\n\nDISPLAY & HDR\nDisplay: Built-in\n\nOPENGL ES LIMITS (1)\nmaxTextureSize: 16384\n\nOPENGL ES EXTENSIONS (1)\nGL_EXT_test\n\nEGL DISPLAY EXTENSIONS (1)\nEGL_EXT_test\n\nEGL CLIENT EXTENSIONS (1)\nEGL_EXT_client\n\nCOMPRESSED TEXTURE FORMATS (0)\n\nSHADER BINARY FORMATS (0)\n\nPROGRAM BINARY FORMATS (0)\n\nSHADER PRECISION (1)\nvertex | high_float | range -126..127 | precision 23\n\nQUERY DIAGNOSTICS (1)\nmaxTextureSize: Available\n\nEGL CONFIGS (1)\n1 | test\n`;
  return {schemaVersion:2,application:{name:'OpenGLESScope',packageName:'com.efishell.openglesscope',version,versionCode},device:{manufacturer:'Test',model:'Device',product:'product',androidRelease:'17',sdk:37},gpu:{name:'Adreno Test',vendor:'Qualcomm'},driver:{mode:'System OpenGL ES/EGL',version:'OpenGL ES 3.2 Test'},opengles:{version:'OpenGL ES 3.2 Test',major:3,minor:2,glslVersion:'OpenGL ES GLSL ES 3.20',extensions:['GL_EXT_test'],extensionCount:1},egl:{vendor:'Android',version:'1.5',initializedVersion:'1.5',clientApis:'OpenGL_ES',extensions:['EGL_EXT_test'],clientExtensions:['EGL_EXT_client'],extensionCount:1,clientExtensionCount:1},display:{...display},collection:{status:'available',complete:true,source:'active Android system EGL/OpenGL ES implementation'},technicalReport:{schemaVersion:1,limits:[{name:'maxTextureSize',value:'16384'}],extensions:['GL_EXT_test'],eglExtensions:['EGL_EXT_test'],eglClientExtensions:['EGL_EXT_client'],compressedFormats:[],shaderBinaryFormats:[],programBinaryFormats:[],precision:[{shader:'vertex',type:'high_float',rangeMin:-126,rangeMax:127,precision:23}],queryDiagnostics:[{name:'maxTextureSize',status:'Available',detail:''}],eglConfigs:[{id:1,red:8,green:8,blue:8,alpha:8,depth:24,stencil:8,sampleBuffers:0,samples:0,surfaceType:'WINDOW',renderableType:'OPENGL_ES3',conformant:'OPENGL_ES3',configCaveat:'EGL_NONE',colorBufferType:'EGL_RGB_BUFFER',level:0,nativeRenderable:0,nativeVisualId:0,minSwapInterval:0,maxSwapInterval:1,bufferSize:32,luminanceSize:0,alphaMaskSize:0,bindToTextureRgb:0,bindToTextureRgba:0,maxPbufferWidth:4096,maxPbufferHeight:4096,maxPbufferPixels:16777216,nativeVisualType:0,transparentType:'EGL_NONE',transparentRed:0,transparentGreen:0,transparentBlue:0}],display:{...display}},reportText};
}
const db=new DB(),env={DB:db,ALLOWED_ORIGIN:'https://efishell0.github.io'};
async function call(path,method='GET',body=null,headers={}){const init={method,headers:{origin:'https://efishell0.github.io',...headers}};if(body!==null)init.body=typeof body==='string'?body:JSON.stringify(body);return worker.fetch(new Request('https://api.example'+path,init),env)}
async function expect(name,response,status){if(response.status!==status)throw new Error(`${name}: expected ${status}, got ${response.status} ${await response.text()}`);console.log('PASS',name,status);return response}
let r=await call('/v1/health');await expect('health',r,200);const h=await r.json();if(h.databaseVersion!=='0.1.19'||h.compatibleProducer!=='OpenGLESScope 0.1.17+')throw new Error('health metadata mismatch');
r=await call('/v1/reports','POST',payload(),{'content-type':'application/json; charset=utf-8'});await expect('current 0.1.23 submission',r,201);const accepted=await r.json();
r=await call('/v1/reports/'+accepted.id);await expect('detail read',r,200);const detail=await r.json();if('normalized' in detail)throw new Error('structured detail should not duplicate normalized payload');

r=await call('/v1/reports','POST',payload('0.1.17',117,'legacy'),{'content-type':'application/json'});await expect('legacy 0.1.17 header',r,201);
const badHeader=payload();badHeader.reportText=badHeader.reportText.replace('Application version: 0.1.23','Application version: 9.9.9');r=await call('/v1/reports','POST',badHeader,{'content-type':'application/json'});await expect('reject TXT/structured version mismatch',r,400);
const badCount=payload();badCount.opengles.extensionCount=2;r=await call('/v1/reports','POST',badCount,{'content-type':'application/json'});await expect('reject extension count mismatch',r,400);
const badSet=payload();badSet.technicalReport.extensions=['GL_EXT_other'];r=await call('/v1/reports','POST',badSet,{'content-type':'application/json'});await expect('reject duplicated extension-set mismatch',r,400);

const old=payload('0.1.16',116,'legacy');r=await call('/v1/reports','POST',old,{'content-type':'application/json'});await expect('reject below compatibility floor',r,400);
const extra=payload();extra.device.extra='x';r=await call('/v1/reports','POST',extra,{'content-type':'application/json'});await expect('reject extra schema field',r,400);
const badDisplay=payload();badDisplay.technicalReport.display.width=1;r=await call('/v1/reports','POST',badDisplay,{'content-type':'application/json'});await expect('reject duplicated display mismatch',r,400);
const badStatus=payload();badStatus.technicalReport.queryDiagnostics[0].status='SUPPORTED';r=await call('/v1/reports','POST',badStatus,{'content-type':'application/json'});await expect('reject noncanonical diagnostic state',r,400);
r=await call('/v1/reports','POST',payload(),{'content-type':'application/jsonp'});await expect('reject media-type lookalike',r,415);
r=await worker.fetch(new Request('https://api.example/v1/health',{headers:{origin:'https://evil.example'}}),env);await expect('reject foreign origin',r,403);
r=await call('/v1/reports/not-a-hash');await expect('reject invalid id',r,400);
r=await call('/v1/reports?beforeSubmittedAt=2026-08-21T00:00:00Z');await expect('reject incomplete cursor pair',r,400);
r=await call('/v1/reports?beforeSubmittedAt=bad&beforeId='+'a'.repeat(64));await expect('reject malformed cursor',r,400);
r=await call('/v1/reports/'+'f'.repeat(64));await expect('missing report',r,404);
r=await call('/v1/not-found');await expect('unknown route',r,404);

r=await call('/v1/health','POST','{}',{'content-type':'application/json'});await expect('method allow',r,405);if(r.headers.get('allow')!=='GET, OPTIONS')throw new Error('Allow mismatch');
const large='x'.repeat(2*1024*1024+1);r=await call('/v1/reports','POST',large,{'content-type':'application/json'});await expect('stream body bound',r,413);
console.log('ALL PASS');
