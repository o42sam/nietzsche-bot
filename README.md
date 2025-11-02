# Nietzsche Quote Bot for X (Twitter)

An automated bot that extracts random sentences from "Beyond Good and Evil" by Friedrich Nietzsche, rephrases them using a local Ollama AI model, and posts them to X (Twitter) every 2 hours.

## Features

- PDF text extraction with sentence parsing
- AI-powered quote rephrasing using Ollama
- Automated posting to X using API v2
- Scheduled posting every 2 hours
- Comprehensive logging
- Graceful error handling
- Easy configuration via environment variables

## Prerequisites

1. **Python 3.8+**
2. **Ollama** - Running locally with a model installed (e.g., llama2)
3. **X (Twitter) Developer Account** with API access
   - Basic tier required (Free tier cannot post tweets)
   - App permissions: Read and Write

## Installation

### 1. Install Ollama

```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model (e.g., llama2)
ollama pull llama2

# Start Ollama server
ollama serve
```

### 2. Clone/Setup Project

```bash
cd /home/taliban/nietzsche_bot
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Get X API Credentials

1. Go to https://developer.x.com/
2. Create a new project and app
3. Set app permissions to "Read and Write"
4. Generate API keys and access tokens
5. Save your credentials:
   - API Key (Consumer Key)
   - API Secret (Consumer Secret)
   - Access Token
   - Access Token Secret

**Important:** If you change permissions after creating tokens, regenerate them.

### 5. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

Update the following in `.env`:
```bash
X_API_KEY=your_api_key_here
X_API_SECRET=your_api_secret_here
X_ACCESS_TOKEN=your_access_token_here
X_ACCESS_SECRET=your_access_token_secret_here
PDF_PATH=./nietzsche.pdf
```

### 6. Load Environment Variables

```bash
# Export environment variables
export $(cat .env | xargs)
```

## Usage

### Test the Bot

```bash
python bot.py
```

The bot will:
1. Test all components (PDF, Ollama, X API)
2. Post an initial quote (if `POST_ON_STARTUP=true`)
3. Schedule posts every 2 hours

### Run as a Service (Systemd)

Create a systemd service for automatic startup and management:

```bash
sudo nano /etc/systemd/system/nietzsche-bot.service
```

Add the following:

```ini
[Unit]
Description=Nietzsche Quote Bot for X
After=network.target

[Service]
Type=simple
User=taliban
WorkingDirectory=/home/taliban/nietzsche_bot
Environment="PDF_PATH=/home/taliban/nietzsche_bot/nietzsche.pdf"
Environment="X_API_KEY=your_api_key"
Environment="X_API_SECRET=your_api_secret"
Environment="X_ACCESS_TOKEN=your_access_token"
Environment="X_ACCESS_SECRET=your_access_secret"
Environment="OLLAMA_URL=http://localhost:11434"
Environment="OLLAMA_MODEL=llama2"
Environment="POST_INTERVAL_HOURS=2"
Environment="POST_ON_STARTUP=false"
ExecStart=/usr/bin/python3 /home/taliban/nietzsche_bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable nietzsche-bot.service
sudo systemctl start nietzsche-bot.service
```

Check status:

```bash
sudo systemctl status nietzsche-bot.service
```

View logs:

```bash
sudo journalctl -u nietzsche-bot.service -f
```

## Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `PDF_PATH` | Path to the Nietzsche PDF | Required |
| `X_API_KEY` | X API consumer key | Required |
| `X_API_SECRET` | X API consumer secret | Required |
| `X_ACCESS_TOKEN` | X access token | Required |
| `X_ACCESS_SECRET` | X access token secret | Required |
| `OLLAMA_URL` | Ollama server URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | Ollama model name | `llama2` |
| `POST_INTERVAL_HOURS` | Hours between posts | `2` |
| `POST_ON_STARTUP` | Post immediately on startup | `false` |
| `LOG_DIR` | Directory for log files | `logs` |

## Project Structure

```
nietzsche_bot/
├── bot.py                  # Main application with scheduling
├── pdf_extractor.py        # PDF text extraction utility
├── ollama_processor.py     # Ollama integration
├── x_poster.py            # X API v2 posting functionality
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment configuration
├── README.md             # This file
└── logs/                 # Log files (created automatically)
```

## How It Works

1. **PDF Extraction**: Loads "Beyond Good and Evil" and extracts sentences (20-280 characters)
2. **Random Selection**: Picks a random sentence from the extracted collection
3. **AI Rephrasing**: Sends the sentence to Ollama with a prompt to rephrase it in a modern, engaging way
4. **Posting**: Posts the rephrased quote to X using API v2
5. **Scheduling**: Repeats every 2 hours (configurable)

## Logging

Logs are stored in the `logs/` directory with daily rotation:
- Format: `nietzsche_bot_YYYYMMDD.log`
- Contains: Timestamps, log levels, component names, and messages
- Also outputs to console for real-time monitoring

## Troubleshooting

### Ollama Connection Error
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve
```

### X API Authentication Error
- Verify your API credentials are correct
- Ensure app has "Read and Write" permissions
- Regenerate tokens after changing permissions
- Check you have Basic tier or higher (Free tier cannot post)

### PDF Not Found
- Verify the PDF path in `.env` is correct
- Use absolute path to the PDF file

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Remote Server Deployment

### Using SSH and Screen/Tmux

```bash
# SSH to your remote server
ssh user@your-server.com

# Install dependencies
cd /home/taliban/nietzsche_bot
pip install -r requirements.txt

# Start in screen session
screen -S nietzsche-bot
export $(cat .env | xargs)
python bot.py

# Detach: Ctrl+A then D
# Reattach: screen -r nietzsche-bot
```

### Using Docker (Optional)

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

Build and run:

```bash
docker build -t nietzsche-bot .
docker run -d --name nietzsche-bot --env-file .env nietzsche-bot
```

## License

This project is for educational purposes. Ensure you comply with:
- X API Terms of Service
- Nietzsche's work copyright status in your jurisdiction
- Ollama's usage terms

## Support

For issues or questions:
- Check logs in `logs/` directory
- Verify all environment variables are set
- Test each component individually using `test_components()`
