from datetime import timedelta
import urllib.request
import urllib.parse
import json
import asyncio

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token
from app.core.config import settings

router = APIRouter()

TURNSTILE_VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


def _verify_turnstile_sync(token: str, remote_ip: str | None) -> bool:
    if not settings.TURNSTILE_SECRETKEY:
        return True
    if not token:
        return False
    data = urllib.parse.urlencode({
        "secret": settings.TURNSTILE_SECRETKEY,
        "response": token,
        **({"remoteip": remote_ip} if remote_ip else {}),
    }).encode("utf-8")
    req = urllib.request.Request(
        TURNSTILE_VERIFY_URL,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read().decode())
            return body.get("success") is True
    except Exception:
        return False


@router.post("/token")
async def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    # Only verify Turnstile when client sent X-Turnstile-Token (e.g. frontend). Swagger never sends it → skip.
    turnstile_token = (request.headers.get("X-Turnstile-Token") or "").strip()
    if settings.TURNSTILE_SECRETKEY and turnstile_token:
        remote_ip = request.client.host if request.client else None
        ok = await asyncio.to_thread(_verify_turnstile_sync, turnstile_token, remote_ip)
        if not ok:
            raise HTTPException(
                status_code=400,
                detail="Verification failed. Please complete the challenge and try again.",
            )

    if form_data.username != settings.API_ADMIN_USERNAME:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if form_data.password != settings.API_ADMIN_PASSWORD:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=expires_delta)
    return {"access_token": access_token, "token_type": "bearer"}