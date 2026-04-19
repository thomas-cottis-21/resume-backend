from __future__ import annotations

import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from passlib.context import CryptContext

from core.config import Settings
from core.exceptions import AuthenticationError

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    return _pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return _pwd_context.verify(plain, hashed)


def generate_refresh_token() -> tuple[str, str]:
    """Return (raw_hex, sha256_hash). Store only the hash; send raw to the client."""
    raw = secrets.token_bytes(32)
    raw_hex = raw.hex()
    token_hash = hashlib.sha256(raw).hexdigest()
    return raw_hex, token_hash


def hash_token(raw_hex: str) -> str:
    return hashlib.sha256(bytes.fromhex(raw_hex)).hexdigest()


def create_access_token(user_id: UUID, roles: list[str], settings: Settings) -> str:
    now = datetime.now(tz=timezone.utc)
    payload = {
        "sub": str(user_id),
        "roles": roles,
        "iat": now,
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str, settings: Settings) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token has expired")
    except jwt.InvalidTokenError:
        raise AuthenticationError("Invalid token")


def generate_oauth_state(settings: Settings) -> str:
    """Return a tamper-evident state string: '{nonce}.{hmac}'."""
    nonce = secrets.token_hex(16)
    sig = hmac.new(settings.jwt_secret.encode(), nonce.encode(), hashlib.sha256).hexdigest()
    return f"{nonce}.{sig}"


def verify_oauth_state(state: str, settings: Settings) -> bool:
    parts = state.split(".", 1)
    if len(parts) != 2:
        return False
    nonce, sig = parts
    expected = hmac.new(settings.jwt_secret.encode(), nonce.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, sig)
