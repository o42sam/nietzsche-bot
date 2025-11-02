# Grok API Setup Guide

## Current Status

Your Grok API key is valid, but **your account needs credits** to make API calls.

### Error Message
```
Your newly created team doesn't have any credits yet.
You can purchase credits on https://console.x.ai/team/7d39c085-9452-489c-817b-cb0962e335f5
```

## Steps to Add Credits

1. **Visit Your Team Page**:
   https://console.x.ai/team/7d39c085-9452-489c-817b-cb0962e335f5

2. **Add Payment Method**:
   - Click on "Billing" or "Credits"
   - Add a payment method
   - Purchase credits

3. **Credit Pricing** (check current pricing at https://x.ai/api):
   - Pay-as-you-go model
   - Typically charged per token
   - Estimated cost for this bot: ~$1-5/month (depending on usage)

## Alternative Options

### Option 1: Use OpenAI API Instead

OpenAI has a well-established API with potential free credits for new users:

1. Get API key from https://platform.openai.com/
2. Update `.env`:
   ```bash
   OPENAI_API_KEY=sk-your_key_here
   USE_OPENAI=true
   ```
3. I can create an OpenAI processor similar to Grok

### Option 2: Use Free Alternatives

**Groq** (not Grok!) - Free tier available:
- Visit: https://console.groq.com/
- Get free API key
- Fast inference with free tier

**Hugging Face Inference API**:
- Visit: https://huggingface.co/
- Free tier available
- Multiple models to choose from

### Option 3: Testing Mode

For development/testing without API costs, I can create a mock mode that:
- Generates simple rephrased versions locally
- Uses basic text transformation
- No AI API calls needed

## Recommendation

**For immediate testing**: Use Option 3 (mock mode) - see below

**For production**: Add Grok credits (Option 1 is most straightforward)

## Quick Test with Mock Mode

Would you like me to create a simple mock processor that works without any API calls? This would let you:
- Test the full workflow
- Verify X posting works
- Deploy to Render
- Replace with real AI later

Just let me know which option you prefer!

## Cost Comparison

| Service | Free Tier | Paid Pricing | Quality |
|---------|-----------|--------------|---------|
| **Grok** | No | ~$0.50-5/1M tokens | Excellent (Grok-2) |
| **OpenAI** | $5 credit (new users) | ~$0.50-15/1M tokens | Excellent (GPT-4) |
| **Groq** | Yes (limited) | Pay as you go | Good (Fast) |
| **Hugging Face** | Yes | Pay as you go | Varies by model |
| **Mock Mode** | Free | Free | Basic |

## Next Steps

Choose one of:
1. Add credits to Grok ✅ (Recommended for production)
2. Switch to OpenAI
3. Switch to Groq (free tier)
4. Use mock mode for testing

Let me know which you prefer and I'll help you set it up!
