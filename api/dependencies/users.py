from datetime import datetime

from fastapi import Request, HTTPException, Depends, status
from jose import jwt, JWTError
from starlette.responses import JSONResponse, RedirectResponse

from config.config import settings
from db.repositories.user import UserRepository


def get_token(request: Request):
    token = request.session.get("session")

    if not token:
        return JSONResponse(status_code=401, content={"detail": "Токен отсутствует"})
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.KEY, settings.ALGORITHM)
    except JWTError:
        return HTTPException(status_code=401, detail="Неверный формат токена")

    expire: str = payload.get("exp")
    if not expire or int(expire) < datetime.utcnow().timestamp():
        return HTTPException(status_code=401, detail="Токен истек")

    user_id: str = payload.get("sub")
    if not user_id:
        return HTTPException(status_code=401, detail="Неверный логин или пароль")

    user = await UserRepository.get_by_id(int(user_id))

    return user
