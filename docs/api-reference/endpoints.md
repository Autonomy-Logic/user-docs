# API Endpoints

Complete reference for Autonomy Logic API endpoints.

## Base URL

```
https://api.autonomylogic.com/v1
```

## Authentication

All endpoints require authentication. See [Authentication](authentication.md) for details.

## Projects

### List Projects

Get a list of all projects.

```
GET /projects
```

**Response:**

```json
{
  "projects": [
    {
      "id": "proj_123",
      "name": "My Project",
      "created_at": "2025-01-01T00:00:00Z"
    }
  ]
}
```

### Get Project

Get details of a specific project.

```
GET /projects/{project_id}
```

### Create Project

Create a new project.

```
POST /projects
```

**Request Body:**

```json
{
  "name": "New Project",
  "description": "Project description"
}
```

### Update Project

Update an existing project.

```
PUT /projects/{project_id}
```

### Delete Project

Delete a project.

```
DELETE /projects/{project_id}
```

## Devices

### List Devices

Get all devices in a project.

```
GET /projects/{project_id}/devices
```

### Get Device

Get details of a specific device.

```
GET /devices/{device_id}
```

### Register Device

Register a new device.

```
POST /projects/{project_id}/devices
```

**Request Body:**

```json
{
  "name": "Device Name",
  "type": "plc",
  "connection": {
    "host": "192.168.1.100",
    "port": 502
  }
}
```

### Update Device

Update device configuration.

```
PUT /devices/{device_id}
```

### Remove Device

Remove a device from the project.

```
DELETE /devices/{device_id}
```

## Orchestrators

### List Orchestrators

Get all orchestrators.

```
GET /orchestrators
```

### Get Orchestrator

Get orchestrator details.

```
GET /orchestrators/{orchestrator_id}
```

### Create Orchestrator

Create a new orchestrator.

```
POST /orchestrators
```

### Update Orchestrator

Update orchestrator configuration.

```
PUT /orchestrators/{orchestrator_id}
```

### Delete Orchestrator

Delete an orchestrator.

```
DELETE /orchestrators/{orchestrator_id}
```

## Data

### Query Device Data

Query historical data from devices.

```
GET /devices/{device_id}/data
```

**Query Parameters:**

- `start_time` - Start of time range (ISO 8601)
- `end_time` - End of time range (ISO 8601)
- `limit` - Maximum number of records
- `offset` - Pagination offset

### Write Device Data

Write data to a device.

```
POST /devices/{device_id}/data
```

## Webhooks

### List Webhooks

Get all configured webhooks.

```
GET /webhooks
```

### Create Webhook

Create a new webhook.

```
POST /webhooks
```

**Request Body:**

```json
{
  "url": "https://example.com/webhook",
  "events": ["device.connected", "device.disconnected"]
}
```

## Rate Limits

API rate limits are returned in response headers:

- `X-RateLimit-Limit` - Maximum requests per hour
- `X-RateLimit-Remaining` - Remaining requests
- `X-RateLimit-Reset` - Time when limit resets

## Error Handling

All errors follow a consistent format:

```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "code": 400
}
```

## Pagination

List endpoints support pagination:

```
GET /projects?limit=50&offset=0
```

## Next Steps

- Review [Authentication](authentication.md) details
- Learn about [Projects](../user-guide/projects.md)
- Explore [Architecture](../advanced/architecture.md)
