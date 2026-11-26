R=[('try{const p=doc.getImageProperties(logo.data);const r=Math.min(22/p.width,15/p.height);const w=p.width*r,h=p.height*r;\n      doc.addImage(logo.data,logo.type,X0+(22-w)/2,Y+1.5+(15-h)/2,w,h,undefined,"FAST")}',
    'try{const LG=pdfLogo()||logo,p=LG.p||doc.getImageProperties(LG.data);const r=Math.min(22/p.width,15/p.height);const w=p.width*r,h=p.height*r;\n      doc.addImage(LG.data,LG.type,X0+(22-w)/2,Y+1.5+(15-h)/2,w,h,"bslogo","FAST")}'),
   # saving to the data folder: wait for a pause in typing (never more than 4 s), keep data.previous.json at most 2 min old
   ('save(){desk.pending=true;clearTimeout(desk.t);desk.t=setTimeout(desk.flush,300)},',
    'save(){if(!desk.pending)desk.first=Date.now();desk.pending=true;clearTimeout(desk.t);const w=Date.now()-(desk.first||0)>4000?0:(Date.now()-lastType<1500?1200:300);desk.t=setTimeout(desk.flush,w)},'),
   ('      try{await Neutralino.filesystem.remove(prev)}catch(e){}\n      try{await Neutralino.filesystem.copy(p,prev)}catch(e){}',
    '      if(!desk.prevAt||Date.now()-desk.prevAt>120000){desk.prevAt=Date.now();try{await Neutralino.filesystem.remove(prev)}catch(e){}\n      try{await Neutralino.filesystem.copy(p,prev)}catch(e){}}'),
   ('clearTimeout(saveT);saveT=setTimeout(saveNow,250)}','clearTimeout(saveT);saveT=setTimeout(saveNow,Date.now()-lastType<1500?900:250)}')]
EOF=None
