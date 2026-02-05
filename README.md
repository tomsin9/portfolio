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

2. Start all services:
   ```bash
   docker-compose up --build
   ```

3. Open:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000

### Without Docker

**Backend**

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
# Set DATABASE_URL and other vars (see .env.example), then:
uvicorn app.main:app --reload --port 8000
```

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173. Set `VITE_API_URL` if your API is not at `http://localhost:8000`.

## Project Structure

```
├── backend/          # FastAPI app (blog API, DB models)
├── frontend/          # Vue 3 + Vite app
├── docker-compose.yaml
└── .env.example       # Copy to .env and fill in
```

## License

See [LICENSE](LICENSE).
