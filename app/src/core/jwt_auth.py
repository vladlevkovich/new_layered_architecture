from datetime import datetime, timedelta
from typing import Any, Dict, Optional, cast

from fastapi import HTTPException, status
import jwt

from .config import config


class JWTAuth:
    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        expire_minutes: Optional[int] = None,
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def create_access_token(
        self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None
    ) -> str:
        payload = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=1)
        payload.update({"exp": expire})
        access_token: str = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return access_token

    def create_refresh_token(
        self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None
    ) -> str:
        """create access token"""
        payload = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=4)
        payload.update({"exp": expire})
        refresh_token: str = jwt.encode(
            payload, self.secret_key, algorithm=self.algorithm
        )
        return refresh_token

    def decode_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return cast(Dict[str, Any], payload)
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

    def refresh_access_token(self, refresh_token: str) -> str:
        try:
            payload = self.decode_token(refresh_token)

            if "exp" in payload:
                del payload["exp"]

            new_access_token = self.create_access_token(payload)
            return new_access_token

        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )


auth = JWTAuth(secret_key=config.SECRET_KEY, algorithm=config.ALGORITHM)
