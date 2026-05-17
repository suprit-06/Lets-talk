<<<<<<< ours
<div align="center">
  <h1>Let's Talk 💬</h1>
  <p><b>A production-ready AI chat interface powered by FastAPI, Groq API, and Bootstrap.</b></p>
  
  <p>
    <img src="https://img.shields.io/badge/Status-Active-success.svg?style=flat-square" alt="Status">
    <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=flat-square" alt="Python Version">
    <img src="https://img.shields.io/badge/FastAPI-Production_Ready-009688.svg?style=flat-square" alt="FastAPI">
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square" alt="MIT License"></a>
  </p>
</div>

Let's Talk is an open-source, high-performance web-based AI chat application designed to provide a fast, responsive, and seamless conversational experience. Built on a modern Python stack using **FastAPI**, it leverages the ultra-fast **Groq API** for language model generation. Whether you're hosting a private chatbot or building real-time applications, this repository serves as a powerful foundation.

<br />

## 🌟 Features

| Feature | Description |
| ------- | ----------- |
| 🚀 **Ultra-Fast AI** | Exclusively powered by the **Groq API** (Llama 3.1 & more) for near-instant inference and token generation. |
| 🔐 **Secure & Safe** | Built-in user registration and secure login utilizing **JWT** (JSON Web Tokens) and bcrypt password hashing. |
| 💬 **Real-Time UI** | Fluid, character-by-character UI updates powered by **Server-Sent Events (SSE)**. |
| 📂 **Thread Sessions** | Users can create, organize, manage, and switch between multiple distinct conversation threads automatically. |
| 🧠 **Context Aware** | Maintains a sliding window of chat history to optimize Groq token usage and keep the conversation relevant. |
| 📱 **Responsive View** | Clean, modern, and mobile-friendly interface crafted with **Bootstrap 5**. |
| 🗄️ **Flexible DBs** | Uses **SQLAlchemy** and AsyncPG/Aiosqlite. Defaults to SQLite locally, fully compatible with **PostgreSQL** in production. |

<br />

## ⚙️ How It Works

1. 👤 **Authenticate**: Users securely create an account or log in.
2. ⚡ **Connect**: The FastAPI backend establishes an SSE connection for real-time streaming.
3. 🧠 **Process**: User messages are sent to the Groq API alongside the recent context window.
4. 🌊 **Stream**: The AI's response is sent back character-by-character to the custom-styled UI in real-time.
5. 💾 **Store**: Conversations and session tokens are securely archived in your local SQLite or remote PostgreSQL database.

<br />

## 🛠️ Tech Stack

- **Backend Framework**: `FastAPI`, `Uvicorn` (ASGI)
- **Database**: `SQLAlchemy` (ORM), `Alembic` (Migrations), `SQLite`/`PostgreSQL`
- **AI Integration**: Official Python `groq` SDK
- **Frontend**: `Jinja2` Templates, Vanilla JavaScript, `Bootstrap 5`, `CSS3`
- **Security & Auth**: `python-jose`, `passlib` (bcrypt)

<br />

## 🚀 Getting Started

### Prerequisites
- Python `3.10` or higher
- A [Groq API Key](https://console.groq.com/keys)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/lets-talk.git
cd lets-talk
```

**2. Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Set up environment variables**
```bash
cp .env.example .env
```
*Open `.env` and fill in your `GROQ_API_KEY`.*

**4. Install dependencies**
```bash
pip install -r requirements.txt
```

**5. Initialize & Run**
```bash
uvicorn app.main:app --reload
```
Open your browser and navigate to `http://localhost:8000`.

<br />

## 📁 Project Structure

```text
ai-chat-platform/
├── app/
│   ├── config/          # Application settings & environment configurations
│   ├── models/          # SQLAlchemy database models (User, Chat, Message)
│   ├── routes/          # FastAPI API routers (Auth, Chat endpoints)
│   ├── schemas/         # Pydantic schemas for strict data validation
│   ├── services/        # Business logic (Groq API, Authentication)
│   ├── static/          # CSS, JavaScript, and static images
│   ├── templates/       # HTML templates compiled via Jinja2
│   ├── database.py      # Database engine and session setup
│   ├── dependencies.py  # FastAPI dependencies (Get DB, Get User)
│   └── main.py          # FastAPI application factory & instance
├── .env.example         # Template for required environment variables
├── requirements.txt     # Python package dependencies
└── Dockerfile           # Minimal Docker configuration for deployment
```

<br />

## 🤝 Contributing

Contributions are welcome! If you have a suggestion that would make this better, please fork the repo and create a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---
<div align="center">
  <b>Built with ❤️ and powered by Groq</b><br>
  Released under the MIT License
</div>
=======
# SpendWise — Personal Finance & Expense Analytics Platform

SpendWise is a production-oriented full-stack finance platform for tracking income, expenses, budgets, recurring payments, and analytics insights. It uses a modular monolithic architecture with a Next.js frontend, Express REST API, PostgreSQL database, and Prisma ORM.

## Mature Project Prompt

Build **SpendWise**, a secure and scalable personal finance analytics platform that helps users understand and improve their financial behavior. The application must support authenticated users, income and expense tracking, category management, monthly budgets, recurring payments, transaction search/filtering, CSV export, and a responsive analytics dashboard with charts for category distribution, monthly trends, income versus expense, and budget utilization. The system should follow clean software engineering practices, including protected APIs, ownership checks, relational schema design, backend aggregation queries, reusable UI components, environment-based configuration, and production-ready documentation.

## Exact File Structure

```text
spendwise/
├── .dockerignore
├── .env.example
├── .gitignore
├── Procfile
├── README.md
├── docker-compose.prod.yml
├── docker-compose.yml
├── docs/
│   ├── DEPLOYMENT.md
│   └── REPORT.md
├── package.json
├── scripts/
│   └── dev.mjs
└── apps/
    ├── api/
    │   ├── Dockerfile
    │   ├── package.json
    │   ├── prisma/
    │   │   ├── schema.prisma
    │   │   └── seed.ts
    │   ├── src/
    │   │   ├── app.ts
    │   │   ├── config/
    │   │   │   ├── env.ts
    │   │   │   └── prisma.ts
    │   │   ├── middleware/
    │   │   │   ├── auth.ts
    │   │   │   └── error.ts
    │   │   ├── routes/
    │   │   │   ├── auth.routes.ts
    │   │   │   └── finance.routes.ts
    │   │   ├── server.ts
    │   │   ├── services/
    │   │   │   ├── auth.service.ts
    │   │   │   └── finance.service.ts
    │   │   └── utils/
    │   │       ├── auth.ts
    │   │       ├── errors.ts
    │   │       └── http.ts
    │   └── tsconfig.json
    └── web/
        ├── .eslintrc.json
        ├── Dockerfile
        ├── next-env.d.ts
        ├── next.config.mjs
        ├── package.json
        ├── postcss.config.js
        ├── public/
        │   └── .gitkeep
        ├── src/
        │   ├── app/
        │   │   ├── globals.css
        │   │   ├── layout.tsx
        │   │   └── page.tsx
        │   ├── components/
        │   │   ├── Charts.tsx
        │   │   └── StatCard.tsx
        │   └── lib/
        │       └── api.ts
        ├── tailwind.config.ts
        ├── tsconfig.json
        └── vercel.json
```

## Local Setup

### 1. Prerequisites

- Node.js 20+
- npm 10+
- PostgreSQL 15+ or Docker

### 2. Install dependencies

```bash
npm install
```

### 3. Configure environment

```bash
cp .env.example .env
```

Update `DATABASE_URL`, `JWT_SECRET`, and `CORS_ORIGIN` if your local setup differs from the example. `CORS_ORIGIN` accepts comma-separated deployed web origins, and cloud platforms can provide `PORT` instead of `API_PORT`. The demo dashboard can authenticate against the seeded account with `SPENDWISE_DEMO_EMAIL` and `SPENDWISE_DEMO_PASSWORD`.

### 4. Start PostgreSQL

```bash
docker compose up -d postgres
```

If you already have PostgreSQL running locally, skip Docker and use your own connection string.

### 5. Prepare the database

```bash
npm run db:generate
npm run db:migrate
npm run db:seed
```

The seed command creates a demo account:

- Email: `demo@spendwise.local`
- Password: `SpendWise123`

### 6. Run the full stack locally

```bash
npm run dev
```

- Web app: <http://localhost:3000>
- API health check: <http://localhost:4000/api/health>

## API Overview

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `POST` | `/api/auth/register` | Create a user account |
| `POST` | `/api/auth/login` | Authenticate and return a JWT |
| `GET` | `/api/dashboard` | Return summary cards and chart data |
| `GET` | `/api/transactions` | List searchable/filterable transactions |
| `POST` | `/api/transactions` | Create income or expense transaction |
| `PATCH` | `/api/transactions/:id` | Update a user-owned transaction |
| `DELETE` | `/api/transactions/:id` | Delete a user-owned transaction |
| `GET` | `/api/transactions/export.csv` | Export filtered transactions as CSV |
| `GET` | `/api/categories` | List user categories |
| `POST` | `/api/categories` | Create a category |
| `GET` | `/api/budgets` | List monthly budgets |
| `PUT` | `/api/budgets` | Create or update a category budget |
| `GET` | `/api/recurring` | List recurring payments |
| `POST` | `/api/recurring` | Create a recurring payment |
| `PATCH` | `/api/recurring/:id` | Update a recurring payment |

Protected endpoints require `Authorization: Bearer <token>`.

## Production Hardening and Optimization

- JWT-protected finance APIs with user ownership checks before transaction and budget mutations.
- Indexed database fields for user/date/type/category queries and recurring payment scheduling.
- Backend aggregation for dashboard charts to reduce frontend computation.
- Shared Prisma client to avoid excessive database connections.
- Zod validation for environment variables, request bodies, and query strings.
- Centralized async error handling with clean validation, authorization, conflict, and not-found responses.
- Root development runner implemented with Node.js instead of a third-party process manager.
- Responsive chart cards and reusable stat cards in the UI.
- Demo fallback data so the frontend can be previewed before API setup.

## Deployment Notes

Deployment-friendly files are included for familiar hosting flows: `apps/api/Dockerfile`, `apps/web/Dockerfile`, `docker-compose.prod.yml`, `Procfile`, and `apps/web/vercel.json`. See `docs/DEPLOYMENT.md` for Docker, Vercel, Railway, Render, and Heroku-style steps.

- Deploy `apps/web` to Vercel and set `NEXT_PUBLIC_API_URL` to the deployed API URL.
- Deploy `apps/api` to Railway or Render with PostgreSQL and set `DATABASE_URL`, `JWT_SECRET`, `PORT`, and `CORS_ORIGIN`.
- Prefer a long random `JWT_SECRET` in production.
- Run production Prisma migrations during deployment with `npm run db:deploy --workspace apps/api` or your platform's release command.
>>>>>>> theirs
