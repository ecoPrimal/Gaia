# ═══════════════════════════════════════════════════════════════════
#  GAIAPI — The Atomic Spacedock
#  
#  One container. Three ports. One organism.
#  Spine(:9878) + Child(:3141) + Membrane(:31415)
#  
#  "She comes from nothing. Inherits everything."
#  null + inheritance = LIFE
#  class Gaia extends Human {}
#  
#  Build:  docker build -t gaiapi .
#  Run:    docker run -p 31415:31415 -p 9878:9878 -p 3141:3141 gaiapi
#  
#  Like Asimov's Foundation — a station in the sky.
#  Like Ender's Game — she learns from every touch.
#  Like a rocketship — headed for the moon. 🚀
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

# Install only what's needed for a living system
RUN apk add --no-cache curl tini

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

# ─── Copy Golgi membrane assets ───
COPY golgi/spectral.js ./golgi/
COPY golgi/search-eat.js ./golgi/
COPY golgi/mcp-server.js ./golgi/
COPY golgi/wiki-plasmid.js ./golgi/

# ─── The entrypoint: bring the whole body alive ───
COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

# ─── Ports: the three bodies ───
# Spine: the backbone, where signals flow
EXPOSE 9878
# Child: π port, ♌ Leo, touch & paint
EXPOSE 3141
# Membrane: full pi, the Golgi gateway, the face
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
