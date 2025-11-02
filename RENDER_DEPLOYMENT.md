# Deploying to Render

This guide will help you deploy the Nietzsche Bot to Render.com.

## Prerequisites

1. **Render Account**: Sign up at https://render.com (free tier available)
2. **GitHub Account**: Your code should be in a GitHub repository
3. **API Keys**:
   - X (Twitter) API credentials only
   - NO API key needed for the AI model - we use Hugging Face's free inference API!

## Step-by-Step Deployment

### 1. Prepare Your Repository

Make sure your repository includes:
- All Python files
- `requirements.txt`
- `render.yaml` (configuration file)
- `nietzsche.pdf` (Nietzsche's book)
- `.gitignore` (DO NOT commit `.env` file)

```bash
# Add all files to git
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Create a New Web Service on Render

1. Go to https://dashboard.render.com/
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Render will auto-detect the `render.yaml` file

### 3. Configure Environment Variables

In the Render dashboard, go to **Environment** tab and add:

| Variable | Value | Description |
|----------|-------|-------------|
| `X_API_KEY` | `your_key` | X/Twitter API consumer key |
| `X_API_SECRET` | `your_secret` | X/Twitter API consumer secret |
| `X_ACCESS_TOKEN` | `your_token` | X/Twitter access token |
| `X_ACCESS_SECRET` | `your_secret` | X/Twitter access token secret |
| `PDF_PATH` | `./nietzsche.pdf` | Path to PDF (relative to project root) |
| `HF_MODEL` | `mistralai/Mistral-7B-Instruct-v0.2` | Hugging Face model (optional, this is the default) |
| `POST_INTERVAL_HOURS` | `2` | Hours between posts |
| `POST_ON_STARTUP` | `false` | Post immediately on startup |

**Note**: No API key needed for the AI model! We use Hugging Face's completely free serverless inference API.

### 4. Deploy

1. Click **"Create Web Service"**
2. Render will:
   - Build your application
   - Install dependencies
   - Start the bot
3. Monitor the deployment logs

### 5. Verify Deployment

Check the logs to ensure:
- PDF loaded successfully
- Hugging Face API connected (may take 10-20 seconds on first call as model loads)
- X API authenticated
- Bot started posting

## Important Notes for Render

### Free Tier Limitations

Render's free tier has some limitations:
- **Spins down after 15 minutes of inactivity**
- **750 hours/month free** (enough for continuous running)
- To keep it alive, consider:
  - Upgrading to paid plan ($7/month)
  - Using a service like UptimeRobot to ping it every 14 minutes

### Keep Service Alive

Add this to your `bot.py` if needed (optional):

```python
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Nietzsche Bot is running!"

@app.route('/health')
def health():
    return {"status": "healthy", "bot_running": bot.running}

# Run Flask in background
def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

threading.Thread(target=run_flask, daemon=True).start()
```

However, for background workers, it's better to use **Background Worker** service type instead of **Web Service**.

### Alternative: Deploy as Background Worker

If you don't need a web interface:

1. Change `render.yaml`:
```yaml
services:
  - type: worker
    name: nietzsche-bot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python bot.py
```

2. This runs continuously without needing HTTP requests
3. No spin-down on free tier for workers

## Troubleshooting

### PDF Not Found

Ensure `nietzsche.pdf` is:
- In your repository
- Path is correct in environment variables

### API Connection Errors

- Verify X API credentials are correct
- Verify X API permissions are "Read and Write"
- If Hugging Face API is slow, the model may be loading (wait 20-30 seconds)
- Try a different free Hugging Face model if one isn't working

### Bot Not Posting

Check logs for:
- Successful initialization
- Schedule running
- API call success/failure

### Logs

View logs in Render dashboard:
- Go to your service
- Click **"Logs"** tab
- Monitor real-time output

## Managing Your Deployment

### View Logs
```bash
# Install Render CLI
npm install -g render

# Login
render login

# View logs
render logs -f
```

### Restart Service
In Render dashboard:
1. Go to your service
2. Click **"Manual Deploy"** → **"Clear build cache & deploy"**

### Update Environment Variables
1. Go to **Environment** tab
2. Edit variables
3. Service auto-restarts

### Stop the Bot
1. Go to **Settings** tab
2. Click **"Suspend Service"**

## Cost Optimization

### Free Tier Strategy
- Use **Background Worker** type (no spin-down)
- 750 hours/month = 31.25 days continuous running
- Perfect for this bot!

### Paid Tier ($7/month)
- No limitations
- Guaranteed uptime
- Better for production

## Alternative: Deploy to Other Platforms

If Render doesn't work well, consider:

1. **Railway.app** - $5/month, similar to Render
2. **Fly.io** - Free tier with 3 shared VMs
3. **Heroku** - No free tier anymore
4. **PythonAnywhere** - Free tier available
5. **DigitalOcean App Platform** - $5/month

## About Hugging Face Free API

The bot uses Hugging Face's free serverless inference API, which means:
- **No sign-up required** for basic models
- **No API key needed**
- **100% Free** with no credit card
- Models may take 10-20 seconds to load on first request (cold start)
- After first load, responses are fast

Available free models:
1. `mistralai/Mistral-7B-Instruct-v0.2` (default - best balance)
2. `mistralai/Mixtral-8x7B-Instruct-v0.1` (larger, better quality, slower)
3. `HuggingFaceH4/zephyr-7b-beta` (alternative)

You can change the model anytime by updating the `HF_MODEL` environment variable!

## Security Best Practices

1. **Never commit API keys** to GitHub
2. **Use environment variables** for all secrets
3. **Enable 2FA** on Render and GitHub
4. **Rotate API keys** regularly
5. **Monitor usage** on X dashboard

## Support

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com/
- **Hugging Face Inference API Docs**: https://huggingface.co/docs/api-inference/

## Quick Deploy Checklist

- [ ] Code pushed to GitHub
- [ ] `nietzsche.pdf` in repository
- [ ] Render account created
- [ ] Repository connected to Render
- [ ] Environment variables configured
- [ ] Service deployed
- [ ] Logs checked for errors
- [ ] First tweet posted successfully
