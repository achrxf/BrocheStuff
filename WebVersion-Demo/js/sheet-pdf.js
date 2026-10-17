/* Draws the A4 tool list sheet as a PDF (jsPDF). Labels in English and French. */
/* ---------- PDF drawing (A4, mm) ---------- */
const C={ink:[16,23,30],red:[158,15,18],mid:[105,116,127],soft:[154,165,175],hair:[211,217,222],fill:[243,245,247],white:[255,255,255]};
const PT=0.3528;
const SHEETL={
  en:{spine:"TOOL LIST",title:"Tool List",sub:"FICHE OUTILS",article:"ARTICLE",des:"DESIGNATION",prog:"PROGRAM",mach:"MACHINE",mat:"MATERIAL",index:"INDEX",
      head:["TOOL","TYPE","Ø","R /","LS","Z","HOLDER","CODE"],allmm:"All dimensions in",ls:"length out of the holder (stick-out)",ra:"corner radius or point angle",z:"flutes / inserts",
      notes:"NOTES",prep:"PREPARED BY",appr:"APPROVED BY",date:"DATE",doc:"Tool list"},
  fr:{spine:"FICHE OUTILS",title:"Fiche Outils",sub:"TOOL LIST",article:"ARTICLE",des:"DÉSIGNATION",prog:"PROGRAMME",mach:"MACHINE",mat:"MATIÈRE",index:"INDICE",
      head:["OUTIL","TYPE","Ø","R /","LS","Z","PORTE-OUTIL","CODE"],allmm:"Toutes les cotes en",ls:"longueur de sortie (hors porte-outil)",ra:"rayon de bec ou angle de pointe",z:"nombre de dents / plaquettes",
      notes:"REMARQUES",prep:"ÉTABLI PAR",appr:"APPROUVÉ PAR",date:"DATE",doc:"Fiche outils"}};
