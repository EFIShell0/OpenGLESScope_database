import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const script=fs.readFileSync('assets/app.v3028.js','utf8');
const segment=script.slice(script.indexOf('const OGS_GPU_SIGNATURES='),script.indexOf('const summaryGpuLogoCell='));
assert.ok(segment.startsWith('const OGS_GPU_SIGNATURES='));
const fixture=`const OGS_VENDOR_NAMES=[];const implementationLayerText=()=>false;const esc=x=>x;${segment};({gpuIdentity,gpuLogoKey,explicitGpuSignature,translationLayer})`;
const values=vm.runInNewContext(fixture);
const cases=[
 ['Android Emulator OpenGL ES Translator (NVIDIA GeForce RTX 3050 Ti Laptop GPU/PCIe/SSE2)','NVIDIA GeForce RTX 3050 Ti Laptop GPU','nvidia','NVIDIA'],
 ['Android Emulator OpenGL ES Translator (AMD Radeon RX 7900 XT/PCIe)','AMD Radeon RX 7900 XT','amd','AMD'],
 ['Android Emulator OpenGL ES Translator (Intel(R) Iris Xe Graphics)','Intel(R) Iris Xe Graphics','intel','Intel'],
 ['Android Emulator OpenGL ES Translator (Adreno (TM) 710)','Adreno (TM) 710','qualcomm','Qualcomm'],
 ['Android Emulator OpenGL ES Translator (Mali-G78)','Mali-G78','arm','Arm'],
 ['Android Emulator OpenGL ES Translator (Immortalis-G715)','Immortalis-G715','arm','Arm'],
 ['Android Emulator OpenGL ES Translator (PowerVR GE8320)','PowerVR GE8320','imagination','Imagination Technologies'],
 ['Android Emulator OpenGL ES Translator (Xclipse 920)','Xclipse 920','samsung','Samsung'],
 ['Android Emulator OpenGL ES Translator (VideoCore VI)','VideoCore VI','broadcom','Broadcom'],
 ['Android Emulator OpenGL ES Translator (Vivante GC7000)','Vivante GC7000','vivante','Vivante'],
 ['Android Emulator OpenGL ES Translator (Maleoon 910)','Maleoon 910','huawei','Huawei'],
 ['Android Emulator OpenGL ES Translator (VeriSilicon VIP9000)','VeriSilicon VIP9000','unknown','VeriSilicon'],
 ['Android Emulator OpenGL ES Translator (Apple M2 Pro)','Apple M2 Pro','unknown','Apple'],
 ['ANGLE (NVIDIA, GeForce RTX 4090, Vulkan 1.3)','GeForce RTX 4090','nvidia','NVIDIA']
];
for(const [raw,model,logo,maker] of cases){
 const result=values.gpuIdentity('Google Inc.',raw);
 assert.equal(result.gpu,model,raw);
 assert.equal(result.rawRenderer,raw);
 assert.equal(result.rawVendor,'Google Inc.');
 assert.equal(values.gpuLogoKey('Google Inc.',raw),logo,raw);
 assert.equal(result.vendor,`Google LLC (${maker})`,raw);
 assert.ok(values.translationLayer(raw),raw);
}
const observed=values.gpuIdentity('Google (NVIDIA Corporation)',cases[0][0]);
assert.equal(observed.vendor,'Google (NVIDIA Corporation)');
assert.equal(observed.gpu,'NVIDIA GeForce RTX 3050 Ti Laptop GPU');
assert.equal(values.gpuLogoKey('Google (NVIDIA Corporation)',cases[0][0]),'nvidia');
for(const raw of [
 'Android Emulator OpenGL ES Translator (NVIDIA Corporation)',
 'Android Emulator OpenGL ES Translator (Unknown GPU)',
 'Android Emulator OpenGL ES Translator (SwiftShader NVIDIA GeForce RTX 3050 Ti Laptop GPU)',
 'Android Emulator OpenGL ES Translator (NVIDIA GeForce RTX 3050 Ti, AMD Radeon RX 7900 XT)',
 'Android Emulator OpenGL ES Translator (GeForce RTX 4090 and GeForce RTX 3050 Ti)',
 'ANGLE (NVIDIA, GeForce RTX 4090, SwiftShader)',
 'Bare unrecognized GPU'
]){
 assert.equal(values.gpuIdentity('Google Inc.',raw).gpu,raw,raw);
 assert.equal(values.gpuLogoKey('Google Inc.',raw),'unknown',raw);
}
assert.ok(script.includes('neutral artwork (no verified manufacturer logo)'));
for(const token of ['const OGS_EMULATOR_PREFIX=', 'raw.matchAll(new RegExp(re.source', 'matches.length===1?', "rawRenderer,logo:", "gpuIdentity(r.vendor||r.gpu_vendor,r.gpu_name).gpu"]){assert.ok(script.includes(token),token)}
for(const mutation of [segment.replace('OGS_EMULATOR_PREFIX.test(raw)','false'),segment.replace('matches.length===1?','matches.length>=1?'),segment.replace('OGS_SOFTWARE_RENDERER.test(raw)','false')]){
 const candidate=vm.runInNewContext(`const OGS_VENDOR_NAMES=[];const implementationLayerText=()=>false;const esc=x=>x;${mutation};({gpuIdentity,gpuLogoKey})`);
 const probe='Android Emulator OpenGL ES Translator (NVIDIA GeForce RTX 3050 Ti Laptop GPU/PCIe/SSE2)';
 const ambiguous='Android Emulator OpenGL ES Translator (NVIDIA GeForce RTX 3050 Ti, AMD Radeon RX 7900 XT)';
 const software='Android Emulator OpenGL ES Translator (SwiftShader NVIDIA GeForce RTX 3050 Ti Laptop GPU)';
 assert.ok(candidate.gpuIdentity('Google Inc.',probe).gpu!==values.gpuIdentity('Google Inc.',probe).gpu||candidate.gpuLogoKey('Google Inc.',ambiguous)!==values.gpuLogoKey('Google Inc.',ambiguous)||candidate.gpuIdentity('Google Inc.',software).gpu!==values.gpuIdentity('Google Inc.',software).gpu);
}
console.log('3.0.28 Database translator models/logos/raw evidence + negative mutation: PASS');
