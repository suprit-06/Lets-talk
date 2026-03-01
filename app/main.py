from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from app.routes import auth, chat

from contextlib import asynccontextmanager
from app.database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Let's Talk", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static directories exist before mounting
static_path = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_path):
    os.makedirs(os.path.join(static_path, "css"), exist_ok=True)
    os.makedirs(os.path.join(static_path, "js"), exist_ok=True)

app.mount("/static", StaticFiles(directory=static_path), name="static")

templates_path = os.path.join(os.path.dirname(__file__), "templates")
if not os.path.exists(templates_path):
    os.makedirs(templates_path, exist_ok=True)
templates = Jinja2Templates(directory=templates_path)

app.include_router(auth.router)
app.include_router(chat.router)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
