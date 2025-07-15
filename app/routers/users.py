from fastapi import APIRouter,Depends,status,HTTPException
from ..core import oauth2
from .. import schemas,models,utils
from sqlalchemy.orm import Session
from ..core.databases import get_db
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, status, HTTPException
from ..core.redis_conn import redis_client
from ..core.oauth2 import oauth2_scheme  
from ..core.config import settings
from jose import jwt,JWTError
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

router=APIRouter(prefix='/api',
                 tags=["Users"])

@router.post('/register',response_model=schemas.User_info)
def register_user(register:schemas.Register_user,db: Session=Depends(get_db)):

    #Hashing Password
    hashed_password = utils.hashing(register.password)
    register.password = hashed_password
    data=db.query(models.User).filter(models.User.email==register.email,models.User.username==register.username).first()
    
    if data:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="This username or email already exist:) ")
    
    user=models.User(**register.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)          #updates values in python object as well that get creayed in db like timestamps
    return user


@router.post('/login')
def login_user(login:schemas.Login_user,db:Session=Depends(get_db)):
    data=db.query(models.User).filter(models.User.email==login.email).first()
    password=utils.verify_password(login.password,data.password)  
    if not password:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    if not data:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentaials")
            
    access_token= oauth2.create_token(data={"user_id":data.user_id})
    return{"access_token":access_token,"token_type":"bearer token"}
    

@router.post('/logout')
def logout(token: str = Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(token,settings.secret_key,algorithms = [settings.algorithm])
        exp = payload.get("exp")
        if not exp:
            raise HTTPException(status_code=400, detail="Token missing expiration")

        # Calculate TTL (expiration in seconds)
        import time
        ttl = int(exp - time.time())
        if ttl > 0:
            redis_client.setex(token, ttl, "blacklisted")

        return {"message": "Successfully logged out."}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
