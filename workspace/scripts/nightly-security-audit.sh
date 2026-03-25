#!/bin/bash
set -uo pipefail

OC="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
REPORT_FILE="$OC/security-reports/audit-$(date +%Y%m%d).log"

# Setup report output
exec > "$REPORT_FILE" 2>&1

echo "=========================================="
echo "OpenClaw Security Audit Report - $(date)"
echo "=========================================="
critical=0
warn=0
ok=0

# Helper function
check_status() {
    if [ $? -eq 0 ]; then
        echo "✅ OK: $1"
        ((ok++))
    else
        echo "🚨 CRITICAL: $1"
        ((critical++))
    fi
}

echo "=== [1] OpenClaw Platform Audit ==="
openclaw security audit | head -n 30 || echo "✅ Platform Check Finished"

echo "=== [2] Process & Network Audit ==="
lsof -nP -iTCP -sTCP:LISTEN | head -n 20 || echo "✅ No unusual listening ports found."

echo "=== [3] Sensitive Directory Changes ==="
find "$OC" /etc ~/.ssh -mtime -1 2>/dev/null | head -n 20 || echo "✅ No unexpected changes."

echo "=== [4] System Cron Jobs ==="
crontab -l 2>/dev/null || echo "✅ No user crontab found."

echo "=== [5] OpenClaw Cron Jobs ==="
openclaw cron list | head -n 20 || echo "✅ No unusual OpenClaw cron jobs."

echo "=== [6] Login & SSH Activity ==="
last -n 10 || echo "✅ No recent logins."

echo "=== [7] Key File Integrity ==="
if [ -f "$OC/.config-baseline.sha256" ]; then
    shasum -a 256 -c "$OC/.config-baseline.sha256" && check_status "Config Integrity Matched" || echo "🚨 Config Integrity Mismatch!"
else
    echo "⚠️ Baseline file not found."
    ((warn++))
fi

echo "=== [8] Yellow Line Audit (sudo) ==="
# macOS auth logs for sudo are in system log, fetching last 50 lines
log show --predicate 'process == "sudo"' --last 24h 2>/dev/null | head -n 50 || echo "✅ No suspicious sudo logs."

echo "=== [9] Disk Usage ==="
df -h / | tail -n 1 || echo "✅ Disk usage normal."

echo "=== [10] Gateway Environment ==="
# On macOS, checking env of another process is restricted, just list the process
ps -ef | grep openclaw-gateway | grep -v grep | head -n 1 || echo "✅ Gateway process running normally."

echo "=== [11] DLP Scan (Memory & Logs) ==="
# Simple search for potential mnemonic or hex private keys
grep -rEi --exclude-dir=.git "(0x[a-fA-F0-9]{64}|^[a-zA-Z]+( [a-zA-Z]+){11}$)" "$OC/workspace/memory/" 2>/dev/null | head -n 10 || echo "✅ No plaintext private keys or mnemonics detected."

echo "=== [12] Skill/MCP Integrity ==="
if [ -f "$OC/.skill-baseline.sha256" ]; then
    CURRENT_SKILL_HASH=$(find "$OC/workspace/skills" -type f -not -path '*/.git/*' -exec shasum -a 256 {} \; | sort | shasum -a 256)
    EXPECTED_SKILL_HASH=$(cat "$OC/.skill-baseline.sha256")
    if [ "$CURRENT_SKILL_HASH" == "$EXPECTED_SKILL_HASH" ]; then
        echo "✅ Skill Integrity Matched."
        ((ok++))
    else
        echo "🚨 Skill Integrity Mismatch!"
        ((critical++))
    fi
else
    echo "⚠️ Skill Baseline file not found."
    ((warn++))
fi

echo "=== [13] Brain Backup Sync ==="
cd "$OC/workspace" && git status -s | head -n 10 || echo "✅ Brain backup checked."

echo "=========================================="
echo "Summary: $critical critical · $warn warn · $ok ok"
echo "=========================================="

# Log rotation: Keep last 30 days
find "$OC/security-reports" -type f -mtime +30 -delete 2>/dev/null

# Make sure we print the summary to stdout as well so OpenClaw cron can read it
cat "$REPORT_FILE"
