const COLW=(()=>{const ws=SPEC.map(s=>s[1]);if(!BLANK)Object.entries(GJ).forEach(([k,L])=>{if(KI[k]!=null)ws[KI[k]]+=Math.min(24,L.reduce((a,j)=>a+(SPW[j]||12)*0.45,0))});
    // what each column holds: NE = width at the normal text size, FLR = width at the smallest size still readable on A4.
    // A column is never made narrower than FLR, so nothing gets cut; the text gets smaller instead.
    const MINW={type:30,holder:24,insert:19,code:16,loc:16},mnW=k=>k.startsWith("x_")?10:(MINW[k]||0);
    const NE=[],FLR=[];
    if(!BLANK){const LO=v=>String(v??"").replace(/\r/g,"").split("\n").map(s=>s.trim()).filter(Boolean),prev=SK,TL=tools,widest=(k,f,s,vals,cs)=>{useK(k);font(f,s);let m=0;vals.forEach(v=>{if(v)m=Math.max(m,tw(v,cs||0))});return m};
      const HEADK={diameter:lab("diameter","Ø"),ra:lab("ra","R / °"),ls:lab("ls",L.head[3]),oal:lab("oal",L.head[4]),z:lab("z",L.head[5])};
      const headWord=h=>{font("Plex5",6.2);return Math.max(0,...String(h||"").split(/\s+/).map(w=>tw(w)))};
      KEYS.forEach((k,i)=>{let n=null,fl=null;
        if(k==="type"){let c=0,cmin=0;TL.forEach(t=>{const tl=LO(t.type),dl=inT("diameter")?LO(t.diameter):[],rl=inT("ra")?LO(t.ra):[];
            for(let li=0;li<Math.max(tl.length,dl.length,rl.length,1);li++){const ty=(tl[li]||"").toUpperCase(),d=normDia(dl[li]||""),ra=normRA(rl[li]||""),dims=[d?"Ø"+d:"",ra.kind==="R"?"R"+ra.val:ra.kind==="A"?ra.val+"°":""].filter(Boolean).join("  ");
              useK("type");font("BarlowB",8.4);const w=tw(ty,0.18);font("BarlowB",5.4);const wl=Math.max(0,...ty.split(/\s+/).map(x=>tw(x,0.18)));let dw=0;if(dims){font("Mono5",9.6);dw=tw(dims)+2.4}
              c=Math.max(c,w+dw);cmin=Math.max(cmin,wl+dw)}
            if(inT("insert"))LO(t.insert).forEach(v=>{useK("type");font("Plex5",6.6);const lw=tw((L.insS||L.ins||"Insert")+" ");font("Mono5",7.6);const w=tw(v.toUpperCase());c=Math.max(c,lw+w);cmin=Math.max(cmin,w*5/7.6)});
            if(OPT.tnotes&&clean(t.notes)){font("Plex5",7);c=Math.max(c,Math.min(tw(clean(t.notes)),60))}});
          n=Math.min(80,Math.max(MINW.type,c+4));fl=Math.max(20,cmin+4)}
        else if(k==="holder"){const parts=TL.flatMap(t=>LO(t.holder).flatMap(v=>{const p=v.split(/\s*\+\s*/).filter(Boolean);return p.length>1?[p[0],"+ "+p.slice(1).join(" + ")]:[v]}));
          const c=widest(k,"Plex5",8.4,parts),cmin=widest(k,"Plex5",4.6,parts.map(v=>/\s/.test(v)&&v.length>24?v.slice(0,Math.ceil(v.length/2)):v));
          n=Math.min(48,Math.max(MINW.holder,c+3.8,headWord(lab("holder",L.head[6]))+3));fl=Math.max(14,cmin+3.4)}
        else if(k==="insert"){const V=TL.flatMap(t=>LO(t.insert).map(v=>v.toUpperCase())),c=widest(k,"Mono5",8.6,V);n=Math.min(40,Math.max(MINW.insert,c+3.6));fl=Math.max(10,widest(k,"Mono5",5,V)+3.2)}
        else if(k.startsWith("x_")||k==="loc"){const x=EXTRA.find(e=>"x_"+e.id===k),hd=k==="loc"?lab("loc",LANG==="fr"?"Emplacement":"Location"):(x?x.label:""),V=TL.flatMap(t=>LO(t[k]));
          n=Math.min(k==="loc"?42:40,Math.max(mnW(k),widest(k,"Plex5",8.4,V)+3.6,headWord(hd)+3.2));fl=Math.max(8,widest(k,"Plex5",4.8,V)+3.2,headWord(hd)*0.85+2.4)}
        else if(k==="code"){let c=widest(k,"MonoB",9.5,TL.flatMap(t=>LO(t.code).map(v=>v.toUpperCase())),-0.1),cmin=c*5/9.5;
          (GJ.code||[]).forEach(j=>{const lb=j==="loc"&&!clean(LAB.loc)?(LANG==="fr"?"Empl. ":"Loc. "):"";font("Plex5",6.2);const lw=lb?tw(lb):0,f=/^(holder|type|loc)$/.test(j)||j.startsWith("x_")?"Plex5":"Mono5",V=TL.flatMap(t=>LO(t[j]));
            c=Math.max(c,lw+widest(j,f,7.6,V));cmin=Math.max(cmin,widest(j,f,4.8,V))});
          if(GJ.code&&GJ.code.length){font("Plex5",6.6);n=Math.min(44,Math.max(20,c+3.8,tw(lab("code",L.head[7]))+3))}fl=Math.max(11,cmin+3.4)}
        else if(/^(diameter|ra|ls|oal|z)$/.test(k)){const fm=k==="diameter"?v=>{const d=normDia(v);return d?"Ø"+d:v}:k==="ra"?v=>{const r=normRA(v);return r.kind==="R"?"R"+r.val:r.kind==="A"?r.val+"°":v}:v=>v;
          const big=k==="ls"||k==="oal",V=TL.flatMap(t=>LO(t[k]).map(fm)),c=widest(k,big?"MonoB":"Mono5",big?10.5:9.6,V);
          n=Math.min(ws[i],Math.max(k==="z"?7:9,c+3.6,headWord(HEADK[k]||"")+3));fl=Math.max(6,widest(k,big?"MonoB":"Mono5",5,V)+3)}
        NE[i]=n;FLR[i]=fl});
      SK=prev;
      // the usual widths don't fit, or a column would be too narrow for what it holds: size the columns to their content
      if(W-ws.reduce((a,b)=>a+b,0)<0||KEYS.some((k,i)=>FLR[i]!=null&&ws[i]<FLR[i]-0.05)){NE.forEach((n,i)=>{if(n!=null)ws[i]=Math.max(n,FLR[i]||0)});
        // room left: Type first gets back the width it usually has, the rest is shared as before
        if(KI.type!=null){const dd=W-ws.reduce((a,b)=>a+b,0),i=KI.type;if(dd>0&&ws[i]<48)ws[i]+=Math.min(dd,48-ws[i])}}}
    let d=W-ws.reduce((a,b)=>a+b,0);
    if(d>0){const grow=["type","holder","insert"].filter(k=>KI[k]!=null);if(!grow.length)grow.push(...KEYS.filter(k=>k!=="t"&&k!=="corr"));if(!grow.length)grow.push("t");grow.forEach((k,j)=>ws[KI[k]]+=d*(grow.length===1?1:j===0?0.6:0.4/(grow.length-1)))}
    else if(d<0&&!BLANK){let over=-d;
      // too wide: every column gives up room in proportion to what it has above the width its content needs at the smallest size
      const FIX={t:9,corr:10,asm:13,chk:8},fl=(k,i)=>FLR[i]!=null?FLR[i]:(FIX[k]||mnW(k)||8);
      const FL=KEYS.map((k,i)=>[k,i]),room=FL.reduce((a,[k,i])=>a+Math.max(0,ws[i]-fl(k,i)),0);
      if(room>0){const f=Math.min(1,over/room);FL.forEach(([k,i])=>{ws[i]-=Math.max(0,ws[i]-fl(k,i))*f})}}
    else if(d<0){let over=-d;for(const [k,min] of [["type",22],["holder",22],["insert",14],["code",15]]){if(over<=0||KI[k]==null)continue;const i=KI[k],cut=Math.min(over,ws[i]-min);if(cut>0){ws[i]-=cut;over-=cut}}
      if(over>0){const ex=KEYS.map((k,i)=>i).filter(i=>KEYS[i].startsWith("x_"));const per=over/Math.max(1,ex.length);ex.forEach(i=>ws[i]=Math.max(9,ws[i]-per))}}
    if(!BLANK&&KI.code!=null&&!(GJ.code&&GJ.code.length)){const i=KI.code,prev=SK;let need=0;
      useK("code");font("MonoB",9.5);tools.forEach(t=>String(t.code||"").split("\n").forEach(v=>{v=v.trim().toUpperCase();if(v)need=Math.max(need,tw(v,-0.1))}));
      font("Mono5",10);need=Math.max(need,tw("___"));SK=null;font("Plex5",7.8);need=Math.max(need,tw(lab("code",L.head[7])));SK=prev;
      need=Math.ceil((need+3.8)*2)/2;
      const to=[KI.holder,KI.type].find(j=>j!=null&&j!==i);
      if(to!=null&&ws[i]>need){ws[to]+=ws[i]-need;ws[i]=need}}
    {const S=ws.reduce((a,b)=>a+b,0);if(S>W+0.01)ws.forEach((w,i)=>ws[i]=w*W/S)}
    return ws})();
