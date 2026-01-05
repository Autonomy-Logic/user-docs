# First User Setup

When you install OpenPLC Runtime v4 for the first time, there are no user accounts configured. You must create the first user before you can upload programs or control the runtime.

## Understanding the First-User Flow

OpenPLC Runtime v4 uses JWT (JSON Web Token) authentication for all API operations. Unlike Runtime v3, there is no default username or password. The first user must be created through the editor or API.

### How It Works

1. When no users exist, the `/api/get-users-info` endpoint returns a 404 status
2. OpenPLC Editor detects this and prompts you to create the first user
3. After creating the user, you can authenticate and access all runtime features

## Creating the First User via OpenPLC Editor

### Desktop Editor

1. Open OpenPLC Editor
2. Navigate to **Device** > **Configuration**
3. Enter the runtime's IP address and port (default: 8443)
4. Click **Connect**
5. The editor will detect no users exist and show a "Create User" dialog
6. Enter your desired username and password
7. Click **Create User**
8. You're now connected and can upload programs

### Web Editor (Autonomy Edge)

1. Open your project in Autonomy Edge
2. Navigate to **Device** > **Orchestrators**
3. Select your orchestrator and vPLC
4. Click **Connect**
5. If this is a new vPLC, you'll see the "Create User" dialog
6. Enter your desired username and password
7. Click **Create User**
8. You're now connected to the vPLC

## Creating the First User via API

For automated deployments, you can create the first user directly via the REST API:

### Check if Users Exist

```bash
curl -k https://localhost:8443/api/get-users-info
```

Response when no users exist:
```json
{
  "status": 404,
  "message": "No users found"
}
```

### Create First User

```bash
curl -k -X POST https://localhost:8443/api/create-user \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your-secure-password"}'
```

Response:
```json
{
  "success": true,
  "message": "User created successfully"
}
```

## Security Recommendations

### Choose a Strong Password

- Use at least 12 characters
- Include uppercase, lowercase, numbers, and symbols
- Avoid common words or patterns

### Secure Your Runtime

- Change the default port if exposed to the internet
- Use a firewall to restrict access
- Consider VPN for remote access

### Document Your Credentials

- Store credentials securely
- The runtime does not have a password recovery mechanism
- If you lose access, you may need to reinstall

## Troubleshooting

### "Create User" Dialog Doesn't Appear

1. Verify the runtime is running
2. Check you can reach the runtime on port 8443
3. Ensure you're using HTTPS (not HTTP)

### User Creation Fails

1. Check the runtime logs for errors
2. Verify network connectivity
3. Ensure the password meets any requirements

### Forgot Password

If you forget your password and cannot log in:

1. Stop the runtime
2. Delete the user database file (location varies by installation)
3. Restart the runtime
4. Create a new first user

> **Warning**: This will remove all user accounts. Use as a last resort.
