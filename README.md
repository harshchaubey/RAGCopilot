# RAGCopilot

Access-controlled RAG system with role-based document permissions, conversation memory, and admin analytics.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI + Motor (async MongoDB) |
| Vector DB | ChromaDB (local persistent) |
| Embeddings | `paraphrase-multilingual-MiniLM-L12-v2` |
| LLM | Ollama (`phi3:mini` — local, lightweight) |
| Database | MongoDB |
| Frontend | React + Vite |

## Roles & Access Control

| Role | Document Access | Features |
|------|----------------|---------|
| **Admin** | All documents | Chat, upload/delete docs, analytics dashboard, user management |
| **Employee** | `employee` + `all` docs | Chat only |
| **User** | `all` docs only | Chat only |

> The **first registered account** automatically becomes Admin. All subsequent registrations are Users.

Document chunks are stored in ChromaDB with `access_level` metadata (`admin` / `employee` / `all`). Queries are filtered at retrieval time based on the requesting user's role.

## Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB running on `localhost:27017`
- [Ollama](https://ollama.com) installed and running

## Setup

### 1. Pull the LLM model

```bash
ollama pull phi3:mini
```

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The embedding model (`paraphrase-multilingual-MiniLM-L12-v2`) downloads automatically on first startup (~120 MB).

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173).

## Environment Variables

Copy `backend/.env` and adjust as needed:

```env
MONGO_URL=mongodb://localhost:27017
MONGO_DB=enterprise_copilot
JWT_SECRET=your-secret-key
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=phi3:mini      # swap for llama3.2:3b, mistral, etc.
CHROMA_PATH=./chroma_db
```

## API Endpoints

### Auth
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/register` | Register (first = admin) |
| POST | `/api/auth/login` | Login, returns JWT |
| GET | `/api/auth/me` | Current user info |

### Documents (admin only for write)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/documents/` | List accessible documents |
| POST | `/api/documents/upload` | Upload + index document |
| DELETE | `/api/documents/{id}` | Delete document + chunks |

### Chat
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/chat/query` | Send message, get RAG answer |
| GET | `/api/chat/conversations` | List user conversations |
| GET | `/api/chat/conversations/{id}` | Load conversation history |

### Admin
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/admin/users` | All users |
| PATCH | `/api/admin/users/{id}/role` | Promote/demote user |
| GET | `/api/admin/analytics` | Metrics dashboard data |
| GET | `/api/admin/audit-logs` | Paginated audit log |
| GET | `/api/admin/document-access/{doc_id}` | Who accessed a document |

## Audit Logging

Every action is recorded via `utils/audit.py → log_event()`. Events:

- `register` / `login`
- `document_upload` / `document_delete`
- `chat_query` (includes sources accessed, latency)
- `role_change`

Admin analytics are computed by aggregating these logs — no separate metrics store needed.

## Project Structure

```
enterprise-copilot/
├── backend/
│   ├── main.py              # FastAPI app + lifespan
│   ├── config.py            # Pydantic settings
│   ├── database.py          # MongoDB (Motor)
│   ├── vector_store.py      # ChromaDB wrapper
│   ├── utils/audit.py       # Central audit logger
│   ├── models/schemas.py    # Pydantic request/response models
│   ├── services/
│   │   ├── embedding.py     # Sentence-transformers + chunking
│   │   ├── llm.py           # Ollama API client
│   │   └── rag.py           # RAG pipeline (retrieve + generate)
│   └── routes/
│       ├── auth.py          # Register, login, JWT
│       ├── documents.py     # Upload, list, delete
│       ├── chat.py          # Query + conversation history
│       └── admin.py         # Users, analytics, audit logs
└── frontend/
    └── src/
        ├── App.jsx                  # Router + auth guards
        ├── App.css                  # All styles
        ├── contexts/AuthContext.jsx # JWT auth state
        ├── services/api.js          # Axios client
        └── pages/
            ├── LoginPage.jsx        # Login / Register
            ├── ChatPage.jsx         # Chat UI + conversation list
            ├── DocumentsPage.jsx    # Upload/delete (admin)
            └── AdminPage.jsx        # Analytics, users, audit logs
```

## Supported Document Formats

- PDF (`.pdf`)
- Word documents (`.docx`)
- Plain text (`.txt`)

## Docker Deployment

### Production Build

Build and run all services (MongoDB, FastAPI backend, React frontend):

```bash
docker-compose up --build
```

Then:
- **Frontend** at [http://localhost](http://localhost)
- **Backend API** at [http://localhost:8000](http://localhost:8000)
- **MongoDB** on localhost:27017

> **Important:** Ollama must run on your host machine separately (not in Docker):
> ```bash
> ollama pull phi3:mini
> ollama serve
> ```
> Docker containers connect via `host.docker.internal:11434`.

### Development with Hot-Reload

```bash
docker-compose -f docker-compose.dev.yml up
```

- Frontend hot-reloads at [http://localhost:5173](http://localhost:5173)
- Backend hot-reloads on file save
- MongoDB persists in Docker volume

### Build Individual Images

**Backend:**
```bash
docker build -f backend.Dockerfile -t enterprise-copilot-backend .
docker run -p 8000:8000 -e MONGO_URL=mongodb://host.docker.internal:27017 enterprise-copilot-backend
```

**Frontend:**
```bash
docker build -f frontend.Dockerfile -t enterprise-copilot-frontend .
docker run -p 80:80 enterprise-copilot-frontend
```

### Environment Variables (Production)

In `docker-compose.yml`, update:
- `JWT_SECRET` — use a strong random string
- `OLLAMA_URL` — adjust if Ollama runs elsewhere
- Database credentials if using remote MongoDB

### Troubleshooting

**"Cannot connect to Ollama":** Make sure Ollama is running on your host with `ollama serve` and accessible at `http://host.docker.internal:11434`.

**"MongoDB connection refused":** Ensure the `mongodb` service is healthy before backend starts. Docker Compose handles this with `depends_on` + health checks.

**"Frontend can't reach backend":** Check that backend container is running and port 8000 is mapped.
