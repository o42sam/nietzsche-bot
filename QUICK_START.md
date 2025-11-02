# Quick Start Guide - Nietzsche Bot with Groq API

This bot posts Nietzsche quotes to X (Twitter) using Groq API for rephrasing.

## Prerequisites

1. **Groq API Key** - Get from https://console.groq.com/
2. **X (Twitter) API Credentials** - Get from https://developer.x.com/
3. **Nietzsche PDF** - "Beyond Good and Evil" PDF file

## Local Testing

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure Environment

Edit `.env` file:

```bash
# X (Twitter) API Credentials
X_API_KEY=your_x_api_key
X_API_SECRET=your_x_api_secret
X_ACCESS_TOKEN=your_access_token
X_ACCESS_SECRET=your_access_token_secret

# PDF Configuration
PDF_PATH=./nietzsche.pdf

# Groq API Configuration (FREE!)
GROQ_API_KEY=gsk_your_groq_api_key_here

# Bot Configuration
POST_INTERVAL_HOURS=2
POST_ON_STARTUP=false
LOG_DIR=logs
```

### 3. Test Components

```bash
# Load environment variables
set -a && source .env && set +a

# Test Groq API only
python test_groq.py

# Test full workflow (posts to X)
python test_single_post.py
```

### 4. Run the Bot

```bash
# Start the bot
python bot.py
```

## Deploy to Render (Production)

### Option 1: Using GitHub (Recommended)

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/nietzsche-bot.git
   git push -u origin main
   ```

2. **Deploy on Render**:
   - Go to https://dashboard.render.com/
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Render auto-detects `render.yaml`
   - Add environment variables in dashboard
   - Click "Create Web Service"

3. **Add Environment Variables in Render**:
   - `GROQ_API_KEY`
   - `X_API_KEY`
   - `X_API_SECRET`
   - `X_ACCESS_TOKEN`
   - `X_ACCESS_SECRET`
   - `PDF_PATH` (use `./nietzsche.pdf` - relative to project root)

### Option 2: Manual Deploy

See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for detailed instructions.

## Getting API Keys

### Groq API Key (FREE!)

1. Visit https://console.groq.com/
2. Sign up / Log in (No credit card required!)
3. Go to "API Keys"
4. Click "Create API Key"
5. Copy key (starts with `gsk_`)
6. Save securely - you won't see it again!

**Note**: Groq offers a generous FREE tier - perfect for this bot!

### X (Twitter) API

1. Visit https://developer.x.com/
2. Create a project and app
3. Set permissions to "Read and Write"
4. Generate API keys and access tokens
5. Save all credentials

**Important**: Free tier may have limitations. Check X API pricing.

## Project Files

```
nietzsche_bot/
├── bot.py                      # Main bot
├── groq_processor.py          # Groq API integration (NEW)
├── pdf_extractor.py           # PDF extraction
├── x_poster.py               # X/Twitter posting
├── test_groq.py              # Test Groq API (NEW)
├── test_single_post.py       # Test full workflow
├── requirements.txt          # Python dependencies
├── .env                      # Configuration (local)
├── render.yaml              # Render config (NEW)
├── RENDER_DEPLOYMENT.md     # Deployment guide (NEW)
└── nietzsche.pdf            # Source material
```

## Troubleshooting

### Groq API Errors

**401 Unauthorized**:
- Check API key is correct
- Verify key is active at https://console.groq.com/

**429 Too Many Requests**:
- Rate limit exceeded
- Wait and retry
- Check your API quota

**Invalid Model**:
- Check model name in groq_processor.py
- Check Grok service status

### X API Errors

**403 Forbidden**:
- App permissions not set to "Read and Write"
- Regenerate tokens after changing permissions

**Duplicate Tweet**:
- X doesn't allow identical tweets
- This is normal if testing repeatedly

### PDF Errors

**File not found**:
- Check PDF_PATH is correct
- Use absolute path
- Ensure file exists

## Monitoring

### Check Logs on Render

1. Go to your service dashboard
2. Click "Logs" tab
3. Monitor real-time output

### Health Check

The bot logs:
- PDF loading status
- API connection status
- Each post attempt
- Errors with stack traces

## Cost Estimation

### Groq API
- **FREE tier** - No cost for our usage!
- Monitor usage at https://console.groq.com/

### Render Hosting
- **Free Tier**: 750 hours/month (enough for continuous running)
- **Paid Tier**: $7/month (no limitations)

### X API
- Basic tier required for posting
- Check pricing at https://developer.x.com/

## Support

- **Groq API Docs**: https://console.groq.com/docs/
- **Render Docs**: https://render.com/docs
- **X API Docs**: https://developer.x.com/en/docs

## Security Checklist

- [ ] Never commit `.env` to GitHub
- [ ] Add `.env` to `.gitignore`
- [ ] Use environment variables in Render
- [ ] Keep API keys secret
- [ ] Enable 2FA on all accounts
- [ ] Monitor API usage regularly

## Next Steps

1. Test locally with `test_groq.py`
2. Verify with `test_single_post.py`
3. Run locally with `python bot.py`
4. Deploy to Render
5. Monitor logs and posts
6. Adjust posting interval as needed

---

**Note**: This bot uses Groq API instead of local Ollama, making it perfect for cloud deployment!
