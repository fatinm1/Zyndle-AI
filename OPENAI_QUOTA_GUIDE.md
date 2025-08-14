# 🚀 OpenAI API Quota Management Guide

## **💰 Understanding OpenAI Pricing**

### **GPT-3.5-turbo (Recommended for Zyndle AI)**
- **Input tokens**: $0.0015 per 1K tokens
- **Output tokens**: $0.002 per 1K tokens
- **Cost per video analysis**: ~$0.002-0.005
- **Cost per chat response**: ~$0.0005-0.001
- **Cost per quiz**: ~$0.002-0.004

### **GPT-4 (More Expensive)**
- **Input tokens**: $0.03 per 1K tokens
- **Output tokens**: $0.06 per 1K tokens
- **Cost per video analysis**: ~$0.05-0.10
- **Cost per chat response**: ~$0.01-0.02
- **Cost per quiz**: ~$0.02-0.04

## **🎯 How to Prevent Quota Exceeded Errors**

### **1. Set Up Usage Limits**

**Step 1: Visit OpenAI Dashboard**
```
https://platform.openai.com/account/billing/overview
```

**Step 2: Set Spending Limits**
- Click "Set limits"
- Set daily spending limit (recommended: $5-10)
- Set monthly spending limit (recommended: $50-100)
- Enable usage alerts

**Step 3: Monitor Usage**
- Check usage dashboard regularly
- Set up email alerts for 80% and 100% usage

### **2. Optimize Your Application**

**Reduce Token Usage:**
```python
# In backend/services/ai_service.py
# Limit transcript length
transcript = transcript[:1500]  # Limit to 1500 chars

# Limit summary length  
summary = summary[:500]  # Limit to 500 chars

# Use shorter prompts
prompt = f"Summarize this video: {transcript[:1000]}"
```

**Implement Caching:**
```python
# Cache responses to avoid duplicate API calls
import hashlib
import json

def get_cache_key(video_id, request_type):
    return hashlib.md5(f"{video_id}_{request_type}".encode()).hexdigest()

# Check cache before making API call
cache_key = get_cache_key(video_id, "summary")
if cache_key in cache:
    return cache[cache_key]
```

### **3. Use Request Throttling**

**Add Rate Limiting:**
```python
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests=10, time_window=60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = defaultdict(list)
    
    def can_make_request(self, user_id):
        now = time.time()
        user_requests = self.requests[user_id]
        
        # Remove old requests
        user_requests = [req for req in user_requests if now - req < self.time_window]
        self.requests[user_id] = user_requests
        
        if len(user_requests) < self.max_requests:
            user_requests.append(now)
            return True
        return False
```

### **4. Implement Fallback Strategies**

**Graceful Degradation:**
```python
def generate_summary(self, transcript: str, title: str) -> Dict:
    try:
        # Try real AI first
        return self._call_openai_api(transcript, title)
    except Exception as e:
        if "quota" in str(e) or "429" in str(e):
            # Use enhanced mock as fallback
            return self._get_enhanced_mock_summary(title, transcript)
        else:
            # Use basic mock for other errors
            return self._get_mock_summary(title)
```

## **📊 Usage Monitoring**

### **Check Current Usage**
```bash
# Run the usage checker
python check_openai_usage.py
```

### **Set Up Alerts**
1. Go to OpenAI dashboard
2. Navigate to Billing → Usage limits
3. Set up email alerts for:
   - 50% of daily limit
   - 80% of daily limit
   - 100% of daily limit

### **Track Usage in Your App**
```python
# Add usage tracking to your AI service
class AIService:
    def __init__(self):
        self.total_tokens_used = 0
        self.total_cost = 0
    
    def track_usage(self, response):
        if hasattr(response, 'usage'):
            self.total_tokens_used += response.usage.total_tokens
            # Calculate cost (approximate)
            input_cost = response.usage.prompt_tokens * 0.0015 / 1000
            output_cost = response.usage.completion_tokens * 0.002 / 1000
            self.total_cost += input_cost + output_cost
```

## **💡 Cost Optimization Strategies**

### **1. Use GPT-3.5-turbo Instead of GPT-4**
- **GPT-3.5-turbo**: $0.002 per 1K tokens
- **GPT-4**: $0.06 per 1K tokens (30x more expensive!)

### **2. Limit Response Length**
```python
# In your API calls
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    max_tokens=500,  # Limit response length
    temperature=0.7
)
```

### **3. Use Shorter Prompts**
```python
# Instead of sending full transcript
prompt = f"Summarize this video in 3 key points: {transcript[:1000]}"

# Instead of long explanations
prompt = "Generate 5 quiz questions about this video content."
```

### **4. Implement Caching**
```python
# Cache video summaries
def get_video_summary(video_id, transcript):
    cache_key = f"summary_{video_id}"
    if cache_key in cache:
        return cache[cache_key]
    
    # Generate new summary
    summary = ai_service.generate_summary(transcript)
    cache[cache_key] = summary
    return summary
```

## **🚨 Emergency Quota Management**

### **If You Hit Quota Limits:**

1. **Immediate Actions:**
   - Check usage dashboard
   - Set lower spending limits
   - Enable enhanced mock responses

2. **Short-term Solutions:**
   - Use cached responses
   - Implement request throttling
   - Switch to cheaper models

3. **Long-term Solutions:**
   - Upgrade to paid plan
   - Implement better caching
   - Optimize prompts and responses

## **🔧 Railway Environment Variables**

### **Set Up in Railway Dashboard:**
```
OPENAI_API_KEY=your_api_key_here
OPENAI_USAGE_LIMIT=5  # Daily spending limit in USD
OPENAI_MODEL=gpt-3.5-turbo  # Use cheaper model
```

### **Monitor Usage in Railway:**
```bash
# Check logs for API usage
railway logs

# Look for quota exceeded errors
grep "quota" railway logs
```

## **📈 Usage Estimates for Zyndle AI**

### **Per Video Analysis:**
- **Summary generation**: ~500-1000 tokens = $0.001-0.002
- **Quiz generation**: ~800-1500 tokens = $0.002-0.004
- **Chat responses**: ~200-500 tokens = $0.0005-0.001

### **Monthly Usage Scenarios:**
- **Light usage (10 videos/day)**: ~$5-10/month
- **Moderate usage (50 videos/day)**: ~$25-50/month
- **Heavy usage (100 videos/day)**: ~$50-100/month

## **🎯 Best Practices**

1. **Start Small**: Begin with low spending limits
2. **Monitor Regularly**: Check usage dashboard daily
3. **Use Caching**: Avoid duplicate API calls
4. **Implement Fallbacks**: Always have mock responses ready
5. **Optimize Prompts**: Keep them concise and focused
6. **Use Cheaper Models**: GPT-3.5-turbo is sufficient for most use cases

## **🔗 Useful Links**

- **OpenAI Usage Dashboard**: https://platform.openai.com/usage
- **Billing Overview**: https://platform.openai.com/account/billing/overview
- **API Documentation**: https://platform.openai.com/docs/api-reference
- **Pricing Page**: https://openai.com/pricing

---

**💡 Pro Tip**: Start with a $5 daily limit and gradually increase based on your usage patterns. This prevents unexpected charges while allowing your app to function normally! 