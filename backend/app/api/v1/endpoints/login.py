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


def _is_swagger_or_docs_request(request: Request) -> bool:
    """True if request is from Swagger UI / OpenAPI docs (so we can skip Turnstile)."""
    referer = (request.headers.get("referer") or "").lower()
    return "/admin" in referer or "swagger" in referer or "openapi" in referer


@router.post("/token")
async def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    # Require Turnstile only for non-Swagger requests (Swagger UI cannot send X-Turnstile-Token)
    if settings.TURNSTILE_SECRETKEY and not _is_swagger_or_docs_request(request):
        turnstile_token = request.headers.get("X-Turnstile-Token") or ""
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