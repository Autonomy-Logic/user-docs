# Edge Functions

Autonomy Edge provides a REST API that powers the web IDE at edge.autonomylogic.com. You can use this same API to build custom integrations, automate workflows, and extend the platform with external tools. This reference covers the available endpoints, authentication, and common integration patterns.

## Authentication

All API requests (except authentication endpoints themselves) require a JWT bearer token. Get one by signing in:

```
POST /auth/signin
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "your-password"
}
```

The response includes an access token and a refresh token:

```json
{
  "statusCode": 200,
  "data": {
    "accessToken": "eyJhbG...",
    "refreshToken": "eyJhbG..."
  }
}
```

Use the access token in subsequent requests:

```
Authorization: Bearer eyJhbG...
```

When the access token expires, refresh it:

```
POST /auth/refresh
Content-Type: application/json

{
  "refreshToken": "eyJhbG..."
}
```

## Response Format

All API responses follow a consistent envelope format:

```json
{
  "statusCode": 200,
  "data": { ... }
}
```

Error responses include a message:

```json
{
  "statusCode": 400,
  "message": "Validation error description"
}
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/signup` | Register a new user account |
| POST | `/auth/signin` | Authenticate and receive tokens |
| GET | `/auth/me` | Get current user profile |
| POST | `/auth/refresh` | Refresh access token |
| PUT | `/auth/user/:id` | Update user profile |
| POST | `/auth/verify-email` | Verify email address |
| POST | `/auth/forgot-password` | Request password reset |
| POST | `/auth/reset-password` | Reset password with verification code |
| POST | `/auth/resend-verification-email` | Resend email verification |

OAuth providers (Google, Microsoft, Apple) are also available for browser-based authentication flows.

### Projects

Projects are the core organizational unit. Each project contains PLC source code, configuration, and metadata.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/projects` | Create a new project |
| GET | `/projects` | List projects (paginated, filterable) |
| GET | `/projects/:projectId/details` | Get project details with files |
| PUT | `/projects/:id` | Update project metadata |
| DELETE | `/projects/:id` | Soft-delete a project |
| PATCH | `/projects/:id/rename` | Rename a project |
| PUT | `/projects/:id/move` | Move project to a folder |
| PATCH | `/projects/:id/trash` | Move project to trash |
| PATCH | `/projects/:id/restore` | Restore from trash |
| DELETE | `/projects/:id/permanent` | Permanently delete |
| POST | `/projects/:projectId/files/save` | Save project files |
| POST | `/projects/:projectId/clone` | Clone a public project |
| GET | `/projects/:projectId/download` | Download project as ZIP |
| POST | `/projects/import` | Import a project from ZIP |
| POST | `/projects/empty-trash` | Empty the trash |

**Listing projects with filters:**

```
GET /projects?page=1&limit=20&sortBy=updatedAt&sortOrder=desc
```

Query parameters:
- `page` — Page number (default: 1)
- `limit` — Items per page (default: 20)
- `sortBy` — Sort field (`name`, `createdAt`, `updatedAt`)
- `sortOrder` — Sort direction (`asc`, `desc`)

### Devices

Devices represent virtual PLC runtime instances. You can manage them through the API just like you do in the dashboard.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/devices` | Create a new device |
| GET | `/devices` | List devices (paginated) |
| GET | `/device/:deviceId/details` | Get device details with resource usage |
| DELETE | `/devices/:deviceId` | Delete a device |
| PATCH | `/devices/:deviceId/rename` | Rename a device |
| POST | `/devices/:deviceId/start` | Start the device |
| POST | `/devices/:deviceId/stop` | Stop the device |
| POST | `/devices/:deviceId/restart` | Restart the device |
| GET | `/devices/runtime-versions` | Get available runtime versions |

**Device lifecycle:**

```
Create → Start → (Running) → Stop → Start → ... → Delete
```

### Orchestrators

Orchestrators are agents running on your edge hardware that manage device instances.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/orchestrators` | Register a new orchestrator |
| GET | `/orchestrators` | List orchestrators (paginated) |
| GET | `/orchestrators/:orchestratorId/details` | Get orchestrator details with resource data |
| DELETE | `/orchestrators/:orchestratorId` | Remove an orchestrator |
| PATCH | `/orchestrators/:orchestratorId/rename` | Rename an orchestrator |
| POST | `/orchestrators/:orchestratorId/start` | Start the orchestrator |
| POST | `/orchestrators/:orchestratorId/stop` | Stop the orchestrator |
| POST | `/orchestrators/:orchestratorId/restart` | Restart the orchestrator |

### Folders

Folders organize projects in the dashboard.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/folders` | Create a folder |
| GET | `/folders` | List user folders |
| PUT | `/folders/:id/rename` | Rename a folder |
| PUT | `/folders/:id/move` | Move a folder |
| PATCH | `/folders/:id/trash` | Move to trash |
| PATCH | `/folders/:id/restore` | Restore from trash |
| DELETE | `/folders/:id/permanent` | Permanently delete |

### Pinned Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/pinned-projects` | List pinned projects |
| POST | `/pinned-projects/:projectId/pin` | Pin a project |
| DELETE | `/pinned-projects/:projectId/unpin` | Unpin a project |

### AI Assistant

The AI assistant provides code completion and chat capabilities for PLC programming.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/ai/chat` | Stream AI chat response (SSE) |
| POST | `/ai/complete` | Get code completion |
| GET | `/ai/credits` | Check remaining AI credits |

### Feedback

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/feedback` | Submit feedback (rate-limited: 5/hour) |

### Trash

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/trash` | List all trashed items |

## Common Integration Patterns

### Automated Project Deployment

Deploy a project to a device programmatically:

1. **Get the project** — `GET /projects/:projectId/details`
2. **Download the program** — `GET /projects/:projectId/download`
3. **Ensure the device is stopped** — `POST /devices/:deviceId/stop`
4. **Deploy and start** — `POST /devices/:deviceId/start`

### Monitoring Device Status

Poll device status for a monitoring dashboard:

```
GET /devices
```

Each device in the response includes its current status (`running`, `stopped`, `creating`, `deleting`, `error`) and resource consumption data (CPU, memory).

For orchestrator-level health monitoring:

```
GET /orchestrators/:orchestratorId/details
```

This includes CPU usage, memory usage, disk usage, and uptime.

### Batch Project Management

Automate project organization:

```bash
# Create a folder
curl -X POST https://edge.autonomylogic.com/api/folders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Production Programs"}'

# Move projects to the folder
curl -X PUT https://edge.autonomylogic.com/api/projects/$PROJECT_ID/move \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"folderId": "folder-uuid"}'
```

## Rate Limiting

Some endpoints are rate-limited to prevent abuse:

| Endpoint Category | Limit |
|-------------------|-------|
| Authentication | Throttled per IP |
| AI endpoints | Throttled per user (credit-based) |
| Feedback | 5 requests per hour |
| General API | Standard rate limits apply |

If you receive a `429 Too Many Requests` response, wait before retrying.

## What's Next?

- [Custom Libraries](custom-libraries) — Create reusable function block libraries
- [Network Issues](../troubleshooting/network-issues) — Troubleshoot connectivity
- [Runtime Debugging](../troubleshooting/runtime-debugging) — Debug deployed programs
