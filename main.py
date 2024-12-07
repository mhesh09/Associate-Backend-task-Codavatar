from typing import Optional
from fastapi import FastAPI,Depends,HTTPException,status,Header
from sqlalchemy.orm import Session
from sql_app.database import Base,engine,SessionLocal
from user.models import User
from user.schemas import UserRegistration,TokenSchema,UserLogin
from user.crud import create_user
from telephone.models import VirtualPhoneNumber,CallLog
from user.utils import verify_password,create_access_token,create_refresh_token
from telephone.schemas import VirtualPhoneNumberDetail,VirtualPhoneNumberDetailResponse
from telephone.telephone_crud import create_virtual_phone
from user.auth_bearer import JWTBearer


#Instance of FastAPI
app = FastAPI()

#It creates a Table of User, VirtualPhoneNumber and CallLog
Base.metadata.create_all(bind=engine)

#It provides a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#It retrieves the user id through header
def get_id_from_auth_header(authorization:Optional[str]=Header(None)) -> str:
    if authorization is None:
        return None
    jwt = JWTBearer()
    token_is_valid=jwt.verify_jwt(authorization.split(" ")[1])
    if token_is_valid:
        user_id = jwt.retrieve_id_in_token(authorization.split(" ")[1])
        return user_id
    return None


#Path function for user login
@app.post("/users/login",response_model=TokenSchema)
def login(login:UserLogin,db:Session=Depends(get_db) ):
    login_dict = dict(login)
    user = db.query(User).filter(User.email == login_dict['email']).first()
    if not user or not verify_password(login_dict['password'],user.password):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid username or password"
                            )
    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)

    return {
        "access_token": access,
        "refresh_token": refresh,
    }

#path function for user register
@app.post("/user/register")
async def register(register:UserRegistration,db:Session=Depends(get_db)):
    if register.password != register.confirm_password:
        return{
            "msg":"Password din't match"
        }
    db_user = await create_user(db=db,user=register)
    return {
        "msg":"Successfully! Register"
        }

#path function for creating virtual phone number
@app.post("/create/virtual/phone/number")
async def create_virtual_phone_number(details:VirtualPhoneNumberDetail,db:Session=Depends(get_db),dependencies=Depends(JWTBearer()),user_id:str=Depends(get_id_from_auth_header)):
    db_telephone = await create_virtual_phone(db=db,virtual_phone_number=details,user_id=user_id)
    return {
        "msg":"Successfully! Created Virtual Number"
    }

#path function for retriving phone number
@app.get("/retrieve/virtual/phone/number",response_model=VirtualPhoneNumberDetailResponse)
async def retrieve_virtual_phone_number(db:Session=Depends(get_db),dependencies=Depends(JWTBearer()),userId:str=Depends(get_id_from_auth_header)):
    db_telephone = db.query(VirtualPhoneNumber).filter(VirtualPhoneNumber.user_id==userId).all()
    return {
        "count":len(db_telephone),
        "data": db_telephone
    }