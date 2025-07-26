# Environment Variables Setup Guide

To enable real AI features in your Zyndle AI application, you need to set up the following environment variables in Railway:

## Required Environment Variables

### 1. OpenAI API Key (Required for AI features)
- **Variable Name**: `OPENAI_API_KEY`
- **How to get it**: 
  1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
  2. Sign up or log in
  3. Click "Create new secret key"
  4. Copy the key (starts with `sk-`)

### 2. YouTube Data API Key (Optional, for better video metadata)
- **Variable Name**: `YOUTUBE_API_KEY`
- **How to get it**:
  1. Go to [Google Cloud Console](https://console.cloud.google.com/)
  2. Create a new project or select existing
  3. Enable YouTube Data API v3
  4. Create credentials (API Key)
  5. Copy the key

## Setting Environment Variables in Railway

1. Go to your Railway project dashboard
2. Click on your service
3. Go to the "Variables" tab
4. Add each variable:
   - Key: `OPENAI_API_KEY`
   - Value: `sk-your-openai-key-here`
5. Click "Add"
6. Repeat for `YOUTUBE_API_KEY` if desired

## Cost Estimates

### OpenAI API Usage (per video analysis):
- **Summary Generation**: ~$0.01-0.03
- **Chat Response**: ~$0.005-0.02 per question
- **Quiz Generation**: ~$0.01-0.03
- **Total per video**: ~$0.02-0.08

### YouTube API Usage:
- **Free tier**: 10,000 requests/day
- **Cost**: Free for most use cases

## Testing

After setting the environment variables:
1. Redeploy your application
2. Try analyzing a YouTube video
3. Check the logs to see if real data is being fetched
4. Test chat and quiz features

## Troubleshooting

- If you see "Using fallback metadata" in logs, YouTube API key is missing
- If you see "Using mock summary" in logs, OpenAI API key is missing
- Check Railway logs for any API errors 