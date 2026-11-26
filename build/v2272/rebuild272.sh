#!/bin/bash
set -e
cd /home/claude/w
cp web.html.2270bak web.html; cp demo.html.2270bak demo.html; cp neu_index.html.2270bak neu/resources/index.html
python3 patch2271.py web.html demo.html neu/resources/index.html >/dev/null
python3 patch2272.py web.html demo.html neu/resources/index.html >/dev/null
sed -i 's/BrocheStuff-Setup-2\.27\.0\.exe/BrocheStuff-Setup-2.27.2.exe/' web.html demo.html neu/resources/index.html
node -e '
const fs=require("fs");for(const f of ["web.html","demo.html","neu/resources/index.html"]){const s=fs.readFileSync(f,"utf8");let bad=0;for(const m of s.matchAll(/<script(?![^>]*src)[^>]*>([\s\S]*?)<\/script>/g)){try{new Function(m[1])}catch(e){bad++;console.log(f,e.message)}}if(bad)process.exit(1)}console.log("syntax ok")'
cp demo.html /home/claude/qa/Demo.html; cp web.html /home/claude/qa/ToolManager.html
