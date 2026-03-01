from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.auth import UserCreate
from app.utils.security import get_password_hash, verify_password, create_access_token
from datetime import timedelta
from app.config.settings import settings

async def register_user(db: AsyncSession, user_data: UserCreate):
    # Check if username or email exists
    result_user = await db.execute(select(User).filter(User.username == user_data.username))
    if result_user.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already registered")
        
    result_email = await db.execute(select(User).filter(User.email == user_data.email))
    if result_email.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pw
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def authenticate_user(db: AsyncSession, username: str, password: str):
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_user_token(user: User):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
