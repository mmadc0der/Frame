# Frame API Documentation

## Authentication

### POST /api/auth/register
Register a new user.

**Request:**
```json
{
  "email": "string",
  "password": "string",
  "username": "string"
}
```

**Response:**
```json
{
  "id": "string",
  "username": "string",
  "email": "string",
  "created_at": "string"
}
```

### POST /api/auth/login
Authenticate user and receive tokens.

**Request:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "access_token": "string",
  "refresh_token": "string"
}
```

## Dashboard Components

### GET /api/dashboard
Get user's dashboard configuration and data.

**Response:**
```json
{
  "weather": {
    "temperature": "number",
    "condition": "string",
    "location": "string"
  },
  "quote": {
    "text": "string",
    "author": "string"
  },
  "tasks": [
    {
      "id": "string",
      "title": "string",
      "completed": "boolean",
      "created_at": "string"
    }
  ],
  "habits": [
    {
      "id": "string",
      "name": "string",
      "progress": "number",
      "target": "number"
    }
  ],
  "notes": [
    {
      "id": "string",
      "content": "string",
      "updated_at": "string"
    }
  ]
}
```

### Tasks API

#### POST /api/tasks
Create a new task.

#### PUT /api/tasks/{id}
Update existing task.

#### DELETE /api/tasks/{id}
Delete a task.

### Habits API

#### POST /api/habits
Create a new habit tracker.

#### PUT /api/habits/{id}
Update habit progress.

#### DELETE /api/habits/{id}
Delete a habit tracker.

### Notes API

#### POST /api/notes
Create a new note.

#### PUT /api/notes/{id}
Update note content.

#### DELETE /api/notes/{id}
Delete a note.

## Error Responses

All endpoints may return these errors:

```json
{
  "error": {
    "code": "string",
    "message": "string"
  }
}
```

Common error codes:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 429: Too Many Requests
- 500: Internal Server Error