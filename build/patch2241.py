import sys
# 2.24.1: PDF column widths follow what is actually in the columns. Before, when the page was too narrow, Type was cut to
# 30 mm first (types and insert references cut off or shrunk) while your own columns kept 18 mm even when nearly empty
# and Code + Location was squeezed to 16 mm.
OLD='''const COLW=(()=>{const ws=SPEC.map(s=>s[1]);if(!BLANK)Object.entries(GJ).forEach(([k,L])=>{if(KI[k]!=null)ws[KI[k]]+=Math.min(24,L.reduce((a,j)=>a+(SPW[j]||12)*0.45,0))});let d=W-ws.reduce((a,b)=>a+b,0);
    if(d>0){'''
NEW='''const COLW=(()=>{const ws=SPEC.map(s=>s[1]);if(!BLANK)Object.entries(GJ).forEach(([k,L])=>{if(KI[k]!=null)ws[KI[k]]+=Math.min(24,L.reduce((a,j)=>a+(SPW[j]||12)*0.45,0))});
    // the width each text column really needs (its longest line), so nothing is cut while an almost empty column takes room
    const MINW={type:30,holder:24,insert:19,code:16,loc:16},mnW=k=>k.startsWith("x_")?10:(MINW[k]||0);
    if(!BLANK&&W-ws.reduce((a,b)=>a+b,0)<0){const LO=v=>String(v??"").replace(/\\r/g,"").split("\\n").map(s=>s.trim()).filter(Boolean),prev=SK,TL=tools,widest=(k,f,s,vals,cs)=>{useK(k);font(f,s);let m=0;vals.forEach(v=>{if(v)m=Math.max(m,tw(v,cs||0))});return m};
      const HEADK={diameter:lab("diameter","Ø"),ra:lab("ra","R / °"),ls:lab("ls",L.head[3]),oal:lab("oal",L.head[4]),z:lab("z",L.head[5])};
      const headWord=h=>{font("Plex5",6.6);return Math.max(0,...String(h||"").split(/\\s+/).map(w=>tw(w)))};
      KEYS.forEach((k,i)=>{let n=null;
        if(k==="type"){n=0;TL.forEach(t=>{const tl=LO(t.type),dl=inT("diameter")?LO(t.diameter):[],rl=inT("ra")?LO(t.ra):[];
            for(let li=0;li<Math.max(tl.length,dl.length,rl.length,1);li++){const ty=(tl[li]||"").toUpperCase(),d=normDia(dl[li]||""),ra=normRA(rl[li]||""),dims=[d?"Ø"+d:"",ra.kind==="R"?"R"+ra.val:ra.kind==="A"?ra.val+"°":""].filter(Boolean).join("  ");
              useK("type");font("BarlowB",8.4);let w=tw(ty,0.18);if(dims){font("Mono5",9.6);w+=tw(dims)+2.4}n=Math.max(n,w)}
            if(inT("insert"))LO(t.insert).forEach(v=>{useK("type");font("Plex5",6.2);const lw=tw((L.ins||"Insert")+" ");font("Mono5",8);n=Math.max(n,lw+tw(v.toUpperCase()))});
            if(OPT.tnotes&&clean(t.notes)){font("Plex5",7);n=Math.max(n,Math.min(tw(clean(t.notes)),60))}});
          n=Math.min(80,Math.max(MINW.type,n+4))}
        else if(k==="holder"){n=Math.min(48,Math.max(MINW.holder,widest(k,"Plex5",8.4,TL.flatMap(t=>LO(t.holder)))+3.8,headWord(lab("holder",L.head[6]))+3))}
        else if(k==="insert"){n=Math.min(40,Math.max(MINW.insert,widest(k,"Mono5",8.6,TL.flatMap(t=>LO(t.insert).map(v=>v.toUpperCase())))+3.6))}
        else if(k.startsWith("x_")||k==="loc"){const x=EXTRA.find(e=>"x_"+e.id===k),hd=k==="loc"?lab("loc",LANG==="fr"?"Emplacement":"Location"):(x?x.label:"");
          n=Math.min(k==="loc"?42:40,Math.max(mnW(k),widest(k,"Plex5",8.4,TL.flatMap(t=>LO(t[k])))+3.6,headWord(hd)+3.2))}
        else if(k==="code"&&GJ.code&&GJ.code.length){n=widest(k,"MonoB",9.5,TL.flatMap(t=>LO(t.code).map(v=>v.toUpperCase())),-0.1);
          GJ.code.forEach(j=>{const lb=j==="loc"&&!clean(LAB.loc)?(LANG==="fr"?"Empl. ":"Loc. "):"";font("Plex5",6.2);const lw=lb?tw(lb):0;
            n=Math.max(n,lw+widest(j,/^(holder|type|loc)$/.test(j)||j.startsWith("x_")?"Plex5":"Mono5",7.6,TL.flatMap(t=>LO(t[j]))))});
          font("Plex5",6.6);n=Math.min(44,Math.max(20,n+3.8,tw(lab("code",L.head[7]))+3))}
        else if(/^(diameter|ra|ls|oal|z)$/.test(k)){const fm=k==="diameter"?v=>{const d=normDia(v);return d?"Ø"+d:v}:k==="ra"?v=>{const r=normRA(v);return r.kind==="R"?"R"+r.val:r.kind==="A"?r.val+"°":v}:v=>v;
          const big=k==="ls"||k==="oal";n=Math.min(ws[i],Math.max(k==="z"?7:9,widest(k,big?"MonoB":"Mono5",big?10.5:9.6,TL.flatMap(t=>LO(t[k]).map(fm)))+3.6,headWord(HEADK[k]||"")+3))}
        if(n!=null)ws[i]=n});
      SK=prev;
      // room left: Type first gets back the width it usually has, the rest is shared as before
      if(KI.type!=null){const dd=W-ws.reduce((a,b)=>a+b,0),i=KI.type;if(dd>0&&ws[i]<48)ws[i]+=Math.min(dd,48-ws[i])}}
    let d=W-ws.reduce((a,b)=>a+b,0);
    if(d>0){'''
OLD2='''else if(d<0){let over=-d;for(const [k,min] of (BLANK?'''
NEW2='''else if(d<0&&!BLANK){let over=-d;
      // too wide: every text column gives up room in proportion to what it has above its minimum
      const FL=KEYS.map((k,i)=>[k,i]).filter(([k])=>/^(type|holder|insert|code|loc)$/.test(k)||k.startsWith("x_")),room=FL.reduce((a,[k,i])=>a+Math.max(0,ws[i]-mnW(k)),0);
      if(room>0){const f=Math.min(1,over/room);FL.forEach(([k,i])=>{ws[i]-=Math.max(0,ws[i]-mnW(k))*f});over=Math.max(0,over-room)}
      if(over>0){const ex=KEYS.map((k,i)=>i).filter(i=>KEYS[i].startsWith("x_"));const per=over/Math.max(1,ex.length);ex.forEach(i=>ws[i]=Math.max(9,ws[i]-per))}}
    else if(d<0){let over=-d;for(const [k,min] of (BLANK?'''
OLD3='''    return ws})();
  const typeHead='''
NEW3='''    {const S=ws.reduce((a,b)=>a+b,0);if(S>W+0.01)ws.forEach((w,i)=>ws[i]=w*W/S)}
    return ws})();
  const typeHead='''
R=[(OLD,NEW),(OLD2,NEW2),(OLD3,NEW3)]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:80]);s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
