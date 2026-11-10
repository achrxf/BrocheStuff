import sys
R=[
# 1) measure text the way it is printed (capitals style)
('''  const tw=(s,cs=0)=>doc.getTextWidth(s)+cs*Math.max(0,s.length-1);''',
 '''  const tw=(s,cs=0)=>{s=String(s);if(SK&&SK.u)s=s.toUpperCase();return doc.getTextWidth(s)+cs*Math.max(0,s.length-1)};'''),
# 2) the Code column takes only the room its codes need; the rest goes to the holder (or the type)
('''      if(over>0){const ex=KEYS.map((k,i)=>i).filter(i=>KEYS[i].startsWith("x_"));const per=over/Math.max(1,ex.length);ex.forEach(i=>ws[i]=Math.max(9,ws[i]-per))}}
    return ws})();''','''      if(over>0){const ex=KEYS.map((k,i)=>i).filter(i=>KEYS[i].startsWith("x_"));const per=over/Math.max(1,ex.length);ex.forEach(i=>ws[i]=Math.max(9,ws[i]-per))}}
    if(!BLANK&&KI.code!=null&&!(GJ.code&&GJ.code.length)){const i=KI.code,prev=SK;let need=0;
      useK("code");font("MonoB",9.5);tools.forEach(t=>String(t.code||"").split("\\n").forEach(v=>{v=v.trim().toUpperCase();if(v)need=Math.max(need,tw(v,-0.1))}));
      font("Mono5",10);need=Math.max(need,tw("___"));SK=null;font("Plex5",7.8);need=Math.max(need,tw(lab("code",L.head[7])));SK=prev;
      need=Math.ceil((need+3.8)*2)/2;
      const to=[KI.holder,KI.type].find(j=>j!=null&&j!==i);
      if(to!=null&&ws[i]>need){ws[to]+=ws[i]-need;ws[i]=need}}
    return ws})();'''),
# 3) holder: a typed line too long for its box goes on two lines instead of shrinking to tiny letters
('''  const holderLines=t=>{if(KI.holder==null)return 1;const hol=clean(t.holder);if(!hol)return 1;const hl=linesOf(t.holder);if(hl.length>1)return hl.length;
    if(/\\s*\\+\\s*/.test(hol))return 2;font("Plex5",8.6);return tw(hol)>(COLW[KI.holder]-3.2)*1.25?2:1};''',
 '''  const holderShow=t=>{const hl=linesOf(t.holder),prev=SK;useK("holder");const HW=COLW[KI.holder]-3.2,f0=hl.length>2?7.2:7.6,MIN=6.4,out=[];
    hl.forEach(v=>{let f=f0;font("Plex5",f);while(f>MIN&&tw(v)>HW){f-=0.3;font("Plex5",f)}
      if(tw(v)<=HW){out.push([v,f]);return}
      // two even lines (no lonely last word), at the normal size if they fit, else a bit smaller
      const w=v.split(/\\s+/);for(let g=f0;g>=MIN-0.01;g-=0.3){font("Plex5",g);let best=null;
        for(let i=1;i<w.length;i++){const a=w.slice(0,i).join(" "),b=w.slice(i).join(" "),m=Math.max(tw(a),tw(b));if(m<=HW&&(!best||m<best[2]))best=[a,b,m]}
        if(best){out.push([best[0],g],[best[1],g]);return}}
      font("Plex5",MIN);const P=doc.splitTextToSize(SK&&SK.u?v.toUpperCase():v,HW);P.forEach(p=>out.push([p,MIN]))});
    SK=prev;return out.length>5?[...out.slice(0,4),[out.slice(4).map(x=>x[0]).join(" "),6.4]]:out};
  const holderLines=t=>{if(KI.holder==null)return 1;const hol=clean(t.holder);if(!hol)return 1;const hl=linesOf(t.holder);if(hl.length>1)return holderShow(t).length;
    if(/\\s*\\+\\s*/.test(hol))return 2;const prev=SK;useK("holder");font("Plex5",8.6);const two=tw(hol)>(COLW[KI.holder]-3.2)*1.25;SK=prev;return two?2:1};'''),
('''     if(hl.length>1){const n=hl.length;hl.forEach((v,li)=>{let f=n>2?7.2:7.6;font("Plex5",f);while(f>5.4&&tw(v)>HW){f-=0.3;font("Plex5",f)}txt(fit(v,HW),hx+1.8,yAt(mid,li,n))})}''',
 '''     if(hl.length>1){const S2=holderShow(t),n=S2.length;S2.forEach(([v,f],li)=>{font("Plex5",f);txt(fit(v,HW),hx+1.8,yAt(mid,li,n))})}'''),
('''       if(parts.length===1){const l=doc.splitTextToSize(hol,HW);''','''       if(parts.length===1){font("Plex5",7.6);const l=doc.splitTextToSize(SK&&SK.u?hol.toUpperCase():hol,HW);'''),
]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:90])
    s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
