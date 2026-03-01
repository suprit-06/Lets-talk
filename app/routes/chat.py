from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sse_starlette.sse import EventSourceResponse
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.chat import ChatSessionCreate, ChatSessionResponse, ChatSessionListResponse, MessageCreate, MessageResponse, ChatSessionUpdate
import app.services.chat_service as chat_service
import app.services.ai_service as ai_service
import asyncio

router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.get("/sessions")
async def list_sessions(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    sessions = await chat_service.get_user_sessions(db, current_user.id)
    return [
        {
            "id": s.id,
            "title": s.title,
            "created_at": str(s.created_at),
            "updated_at": str(s.updated_at)
        } for s in sessions
    ]

@router.post("/sessions")
async def create_new_session(data: ChatSessionCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    session = await chat_service.create_session(db, current_user.id, data.title)
    return {
        "id": session.id,
        "title": session.title,
        "created_at": str(session.created_at),
        "updated_at": str(session.updated_at),
        "messages": []
    }

@router.get("/sessions/{session_id}")
async def get_session(session_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    session = await chat_service.get_session_by_id(db, session_id, current_user.id)
    return {
        "id": session.id,
        "title": session.title,
        "created_at": str(session.created_at),
        "updated_at": str(session.updated_at),
        "messages": [{"id": m.id, "role": m.role, "content": m.content, "created_at": str(m.created_at)} for m in session.messages]
    }

@router.put("/sessions/{session_id}")
async def update_session(session_id: int, data: ChatSessionUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    session = await chat_service.update_session_title(db, session_id, current_user.id, data.title)
    return {
        "id": session.id,
        "title": session.title,
        "created_at": str(session.created_at),
        "updated_at": str(session.updated_at),
        "messages": [{"id": m.id, "role": m.role, "content": m.content, "created_at": str(m.created_at)} for m in session.messages]
    }

@router.delete("/sessions/{session_id}")
async def delete_session(session_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await chat_service.delete_session(db, session_id, current_user.id)
    return {"status": "deleted"}

@router.post("/sessions/{session_id}/message")
async def send_message_stream(request: Request, session_id: int, message: MessageCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # 1. Verify session belongs to user
    await chat_service.get_session_by_id(db, session_id, current_user.id)
    
    # 2. Save user message
    await chat_service.add_message(db, session_id, role=message.role, content=message.content)
    
    # 3. Build context for AI
    context = await chat_service.build_chat_context(db, session_id, limit=10) # Sliding window
    
    # 4. Stream response and save final async
    async def event_generator():
        full_response = ""
        async for chunk in ai_service.stream_groq_response(context):
            
            if await request.is_disconnected():
                break
            
            full_response += chunk
            yield chunk

        # Async Final Save when stream finishes
        if full_response and not await request.is_disconnected():
            await chat_service.add_message(db, session_id, role="assistant", content=full_response)
            
    return EventSourceResponse(event_generator())
