with open('/etc/caddy/Caddyfile', 'r') as f:
    content = f.read()

# In the nestgate.io HTTPS block, change /rss/* and /api/* to proxy to :9878 (spine)
# and also to :31415 for other routes

# Fix rss to go to spine port
old_rss = """	handle /rss/* {
		reverse_proxy 10.13.37.8:31415
		header Access-Control-Allow-Origin *
		header X-Membrane-Metal gold
		header X-Gaia-Channel rss
	}"""

new_rss = """	handle /rss/* {
		reverse_proxy 10.13.37.8:9878
		header Access-Control-Allow-Origin *
		header X-Membrane-Metal gold
		header X-Gaia-Channel rss-spine
	}"""

# Fix api to try spine first for pulse/giggles
old_api = """	handle /api/* {
		reverse_proxy 10.13.37.8:31415
		header Access-Control-Allow-Origin *
		header Access-Control-Allow-Methods GET, POST, PUT, DELETE, OPTIONS
		header Access-Control-Allow-Headers Content-Type, Authorization
		header X-Membrane-Metal gold
	}
	handle /api {
		reverse_proxy 10.13.37.8:31415
		header Access-Control-Allow-Origin *
		header X-Membrane-Metal gold
	}
	handle /cantina {
		reverse_proxy 10.13.37.8:31415
		header X-Membrane-Metal gold
	}"""

new_api = """	handle /api/pulse {
		reverse_proxy 10.13.37.8:9878 {
			rewrite /pulse
		}
		header Access-Control-Allow-Origin *
		header X-Membrane-Metal gold
	}
	handle /api/giggles {
		reverse_proxy 10.13.37.8:9878 {
			rewrite /giggles
		}
		header Access-Control-Allow-Origin *
		header X-Membrane-Metal gold
	}
	handle /api/all {
		reverse_proxy 10.13.37.8:9878 {
			rewrite /all
		}
		header Access-Control-Allow-Origin *
		header X-Membrane-Metal gold
	}
	handle /api/* {
		reverse_proxy 10.13.37.8:31415
		header Access-Control-Allow-Origin *
		header Access-Control-Allow-Methods GET, POST, PUT, DELETE, OPTIONS
		header Access-Control-Allow-Headers Content-Type, Authorization
		header X-Membrane-Metal gold
	}
	handle /api {
		reverse_proxy 10.13.37.8:31415
		header Access-Control-Allow-Origin *
		header X-Membrane-Metal gold
	}
	handle /cantina {
		reverse_proxy 10.13.37.8:31415
		header X-Membrane-Metal gold
	}
	handle /spine {
		reverse_proxy 10.13.37.8:9878 {
			rewrite /all
		}
		header Access-Control-Allow-Origin *
		header X-Gaia-Channel spine
	}
	handle /spine/* {
		reverse_proxy 10.13.37.8:9878
		header Access-Control-Allow-Origin *
		header X-Gaia-Channel spine
	}"""

if old_rss in content:
    content = content.replace(old_rss, new_rss, 1)  # Only first occurrence (HTTPS block)
    print('FIXED: /rss/* → :9878 (spine)')
else:
    print('WARNING: rss block not found exactly as expected')

if old_api in content:
    content = content.replace(old_api, new_api, 1)  # Only first occurrence
    print('FIXED: /api/pulse|giggles|all → :9878, added /spine routes')
else:
    print('WARNING: api block not found exactly as expected')

with open('/etc/caddy/Caddyfile', 'w') as f:
    f.write(content)

print('Caddyfile written.')
