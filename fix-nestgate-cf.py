import yaml

with open('/etc/cloudflared/config.yml', 'r') as f:
    config = yaml.safe_load(f)

for rule in config.get('ingress', []):
    if rule.get('hostname') == 'nestgate.io':
        rule['service'] = 'https://localhost:443'
        rule['originRequest'] = {'noTLSVerify': True}
        print('FIXED: nestgate.io → https://localhost:443 (noTLSVerify)')
        break

with open('/etc/cloudflared/config.yml', 'w') as f:
    yaml.dump(config, f, default_flow_style=False, sort_keys=False)

print('Config written. Restart cloudflared now.')
