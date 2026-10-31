#!/bin/bash
echo "=== KILLING STALE SSH SESSIONS ==="
MY_SSHD_PID=$(cat /proc/$PPID/status 2>/dev/null | grep PPid | awk '{print $2}')
echo "Our SSH parent: $MY_SSHD_PID"

count=0
for pid in $(pgrep -f 'sshd-session:'); do
  if [ "$pid" != "$PPID" ] && [ "$pid" != "$MY_SSHD_PID" ]; then
    kill "$pid" 2>/dev/null && count=$((count+1))
  fi
done
echo "Killed $count stale SSH sessions"

echo "=== KILLING VESICLE.JS (Oct 28 zombie, 45MB) ==="
kill 1603577 && echo "Killed vesicle.js PID 1603577" || echo "Already dead"

sleep 1

echo "=== VERIFY ==="
echo "SSH sessions remaining: $(pgrep -f 'sshd-session:' | wc -l)"
echo "Node processes:"
ps aux | grep '[n]ode'
echo "=== DONE ==="
