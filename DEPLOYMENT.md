# Deployment Guide - Running on Remote Server

This guide covers multiple methods to keep your Nietzsche bot running continuously on a remote server.

## Prerequisites

- Remote server with SSH access (Ubuntu/Debian recommended)
- Python 3.8+ installed
- Ollama installed and running
- Your `.env` file with credentials

## Method 1: Systemd Service (Recommended for Production)

### 1. Transfer files to server

```bash
# From your local machine
scp -r /home/taliban/nietzsche_bot user@your-server:/home/user/
```

### 2. Set up on the server

```bash
# SSH into your server
ssh user@your-server

# Navigate to project directory
cd /home/user/nietzsche_bot

# Create virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Create systemd service

```bash
sudo nano /etc/systemd/system/nietzsche-bot.service
```

Copy the content from `nietzsche-bot.service` file (included in this repo).

### 4. Enable and start the service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable nietzsche-bot

# Start the service
sudo systemctl start nietzsche-bot

# Check status
sudo systemctl status nietzsche-bot

# View logs
sudo journalctl -u nietzsche-bot -f
```

### 5. Manage the service

```bash
# Stop the bot
sudo systemctl stop nietzsche-bot

# Restart the bot
sudo systemctl restart nietzsche-bot

# View recent logs
sudo journalctl -u nietzsche-bot -n 100

# View live logs
sudo journalctl -u nietzsche-bot -f
```

## Method 2: Screen/Tmux (Quick Setup)

### Using Screen

```bash
# SSH into server
ssh user@your-server

# Start a screen session
screen -S nietzsche-bot

# Navigate to project and activate venv
cd /home/user/nietzsche_bot
source venv/bin/activate

# Run the bot
python bot.py

# Detach: Press Ctrl+A, then D

# Reattach later
screen -r nietzsche-bot

# List all screens
screen -ls
```

### Using Tmux

```bash
# Start a tmux session
tmux new -s nietzsche-bot

# Navigate to project and activate venv
cd /home/user/nietzsche_bot
source venv/bin/activate

# Run the bot
python bot.py

# Detach: Press Ctrl+B, then D

# Reattach later
tmux attach -t nietzsche-bot

# List all sessions
tmux ls
```

## Method 3: Docker (Containerized)

See `Dockerfile` and `docker-compose.yml` for containerized deployment.

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## Method 4: PM2 (Node.js Process Manager)

PM2 works great with Python too:

```bash
# Install PM2 globally
npm install -g pm2

# Start the bot
pm2 start bot.py --name nietzsche-bot --interpreter python3

# Save PM2 configuration
pm2 save

# Setup PM2 to start on boot
pm2 startup

# View status
pm2 status

# View logs
pm2 logs nietzsche-bot

# Restart
pm2 restart nietzsche-bot

# Stop
pm2 stop nietzsche-bot
```

## Setting Up Ollama on Remote Server

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull your model
ollama pull mistral:latest

# Run Ollama as a service (usually auto-configured)
# Check status
systemctl status ollama

# If not running as service, start it
ollama serve
```

## Monitoring and Maintenance

### Log Files

The bot creates log files in the `logs/` directory:
- Format: `nietzsche_bot_YYYYMMDD.log`
- Location: `/home/user/nietzsche_bot/logs/`

### Health Checks

Create a simple health check script:

```bash
#!/bin/bash
# health_check.sh

if systemctl is-active --quiet nietzsche-bot; then
    echo "Bot is running"
    exit 0
else
    echo "Bot is down, restarting..."
    sudo systemctl start nietzsche-bot
    exit 1
fi
```

### Cron Job for Health Check

```bash
# Edit crontab
crontab -e

# Add health check every 15 minutes
*/15 * * * * /home/user/nietzsche_bot/health_check.sh
```

## Firewall Configuration

If you need to access logs remotely or run a web dashboard:

```bash
# Allow SSH
sudo ufw allow 22/tcp

# Allow Ollama (if needed externally)
sudo ufw allow 11434/tcp

# Enable firewall
sudo ufw enable
```

## Security Best Practices

1. **Never commit `.env` file** to version control
2. **Use SSH keys** instead of passwords
3. **Keep secrets secure**:
   ```bash
   chmod 600 .env
   ```
4. **Regular updates**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
5. **Use a non-root user** for running the bot

## Troubleshooting

### Bot won't start

```bash
# Check logs
sudo journalctl -u nietzsche-bot -n 50

# Check if Ollama is running
curl http://localhost:11434/api/tags

# Verify Python environment
source venv/bin/activate
python -c "import tweepy; print('Tweepy OK')"
```

### High memory usage

Monitor with:
```bash
htop
# or
top
```

### Ollama issues

```bash
# Restart Ollama
sudo systemctl restart ollama

# Check Ollama logs
sudo journalctl -u ollama -n 50
```

## Backup Strategy

```bash
# Backup logs and configuration
tar -czf nietzsche_bot_backup_$(date +%Y%m%d).tar.gz \
    .env \
    logs/ \
    *.py \
    requirements.txt

# Copy to safe location
scp nietzsche_bot_backup_*.tar.gz backup-server:/backups/
```

## Cost Optimization

### Using Free Tier Services

- **Oracle Cloud**: Free VPS with ARM instances
- **AWS Free Tier**: 750 hours/month for 12 months
- **Google Cloud**: $300 credit for 90 days
- **DigitalOcean**: $200 credit for 60 days (with referral)

### Resource Requirements

- **CPU**: 1 core minimum (2 cores recommended)
- **RAM**: 2GB minimum (4GB recommended for Ollama)
- **Storage**: 10GB minimum
- **Network**: Minimal (API calls only)

## Quick Start Commands

```bash
# Complete setup on fresh server
git clone <your-repo> nietzsche_bot  # or upload files
cd nietzsche_bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Copy and configure .env
nano .env

# Test
python test_single_post.py

# Deploy with systemd
sudo cp nietzsche-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now nietzsche-bot
```
