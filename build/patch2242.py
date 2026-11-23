import sys
# 2.24.2: insert references are never cut on the PDF: they get smaller first (still readable on A4),
# then drop the "Insert" word, and only cut as a very last resort.
R=[('''if(kind==="ins"){font("Plex5",7);color(C.mid);const lw=txt(L.insS+" ",cx2+1.8,yS);font("Mono5",7.6);color(C.ink);txt(fit(v,w2-3.6-lw),cx2+1.8+lw,yS)}''',
'''if(kind==="ins"){const RM=w2-3.6;font("Plex5",6.6);let lw=tw(L.insS+" "),f=7.6;font("Mono5",f);while(f>5.6&&tw(v)>RM-lw){f-=0.2;font("Mono5",f)}
         if(tw(v)>RM-lw){lw=0;f=7.6;font("Mono5",f);while(f>5&&tw(v)>RM){f-=0.2;font("Mono5",f)}}
         if(lw){font("Plex5",Math.min(6.6,f));color(C.mid);txt(L.insS+" ",cx2+1.8,yS)}font("Mono5",f);color(C.ink);txt(fit(v,RM-lw),cx2+1.8+lw,yS)}'''),
('''stack(v,X_("insert")+1.6,W_("insert")-2.8,"Mono5",8.4,5.6,"left")''','''stack(v,X_("insert")+1.6,W_("insert")-2.8,"Mono5",8.4,5,"left")''')]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:80]);s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
