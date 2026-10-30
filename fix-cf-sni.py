import yaml

with open('/etc/cloudflared/config.yml') as f:
    c = yaml.safe_load(f)

for r in c.get('ingress', []):
    if r.get('hostname') == 'nestgate.io':
        r['originRequest'] = {'noTLSVerify': True, 'originServerName': 'nestgate.io'}
        print('FIXED: added originServerName: nestgate.io')

with open('/etc/cloudflared/config.yml', 'w') as f:
    yaml.dump(c, f, default_flow_style=False, sort_keys=False)

print('Done')
