# Authentication

Learn how to authenticate with the Autonomy Logic API.

## Authentication Overview

The Autonomy Logic API uses token-based authentication to secure access to resources. All API requests must include valid authentication credentials.

## Authentication Methods

### API Keys

API keys provide programmatic access to the API.

#### Generating an API Key

1. Log in to your account
2. Navigate to Settings > API Keys
3. Click "Generate New Key"
4. Copy and securely store your key
5. Use the key in API requests

#### Using API Keys

Include your API key in the request header:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://api.autonomylogic.com/v1/projects
```

### OAuth 2.0

OAuth 2.0 is recommended for applications that need to access the API on behalf of users.

#### OAuth Flow

1. Register your application
2. Request authorization
3. Exchange authorization code for access token
4. Use access token in API requests

### JWT Tokens

JSON Web Tokens (JWT) are used for session-based authentication.

## Security Best Practices

### Protecting Your Credentials

- Never commit API keys to version control
- Store credentials securely using environment variables
- Rotate keys regularly
- Use different keys for different environments
- Revoke compromised keys immediately

### Token Expiration

Access tokens expire after a set period. Implement token refresh logic in your applications.

### Rate Limiting

API requests are rate-limited to prevent abuse:

- Standard tier: 1000 requests/hour
- Premium tier: 10000 requests/hour

## Authentication Errors

### Common Error Codes

- `401 Unauthorized` - Invalid or missing credentials
- `403 Forbidden` - Valid credentials but insufficient permissions
- `429 Too Many Requests` - Rate limit exceeded

### Error Response Format

```json
{
  "error": "unauthorized",
  "message": "Invalid API key",
  "code": 401
}
```

## Testing Authentication

Test your authentication setup:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://api.autonomylogic.com/v1/auth/verify
```

## Next Steps

- Explore available [API Endpoints](endpoints.md)
- Review [Projects](../user-guide/projects.md) documentation
- Learn about [Deployment](../advanced/deployment.md) strategies
