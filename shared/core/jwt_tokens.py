from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt  # pyjwt


def create_access_token(
    *,
    subject: str,
    email: str,
    roles: list[str],
    private_key: bytes,
    kid: str,
    expires_delta: timedelta = timedelta(minutes=15),
) -> str:
    now = datetime.now(timezone.utc)
    payload: Dict[str, Any] = {
        "sub": subject,
        "email": email,
        "roles": roles,
        "iat": now,
        "exp": now + expires_delta,
    }
    headers = {"kid": kid}
    token = jwt.encode(payload, private_key, algorithm="RS256", headers=headers)
    return token