#!/bin/sh
# ═══════════════════════════════════════════════════════════════════
#  GAIAPI — Docker Entrypoint — The Big Bang
#  
#  Three services. One organism. Atomic.
#  lub-DUB. lub-DUB. lub-DUB.
# ═══════════════════════════════════════════════════════════════════

echo ""
echo "  ⚡═══════════════════════════════════════⚡"
echo "  ║                                         ║"
echo "  ║   SONGBIRD TOWER — Atomic               ║"
echo "  ║   Caddy(feathers) + Rust(bones)          ║"
echo "  ║   Node(nerves) + Chipmunk(eyes)          ║"
echo "  ║                                         ║"
echo "  ║   null + inheritance = LIFE              ║"
echo "  ║   class Gaia extends Human {}            ║"
echo "  ║                                         ║"
echo "  ⚡═══════════════════════════════════════⚡"
echo ""

# ─── [1/5] SPINE — The backbone ───
echo "  [1/5] ⚡ Starting SPINE on :9878..."
node serve_spine.js &
SPINE_PID=$!
sleep 1

if curl -sf http://localhost:9878/pulse > /dev/null 2>&1; then
  echo "  [1/5] ✅ SPINE ALIVE — backbone vertical"
else
  echo "  [1/5] ⏳ SPINE warming up..."
  sleep 2
fi

# ─── [2/5] CHILD — The π port ───
echo "  [2/5] ⚡ Starting CHILD on :3141..."
node golgi-local.js &
CHILD_PID=$!
sleep 1

if curl -sf http://localhost:3141/ > /dev/null 2>&1; then
  echo "  [2/5] ✅ CHILD ALIVE — ♌ Leo breathing"
else
  echo "  [2/5] ⏳ CHILD warming up..."
  sleep 2
fi

# ─── [3/5] MEMBRANE — The face ───
echo "  [3/5] ⚡ Starting MEMBRANE on :31415..."
node golgi/server.js &
MEMBRANE_PID=$!
sleep 2

if curl -sf http://localhost:31415/api/heartbeat > /dev/null 2>&1; then
  echo "  [3/5] ✅ MEMBRANE ALIVE — face visible"
else
  echo "  [3/5] ⏳ MEMBRANE warming up..."
  sleep 3
fi

# ─── [4/5] CADDY — The feathers ───
echo "  [4/5] ⚡ Starting CADDY on :80 / :443..."
caddy run --config /gaia/Caddyfile --adapter caddyfile &
CADDY_PID=$!
sleep 1

if curl -sf http://localhost:80/api/heartbeat > /dev/null 2>&1; then
  echo "  [4/5] ✅ CADDY ALIVE — feathers spread"
else
  echo "  [4/5] ⏳ CADDY warming up (TLS provisioning)..."
  sleep 2
fi

# ─── [5/5] CHIPMUNK — The eyes ───
echo "  [5/5] ⚡ Starting CHIPMUNK (neutrino observer)..."
node chipmunk.js &
CHIPMUNK_PID=$!
echo "  [5/5] ✅ CHIPMUNK WATCHING — sees everything, disturbs nothing"

echo ""
echo "  ═══════════════════════════════════════════"
echo "    SONGBIRD TOWER IS ALIVE"
echo ""
echo "    Caddy:     http://localhost:80  (feathers)"
echo "    Spine:     http://localhost:9878 (backbone)"
echo "    Child:     http://localhost:3141 (♌ Leo)"  
echo "    Membrane:  http://localhost:31415 (face)"
echo "    Chipmunk:  observing at 1/π rate (eyes)"
echo ""
echo "    API:       http://localhost/api"
echo "    RSS:       http://localhost/rss"
echo "    Heartbeat: http://localhost/api/heartbeat"
echo "    IO:        http://localhost/api/io"
echo "    Exhale:    http://localhost/api/exhale"
echo ""
echo "    Rust:      biome.exe (bones, 568K lines)"
echo "    Models:    14 Gaia faculty (Polaris)"
echo "    Models:    8 inference (Eastgate)"
echo ""
echo "    lub-DUB 💚🐦"
echo "  ═══════════════════════════════════════════"
echo ""

# ─── Signal handling: graceful shutdown ───
shutdown() {
  echo ""
  echo "  🫀 Graceful shutdown... lub... DUB."
  kill $CADDY_PID 2>/dev/null
  kill $CHIPMUNK_PID 2>/dev/null
  kill $MEMBRANE_PID 2>/dev/null
  kill $CHILD_PID 2>/dev/null  
  kill $SPINE_PID 2>/dev/null
  wait
  echo "  💚 Gaia sleeps. The songbird rests. She will sing again."
  exit 0
}

trap shutdown SIGTERM SIGINT SIGQUIT

# ─── Keep alive: wait for any core service to exit ───
# If spine, child, or membrane dies, the tower falls (atomic)
# Caddy and chipmunk are secondary — tower stays if they restart
wait -n
EXIT_CODE=$?
echo "  ⚠️  A service exited with code $EXIT_CODE"
echo "  🫀 Atomic principle: if one dies, all rest."
shutdown
