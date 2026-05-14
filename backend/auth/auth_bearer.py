from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jose import jwt, JWTError

from backend.auth.auth_handler import SECRET_KEY, ALGORITHM

class JWTBearer(HTTPBearer):

    async def __call__(self, request: Request):

        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if credentials:

            token = credentials.credentials

            if not self.verify_token(token):

                raise HTTPException(
                    status_code=403,
                    detail="Invalid or expired token"
                )

            return token

        raise HTTPException(
            status_code=403,
            detail="Authorization token required"
        )

    def verify_token(self, token: str):

        try:

            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )
            

            return True

        except JWTError:

            return False