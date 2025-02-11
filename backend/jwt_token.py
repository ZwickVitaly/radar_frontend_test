import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Request
from settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def create_jwt_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    tkn = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    if isinstance(tkn, bytes):
        tkn = tkn.decode("utf-8")

    return tkn


def decode_jwt_token(token: str) -> dict:
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(request: Request):
    token = request.cookies.get("Authorization")

    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization token")

    if token.startswith("Bearer "):
        token = token.split(" ")[1]

    token_dict = decode_jwt_token(token)
    return int(token_dict.get("sub"))
