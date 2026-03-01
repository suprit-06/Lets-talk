<div align="center">
  <h1>Let's Talk 💬</h1>
  <p><b>A production-ready AI chat interface powered by FastAPI, Groq API, and Bootstrap.</b></p>
  
  <p>
    <a href="https://github.com/yourusername/lets-talk/stargazers"><img src="https://img.shields.io/github/stars/yourusername/lets-talk?style=flat-square&color=blue" alt="Stars"></a>
    <a href="https://github.com/yourusername/lets-talk/network/members"><img src="https://img.shields.io/github/forks/yourusername/lets-talk?style=flat-square&color=blue" alt="Forks"></a>
    <a href="https://github.com/yourusername/lets-talk/issues"><img src="https://img.shields.io/github/issues/yourusername/lets-talk?style=flat-square&color=red" alt="Issues"></a>
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
├── Dockerfile           # Minimal Docker configuration for deployment
└── render.yaml          # Blueprint for easy deployment to Render
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
