// Source-level DOM mock tests only. No browser, file URL navigation or network.
const fs=require('fs'), vm=require('vm'), assert=require('assert');
const file=process.argv[2];const html=fs.readFileSync(file,'utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
class Node {
  constructor(tag,doc){this.tagName=tag;this.doc=doc;this.children=[];this.events={};this.attrs={};this.style={};this._text='';this.value='';this.disabled=false}
  set textContent(v){this._text=String(v);this.children=[]}get textContent(){return this._text+this.children.map(c=>c.textContent).join(' ')}
  append(...nodes){this.children.push(...nodes);if(this.tagName==='select'&&!this.value&&nodes[0])this.value=nodes[0].value}
  replaceChildren(...nodes){this.children=[];this._text='';this.append(...nodes)}
  setAttribute(k,v){this.attrs[k]=v}addEventListener(k,fn){this.events[k]=fn}
  click(){if(this.disabled)return;if(this.tagName==='a')this.doc.downloads.push({name:this.download,url:this.href});if(this.events.click)this.events.click()}
  scrollIntoView(){}
}
function setup(storage={},denyStorage=false){
 const document={elements:{},downloads:[],createElement(tag){return new Node(tag,this)},getElementById(id){if(!this.elements[id])this.elements[id]=new Node(id==='course'?'select':'div',this);return this.elements[id]},querySelectorAll(){return[]}};
 const blobs=[]; const context={document,console,localStorage:{getItem(k){if(denyStorage)throw Error('blocked');return storage[k]??null},setItem(k,v){if(denyStorage)throw Error('blocked');storage[k]=v}},window:{confirm(){return true},print(){}},URL:{createObjectURL(b){blobs.push(b);return 'mock:'+blobs.length},revokeObjectURL(){}},Blob:class{constructor(parts,opt){this.parts=parts;this.type=opt.type}},setTimeout(fn){fn()}};
 vm.createContext(context);vm.runInContext(script,context,{timeout:5000});return{context,document,storage,blobs};
}
let checks=0;const ok=(description,fn)=>{fn();checks++;console.log('PASS '+description)};
const t=setup(),$=id=>t.document.getElementById(id);
ok('four course options',()=>assert.equal($('course').children.length,4));
ok('initial lesson is ZIM M01',()=>assert.match($('lesson').textContent,/ZIM-M01/));
ok('36 lessons tracked',()=>assert.match($('count').textContent,/0 of 36/));
ok('first previous button disabled',()=>assert.equal($('prev').disabled,true));
ok('next renders second lesson',()=>{$('next').click();assert.match($('lesson').textContent,/ZIM-M02/)});
ok('course selection updates lesson',()=>{$('course').value='ZDV';$('course').events.change();assert.match($('lesson').textContent,/ZDV-M01/)});
ok('search filters to sync lesson',()=>{$('search').value='synchronization';$('search').events.input();assert.equal($('modules').children.length,1);assert.match($('modules').textContent,/ZDV-M09/)});
ok('search has empty result message',()=>{$('search').value='no_possible_match';$('search').events.input();assert.match($('modules').textContent,/No matching lessons/)});
ok('all 36 lessons render required sections',()=>{let n=0;$('search').value='';for(const cid of ['ZIM','ZDV','AAB','CAW']){$('course').value=cid;$('course').events.change();for(const b of [...$('modules').children]){b.click();const text=$('lesson').textContent;for(const expected of ['Guided practice steps','Expected output','Test a failure','Recover and retest','Independent assignment','Acceptance checks'])assert(text.includes(expected));n++}}assert.equal(n,36)});
ok('trainer view includes scoring',()=>{$('trainer').click();assert.match($('lesson').textContent,/Trainer expected result/);assert.equal($('trainer').attrs['aria-pressed'],'true')});
ok('learner view hides trainer block',()=>{$('learner').click();assert(!$('lesson').textContent.includes('Trainer expected result'))});
ok('checklist saves and updates count',()=>{const label=$('lesson').children.find(n=>n.className==='check');const box=label.children[0];box.checked=true;box.events.change();assert.match($('count').textContent,/1 of 36/);assert.equal(JSON.parse(t.storage.wooplix_v2_checklist)['CAW-M04'],true)});
ok('checklist survives simulated reload',()=>{const r=setup(t.storage);assert.match(r.document.elements.count.textContent,/1 of 36/)});
ok('lesson download contains selected Markdown',()=>{$('download').click();assert.equal(t.document.downloads.at(-1).name,'CAW-M04_lesson.md');assert(t.blobs.at(-1).parts[0].startsWith('# CAW-M04'))});
ok('evidence worksheet includes selected module',()=>{$('worksheet').click();assert(t.blobs.at(-1).parts[0].includes('CAW-M04,'))});
ok('reset clears personal checklist',()=>{$('reset').click();assert.match($('count').textContent,/0 of 36/)});
ok('unavailable storage does not prevent startup',()=>{const r=setup({},true);assert.match(r.document.elements.lesson.textContent,/ZIM-M01/)});
ok('corrupted null storage does not prevent startup',()=>{const r=setup({wooplix_v2_checklist:'null'});assert.match(r.document.elements.count.textContent,/0 of 36/)});
ok('invalid JSON storage does not prevent startup',()=>{const r=setup({wooplix_v2_checklist:'bad json'});assert.match(r.document.elements.count.textContent,/0 of 36/)});
console.log(checks+' source-level logic checks passed. Browser layout and real downloads are not verified by this DOM mock.');
