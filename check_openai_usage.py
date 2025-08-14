#!/usr/bin/env python3
"""
OpenAI API Usage Checker
Check your current usage and quota limits
"""

import os
import requests
from datetime import datetime, timedelta
from openai import OpenAI

def check_openai_usage():
    """Check OpenAI API usage and quota"""
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        return
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Get usage information
        print("🔍 Checking OpenAI API usage...")
        
        # Note: OpenAI doesn't provide a direct usage API endpoint
        # You'll need to check your OpenAI dashboard
        
        print("\n📊 To check your usage:")
        print("1. Go to https://platform.openai.com/usage")
        print("2. Log in with your OpenAI account")
        print("3. Check your current usage and limits")
        
        # Test API call to see if it works
        print("\n🧪 Testing API connection...")
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            print("✅ API connection successful!")
            print(f"Model used: {response.model}")
            print(f"Tokens used: {response.usage.total_tokens}")
            
        except Exception as e:
            if "quota" in str(e).lower() or "429" in str(e):
                print("❌ API quota exceeded!")
            else:
                print(f"⚠️ API test failed: {e}")
                
    except Exception as e:
        print(f"❌ Error checking usage: {e}")

def get_cost_estimates():
    """Show cost estimates for different usage levels"""
    print("\n💰 OpenAI GPT-3.5-turbo Cost Estimates:")
    print("┌─────────────────┬─────────────┬─────────────┐")
    print("│ Usage Level     │ Input Tokens│ Cost/Month  │")
    print("├─────────────────┼─────────────┼─────────────┤")
    print("│ Light Usage     │ 10,000      │ ~$0.02     │")
    print("│ Moderate Usage  │ 100,000     │ ~$0.20     │")
    print("│ Heavy Usage     │ 1,000,000   │ ~$2.00     │")
    print("│ Very Heavy      │ 10,000,000  │ ~$20.00    │")
    print("└─────────────────┴─────────────┴─────────────┘")
    
    print("\n📝 Cost per request (approximate):")
    print("• Video summary: ~500-1000 tokens = $0.001-0.002")
    print("• Chat response: ~200-500 tokens = $0.0004-0.001")
    print("• Quiz generation: ~800-1500 tokens = $0.0016-0.003")

def quota_management_tips():
    """Provide tips for managing API quota"""
    print("\n🎯 Quota Management Tips:")
    print("1. **Set Usage Limits**:")
    print("   - Go to OpenAI dashboard → Billing → Usage limits")
    print("   - Set daily/monthly spending limits")
    
    print("\n2. **Monitor Usage**:")
    print("   - Check usage dashboard regularly")
    print("   - Set up usage alerts")
    
    print("\n3. **Optimize Requests**:")
    print("   - Use shorter prompts")
    print("   - Limit max_tokens in requests")
    print("   - Cache responses when possible")
    
    print("\n4. **Alternative Strategies**:")
    print("   - Use enhanced mock responses for development")
    print("   - Implement request throttling")
    print("   - Use different models (GPT-3.5-turbo is cheaper than GPT-4)")

if __name__ == "__main__":
    print("🚀 OpenAI API Usage Checker")
    print("=" * 40)
    
    check_openai_usage()
    get_cost_estimates()
    quota_management_tips()
    
    print("\n🔧 To set up usage limits:")
    print("1. Visit: https://platform.openai.com/account/billing/overview")
    print("2. Click 'Set limits'")
    print("3. Set daily/monthly spending limits")
    print("4. Enable usage alerts") 