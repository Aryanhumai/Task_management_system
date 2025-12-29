from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY="secretkey"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRES_IN = timedelta(minutes=30)

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password: str):
    var= pwd_context.hash(password)
    return var

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data: dict,expires_delta: timedelta=None):
    to_encode=data.copy()
    expire = datetime.now() + (expires_delta or  ACCESS_TOKEN_EXPIRES_IN)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, expire