from jose import JWTError, jwt
from fastapi import WebSocketException, status
from sqlalchemy.orm import Session
from .. import models
from .oauth2 import SECRET_KEY, ALGORITHM

def get_user_from_token(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid token payload")

        user = db.query(models.User).filter(models.User.user_id == user_id).first()
        if user is None:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="User not found")
        
        return user

    except JWTError:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Token decode failed")
 