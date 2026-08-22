import worker from '../src/index.js';
class Stmt{
  constructor(db,sql){this.db=db;this.sql=sql;this.args=[]}
  bind(...args){this.args=args;return this}
  async run(){
    if(this.sql.startsWith('INSERT OR IGNORE')){
      const [id,submitted_at,schema_version,gpu_name,vendor,opengles_version,egl_version,manufacturer,model,application_version,application_version_code,payload_json]=this.args;
      if(!this.db.rows.has(id))this.db.rows.set(id,{id,submitted_at,schema_version,gpu_name,vendor,opengles_version,egl_version,manufacturer,model,application_version,application_version_code,payload_json});
    }
    return {success:true};
  }
  async first(){
    if(this.sql.startsWith('SELECT submitted_at')){const r=this.db.rows.get(this.args[0]);return r?{submitted_at:r.submitted_at}:null}
    if(this.sql.startsWith('SELECT payload_json')){const r=this.db.rows.get(this.args[0]);return r?{payload_json:r.payload_json,submitted_at:r.submitted_at,id:r.id}:null}
    return null;
  }
  async all(){
    const rows=[...this.db.rows.values()].sort((a,b)=>b.submitted_at.localeCompare(a.submitted_at)||b.id.localeCompare(a.id));
    const limit=this.args.at(-1)||100;
    return {results:rows.slice(0,limit).map(({payload_json,...r})=>r)};
  }
}
class DB{constructor(){this.rows=new Map}prepare(sql){return new Stmt(this,sql)}}
const display={name:'Built-in',modeId:1,width:2400,height:1080,refreshRate:120,supportedModes:['2400x1080 @ 120 Hz'],wideColor:true,hdrTypes:[],desiredMaxLuminance:null,desiredMaxAverageLuminance:null,desiredMinLuminance:null};
const driverVersion='Unavailable (OpenGL ES does not expose a standardized driver-version query)';
const precisionNames=['GL_VERTEX_SHADER/GL_LOW_FLOAT','GL_VERTEX_SHADER/GL_MEDIUM_FLOAT','GL_VERTEX_SHADER/GL_HIGH_FLOAT','GL_VERTEX_SHADER/GL_LOW_INT','GL_VERTEX_SHADER/GL_MEDIUM_INT','GL_VERTEX_SHADER/GL_HIGH_INT','GL_FRAGMENT_SHADER/GL_LOW_FLOAT','GL_FRAGMENT_SHADER/GL_MEDIUM_FLOAT','GL_FRAGMENT_SHADER/GL_HIGH_FLOAT','GL_FRAGMENT_SHADER/GL_LOW_INT','GL_FRAGMENT_SHADER/GL_MEDIUM_INT','GL_FRAGMENT_SHADER/GL_HIGH_INT'];
function makePayload(version='0.2.2',versionCode=202,header='current'){
  const extensions=['GL_KHR_debug','GL_EXT_disjoint_timer_query'];
  const eglExtensions=['EGL_KHR_create_context'];
  const eglClientExtensions=['EGL_EXT_client_extensions'];
  const limits=[
    {name:'GL_MAX_TEXTURE_SIZE',value:'16384'},
    {name:'GL_MAX_DEBUG_MESSAGE_LENGTH',value:'1024'},
    {name:'GL_MAX_DEBUG_LOGGED_MESSAGES',value:'64'},
    {name:'GL_MAX_DEBUG_GROUP_STACK_DEPTH',value:'64'},
    {name:'GL_MAX_LABEL_LENGTH',value:'256'},
    {name:'GL_TIME_ELAPSED_EXT_QUERY_COUNTER_BITS',value:'64'},
    {name:'GL_TIMESTAMP_EXT_QUERY_COUNTER_BITS',value:'64'}
  ];
  const precision=[{shader:'GL_VERTEX_SHADER',type:'GL_HIGH_FLOAT',rangeMin:-126,rangeMax:127,precision:23}];
  const queryDiagnostics=[
    {name:'GL_EXTENSIONS',status:'Available',detail:''},
    {name:'EGL_EXTENSIONS',status:'Available',detail:''},
    {name:'EGL_NO_DISPLAY/EGL_EXTENSIONS',status:'Available',detail:''},
    {name:'EGL_VENDOR',status:'Available',detail:''},
    {name:'EGL_VERSION',status:'Available',detail:''},
    {name:'EGL_CLIENT_APIS',status:'Available',detail:''},
    {name:'compressedFormats',status:'Available',detail:''},
    {name:'shaderBinaryFormats',status:'Available',detail:''},
    {name:'programBinaryFormats',status:'Available',detail:''},
    ...limits.map(x=>({name:x.name,status:'Available',detail:''})),
    ...precisionNames.map(name=>({name,status:'Available',detail:''}))
  ];
  const eglConfigs=[{id:1,red:8,green:8,blue:8,alpha:8,depth:24,stencil:8,sampleBuffers:0,samples:0,surfaceType:'WINDOW',renderableType:'OPENGL_ES3',conformant:'OPENGL_ES3',configCaveat:'EGL_NONE',colorBufferType:'EGL_RGB_BUFFER',level:0,nativeRenderable:0,nativeVisualId:0,minSwapInterval:0,maxSwapInterval:1,bufferSize:32,luminanceSize:0,alphaMaskSize:0,bindToTextureRgb:0,bindToTextureRgba:0,maxPbufferWidth:4096,maxPbufferHeight:4096,maxPbufferPixels:16777216,nativeVisualType:0,transparentType:'EGL_NONE',transparentRed:0,transparentGreen:0,transparentBlue:0}];
  const p={schemaVersion:2,application:{name:'OpenGLESScope',packageName:'com.efishell.openglesscope',version,versionCode},device:{manufacturer:'Test',model:'Device',product:'product',androidRelease:'17',sdk:37,securityPatch:'2026-06-01'},gpu:{name:'Adreno Test',vendor:'Qualcomm'},driver:{mode:'System OpenGL ES/EGL',version:driverVersion},opengles:{version:'OpenGL ES 3.2 Test',major:3,minor:2,glslVersion:'OpenGL ES GLSL ES 3.20',extensions,extensionCount:extensions.length},egl:{vendor:'Android',version:'1.5',initializedVersion:'1.5',clientApis:'OpenGL_ES',extensions:eglExtensions,clientExtensions:eglClientExtensions,extensionCount:eglExtensions.length,clientExtensionCount:eglClientExtensions.length},display:{...display},collection:{status:'available',complete:true,source:'active Android system EGL/OpenGL ES implementation'},technicalReport:{schemaVersion:1,limits,extensions:[...extensions],eglExtensions:[...eglExtensions],eglClientExtensions:[...eglClientExtensions],compressedFormats:[],shaderBinaryFormats:[],programBinaryFormats:[],precision,queryDiagnostics,eglConfigs,display:{...display}},reportText:''};
  if(header==='legacy'){
    p.reportText=`OpenGLESScope ${version}\n\nOPENGL ES\nGL_VERSION: ${p.opengles.version}\n\nEGL\nEGL_VERSION: ${p.egl.version}\n\nDISPLAY & HDR\nDisplay: ${p.display.name}\n\nOPENGL ES LIMITS (${limits.length})\n${limits.map(x=>`${x.name}: ${x.value}`).join('\n')}\n\nOPENGL ES EXTENSIONS (${extensions.length})\n${extensions.join('\n')}\n\nEGL DISPLAY EXTENSIONS (${eglExtensions.length})\n${eglExtensions.join('\n')}\n\nEGL CLIENT EXTENSIONS (${eglClientExtensions.length})\n${eglClientExtensions.join('\n')}\n\nCOMPRESSED TEXTURE FORMATS (0)\n\nSHADER BINARY FORMATS (0)\n\nPROGRAM BINARY FORMATS (0)\n\nSHADER PRECISION (${precision.length})\nGL_VERTEX_SHADER | GL_HIGH_FLOAT | range -126..127 | precision 23\n\nQUERY DIAGNOSTICS (${queryDiagnostics.length})\n${queryDiagnostics.map(x=>`${x.name}: ${x.status}`).join('\n')}\n\nEGL CONFIGS (${eglConfigs.length})\n1 | test\n`;
    return p;
  }
  p.reportText=`OpenGLESScope report\n==================\nApplication: OpenGLESScope\nApplication version: ${version}\nApplication version code: ${versionCode}\nApplication package: com.efishell.openglesscope\nApplication ABI: arm64-v8a\nDeveloper: Semih Boran\nNickname: EFI Shell\nGitHub: https://github.com/EFIShell0\nGPU: ${p.gpu.name}\nDriver mode: ${p.driver.mode}\nDriver version: ${p.driver.version}\nOpenGL ES: ${p.opengles.version}\nEGL: ${p.egl.initializedVersion}\nDisplay: 2400x1080 @ 120.00 Hz\nHDR types: Unavailable\nAndroid: ${p.device.manufacturer} ${p.device.model}, ${p.device.androidRelease} (SDK ${p.device.sdk})\nAndroid security patch: ${p.device.securityPatch}\nSupported device ABIs: arm64-v8a, armeabi-v7a\nCollection status: Available\nCollection source: ${p.collection.source}\n\nDEVICE\nManufacturer: ${p.device.manufacturer}\nModel: ${p.device.model}\nProduct: ${p.device.product}\nAndroid: ${p.device.androidRelease} / API ${p.device.sdk}\nSecurity patch: ${p.device.securityPatch}\n\nOPENGL ES\nGL_RENDERER: ${p.gpu.name}\nGL_VENDOR: ${p.gpu.vendor}\nGL_VERSION: ${p.opengles.version}\nParsed core version: ${p.opengles.major}.${p.opengles.minor}\nGL_SHADING_LANGUAGE_VERSION: ${p.opengles.glslVersion}\n\nEGL\nEGL_VENDOR: ${p.egl.vendor}\nEGL_VERSION: ${p.egl.version}\nInitialized EGL version: ${p.egl.initializedVersion}\nEGL_CLIENT_APIS: ${p.egl.clientApis}\n\nDISPLAY & HDR\nDisplay: ${p.display.name}\nCurrent mode: 1 | 2400x1080 | 120.0 Hz\nSupported display modes (1): 2400x1080 @ 120 Hz\nRefresh rate: 120.0 Hz\nWide color gamut: Reported by Android display API\nHDR types: Unavailable\nDesired max luminance: Unavailable\nDesired max average luminance: Unavailable\nDesired min luminance: Unavailable\n\nOPENGL ES LIMITS (${limits.length})\n${limits.map(x=>`${x.name}: ${x.value}`).join('\n')}\n\nOPENGL ES EXTENSIONS (${extensions.length})\n${extensions.join('\n')}\n\nEGL DISPLAY EXTENSIONS (${eglExtensions.length})\n${eglExtensions.join('\n')}\n\nEGL CLIENT EXTENSIONS (${eglClientExtensions.length})\n${eglClientExtensions.join('\n')}\n\nCOMPRESSED TEXTURE FORMATS (0)\n\nSHADER BINARY FORMATS (0)\n\nPROGRAM BINARY FORMATS (0)\n\nSHADER PRECISION (${precision.length})\nGL_VERTEX_SHADER | GL_HIGH_FLOAT | range -126..127 | precision 23\n\nQUERY DIAGNOSTICS (${queryDiagnostics.length})\n${queryDiagnostics.map(x=>`${x.name}: ${x.status}`).join('\n')}\n\nEGL CONFIGS (${eglConfigs.length})\n1 | test\n`;
  return p;
}
const db=new DB(),env={DB:db,ALLOWED_ORIGIN:'https://efishell0.github.io'};
async function call(path,method='GET',body=null,headers={}){const init={method,headers:{origin:'https://efishell0.github.io',...headers}};if(body!==null)init.body=typeof body==='string'?body:JSON.stringify(body);return worker.fetch(new Request('https://api.example'+path,init),env)}
async function expect(name,response,status){if(response.status!==status)throw new Error(`${name}: expected ${status}, got ${response.status} ${await response.text()}`);console.log('PASS',name,status);return response}
let r=await call('/v1/health');await expect('health',r,200);const h=await r.json();if(h.databaseVersion!=='0.2.4'||h.compatibleProducer!=='OpenGLESScope 0.1.17+ within 0.x schema 2 / technical report 1'||h.currentProducer!=='OpenGLESScope 0.2.2'||h.normalizerVersion!==8||!h.publishedOpenGlesSpec||!h.publishedGlslEsSpec||!h.publishedEglSpec)throw new Error('health metadata mismatch');
r=await call('/v1/reports','POST',makePayload(),{'content-type':'application/json; charset=utf-8'});await expect('current 0.2.2 submission',r,201);const accepted=await r.json();
r=await call('/v1/reports/'+accepted.id);await expect('detail read',r,200);const detail=await r.json();if('normalized' in detail)throw new Error('structured detail should not duplicate normalized payload');if(detail.runtimeMetadata?.applicationAbi!=='arm64-v8a'||detail.runtimeMetadata?.androidRelease!=='17'||detail.runtimeMetadata?.sdk!==37||detail.runtimeMetadata?.supportedDeviceAbis?.length!==2)throw new Error('runtime metadata extraction mismatch');
const withPatch=makePayload();withPatch.device.securityPatch='2026-06-01';r=await call('/v1/reports','POST',withPatch,{'content-type':'application/json'});await expect('accept optional Android security patch',r,201);const withPatchAccepted=await r.json();r=await call('/v1/reports/'+withPatchAccepted.id);await expect('security patch detail read',r,200);const patchDetail=await r.json();if(patchDetail.runtimeMetadata?.securityPatch!=='2026-06-01')throw new Error('security patch metadata mismatch');
const malformedPatch=makePayload();malformedPatch.device.securityPatch='June 2026';r=await call('/v1/reports','POST',malformedPatch,{'content-type':'application/json'});await expect('reject malformed Android security patch',r,400);
const missingPatch=makePayload();delete missingPatch.device.securityPatch;missingPatch.reportText=missingPatch.reportText.replace('Android security patch: 2026-06-01\n','').replace('Security patch: 2026-06-01\n','');r=await call('/v1/reports','POST',missingPatch,{'content-type':'application/json'});await expect('reject current producer without Android security patch evidence',r,400);

