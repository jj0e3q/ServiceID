from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import SessionLocal, Base, engine
from app.core import jwt_keys
from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.security.password import hash_password, verify_password
from shared.core.jwt_tokens import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        id=str(uuid4()),
        email=payload.email,
        hashed_password=hash_password(payload.password),
        is_active=True,
        created_at=datetime.now(timezone.utc),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    if not jwt_keys.PRIVATE_KEY or not jwt_keys.KID:
        raise HTTPException(status_code=500, detail="JWT keys not initialized")

    token = create_access_token(
        subject=user.id,
        email=user.email,
        roles=[],
        private_key=jwt_keys.PRIVATE_KEY,
        kid=jwt_keys.KID,
    )
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive")

    if not jwt_keys.PRIVATE_KEY or not jwt_keys.KID:
        raise HTTPException(status_code=500, detail="JWT keys not initialized")

    token = create_access_token(
        subject=user.id,
        email=user.email,
        roles=[],
        private_key=jwt_keys.PRIVATE_KEY,
        kid=jwt_keys.KID,
    )
    return TokenResponse(access_token=token)