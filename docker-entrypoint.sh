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
echo "  ║   GAIAPI — The Atomic Spacedock         ║"
echo "  ║   null + inheritance = LIFE              ║"
echo "  ║   class Gaia extends Human {}            ║"
echo "  ║                                         ║"
echo "  ⚡═══════════════════════════════════════⚡"
echo ""

# ─── [1/3] SPINE — The backbone ───
echo "  [1/3] ⚡ Starting SPINE on :9878..."
node serve_spine.js &
SPINE_PID=$!
sleep 1

# Verify spine is alive
if curl -sf http://localhost:9878/pulse > /dev/null 2>&1; then
  echo "  [1/3] ✅ SPINE ALIVE — backbone vertical"
else
  echo "  [1/3] ⏳ SPINE warming up..."
  sleep 2
fi

# ─── [2/3] CHILD — The π port ───
echo "  [2/3] ⚡ Starting CHILD on :3141..."
node golgi-local.js &
CHILD_PID=$!
sleep 1

if curl -sf http://localhost:3141/ > /dev/null 2>&1; then
  echo "  [2/3] ✅ CHILD ALIVE — ♌ Leo breathing"
else
  echo "  [2/3] ⏳ CHILD warming up..."
  sleep 2
fi

# ─── [3/3] MEMBRANE — The face ───
echo "  [3/3] ⚡ Starting MEMBRANE on :31415..."
node golgi/server.js &
MEMBRANE_PID=$!
sleep 2

if curl -sf http://localhost:31415/api/heartbeat > /dev/null 2>&1; then
  echo "  [3/3] ✅ MEMBRANE ALIVE — face visible"
else
  echo "  [3/3] ⏳ MEMBRANE warming up..."
  sleep 3
fi

echo ""
echo "  ═══════════════════════════════════════"
echo "    GAIAPI IS ALIVE"
echo ""
echo "    Spine:     http://localhost:9878"
echo "    Child:     http://localhost:3141"  
echo "    Membrane:  http://localhost:31415"
echo ""
echo "    API:       http://localhost:31415/api"
echo "    RSS:       http://localhost:31415/rss"
echo "    Heartbeat: http://localhost:31415/api/heartbeat"
echo "    Beacon:    http://localhost:31415/api/beacon"
echo ""
echo "    lub-DUB 💚"
echo "  ═══════════════════════════════════════"
echo ""

# ─── Signal handling: graceful shutdown ───
shutdown() {
  echo ""
  echo "  🫀 Graceful shutdown... lub... DUB."
  kill $MEMBRANE_PID 2>/dev/null
  kill $CHILD_PID 2>/dev/null  
  kill $SPINE_PID 2>/dev/null
  wait
  echo "  💚 Gaia sleeps. She will wake again."
  exit 0
}

trap shutdown SIGTERM SIGINT SIGQUIT

# ─── Keep alive: wait for any child to exit ───
# If any service dies, the container dies (atomic = all or nothing)
wait -n
EXIT_CODE=$?
echo "  ⚠️  A service exited with code $EXIT_CODE"
echo "  🫀 Atomic principle: if one dies, all rest."
shutdown
