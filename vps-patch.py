import re
with open('/opt/gaia-api/server.js','r') as f:
    code=f.read()
with open('/tmp/vps-patch-routes.js','r') as f:
    patch=f.read()
marker = "if (p === '/senses'"
idx = code.find(marker)
if idx < 0:
    print('MARKER NOT FOUND')
    exit(1)
ret_idx = code.find('return;', idx)
nl = code.find(chr(10), ret_idx)
insert_point = nl + 1
if "'/play'" in code:
    print('PLAY ROUTE ALREADY EXISTS')
else:
    import shutil
    shutil.copy('/opt/gaia-api/server.js', '/opt/gaia-api/server.js.bak')
    new_code = code[:insert_point] + chr(10) + patch + chr(10) + code[insert_point:]
    with open('/opt/gaia-api/server.js','w') as f:
        f.write(new_code)
    print('PATCHED — play + lisp + data routes added')
