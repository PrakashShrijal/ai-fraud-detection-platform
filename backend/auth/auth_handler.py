from datetime import datetime, timedelta

from jose import jwt

SECRET_KEY = "supersecretkey"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Dummy Users Database
fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "admin123"
    }
}

def authenticate_user(username, password):

    user = fake_users_db.get(username)

    if not user:
        return False

    if password != user["password"]:
        return False

    return user

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt