from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True

class UserResponseSchema(BaseModel):
    username: str
    email: str

class UserLoginSchema(BaseModel):
    username: str
    password: str

class UserTokenSchema(BaseModel):
    token: str
    message: str

    class Config:
        orm_mode = True