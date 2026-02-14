# API Keys Documentation

This document lists all API keys required to run the Tier 1 Support Chatbot application.

## Required API Keys

### 1. OpenAI API Key
- **Environment Variable**: `OPENAI_API_KEY`
- **Purpose**: Powers the AI-driven chatbot responses using GPT-3.5-turbo model
- **Required**: Yes
- **How to Obtain**:
  1. Sign up for an OpenAI account at https://platform.openai.com/
  2. Navigate to API Keys section in your account settings
  3. Click "Create new secret key"
  4. Copy and securely store the key (it won't be shown again)
- **Documentation**: https://platform.openai.com/docs/api-reference/authentication
- **Cost**: Pay-per-use (see https://openai.com/pricing)
- **Usage in App**: Used by `get_ai_response()` function to handle unknown queries and provide intelligent responses

### 2. Syncro MSP API Key
- **Environment Variable**: `SYNCRO_API_KEY`
- **Purpose**: Enables ticket creation and escalation to Tier 2 support through Syncro MSP platform
- **Required**: Yes
- **How to Obtain**:
  1. Log in to your Syncro MSP account
  2. Navigate to Admin → API Tokens
  3. Click "New API Token"
  4. Set appropriate permissions (Tickets: Read/Write)
  5. Copy the generated API token
- **Documentation**: https://syncromsp.com/developer-api/
- **Cost**: Requires active Syncro MSP subscription
- **Usage in App**: Used by `create_syncro_ticket()` function to create support tickets when issues need escalation

### 3. Syncro MSP Subdomain
- **Environment Variable**: `SYNCRO_SUBDOMAIN`
- **Purpose**: Identifies your specific Syncro MSP instance
- **Required**: Yes (when using Syncro MSP integration)
- **How to Obtain**: This is your company's Syncro subdomain (e.g., if your Syncro URL is `yourcompany.syncromsp.com`, use `yourcompany`)
- **Usage in App**: Used to construct the Syncro API endpoint URL

## Optional API Keys

### 4. SerpAPI Key
- **Environment Variable**: `SERP_API_KEY`
- **Purpose**: Enables external web search capabilities for queries not covered by knowledge base or AI
- **Required**: No (optional feature)
- **How to Obtain**:
  1. Sign up for a SerpAPI account at https://serpapi.com/
  2. Navigate to your dashboard
  3. Copy your API key from the dashboard
- **Documentation**: https://serpapi.com/docs
- **Cost**: Free tier available (100 searches/month), paid plans for more usage
- **Usage in App**: Used by `search_external_info()` function to provide additional information from web searches
- **Fallback**: If not configured, search functionality will return "No search API key configured"

## Development/Optional Variables

### 5. Flask Debug Mode
- **Environment Variable**: `FLASK_DEBUG`
- **Purpose**: Enables Flask development/debug mode with auto-reload and detailed error messages
- **Required**: No
- **Values**: `"true"` or `"false"` (default: `"false"`)
- **Security Note**: Should NEVER be enabled in production environments
- **Usage in App**: Controls Flask application debug mode

## Setup Instructions

### Quick Setup
1. Copy `.env.example` to `.env`
2. Fill in your API keys in the `.env` file
3. Load environment variables: `source .env` (Unix/Mac) or use your preferred method

### Manual Setup
```bash
# Required
export OPENAI_API_KEY="sk-..."
export SYNCRO_SUBDOMAIN="yourcompany"
export SYNCRO_API_KEY="your-syncro-api-key"

# Optional
export SERP_API_KEY="your-serpapi-key"
export FLASK_DEBUG="false"
```

## Security Best Practices

1. **Never commit API keys to version control**
   - The `.gitignore` file is configured to exclude `.env` files
   - Always use environment variables or secure secret management

2. **Rotate keys regularly**
   - Change API keys periodically
   - Immediately rotate if a key is accidentally exposed

3. **Use minimal permissions**
   - Grant API keys only the permissions they need
   - For Syncro MSP, limit to ticket creation/reading

4. **Secure storage**
   - Store API keys in a password manager
   - Use secret management services in production (AWS Secrets Manager, Azure Key Vault, etc.)

5. **Monitor usage**
   - Regularly check API usage dashboards
   - Set up alerts for unusual activity or rate limit approaches

## Testing Without API Keys

For testing purposes, you can:
- Use mocked API responses (see `tests/test_chatbot.py` for examples)
- Run unit tests without actual API keys using the test suite
- The application will gracefully handle missing API keys with appropriate error messages

## Troubleshooting

### "AI service not configured" error
- Ensure `OPENAI_API_KEY` is set correctly
- Verify the key is valid and not expired
- Check your OpenAI account has available credits

### "Syncro MSP not configured" error
- Verify both `SYNCRO_SUBDOMAIN` and `SYNCRO_API_KEY` are set
- Check the subdomain is correct (without `.syncromsp.com`)
- Ensure API token has proper permissions

### "No search API key configured" message
- This is expected if `SERP_API_KEY` is not set (optional feature)
- Set the key if you want external search functionality

## API Key Checklist

Before deploying, ensure:
- [ ] `OPENAI_API_KEY` is set and valid
- [ ] `SYNCRO_SUBDOMAIN` is set correctly
- [ ] `SYNCRO_API_KEY` is set and has ticket permissions
- [ ] `SERP_API_KEY` is set (if using search feature)
- [ ] `FLASK_DEBUG` is set to `"false"` in production
- [ ] All keys are stored securely
- [ ] `.env` file is not committed to version control
- [ ] Team members know how to access keys securely

## Support

For issues related to:
- **OpenAI API**: Contact OpenAI support or visit https://help.openai.com/
- **Syncro MSP**: Contact Syncro support or visit https://help.syncromsp.com/
- **SerpAPI**: Contact SerpAPI support or visit https://serpapi.com/contact
- **This application**: Open an issue in the GitHub repository
