from jose import JWTError,jwt
from .config import settings
from .. import schemas
from fastapi import Depends,HTTPException,status
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from .redis_conn import redis_client

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')  #responsible for grabbing token from respective route

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTE = settings.access_token_expiry_minutes

def create_token(data:dict):
    payload=data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTE)
    payload.update({"exp":expire})
    Token=jwt.encode(payload,SECRET_KEY,ALGORITHM)
    return Token

def verify_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms = [ALGORITHM])
        id = payload.get("user_id")

        if id is None:
          raise credentials_exception
        token_data=schemas.Tokendata(user_id=int(id))
        if redis_client.get(token):
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked (user logged out)",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise credentials_exception
    return token_data

def Get_Current_User(Token:str=Depends(oauth2_scheme)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail='Credentials are not authorized',headers={'WWW-AUTHENTICATE':'Bearer'})
    return verify_token(Token,credentials_exception)


