/* ===================== 2.28.0 · speed ===================== */
// the logo is decoded once and kept small (sharp enough for print), instead of on every page of every preview
let LOGOC=null;
function pdfLogo(){if(!logo||!logo.data)return null;if(LOGOC&&LOGOC.src===logo.data)return LOGOC.ready||{data:logo.data,type:logo.type,p:LOGOC.p};
  const c={src:logo.data,p:null,ready:null};LOGOC=c;
  try{const im=new Image();im.onload=()=>{if(LOGOC!==c)return;c.p={width:im.naturalWidth,height:im.naturalHeight};
      try{const k=Math.min(1,900/Math.max(im.naturalWidth,im.naturalHeight)),cv=document.createElement("canvas");cv.width=Math.max(1,Math.round(im.naturalWidth*k));cv.height=Math.max(1,Math.round(im.naturalHeight*k));
        const g=cv.getContext("2d");g.fillStyle="#fff";g.fillRect(0,0,cv.width,cv.height);g.drawImage(im,0,0,cv.width,cv.height);c.ready={data:cv.toDataURL("image/jpeg",0.93),type:"JPEG",p:{width:cv.width,height:cv.height}}}catch(_){c.ready={data:logo.data,type:logo.type,p:c.p}}};
    im.src=logo.data}catch(_){}
  return{data:logo.data,type:logo.type,p:null}}
// the live preview waits for a pause in typing and draws when the computer is free
{const idle=window.requestIdleCallback?(f=>requestIdleCallback(f,{timeout:700})):(f=>setTimeout(f,0));
  schedulePreview=function(delay=350){if(!pvOn)return;clearTimeout(pvTimer);
    const go=()=>{if(Date.now()-lastType<700){pvTimer=setTimeout(go,350);return}idle(()=>{try{preview()}catch(e){console.error(e)}})};
    pvTimer=setTimeout(go,Math.max(delay,delay<=30?delay:450))}}
// opening a sheet: the table first, the preview right after
{const s0=pvSetup;pvSetup=function(){const a=pvOn;if(!a)return s0.apply(this,arguments);pvOn=false;try{s0.apply(this,arguments)}finally{pvOn=a}pvLastKey="";schedulePreview(60)}}
