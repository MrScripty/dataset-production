// Pure, dependency-free teaching models. No backend or model calls.
export const WIDTH=20, HEIGHT=12;
export const clone = value => structuredClone(value);
export function pointToUnit(x,y,w=WIDTH,h=HEIGHT){
  if(w<2||h<2) throw new Error('Point-center normalization needs dimensions >= 2');
  return [x/(w-1),y/(h-1)];
}
export function maskBox(mask,w=WIDTH,h=HEIGHT){
  if(mask.length!==w*h) throw new Error('Mask dimensions do not match');
  let minX=w,minY=h,maxX=-1,maxY=-1,count=0;
  mask.forEach((v,i)=>{if(v!==0&&v!==255)throw new Error('Mask must contain only 0 and 255');if(v){const x=i%w,y=Math.floor(i/w);minX=Math.min(minX,x);maxX=Math.max(maxX,x);minY=Math.min(minY,y);maxY=Math.max(maxY,y);count++;}});
  return count?{present:true,pixels:count,xyxy:[minX,minY,maxX+1,maxY+1],normalized:[minX/w,minY/h,(maxX+1)/w,(maxY+1)/h]}:{present:false,pixels:0,xyxy:null,normalized:null};
}
export function presetMask(name='book'){
 const mask=Array(WIDTH*HEIGHT).fill(0);
 if(name==='last')mask[mask.length-1]=255;
 if(name==='book')for(let y=2;y<10;y++)for(let x=5;x<15;x++)if(!(y>=7&&x>=12))mask[y*WIDTH+x]=255;
 return mask;
}
export function fixtureRows(){return [
{id:'a1',object:'A',session:'S1',source:'P1',split:'train'},
{id:'a2',object:'A',session:'S2',source:'P2',split:'test'},
{id:'b1',object:'B',session:'S2',source:'P3',split:'val'},
{id:'b2',object:'B',session:'S3',source:'P4',split:'train'},
{id:'c1',object:'C',session:'S4',source:'P5',split:'test'},
{id:'c2',object:'C',session:'S4',source:'P5',split:'test'},
{id:'d1',object:'D',session:'S5',source:'P6',split:'val'},
{id:'e1',object:'E',session:'S6',source:'P7',split:'train'}];}
export function families(rows,keys=['object','session','source']){
 const parents=rows.map((_,i)=>i);const root=i=>parents[i]===i?i:(parents[i]=root(parents[i]));
 const edges=[];
 for(let i=0;i<rows.length;i++)for(let j=i+1;j<rows.length;j++){
  const links=keys.filter(k=>rows[i][k]&&rows[i][k]===rows[j][k]);
  if(links.length){parents[root(j)]=root(i);edges.push({a:rows[i].id,b:rows[j].id,links});}
 }
 const groups=new Map();rows.forEach((r,i)=>{const key=root(i);if(!groups.has(key))groups.set(key,[]);groups.get(key).push(r);});
 return {groups:[...groups.values()],edges};
}
export function splitWarnings(rows,keys){return families(rows,keys).groups.filter(g=>new Set(g.map(r=>r.split)).size>1).map(g=>({ids:g.map(r=>r.id),splits:[...new Set(g.map(r=>r.split))]}));}
export function repairSplits(rows,keys){
 // Stable component-level assignment. No claim of optimal class balance.
 const output=clone(rows); const groups=families(output,keys).groups.sort((a,b)=>b.length-a.length||a[0].id.localeCompare(b[0].id));
 groups.forEach((g,i)=>g.forEach(r=>r.split=['train','test','val','train'][i%4]));return output;
}
export const candidateFixtures=[
 {id:'c01',scene:'blue',caption:'One blue book on a light desk.',expected:{count:'one',color:'blue'},score:0.92},
 {id:'c02',scene:'coral',caption:'Two blue books on a light desk.',expected:{count:'one',color:'coral'},score:0.97},
 {id:'c03',scene:'green',caption:'One green book, partly hidden by a hand.',expected:{count:'one',color:'green'},score:0.88},
 {id:'c04',scene:'blue',caption:'',expected:{count:'one',color:'blue'},score:0.99}
];
export function checkCandidate(c){
 const text=c.caption.trim().toLowerCase();
 const schema=text.length>=8&&text.length<=200;
 const fact=schema&&text.includes(c.expected.count)&&text.includes(c.expected.color)&&!text.includes('two');
 return {schema,fact};
}
export function decideCandidate(candidate,decision,checklist){
 if(!['accepted','rejected'].includes(decision))throw new Error('Unknown decision');
 const checks=checkCandidate(candidate);
 if(decision==='accepted'&&(!checks.schema||!checks.fact||!checklist))throw new Error('Resolve checks and complete human review before acceptance');
 return {...candidate,status:decision,revision:candidate.revision+1,reviewed:decision==='accepted',checks};
}
export function defaultState(){return {
 version:1,mask:presetMask(),corners:[[5,2],[14,2],[14,9],[5,9]],rows:fixtureRows(),keys:['object','session','source'],
 candidates:candidateFixtures.map(c=>({...clone(c),status:'pending',revision:1,reviewed:false})),
 lineage:[{id:'asset-001',parent:null,operation:'Original fixture',width:20,height:12,annotation:'ann-001',status:'reviewed'}],
 rights:false,releases:[],reviewLog:[],drafts:{}
};}
export function validState(s){
 try {if(!s||s.version!==1||!Array.isArray(s.mask)||s.mask.length!==240||!Array.isArray(s.corners)||s.corners.length!==4||!s.corners.every(p=>Array.isArray(p)&&p.length===2&&p.every(Number.isFinite)))return false;maskBox(s.mask);return Array.isArray(s.rows)&&s.rows.length===8&&s.rows.every(r=>['train','val','test'].includes(r.split))&&Array.isArray(s.candidates)&&s.candidates.length===4&&Array.isArray(s.lineage)&&s.lineage.length>0&&Array.isArray(s.releases)&&Array.isArray(s.reviewLog)&&Array.isArray(s.keys)&&s.keys.every(k=>['object','session','source'].includes(k));}catch{return false;}
}
export function addCrop(lineage,crop){
 const parent=lineage.at(-1);const {x,y,width,height}=crop;
 if(![x,y,width,height].every(Number.isInteger)||x<0||y<0||width<2||height<2||x+width>parent.width||y+height>parent.height)throw new Error('Crop must fit inside the current image and be at least 2 × 2');
 return [...clone(lineage),{id:`asset-${String(lineage.length+1).padStart(3,'0')}`,parent:parent.id,operation:'crop',recipe:'crop-v1',crop:{...crop},width,height,annotation:null,status:'needs-review'}];
}
export function releaseChecks(s){return [
 {id:'rights',label:'Document the fixture’s permitted use',ok:s.rights,detail:'This assertion applies only to this site’s original procedural fixtures. It is not legal clearance for other sources.'},
 {id:'families',label:'Keep linked families in one split',ok:splitWarnings(s.rows,['object','session','source']).length===0,detail:'Release policy always checks object, session, and source together, even if a lab filter is hidden.'},
 {id:'coverage',label:'Retain train, validation, and test groups',ok:['train','val','test'].every(k=>s.rows.some(r=>r.split===k)),detail:'Presence is a structural check. Eight toy rows are too small for real generalization claims.'},
 {id:'drafts',label:'Save or discard unfinished caption drafts',ok:Object.keys(s.drafts||{}).length===0,detail:'A frozen release must not silently leave an edited proposal outside the reviewed selection.'},
 {id:'review',label:'Resolve every synthetic candidate',ok:s.candidates.every(c=>c.status!=='pending')&&s.candidates.some(c=>c.status==='accepted'),detail:'Accept only after schema, known scene properties, and human review; reject unsuitable proposals.'},
 {id:'lineage',label:'Review the latest transformed annotation',ok:s.lineage.at(-1).status==='reviewed',detail:'A crop changes the coordinate frame. Parent annotations cannot silently remain valid.'},
 {id:'geometry',label:'Validate binary-mask encoding',ok:s.mask.every(v=>v===0||v===255),detail:'An empty mask is a valid no-object example; its localization target is absent.'}
];}
export function snapshot(s){
 const checks=releaseChecks(s);if(checks.some(c=>!c.ok))throw new Error('Resolve release gates before freezing');
 return {schema:'dataset-production-demo/v1',id:`release-${String(s.releases.length+1).padStart(3,'0')}`,created_at:new Date().toISOString(),simulation:true,scope:'Educational manifest, not a loader-tested training bundle',task:'book-geometry-and-caption-demo',source_policy:'Original procedural fixtures only; no personal data',split_policy:['object','session','source'],rows:clone(s.rows),annotation:{id:'lab-annotation',image_width:WIDTH,image_height:HEIGHT,corners:s.corners.map(p=>pointToUnit(...p)),corner_convention:'pixel-centers/(dimension-1)',mask_encoding:'binary-0-or-255',mask:clone(s.mask),box:maskBox(s.mask),box_convention:'half-open-edges/dimension'},candidates:clone(s.candidates),lineage:clone(s.lineage),review_log:clone(s.reviewLog),gates:checks.map(c=>({id:c.id,passed:c.ok})),consumer_validation:'Not run; requires a task-specific adapter and real loader tests'};
}
const crcTable=Array.from({length:256},(_,n)=>{for(let k=0;k<8;k++)n=n&1?0xedb88320^(n>>>1):n>>>1;return n>>>0;});
export function crc32(bytes){let c=0xffffffff;for(const b of bytes)c=crcTable[(c^b)&255]^(c>>>8);return (c^0xffffffff)>>>0;}
function chunk(type,data){const out=new Uint8Array(data.length+12),v=new DataView(out.buffer);v.setUint32(0,data.length);out.set(new TextEncoder().encode(type),4);out.set(data,8);v.setUint32(data.length+8,crc32(out.subarray(4,-4)));return out;}
export async function grayscalePng(mask,w=WIDTH,h=HEIGHT){
 maskBox(mask,w,h);const header=new Uint8Array(13),hv=new DataView(header.buffer);hv.setUint32(0,w);hv.setUint32(4,h);header[8]=8;header[9]=0;
 const raw=new Uint8Array((w+1)*h);for(let y=0;y<h;y++)raw.set(mask.slice(y*w,(y+1)*w),y*(w+1)+1);
 const compressed=new Uint8Array(await new Response(new Blob([raw]).stream().pipeThrough(new CompressionStream('deflate'))).arrayBuffer());
 const parts=[new Uint8Array([137,80,78,71,13,10,26,10]),chunk('IHDR',header),chunk('IDAT',compressed),chunk('IEND',new Uint8Array())];
 const png=new Uint8Array(parts.reduce((n,p)=>n+p.length,0));let offset=0;for(const p of parts){png.set(p,offset);offset+=p.length;}return png;
}
