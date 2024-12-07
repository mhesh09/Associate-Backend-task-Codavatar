from pydantic import BaseModel,Field,EmailStr

class UserRegistration(BaseModel):
    first_name : str = Field(..., min_length=3)
    last_name : str = Field(..., min_length=3)
    email : EmailStr
    password : str = Field(..., min_length=8, description="Password must be at least 8 characters long.")
    confirm_password : str = Field(..., min_length=8, description="Password must be at least 8 characters long.")

class TokenSchema(BaseModel):
    access_token:str
    refresh_token:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str = Field(..., min_length=8, description="Password must be at least 8 characters long.")