r=await call('/v1/reports','POST',makePayload('0.1.25',125),{'content-type':'application/json'});await expect('0.1.25 compatibility',r,201);
const badCurrentCode=makePayload('0.2.2',203);r=await call('/v1/reports','POST',badCurrentCode,{'content-type':'application/json'});await expect('reject current producer versionCode mismatch',r,400);
const badLuminance=makePayload();badLuminance.display.desiredMaxLuminance=1000;badLuminance.technicalReport.display.desiredMaxLuminance=1000;badLuminance.reportText=badLuminance.reportText.replace('Desired max luminance: Unavailable','Desired max luminance: 1000');r=await call('/v1/reports','POST',badLuminance,{'content-type':'application/json'});await expect('reject current luminance without cd/m²',r,400);
const goodLuminance=makePayload();goodLuminance.display.desiredMaxLuminance=1000;goodLuminance.technicalReport.display.desiredMaxLuminance=1000;goodLuminance.reportText=goodLuminance.reportText.replace('Desired max luminance: Unavailable','Desired max luminance: 1000.0 cd/m²');r=await call('/v1/reports','POST',goodLuminance,{'content-type':'application/json'});await expect('accept current luminance with cd/m²',r,201);
const majorOne=makePayload('1.0.0',1000);r=await call('/v1/reports','POST',majorOne,{'content-type':'application/json'});await expect('reject unsupported future major producer',r,400);
const leadingZero=makePayload('0.02.1',201);r=await call('/v1/reports','POST',leadingZero,{'content-type':'application/json'});await expect('reject noncanonical producer version',r,400);
r=await call('/v1/reports','POST',makePayload('0.1.24',124),{'content-type':'application/json'});await expect('current 0.1.24 compatibility',r,201);
r=await call('/v1/reports','POST',makePayload('0.1.17',117,'legacy'),{'content-type':'application/json'});await expect('legacy 0.1.17 header',r,201);
const badVersion=makePayload();badVersion.reportText=badVersion.reportText.replace('Application version: 0.2.2','Application version: 9.9.9');r=await call('/v1/reports','POST',badVersion,{'content-type':'application/json'});await expect('reject TXT structured version mismatch',r,400);
const missingAbi=makePayload();missingAbi.reportText=missingAbi.reportText.replace('Application ABI: arm64-v8a\n','');r=await call('/v1/reports','POST',missingAbi,{'content-type':'application/json'});await expect('reject current report without ABI evidence',r,400);
const badDriver=makePayload();badDriver.reportText=badDriver.reportText.replace(`Driver version: ${driverVersion}`, 'Driver version: forged');r=await call('/v1/reports','POST',badDriver,{'content-type':'application/json'});await expect('reject driver TXT mismatch',r,400);
const badEgl=makePayload();badEgl.reportText=badEgl.reportText.replace('Initialized EGL version: 1.5','Initialized EGL version: 9.9');r=await call('/v1/reports','POST',badEgl,{'content-type':'application/json'});await expect('reject EGL TXT mismatch',r,400);
const badCount=makePayload();badCount.opengles.extensionCount++;r=await call('/v1/reports','POST',badCount,{'content-type':'application/json'});await expect('reject extension count mismatch',r,400);
const badSet=makePayload();badSet.technicalReport.extensions=['GL_EXT_other'];r=await call('/v1/reports','POST',badSet,{'content-type':'application/json'});await expect('reject duplicated extension set mismatch',r,400);
const dupExt=makePayload();dupExt.opengles.extensions.push(dupExt.opengles.extensions[0]);dupExt.opengles.extensionCount=dupExt.opengles.extensions.length;dupExt.technicalReport.extensions=[...dupExt.opengles.extensions];dupExt.reportText=dupExt.reportText.replace('OPENGL ES EXTENSIONS (2)','OPENGL ES EXTENSIONS (3)');r=await call('/v1/reports','POST',dupExt,{'content-type':'application/json'});await expect('reject duplicate extension token',r,400);
const dupLimit=makePayload();dupLimit.technicalReport.limits.push({...dupLimit.technicalReport.limits[0]});dupLimit.reportText=dupLimit.reportText.replace('OPENGL ES LIMITS (7)','OPENGL ES LIMITS (8)');r=await call('/v1/reports','POST',dupLimit,{'content-type':'application/json'});await expect('reject duplicate limit name',r,400);
const dupDiag=makePayload();dupDiag.technicalReport.queryDiagnostics.push({...dupDiag.technicalReport.queryDiagnostics[0]});dupDiag.reportText=dupDiag.reportText.replace(`QUERY DIAGNOSTICS (${dupDiag.technicalReport.queryDiagnostics.length-1})`,`QUERY DIAGNOSTICS (${dupDiag.technicalReport.queryDiagnostics.length})`);r=await call('/v1/reports','POST',dupDiag,{'content-type':'application/json'});await expect('reject duplicate diagnostic name',r,400);
const missingLimitEvidence=makePayload();missingLimitEvidence.technicalReport.queryDiagnostics=missingLimitEvidence.technicalReport.queryDiagnostics.filter(x=>x.name!=='GL_MAX_TEXTURE_SIZE');missingLimitEvidence.reportText=missingLimitEvidence.reportText.replace(`QUERY DIAGNOSTICS (${missingLimitEvidence.technicalReport.queryDiagnostics.length+1})`,`QUERY DIAGNOSTICS (${missingLimitEvidence.technicalReport.queryDiagnostics.length})`);r=await call('/v1/reports','POST',missingLimitEvidence,{'content-type':'application/json'});await expect('reject limit without Available diagnostic',r,400);
const missingPrecisionEvidence=makePayload();missingPrecisionEvidence.technicalReport.queryDiagnostics=missingPrecisionEvidence.technicalReport.queryDiagnostics.filter(x=>x.name!=='GL_VERTEX_SHADER/GL_HIGH_FLOAT');missingPrecisionEvidence.reportText=missingPrecisionEvidence.reportText.replace(`QUERY DIAGNOSTICS (${missingPrecisionEvidence.technicalReport.queryDiagnostics.length+1})`,`QUERY DIAGNOSTICS (${missingPrecisionEvidence.technicalReport.queryDiagnostics.length})`);r=await call('/v1/reports','POST',missingPrecisionEvidence,{'content-type':'application/json'});await expect('reject precision without Available diagnostic',r,400);
const badFormatEvidence=makePayload();badFormatEvidence.technicalReport.compressedFormats=['GL_COMPRESSED_TEST'];badFormatEvidence.technicalReport.queryDiagnostics.find(x=>x.name==='compressedFormats').status='Unavailable';badFormatEvidence.reportText=badFormatEvidence.reportText.replace('COMPRESSED TEXTURE FORMATS (0)','COMPRESSED TEXTURE FORMATS (1)');r=await call('/v1/reports','POST',badFormatEvidence,{'content-type':'application/json'});await expect('reject enumerants with unavailable query evidence',r,400);
const missingTimer=makePayload();missingTimer.technicalReport.queryDiagnostics=missingTimer.technicalReport.queryDiagnostics.filter(x=>x.name!=='GL_TIMESTAMP_EXT_QUERY_COUNTER_BITS');missingTimer.reportText=missingTimer.reportText.replace(`QUERY DIAGNOSTICS (${missingTimer.technicalReport.queryDiagnostics.length+1})`,`QUERY DIAGNOSTICS (${missingTimer.technicalReport.queryDiagnostics.length})`);r=await call('/v1/reports','POST',missingTimer,{'content-type':'application/json'});await expect('reject timer extension without query evidence',r,400);
const missingDebug=makePayload();missingDebug.technicalReport.queryDiagnostics=missingDebug.technicalReport.queryDiagnostics.filter(x=>x.name!=='GL_MAX_LABEL_LENGTH');missingDebug.reportText=missingDebug.reportText.replace(`QUERY DIAGNOSTICS (${missingDebug.technicalReport.queryDiagnostics.length+1})`,`QUERY DIAGNOSTICS (${missingDebug.technicalReport.queryDiagnostics.length})`);r=await call('/v1/reports','POST',missingDebug,{'content-type':'application/json'});await expect('reject core debug limit without query evidence',r,400);
const dupConfig=makePayload();dupConfig.technicalReport.eglConfigs.push({...dupConfig.technicalReport.eglConfigs[0]});dupConfig.reportText=dupConfig.reportText.replace('EGL CONFIGS (1)','EGL CONFIGS (2)');r=await call('/v1/reports','POST',dupConfig,{'content-type':'application/json'});await expect('reject duplicate EGL config id',r,400);
const old=makePayload('0.1.16',116,'legacy');r=await call('/v1/reports','POST',old,{'content-type':'application/json'});await expect('reject below compatibility floor',r,400);
const extra=makePayload();extra.device.extra='x';r=await call('/v1/reports','POST',extra,{'content-type':'application/json'});await expect('reject extra schema field',r,400);
const sensitive=makePayload();sensitive.device.account_id='x';r=await call('/v1/reports','POST',sensitive,{'content-type':'application/json'});await expect('reject sensitive or unknown field',r,400);
const badDisplay=makePayload();badDisplay.technicalReport.display.width=1;r=await call('/v1/reports','POST',badDisplay,{'content-type':'application/json'});await expect('reject duplicated display mismatch',r,400);
const badStatus=makePayload();badStatus.technicalReport.queryDiagnostics[0].status='SUPPORTED';r=await call('/v1/reports','POST',badStatus,{'content-type':'application/json'});await expect('reject noncanonical diagnostic state',r,400);
r=await call('/v1/reports','POST',makePayload(),{'content-type':'application/jsonp'});await expect('reject media type lookalike',r,415);
r=await worker.fetch(new Request('https://api.example/v1/health',{headers:{origin:'https://evil.example'}}),env);await expect('reject foreign origin',r,403);
r=await call('/v1/reports/not-a-hash');await expect('reject invalid id',r,400);
r=await call('/v1/reports?beforeSubmittedAt=2026-08-21T00:00:00Z');await expect('reject incomplete cursor pair',r,400);
r=await call('/v1/reports?beforeSubmittedAt=bad&beforeId='+'a'.repeat(64));await expect('reject malformed cursor',r,400);
r=await call('/v1/reports/'+'f'.repeat(64));await expect('missing report',r,404);
r=await call('/v1/not-found');await expect('unknown route',r,404);
r=await call('/v1/health','POST','{}',{'content-type':'application/json'});await expect('method allow',r,405);if(r.headers.get('allow')!=='GET, OPTIONS')throw new Error('Allow mismatch');
r=await call('/v1/reports','OPTIONS');await expect('preflight',r,204);if(r.headers.get('x-content-type-options')!=='nosniff'||r.headers.get('x-frame-options')!=='DENY'||!r.headers.get('content-security-policy'))throw new Error('preflight security headers mismatch');
const large='x'.repeat(2*1024*1024+1);r=await call('/v1/reports','POST',large,{'content-type':'application/json'});await expect('stream body bound',r,413);
console.log('ALL PASS');
