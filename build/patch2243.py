import sys,os
NEWCOLW=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'colw2243.js')).read().rstrip('\n')
# 2.24.3: nothing is cut on the PDF. A holder reference written as one piece stays on one line (smaller text if
# needed); type, Ø, R, LS, codes, locations and your own columns get smaller before anything is cut.
R=[
('COLW',None),
('''@media (max-width:520px){.top .gfbtn{display:none}}''','''@media (max-width:520px){.top .gfbtn{display:none}}\n.tt .colrs{right:0;width:8px}.tt .colrs::after{left:6px}'''),
('''function ttWatch(){const tw=document.querySelector(".ed .tw");if(!tw)return;''','''function ttWatch(){const tw=document.querySelector(".ed .tw");if(!tw)return;const tb0=tw.querySelector("table.tt");if(tb0)wireColResize(tb0);'''),
('''[c=>c.min,c=>c.min==null?SMALL[c.k]:null].forEach(minOf=>{if(need<=avail)return;let over=need-avail;
    const fl=C.filter(c=>c.w&&minOf(c)!=null&&c.w>minOf(c))''','''// the column you just dragged keeps its width; it only gives up room if the others can't make enough
  [[c=>c.min,0],[c=>c.min==null?SMALL[c.k]:null,0],[c=>c.min,1],[c=>c.min==null?SMALL[c.k]:null,1]].forEach(([minOf,all])=>{if(need<=avail)return;let over=need-avail;
    const fl=C.filter(c=>c.w&&minOf(c)!=null&&c.w>minOf(c)&&(all||c.k!==ttFit.pin))'''),
('''lsSet(CWKEY,JSON.stringify(m));ttFit()};''','''lsSet(CWKEY,JSON.stringify(m));ttFit.pin=k;ttFit()};'''),
('''delete m[k];lsSet(CWKEY,JSON.stringify(m));''','''delete m[k];lsSet(CWKEY,JSON.stringify(m));ttFit.pin=null;'''),
('''const fitLine=(txt0,base0)=>{let f=parts.length>1?7.6:8.6;font("Plex5",f);while(f>5.6&&tw(txt0)>HW){f-=0.3;font("Plex5",f)}txt(fit(txt0,HW),hx+1.8,base0)};
       if(parts.length===1){''','''const fitLine=(txt0,base0)=>{let f=parts.length>1?7.6:8.6;font("Plex5",f);while(f>4.6&&tw(txt0)>HW){f-=0.2;font("Plex5",f)}txt(fit(txt0,HW),hx+1.8,base0)};
       if(parts.length===1&&(!/\\s/.test(hol)||(()=>{font("Plex5",6.2);return tw(SK&&SK.u?hol.toUpperCase():hol)<=HW})()))fitLine(hol,base(8.6));
       else if(parts.length===1){'''),
('''if(/\\s*\\+\\s*/.test(hol))return 2;const prev=SK;useK("holder");font("Plex5",8.6);const two=tw(hol)>(COLW[KI.holder]-3.2)*1.25;SK=prev;return two?2:1};''',
 '''if(/\\s*\\+\\s*/.test(hol))return 2;if(!/\\s/.test(hol))return 1;const prev=SK;useK("holder");font("Plex5",6.2);const two=tw(hol)>(COLW[KI.holder]-3.2);SK=prev;return two?2:1};'''),
('''hl.forEach(v=>{let f=f0;font("Plex5",f);while(f>MIN&&tw(v)>HW){f-=0.3;font("Plex5",f)}''','''hl.forEach(v=>{let f=f0;const mn=/\\s/.test(v)?MIN:4.6;font("Plex5",f);while(f>mn&&tw(v)>HW){f-=0.2;font("Plex5",f)}'''),
('''let fs=anyWrap?8.4:n>2?9.4:10.2;font("BarlowB",fs);while(fs>7.2&&tw(ty,0.18)>room){fs-=0.3;font("BarlowB",fs)}''','''let fs=anyWrap?8.4:n>2?9.4:10.2;font("BarlowB",fs);while(fs>5.4&&tw(ty,0.18)>room){fs-=0.2;font("BarlowB",fs)}'''),
('''function stack(vals,x,w,f,size,min,align,cs){const n=vals.length;''','''function stack(vals,x,w,f,size,min,align,cs){min=Math.min(min,4.8);const n=vals.length;'''),
('''while(f>5.6&&tw(v)>w0-lw){f-=0.3;''','''while(f>4.8&&tw(v)>w0-lw){f-=0.2;'''),
]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    if a=='COLW':
      i=s.find('const COLW=(()=>{');j=s.find('return ws})();',i)+len('return ws})();');assert i>0 and j>i;s=s[:i]+NEWCOLW+s[j:];continue
    assert s.count(a)==1,(f,s.count(a),a[:90]);s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
