from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from app.models.chat import ChatSession, Message

async def get_user_sessions(db: AsyncSession, user_id: int):
    stmt = select(ChatSession).filter(ChatSession.user_id == user_id).order_by(ChatSession.updated_at.desc())
    result = await db.execute(stmt)
    return result.unique().scalars().all()

async def create_session(db: AsyncSession, user_id: int, title: str):
    db_session = ChatSession(user_id=user_id, title=title)
    db.add(db_session)
    await db.commit()
    await db.refresh(db_session)
    return db_session

async def update_session_title(db: AsyncSession, session_id: int, user_id: int, title: str):
    session = await get_session_by_id(db, session_id, user_id)
    session.title = title
    await db.commit()
    await db.refresh(session)
    return session

async def delete_session(db: AsyncSession, session_id: int, user_id: int):
    session = await get_session_by_id(db, session_id, user_id)
    await db.delete(session)
    await db.commit()

async def get_session_by_id(db: AsyncSession, session_id: int, user_id: int):
    stmt = select(ChatSession).filter(
        ChatSession.id == session_id, ChatSession.user_id == user_id
    )
    result = await db.execute(stmt)
    session = result.unique().scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return session

async def add_message(db: AsyncSession, session_id: int, role: str, content: str):
    msg = Message(session_id=session_id, role=role, content=content)
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    
    # Touch session to update `updated_at`
    stmt = select(ChatSession).filter(ChatSession.id == session_id)
    result = await db.execute(stmt)
    session = result.unique().scalar_one_or_none()
    if session:
        from sqlalchemy.sql import func
        session.updated_at = func.now()
        await db.commit()
    
    return msg

async def build_chat_context(db: AsyncSession, session_id: int, limit: int = 10):
    """
    Build context window for OpenAI API. Using Sliding Window.
    """
    stmt = select(Message).filter(Message.session_id == session_id).order_by(Message.created_at.desc()).limit(limit)
    result = await db.execute(stmt)
    messages = result.unique().scalars().all()
    # reverse back to chronological order
    messages = list(reversed(messages))
    
    context = [{"role": "system", "content": "You are a helpful AI assistant."}]
    for msg in messages:
        context.append({"role": msg.role, "content": msg.content})
    return context
