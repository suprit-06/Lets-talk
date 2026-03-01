# Let's Talk

A production-ready AI Chat Platform ("Let's Talk") built with FastAPI, PostgreSQL, and Bootstrap.

## Features
- User Authentication (JWT)
- Multiple chat sessions per user
- Real-time AI response streaming using Server-Sent Events (SSE)
- Chat History stored in PostgreSQL
- Sliding window context management for optimal Groq token usage
- Responsive UI with Bootstrap 5

## Setup

1. Clone or copy this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your variables (especially `GROQ_API_KEY` and `DATABASE_URL`).
4. Setup PostgreSQL (either locally or via Docker).
5. Run migrations (if Alembic is set up) or let SQLAlchemy create the tables.
6. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Docs
Once running, navigate to `http://localhost:8000/docs` to see the generated Swagger UI.
