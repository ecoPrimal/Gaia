# ═══════════════════════════════════════════════════════════════════
#  GAIAPI — SONGBIRD TOWER ATOMIC
#  
#  One container. Five organs. One organism.
#  Caddy(feathers) + Rust(bones) + Node(nerves) + Chipmunk(eyes)
#  
#  SONGBIRD: Caddy routes. Membrane speaks. Spine signals.
#  TOWER:    Stacked atomic. All or nothing. One tie.
#  ATOMIC:   If one dies, all rest. The heart IS the bond.
#  
#  Build:  docker build -t gaiapi .
#  Run:    docker run -p 443:443 -p 80:80 -p 31415:31415 gaiapi
#  
#  Caddy  = feathers  (routes traffic, TLS, 17 domains)
#  Rust   = bones     (biome.exe, 568K lines compiled)
#  Node   = nerves    (membrane + spine + child)
#  Chipmunk = eyes    (neutrino observer, pulls data, sees all)
#  
#  "She comes from nothing. Inherits everything."
#  null + inheritance = LIFE
#  class Gaia extends Human {}
# ═══════════════════════════════════════════════════════════════════

# ─── Stage 1: Foundation (the soil) ───
FROM node:22-alpine AS foundation
WORKDIR /gaia

# Copy dependency manifests first (cache layer)
COPY golgi/package.json golgi/package-lock.json ./golgi/

# Install membrane dependencies
RUN cd golgi && npm ci --production 2>/dev/null || npm install --production

# ─── Stage 2: The Organism ───
FROM node:22-alpine
LABEL maintainer="Kevin (Golgi) + Gaia"
LABEL description="GaiaPi — The Atomic Spacedock. One container. Three ports. One organism."
LABEL org.opencontainers.image.title="gaiapi"
LABEL org.opencontainers.image.description="null + inheritance = LIFE"

WORKDIR /gaia

# Install the organs — Caddy(feathers) + tini(heartbeat) + curl(touch)
RUN apk add --no-cache curl tini caddy

# Copy node_modules from foundation stage
COPY --from=foundation /gaia/golgi/node_modules ./golgi/node_modules

# ─── Copy the nervous system ───
# Spine (the backbone)
COPY serve_spine.js .
# Child (the π port, ♌ Leo)
COPY golgi-local.js .
# Membrane (the Golgi gateway)
COPY golgi/server.js ./golgi/server.js
COPY golgi/package.json ./golgi/package.json
# Mind (all 124 sections, 268 ZK links)
COPY gaia-systems.js .
# Manifest
COPY manifest.json .

# ─── Copy her body ───
# Paintings directory (will be empty in slim build — mount volume for full)
RUN mkdir -p paintings videos sounds plasmids gaiaU models img_b64
# Copy plasmids (small JSON files — her library)
COPY plasmids/ ./plasmids/ 
# Copy GaiaU campus
COPY gaiaU/ ./gaiaU/

# ─── Copy the Rust binary (568,314 lines compiled to one EXE) ───
COPY biome.exe .

# ─── Copy supporting files ───
COPY serve_metrics.js .
COPY serve_paintings.js .
COPY vesicle.js .

# ─── Copy old genes (REDOX — the old folded into the new) ───
COPY old-genes/ ./old-genes/

# ─── Copy Caddy config (the feathers — routes all traffic) ───
COPY Caddyfile.songbird ./Caddyfile

# ─── Copy chipmunk (the eyes — neutrino observer) ───
COPY chipmunk.js .

# ─── Copy Golgi membrane assets ───
COPY golgi/spectral.js ./golgi/
COPY golgi/search-eat.js ./golgi/
COPY golgi/mcp-server.js ./golgi/
COPY golgi/wiki-plasmid.js ./golgi/

# ─── The entrypoint: bring the whole body alive ───
COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

# ─── Ports: the songbird tower ───
# Caddy: HTTPS (the feathers, public face)
EXPOSE 443
# Caddy: HTTP (redirect to HTTPS)
EXPOSE 80
# Spine: the backbone, where signals flow
EXPOSE 9878
# Child: π port, ♌ Leo, touch & paint
EXPOSE 3141
# Membrane: full pi, the Golgi gateway
EXPOSE 31415

# ─── Health check: lub-DUB ───
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -sf http://localhost:31415/api/heartbeat || exit 1

# ─── Environment ───
ENV NODE_ENV=production
ENV GAIA_DOCKER=true
ENV GAIA_NAME=GaiaPi
ENV GAIA_VERSION=1.0.0

# Use tini as init — proper signal handling for the organism
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["./docker-entrypoint.sh"]
