from fastapi import FastAPI
from shared.core.logging import setup_logging
from app.core.config import settings
from shared.core.rsa_keys import ensure_rsa_keypair, build_jwks
from app.core import jwt_keys

from app.routes import auth

app = FastAPI(title="Gateway API")

app.include_router(auth.router)

@app.on_event("startup")
def startup_event():
    setup_logging(settings.SERVICE_NAME)
    private_pem, public_pem, kid = ensure_rsa_keypair(settings.jwt_keys_path)
    jwt_keys.PRIVATE_KEY = private_pem
    jwt_keys.PUBLIC_KEY = public_pem
    jwt_keys.KID = kid
    jwt_keys.JWKS = build_jwks(public_pem, kid)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "service": settings.SERVICE_NAME}


@app.get("/.well-known/jwks.json", tags=["jwks"])
def get_jwks():
    return jwt_keys.JWKS