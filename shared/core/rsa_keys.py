from __future__ import annotations

from pathlib import Path
from typing import Tuple

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from jose.utils import base64url_encode
import json
import uuid


PRIVATE_KEY_NAME = "jwt_private.pem"
PUBLIC_KEY_NAME = "jwt_public.pem"
KEY_ID_NAME = "kid.txt"


def ensure_rsa_keypair(keys_dir: Path) -> Tuple[bytes, bytes, str]:
    keys_dir.mkdir(parents=True, exist_ok=True)
    priv_path = keys_dir / PRIVATE_KEY_NAME
    pub_path = keys_dir / PUBLIC_KEY_NAME
    kid_path = keys_dir / KEY_ID_NAME

    if priv_path.exists() and pub_path.exists() and kid_path.exists():
        private_pem = priv_path.read_bytes()
        public_pem = pub_path.read_bytes()
        kid = kid_path.read_text().strip()
        return private_pem, public_pem, kid

    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend(),
    )
    private_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    kid = str(uuid.uuid4())

    priv_path.write_bytes(private_pem)
    pub_path.write_bytes(public_pem)
    kid_path.write_text(kid)

    return private_pem, public_pem, kid


def build_jwks(public_pem: bytes, kid: str) -> dict:
    public_key = serialization.load_pem_public_key(public_pem, backend=default_backend())
    numbers = public_key.public_numbers()

    n = base64url_encode(numbers.n.to_bytes((numbers.n.bit_length() + 7) // 8, "big"))
    e = base64url_encode(numbers.e.to_bytes((numbers.e.bit_length() + 7) // 8, "big"))

    return {
        "keys": [
            {
                "kty": "RSA",
                "alg": "RS256",
                "use": "sig",
                "kid": kid,
                "n": n.decode(),
                "e": e.decode(),
            }
        ]
    }