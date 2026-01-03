# todo app - fastapi rest api

convert the in-memory todo app into a rest api deployable on vercel.

## features

- **rest api endpoints** for all todo operations
- **fastapi framework** for modern python web development
- **cors enabled** for cross-origin requests
- **pydantic validation** for request/response models
- **in-memory storage** (same as phase-i console app)
- **vercel deployment** ready

## rest api endpoints

### get /
root endpoint - returns api info

### get /health
health check endpoint

### get /tasks
list all tasks with optional filtering

**query parameters:**
- `filter` (optional): "all" (default), "pending", or "completed"

**response:**
```json
[
  {
    "id": 1,
    "title": "buy milk",
    "description": "whole milk",
    "completed": false,
    "created_at": "2026-01-03t10:15:22",
    "completed_at": null
  }
]
```

### post /tasks
create a new task

**request body:**
```json
{
  "title": "buy milk",
  "description": "whole milk"
}
```

**response:** (201 created)
```json
{
  "id": 1,
  "title": "buy milk",
  "description": "whole milk",
  "completed": false,
  "created_at": "2026-01-03t10:15:22",
  "completed_at": null
}
```

### get /tasks/{task_id}
get details of a specific task

**response:**
```json
{
  "id": 1,
  "title": "buy milk",
  "description": "whole milk",
  "completed": false,
  "created_at": "2026-01-03t10:15:22",
  "completed_at": null
}
```

### put /tasks/{task_id}
update a task

**request body:**
```json
{
  "title": "buy 2% milk",
  "description": "whole milk",
  "completed": true
}
```

**response:**
```json
{
  "id": 1,
  "title": "buy 2% milk",
  "description": "whole milk",
  "completed": true,
  "created_at": "2026-01-03t10:15:22",
  "completed_at": "2026-01-03t10:30:00"
}
```

### delete /tasks/{task_id}
delete a task

**response:**
```json
{
  "message": "task 1 deleted"
}
```

## local testing

### install dependencies
```bash
pip install -r requirements.txt
```

### run the server
```bash
uvicorn api:app --reload
```

### access api
open http://localhost:8000 in your browser or use curl:

```bash
# create task
curl -x post http://localhost:8000/tasks \
  -h "content-type: application/json" \
  -d '{"title":"buy milk","description":"whole milk"}'

# list tasks
curl http://localhost:8000/tasks

# get task
curl http://localhost:8000/tasks/1

# update task
curl -x put http://localhost:8000/tasks/1 \
  -h "content-type: application/json" \
  -d '{"completed":true}'

# delete task
curl -x delete http://localhost:8000/tasks/1
```

### interactive documentation
fastapi provides interactive api documentation:
- swagger ui: http://localhost:8000/docs
- redoc: http://localhost:8000/redoc

## vercel deployment

### prerequisites
1. vercel account (https://vercel.com)
2. vercel cli installed: `npm install -g vercel`

### deploy
```bash
vercel
```

follow the prompts to deploy your project.

your api will be available at: `https://<project-name>.vercel.app`

## differences from phase-i console app

| feature | console | api |
|---------|---------|-----|
| interaction | stdin/stdout | http requests |
| commands | text commands | rest endpoints |
| storage | in-memory | in-memory (per deployment) |
| hosting | local | vercel (cloud) |
| deployment | local execution | serverless functions |

## notes

- **in-memory**: data is reset on each deployment/restart
- **phase-iii**: add database (postgresql/mongodb) for persistence
- **stateless**: each request is independent; no session storage
- **scalable**: ready for future database integration

