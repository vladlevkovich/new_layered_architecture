from datetime import datetime
from typing import Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .jwt_auth import auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, str]:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Cloud not validate credentials",
    )
    payload = auth.decode_token(token)
    if datetime.utcnow() >= datetime.utcfromtimestamp(payload["exp"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    user_id = payload.get("id")
    if user_id is None:
        raise credential_exception
    return payload
