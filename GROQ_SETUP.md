# Groq API Setup Guide (FREE!)

## Why Groq?

✅ **FREE tier available** - No credit card required to start!
✅ **Fast inference** - One of the fastest LLM APIs
✅ **Good models** - Access to Llama 3.3 70B and other models
✅ **Simple setup** - Just get an API key and go

## Getting Your FREE API Key

### Step 1: Sign Up

1. Visit https://console.groq.com/
2. Click "Sign Up" or "Get Started"
3. Create account (can use Google/GitHub)
4. **No credit card required!**

### Step 2: Create API Key

1. Once logged in, go to "API Keys" section
2. Click "Create API Key"
3. Give it a name (e.g., "nietzsche-bot")
4. Copy the API key (starts with `gsk_`)
5. **Save it securely** - you won't see it again!

### Step 3: Add to .env

Edit your `.env` file:

```bash
# Groq API Configuration (FREE tier available!)
# Get your API key from https://console.groq.com/
GROQ_API_KEY=gsk_your_actual_key_here
```

## Test the Integration

### Test Groq API Only

```bash
# Load environment
set -a && source .env && set +a

# Test Groq
python test_groq.py
```

### Test Full Workflow

```bash
# This will post to X (Twitter)
python test_single_post.py
```

## Free Tier Limits

Groq's free tier is generous:
- **30 requests per minute**
- **Unlimited total requests** (subject to fair use)
- Access to multiple models

For our bot posting every 2 hours:
- ~12 posts/day = 360 posts/month
- **Well within free tier limits!**

## Available Models

The bot uses `llama-3.3-70b-versatile` by default. Other options:

| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| `llama-3.3-70b-versatile` | 70B | Fast | Excellent ✅ |
| `llama-3.1-70b-versatile` | 70B | Fast | Excellent |
| `mixtral-8x7b-32768` | 47B | Very Fast | Good |
| `gemma2-9b-it` | 9B | Ultra Fast | Good |

## Troubleshooting

### Invalid API Key
```
Error: 401 Unauthorized
```
**Solution**: Double-check your API key in `.env`

### Rate Limit
```
Error: 429 Too Many Requests
```
**Solution**: Wait a minute and retry. For our bot, this shouldn't happen.

### Model Not Found
```
Error: Model not available
```
**Solution**: Check if model name is correct in `groq_processor.py`

## Cost Comparison

| Service | Free Tier | Our Bot Cost |
|---------|-----------|--------------|
| **Groq** | ✅ Yes | **$0/month** |
| Grok (xAI) | ❌ No | ~$2-5/month |
| OpenAI | $5 credit | ~$1-3/month |
| Anthropic | ❌ No | ~$5-10/month |

## Next Steps

1. ✅ Get API key from https://console.groq.com/
2. ✅ Add to `.env` file
3. ✅ Test with `python test_groq.py`
4. ✅ Test full workflow with `python test_single_post.py`
5. ✅ Deploy to Render!

## Deployment to Render

When deploying, add `GROQ_API_KEY` as an environment variable in Render:

1. Go to Render dashboard
2. Select your service
3. Go to "Environment" tab
4. Add: `GROQ_API_KEY` = `gsk_your_key_here`
5. Deploy!

## Support

- **Groq Docs**: https://console.groq.com/docs
- **Groq Community**: https://groq.com/
- **Discord**: Check Groq website for community link

## Why We Switched from Grok

Grok required credits/payment, while Groq offers:
- Free tier (no credit card needed)
- Fast inference
- Good quality models
- Perfect for our use case!

---

**Ready to go?** Get your free API key now: https://console.groq.com/
