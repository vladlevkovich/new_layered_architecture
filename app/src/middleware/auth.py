from datetime import datetime

from fastapi import HTTPException, Request, status

from app.src.core import auth


def get_current_user(request: Request) -> Request:
    token = request.headers.get("Authorization")
    if token is None or not token.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    token = token.split(" ")[1]

    try:
        payload = auth.decode_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    if datetime.utcnow() >= datetime.utcfromtimestamp(payload["exp"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )

    request.state.user = payload
    return request
