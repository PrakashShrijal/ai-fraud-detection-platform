from fastapi import APIRouter

from pydantic import BaseModel

from backend.auth.auth_handler import (
    authenticate_user,
    create_access_token
)

router = APIRouter()

class LoginRequest(BaseModel):

    username: str

    password: str

@router.post("/login")
def login(data: LoginRequest):

    user = authenticate_user(
        data.username,
        data.password
    )

    if not user:

        return {
            "error": "Invalid username or password"
        }

    token = create_access_token(
        data={
            "sub": user["username"]
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }