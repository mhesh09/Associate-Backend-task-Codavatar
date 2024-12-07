from fastapi import Request,HTTPException,status
from jose import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .utils import JWT_SECRET_KEY, ALGORITHM

# Now check if token is expired or not.
class JWTBearer(HTTPBearer):
    def __init__(self,auto_error:bool = True):
        super(JWTBearer,self).__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer,self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer" or not self.verify_jwt(credentials.credentials):
                raise credentials_exception
            return credentials.credentials
        else:
            raise credentials_exception
        return await super().__call__(request)
    
    def verify_jwt(self,token:str) -> bool:
        isTokenValid = False
        # print(token)
        try:
            payload = jwt.decode(token,JWT_SECRET_KEY,ALGORITHM)
            if payload:
                isTokenValid=True
        except Exception as e:
            print(f"Unexcepted error: {e}")
            isTokenValid=False
        return isTokenValid

    def retrieve_id_in_token(self,token:str):
        payload = jwt.decode(token,JWT_SECRET_KEY,ALGORITHM)
        return payload["sub"]


jwt_bearer = JWTBearer()