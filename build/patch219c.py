import sys
CSS=r'''.top .moremenu #b-getapp{border-top:1px solid var(--hair)!important;border-radius:0 0 7px 7px!important;margin-top:4px}
/* one line at every computer width */
@media (min-width:761px){
  .top{flex-wrap:nowrap}
  .top #b-role{flex:none}
  body.role-admin .top .rolechip .rl{display:none}
  body.role-admin .top #b-role{width:36px;padding:0}
  .top #tbar,.top .topmore,.top .brand{flex:none}
  .top .mainnav{min-width:0;overflow:hidden}
}
@media (max-width:1700px) and (min-width:761px){body.role-admin .crumbs{display:none}#tbar #b-print .lbl{display:none}}
@media (max-width:1600px) and (min-width:761px){.top .mainnav button{padding:0 10px}}
@media (max-width:1366px) and (min-width:761px){.top .crumbs{display:none}.top .mainnav button{padding:0 8px;font-size:13px;letter-spacing:.06em}}
@media (max-width:1180px) and (min-width:761px){#tbar .tb.xl .lbl2{display:none}.top .mainnav button{padding:0 6px;font-size:12.5px;letter-spacing:.03em}.top .brand h1{font-size:18px}}
@media (max-width:1000px) and (min-width:761px){#tbar .tb.pvtog{display:none}.top .mainnav button{padding:0 5px;font-size:12px;letter-spacing:0}}
@media (max-width:880px) and (min-width:761px){.top #tbar #b-print{display:none}#tbar #b-print+.tb{border-radius:8px 0 0 8px;margin-left:0}.top .brand h1{font-size:16px}.top .mainnav{margin-left:0}.top .mainnav button{padding:0 4px;font-size:11.5px}.top{gap:5px}}
@media (max-width:840px) and (min-width:761px){body.role-admin .top .brand h1{display:none}body.role-admin .top .brand{padding-right:4px}}'''
A='''.top .moremenu #b-getapp{border-top:1px solid var(--hair)!important;border-radius:0 0 7px 7px!important;margin-top:4px}'''
for f in sys.argv[1:]:
  s=open(f).read();assert s.count(A)==1,f;s=s.replace(A,CSS);open(f,'w').write(s);print("patched",f)
