import base64
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page();pg.add_init_script("window.__QA_ROLE='admin'");errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
  pg.goto("file:///home/claude/qa/ToolManager.html");pg.wait_for_timeout(1500)
  r=pg.evaluate("""()=>{const out={};const T=[];for(let i=1;i<=45;i++)T.push({t:'T'+i,type:'FRAISE',diameter:String(i),holder:'MANDRIN À PINCE ER32 SÉRIE LONGUE LG 120 AVEC ARROSAGE\\nBT50AD-ER32-120',code:i%3?'F'+(800+i):'F'+(800+i)+'\\nF'+(900+i)});
    const art={article:{number:'1052',index:'A'},tools:T};
    const c=()=>JSON.parse(JSON.stringify(normCfg({})));
    try{out.long=makePDF({...art,cols:c()}).getNumberOfPages()}catch(e){out.long='ERR '+e.message}
    try{out.blank=makePDF({...art,blank:true,cols:c()}).getNumberOfPages()}catch(e){out.blank='ERR '+e.message}
    try{const k=c();k.joinTo={...(k.joinTo||{}),oal:'code'};out.joined=makePDF({...art,cols:k}).getNumberOfPages()}catch(e){out.joined='ERR '+e.message}
    try{const k=c();k.hidden=[...(k.hidden||[]),'holder'];out.noholder=makePDF({...art,cols:k}).getNumberOfPages()}catch(e){out.noholder='ERR '+e.message}
    try{const k=c();k.style={code:{k:1.3,b:true},holder:{u:true,k:0.9}};const d=makePDF({...art,cols:k});out.styled=d.getNumberOfPages();out.meta=!!d.bsMeta}catch(e){out.styled='ERR '+e.message}
    return out}""")
  print(r)
  # Excel from the same layout
  x=pg.evaluate("""async()=>{try{db.machines.push({id:'m1',abbr:'S3',name:'DMU',createdAt:1});const a={id:'a1',machineId:'m1',article:{number:'1052',index:'A'},tools:[{t:'T1',type:'FRAISE',holder:'MANDRIN À TENON Ø32 AVEC ARROSAGE CENTRAL\\nBT50ADB',code:'F863'}],createdAt:1,updatedAt:1};db.articles.push(a);
     const bl=await sheetXLSX(a);return bl&&bl.size}catch(e){return 'ERR '+e.message}}""")
  print("xlsx",x,"errors",errs)
  b.close()
