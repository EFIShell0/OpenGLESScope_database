import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const script=fs.readFileSync('assets/app.v3022.js','utf8');
const html=fs.readFileSync('index.html','utf8');
const segment=script.slice(script.indexOf('const OGS_GPU_SIGNATURES='),script.indexOf('const summaryGpuLogoCell='));
assert.ok(segment.startsWith('const OGS_GPU_SIGNATURES='),'GPU matcher must be present');
const values=vm.runInNewContext(`const OGS_VENDOR_NAMES=[];const implementationLayerText=()=>false;const esc=x=>x;${segment};({gpuIdentity,gpuLogoKey,explicitGpuSignature})`);
const cases=[
 ['ANGLE (Qualcomm, Vulkan 1.3.284 (Adreno (TM) 710 (0x07010000)), Qualcomm Driver)','Adreno (TM) 710','qualcomm','Qualcomm'],
 ['ANGLE (ARM, Mali-G78, Vulkan 1.3)','Mali-G78','arm','Arm'],
 ['ANGLE (ARM, Immortalis-G715, Vulkan)','Immortalis-G715','arm','Arm'],
 ['ANGLE (Imagination, PowerVR GE8320, Vulkan)','PowerVR GE8320','imagination','Imagination Technologies'],
 ['ANGLE (Samsung, Xclipse 920, Vulkan)','Xclipse 920','samsung','Samsung'],
 ['ANGLE (NVIDIA, GeForce RTX 4090, D3D11)','GeForce RTX 4090','nvidia','NVIDIA'],
 ['ANGLE (AMD, Radeon RX 7900 XT, D3D12)','Radeon RX 7900 XT','amd','AMD'],
 ['ANGLE (Intel, Intel(R) UHD Graphics 620, D3D11)','Intel(R) UHD Graphics 620','intel','Intel'],
 ['ANGLE (Broadcom, VideoCore VI, Vulkan)','VideoCore VI','broadcom','Broadcom'],
 ['ANGLE (Vivante, Vivante GC7000, Vulkan)','Vivante GC7000','vivante','Vivante'],
 ['ANGLE (Huawei, Maleoon 910, Vulkan)','Maleoon 910','huawei','Huawei'],
 ['ANGLE (VeriSilicon, VeriSilicon VIP9000, Vulkan)','VeriSilicon VIP9000','unknown','VeriSilicon'],
 ['ANGLE (Apple, Apple M2 Pro, Metal)','Apple M2 Pro','unknown','Apple']
];
for(const [raw,model,key,maker] of cases){
 const x=values.gpuIdentity('Google Inc.',raw);
 assert.equal(x.gpu,model,raw); assert.equal(x.vendor,`Google LLC (${maker})`,raw);
 assert.equal(values.gpuLogoKey('Google Inc.',raw),key,raw);
 assert.equal(x.rawRenderer,raw);assert.equal(x.rawVendor,'Google Inc.');
}
for(const raw of ['ANGLE (Google, SwiftShader, Adreno (TM) 710)','ANGLE (Unknown, Vulkan 1.3)','ANGLE (Qualcomm, Vulkan 1.3)','ANGLE (NVIDIA, GeForce RTX 4090, AMD Radeon RX 7900)']){
 assert.equal(values.gpuIdentity('Google Inc.',raw).gpu,raw);
 assert.equal(values.gpuLogoKey('Google Inc.',raw),'unknown');
}
assert.equal(values.gpuIdentity('Google Inc. (Qualcomm)',cases[0][0]).vendor,'Google LLC (Qualcomm)');
assert.match(script,/summaryGpu=r=>gpuIdentity\(/);
assert.ok(script.includes("gpuLogoMarkup(summaryVendor(r),r.gpu_name||r.gpu||'')"),'summary GPU icon must retain raw ANGLE renderer for identification');
assert.match(html,/id="settingsEglApisDefault"/);
assert.match(script,/regional\.eglApisExpanded=data\.regional\?\.eglApisExpanded===true/);
assert.match(script,/\['settingsEglApisDefault','eglApisExpanded'\]/);
assert.match(script,/disclosure\(8,'typeToggle','EGL APIs','eglApisExpanded'/);
assert.ok(script.includes("$('#settingsEglApisDefault').checked=regional.eglApisExpanded"));
console.log('3.0.22 multi-brand ANGLE + raw GPU report evidence + EGL APIs settings: PASS');
