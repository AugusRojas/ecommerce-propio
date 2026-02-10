from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    email: EmailStr
    first_name: str
    last_name: str
    is_admin: bool

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'