function makePDF(data){
  const L=SHEETL[(typeof LANG!=="undefined"&&LANG)||"en"]||SHEETL.en;
  const {jsPDF}=window.jspdf;
  const doc=new jsPDF({unit:"mm",format:"a4",compress:true});
  for(const [name,b64] of Object.entries(FONTS)){doc.addFileToVFS(name+".ttf",b64);doc.addFont(name+".ttf",name,"normal")}
  const a=data.article||{}, tools=realTools(data.tools);
  const fill=c=>doc.setFillColor(...c), stroke=c=>doc.setDrawColor(...c), color=c=>doc.setTextColor(...c);
  const font=(f,s)=>{doc.setFont(f,"normal");doc.setFontSize(s)};
  const tw=(s,cs=0)=>doc.getTextWidth(s)+cs*Math.max(0,s.length-1);
  const txt=(s,x,y,o={})=>{const cs=o.cs||0;let X=x;if(o.align==="center")X=x-tw(s,cs)/2;else if(o.align==="right")X=x-tw(s,cs);doc.text(s,X,y,cs?{charSpace:cs}:{});return tw(s,cs)};
  const fit=(s,max,cs=0)=>{if(tw(s,cs)<=max)return s;while(s.length>1&&tw(s+"…",cs)>max)s=s.slice(0,-1);return s+"…"};
  const line=(x1,y1,x2,y2,c,w)=>{stroke(c);doc.setLineWidth(w);doc.line(x1,y1,x2,y2)};
  const angleSym=(x,y,h,c,w=0.25)=>{stroke(c);doc.setLineWidth(w);doc.line(x,y,x+h*0.95,y);doc.line(x,y,x+h*0.8,y-h*0.85);return h*0.95+0.4};
  const X0=17, W=183, X1=X0+W;

  function spine(){
    fill(C.ink);doc.rect(0,0,11,297,"F");
    fill(C.red);doc.rect(0,0,11,36,"F");
    const lab=L.spine, num=a.number||"";
    font("BarlowSB",7.5);const l1=tw(lab,0.95);font("MonoB",11);const l2=num?tw(num,0.08):0;
    const total=l1+(num?4+l2:0);let y=166+total/2;
    color(C.white);font("BarlowSB",7.5);doc.text(lab,6.3,y,{angle:90,charSpace:0.95});
    if(num){font("MonoB",11);doc.text(num,6.9,y-l1-4,{angle:90,charSpace:0.08})}
    stroke(C.soft);doc.setLineWidth(0.35);doc.circle(5.5,285,2,"S");
  }

  function header(){
    // logo
    if(logo){try{const p=doc.getImageProperties(logo.data);const r=Math.min(26/p.width,16/p.height);const w=p.width*r,h=p.height*r;
      doc.addImage(logo.data,logo.type,X0+(26-w)/2,14.5+(16-h)/2,w,h,undefined,"FAST")}catch(e){}}
    else{stroke(C.soft);doc.setLineWidth(0.25);doc.setLineDashPattern([0.9,0.7],0);doc.rect(X0,14.5,26,16);doc.setLineDashPattern([],0);
      color(C.soft);font("BarlowSB",7.5);txt("LOGO",X0+13,23.4,{align:"center",cs:0.6})}
    // title
    color(C.ink);font("BarlowB",30);const w=txt(L.title,47,25.3);color(C.red);txt(".",47+w+0.2,25.3);
    // dimension-style rule
    const dx1=47,dx2=132;font("BarlowSB",7.6);color(C.mid);const lab=L.sub,lw=tw(lab,0.65),cx=(dx1+dx2)/2;
    txt(lab,cx,30.3,{align:"center",cs:0.65});
    stroke(C.soft);doc.setLineWidth(0.25);const yl=29.4;
    doc.line(dx1,yl,cx-lw/2-1.8,yl);doc.line(cx+lw/2+1.8,yl,dx2,yl);
    [dx1,cx-lw/2-1.8,cx+lw/2+1.8,dx2].forEach(x=>doc.line(x,yl-1.2,x,yl+1.2));
    // article plate
    fill(C.ink);doc.roundedRect(136,10,64,25,3,3,"F");doc.rect(136,10,64,12,"F");doc.rect(139.5,10,60.5,25,"F");
    fill(C.red);doc.rect(136,10,64,2.6,"F");
    color(C.white);font("BarlowSB",7.4);txt(L.article,141,24.6,{cs:0.68});
    let size=22;font("MonoB",size);const num=a.number||"—";while(size>11&&tw(num,-0.1)>54){size-=1;font("MonoB",size)}
    txt(num,141,32.4,{cs:-0.1});
  }

  function infoRow(y){
    const ws=[57.4,33.75,33.75,37.1,21], h=15.6;
    line(X0,y+0.3,X1,y+0.3,C.ink,0.6);
    let x=X0;
    const cells=[[L.des,"designation","Plex5"],[L.prog,"program","Mono5"],[L.mach,"machine","Plex5"],[L.mat,"material","Plex5"]];
    cells.forEach(([lab,k,f],i)=>{const pad=i?3:0;font("BarlowSB",6.8);color(C.mid);txt(lab,x+pad,y+5.2,{cs:0.38});
      const v=clean(a[k]);if(v){font(f,10);color(C.ink);txt(fit(v,ws[i]-pad-2.5),x+pad,y+11.4)}
      else{stroke(C.soft);doc.setLineWidth(0.2);doc.setLineDashPattern([0.3,0.6],0);doc.line(x+pad,y+12,x+ws[i]-6,y+12);doc.setLineDashPattern([],0)}
      x+=ws[i];line(x,y+0.6,x,y+h,C.hair,0.25)});
    // index
    fill(C.fill);doc.rect(x,y+0.6,ws[4],h-0.6,"F");
    const cx=x+ws[4]/2;font("BarlowSB",6.8);color(C.mid);txt(L.index,cx,y+5.2,{align:"center",cs:0.38});
    stroke(C.ink);doc.setLineWidth(0.4);doc.setLineJoin("round");doc.triangle(cx,y+6.6,cx-5.4,y+14.2,cx+5.4,y+14.2,"S");
    const iv=clean(a.index);if(iv){let s=11;font("MonoB",s);while(s>6&&tw(iv)>6){s--;font("MonoB",s)}color(C.ink);txt(iv,cx,y+13.2,{align:"center"})}
    line(X0,y+h,X1,y+h,C.hair,0.25);
    return y+h;
  }

  const COLW=[17,51,19,16,16,10,30,24];
  const HEAD=L.head;
  function tableHead(y){
    fill(C.ink);doc.roundedRect(X0,y,W,7.6,2,2,"F");doc.rect(X0,y+3,W,4.6,"F");
    fill(C.red);doc.rect(X0,y+7.6,W,0.9,"F");
    color(C.white);font("BarlowSB",7.6);let x=X0;
    HEAD.forEach((h,i)=>{const px=x+(i?1.8:3);const w=txt(h,px,y+5,{cs:0.5});if(h==="R /")angleSym(px+w+0.9,y+4.95,2.2,C.white,0.3);x+=COLW[i]});
    return y+8.5;
  }
  function row(t,y,rh,i,last){
    if(i%2===1){fill(C.fill);doc.rect(X0,y,W,rh,"F")}
    const mid=y+rh/2, base=s=>mid+s*PT*0.36;
    let x=X0;const cx=[];COLW.forEach(w=>{cx.push(x);x+=w});
    color(C.ink);
    font("MonoB",12.5);txt(normT(t.t),cx[0]+2.2,base(12.5),{cs:-0.15});
    const ty=clean(t.type).toUpperCase();font("BarlowB",10.2);
    if(clean(t.notes)){txt(fit(ty,COLW[1]-3,0.18),cx[1]+1.8,mid-0.4,{cs:0.18});font("Plex4",7);color(C.mid);txt(fit(clean(t.notes),COLW[1]-3),cx[1]+1.8,mid+3.2);color(C.ink)}
    else txt(fit(ty,COLW[1]-3,0.18),cx[1]+1.8,base(10.2),{cs:0.18});
    const dash=(xx)=>{font("Mono5",10.5);txt("—",xx,base(10.5))};
    const d=normDia(t.diameter);font("Mono5",10.5);if(d)txt("Ø"+d,cx[2]+1.8,base(10.5));else dash(cx[2]+1.8);
    const ra=normRA(t.ra);font("Mono5",10.5);if(ra.kind==="R")txt("R"+ra.val,cx[3]+1.8,base(10.5));else if(ra.kind==="A")txt(ra.val+"°",cx[3]+1.8,base(10.5));else dash(cx[3]+1.8);
    const ls=clean(t.ls).replace(",",".");if(ls){font("MonoB",11);txt(ls,cx[4]+1.8,base(11))}
    else{stroke(C.soft);doc.setLineWidth(0.25);doc.setLineDashPattern([0.8,0.6],0);doc.roundedRect(cx[4]+1.4,mid-3.1,COLW[4]-3.4,6.2,1,1,"S");doc.setLineDashPattern([],0)}
    const z=clean(t.z);font("Mono5",10.5);txt(z||"—",cx[5]+COLW[5]/2,base(10.5),{align:"center"});
    const hol=clean(t.holder);font("Plex5",8.8);
    if(hol){const lines=doc.splitTextToSize(hol,COLW[6]-3.2).slice(0,2);if(lines.length===1)txt(lines[0],cx[6]+1.8,base(8.8));else{txt(lines[0],cx[6]+1.8,mid-0.6);txt(fit(lines[1],COLW[6]-3.2),cx[6]+1.8,mid+3)}}
    else dash(cx[6]+1.8);
    const code=clean(t.code).toUpperCase();if(code){let s=13;font("MonoB",s);while(s>8&&tw(code,-0.15)>COLW[7]-3){s--;font("MonoB",s)}txt(code,cx[7]+1.8,base(13),{cs:-0.15})}
    else{font("Mono5",10.5);txt("F ___",cx[7]+1.8,base(10.5))}
    if(last)line(X0,y+rh-0.3,X1,y+rh-0.3,C.ink,0.6);else line(X0,y+rh,X1,y+rh,C.hair,0.25);
  }
  function legend(y){
    let x=X0;const g=5;
    const part=(b,rest)=>{font("MonoB",6.9);color(C.ink);x+=txt(b,x,y)+1.2;font("Plex4",6.9);color(C.mid);x+=txt(rest,x,y)+g};
    font("Plex4",6.9);color(C.mid);x+=txt(L.allmm,x,y)+1.2;font("MonoB",6.9);color(C.ink);x+=txt("mm",x,y)+g;
    part("LS",L.ls);
    font("MonoB",6.9);color(C.ink);x+=txt("R /",x,y)+0.8;x+=angleSym(x,y,1.9,C.ink,0.25)+0.8;font("Plex4",6.9);color(C.mid);x+=txt(L.ra,x,y)+g;
    part("Z",L.z);
  }
  function bottom(){
    const y=263;
    // notes
    line(X0,y+0.3,100,y+0.3,C.ink,0.6);font("BarlowSB",6.8);color(C.mid);txt(L.notes,X0,y+5,{cs:0.38});
    const ly=[y+11.4,y+17.8,y+24.2];ly.forEach(l=>line(X0,l,100,l,C.hair,0.2));
    const n=clean(a.notes);if(n){font("Plex4",8.8);color(C.ink);doc.splitTextToSize(n,82).slice(0,3).forEach((s,i)=>txt(s,X0,ly[i]-1.4))}
    // sign-off
    const xs=104,ws=[34.3,34.3,27.4];line(xs,y+0.3,X1,y+0.3,C.ink,0.6);
    let x=xs;[[L.prep,"preparedBy"],[L.appr,"approvedBy"],[L.date,"date"]].forEach(([lab,k],i)=>{
      if(i===2){fill(C.fill);doc.rect(x,y+0.6,ws[i],23.6,"F")}
      const pad=i?3:0;font("BarlowSB",6.8);color(C.mid);txt(lab,x+pad,y+5,{cs:0.38});
      const v=clean(a[k]);if(v){font(i===2?"Mono5":"Plex5",9.8);color(C.ink);txt(fit(v,ws[i]-pad-2),x+pad,y+20.4)}
      if(i<2)line(x+pad,y+22.2,x+ws[i]-3,y+22.2,C.soft,0.25);
      x+=ws[i];if(i<2)line(x,y+0.6,x,y+24.2,C.hair,0.25)});
  }

  // layout + paging
  const n=tools.length, rh=n>16?9.6:11.6, LIMIT_LAST=257.5, LIMIT=286;
  let i=0,page=0;
  while(true){
    if(page>0)doc.addPage();
    spine();
    let y;
    if(page===0){header();y=infoRow(39)+4}else y=10;
    y=tableHead(y);
    const rem=n-i, capLast=Math.max(0,Math.floor((LIMIT_LAST-y)/rh)), capAll=Math.floor((LIMIT-y)/rh);
    const isLast=rem<=capLast;
    const take=isLast?rem:Math.max(1,Math.min(capAll,rem-1));
    for(let k=0;k<take;k++)row(tools[i+k],y+k*rh,rh,i+k,isLast&&k===take-1||(!isLast&&k===take-1));
    i+=take;y+=take*rh;
    if(isLast){legend(y+4.4);bottom();break}
    page++;
  }
  doc.setProperties({title:`${L.doc} ${a.number||""}`.trim(),creator:"Tool List Maker"});
  return doc;
}

