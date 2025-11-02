#!/bin/bash
# Automated setup script for remote server

set -e

echo "========================================"
echo "Nietzsche Bot - Server Setup"
echo "========================================"
echo

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "Please do not run as root"
    exit 1
fi

# Update system
echo "1. Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and dependencies
echo "2. Installing Python and dependencies..."
sudo apt-get install -y python3 python3-pip python3-venv git curl

# Install Ollama
echo "3. Installing Ollama..."
if ! command -v ollama &> /dev/null; then
    curl -fsSL https://ollama.com/install.sh | sh
    echo "Ollama installed"
else
    echo "Ollama already installed"
fi

# Pull the model
echo "4. Pulling Mistral model (this may take a while)..."
ollama pull mistral:latest

# Set up project directory
PROJECT_DIR="$HOME/nietzsche_bot"
echo "5. Setting up project at $PROJECT_DIR..."

cd "$PROJECT_DIR" || exit 1

# Create virtual environment
echo "6. Creating Python virtual environment..."
python3 -m venv venv

# Activate and install dependencies
echo "7. Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Check if .env exists
if [ ! -f .env ]; then
    echo
    echo "WARNING: .env file not found!"
    echo "Please create .env file with your credentials before continuing."
    echo "You can copy .env.example and fill in your values."
    exit 1
fi

# Make scripts executable
chmod +x health_check.sh
chmod +x setup_server.sh

# Set up systemd service
echo "8. Setting up systemd service..."
CURRENT_USER=$(whoami)
sed -i "s/YOUR_USERNAME/$CURRENT_USER/g" nietzsche-bot.service
sudo cp nietzsche-bot.service /etc/systemd/system/

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable nietzsche-bot

# Test the bot
echo "9. Running test..."
python test_single_post.py

if [ $? -eq 0 ]; then
    echo
    echo "========================================"
    echo "Setup completed successfully!"
    echo "========================================"
    echo
    echo "To start the bot:"
    echo "  sudo systemctl start nietzsche-bot"
    echo
    echo "To view status:"
    echo "  sudo systemctl status nietzsche-bot"
    echo
    echo "To view logs:"
    echo "  sudo journalctl -u nietzsche-bot -f"
    echo
else
    echo
    echo "Test failed. Please check your configuration."
    exit 1
fi
