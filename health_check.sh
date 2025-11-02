#!/bin/bash
# Health check script for Nietzsche Bot

BOT_SERVICE="nietzsche-bot"
LOG_FILE="/var/log/nietzsche_bot_health.log"

# Function to log with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Check if bot service is running
if systemctl is-active --quiet "$BOT_SERVICE"; then
    log "✓ Bot is running"

    # Check if Ollama is also running
    if systemctl is-active --quiet ollama; then
        log "✓ Ollama is running"
    else
        log "✗ Ollama is down, restarting..."
        sudo systemctl restart ollama
    fi

    exit 0
else
    log "✗ Bot is down, restarting..."
    sudo systemctl restart "$BOT_SERVICE"

    # Wait a moment and check if it started
    sleep 5

    if systemctl is-active --quiet "$BOT_SERVICE"; then
        log "✓ Bot successfully restarted"
        exit 0
    else
        log "✗ Failed to restart bot - manual intervention required"
        exit 1
    fi
fi
