# Personal website

A personal website with a Vue 3 frontend and FastAPI backend.

## Tech Stack

- **Frontend:** Vue 3, TypeScript, Vite, Tailwind CSS, shadcn/vue, GSAP, etc.
- **Backend:** FastAPI, SQLModel, PostgreSQL
- **DevOps:** Docker, docker-compose

## Prerequisites

- Node.js (for frontend)
- Python 3.x (for backend)
- Docker & Docker Compose (optional, for running everything in containers)

## Quick Start

### With Docker (recommended)

1. Copy the env file and set your values:
   ```bash
   cp .env.example .env
   ```

2. **Development** – Vite dev server (hot reload), backend with `--reload`:
   ```bash
   docker compose up --build
   ```
   - Frontend: http://localhost:5173  
   - Backend API: http://localhost:8000  

3. **Production** – Built frontend served by nginx, no source mounts:
   ```bash
   docker compose -f docker-compose.yaml -f docker-compose.prod.yaml up --build
   ```
   - Frontend: http://localhost (port 80 by default)  
   - Backend API: http://localhost:8000  
   - If port 80 is already in use on your server, set `FRONTEND_PORT=8080` (or another port) in `.env`.  
   - Frontend uses `frontend/Dockerfile` (multi-stage build + nginx). Dev uses `frontend/Dockerfile.dev`.

## Project Structure

```
├── backend/              # FastAPI app (blog API, DB models)
├── frontend/
│   ├── Dockerfile        # Production: build + nginx
│   ├── Dockerfile.dev    # Development: Vite dev server
│   └── nginx.conf        # SPA config for production serve
├── docker-compose.yaml       # Default: dev mode
├── docker-compose.prod.yaml  # Override for production
└── .env.example             # Copy to .env and fill in
```

## License

See [LICENSE](LICENSE).
