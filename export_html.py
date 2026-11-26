import re,base64,io,os,sys
from PIL import Image
B='build/';s=open(B+'index.html').read()
def R(a,b):
    global s
    assert s.count(a)==1,('MISS',a[:80]);s=s.replace(a,b)
# --- test-build panel: section select + god mode ---
R('<title>Crowd Killer Streets</title>','<title>Crowd Killer Streets (Test Build)</title>')
R('    <div class="startrow">\n      <button id="start"','''    <div class="testbar" id="testbar">
      <b>TEST BUILD</b>
      <label for="testsec">Start at</label>
      <select id="testsec"><option value="0">1-1 Bergie Block</option><option value="1">1-2 Outside Ortlieb's</option><option value="2">1-3 Ortlieb's bar</option><option value="3">1-4 Stage room (Nicky Hitz)</option><option value="4">2-1 Bloomfield Ave</option><option value="5">2-2 Park St</option><option value="6">2-3 The Stairwell</option><option value="7">2-4 Dan Glenzig</option><option value="8">Bonus: Break the car</option><option value="9">3-1 The Sewer</option><option value="10">3-2 Ned Tugent</option></select>
      <label><input type="checkbox" id="testgod"> God mode</label>
    </div>
    <div class="startrow">\n      <button id="start"''')
R('</style>\n','.testbar{display:flex;flex-wrap:wrap;align-items:center;gap:10px 16px;padding:10px 14px;border:2px dashed var(--y);border-radius:3px;font-size:17px;color:var(--fg)}\n.testbar b{color:var(--y);letter-spacing:.12em}\n.testbar select{font:inherit;background:var(--panel-2);color:var(--fg);border:2px solid var(--line);padding:4px 8px}\n.testbar input{width:18px;height:18px;vertical-align:-3px;accent-color:#FFD400}\n</style>\n') if s.count('</style>\n')==1 else None
if '.testbar{' not in s:
    i=s.index('</style>');s=s[:i]+'.testbar{display:flex;flex-wrap:wrap;align-items:center;gap:10px 16px;padding:10px 14px;border:2px dashed var(--y);border-radius:3px;font-size:17px;color:var(--fg)}\n.testbar b{color:var(--y);letter-spacing:.12em}\n.testbar select{font:inherit;background:var(--panel-2);color:var(--fg);border:2px solid var(--line);padding:4px 8px}\n.testbar input{width:18px;height:18px;vertical-align:-3px;accent-color:#FFD400}\n'+s[i:]
R("function startGame(){\n  resetGame(sel);mode='play';",
  "function startGame(){\n  resetGame(sel);mode='play';\n  var ts=+(document.getElementById('testsec').value||0);if(ts>0){loadSection(ts,false);phase='intro';phaseT=110;fadeIn=FADE_IN;}")
R("function hurtPlayer(dmg,fromFace,heavy){","function hurtPlayer(dmg,fromFace,heavy){\n  if(document.getElementById('testgod').checked)return;")
# --- embed every asset ---
names=sorted(set(re.findall(r"""['"]([A-Za-z0-9_]+\.(?:png|jpg|mp3|mp4|wav))['"]""",s)))
total=0;report=[]
for n in names:
    raw=open(B+n,'rb').read()
    if n.endswith('.png'):
        im=Image.open(io.BytesIO(raw));buf=io.BytesIO();im.save(buf,'WEBP',lossless=True,method=6,quality=100)
        w=buf.getvalue()
        data,mime=(w,'image/webp') if len(w)<len(raw) else (raw,'image/png')
    elif n.endswith('.mp3'): data,mime=raw,'audio/mpeg'
    elif n.endswith('.mp4'): data,mime=raw,'video/mp4'
    elif n.endswith('.wav'): data,mime=raw,'audio/wav'
    else: data,mime=raw,'image/jpeg'
    uri='data:%s;base64,%s'%(mime,base64.b64encode(data).decode())
    cnt=0
    for q in ("'",'"'):
        k=s.count(q+n+q);cnt+=k;s=s.replace(q+n+q,q+uri+q)
    total+=len(data);report.append((n,len(raw),len(data),mime,cnt))
open('export/crowd_killer_streets_test.html','w').write(s)
for r in report:print(r)
print('embedded',len(names),'assets; payload',total,'file',os.path.getsize('export/crowd_killer_streets_test.html'))
