from pydantic import BaseModel

class UserRegistration(BaseModel):
    name : str
    username : str
    password : str
    email : str

class UserLogin(BaseModel):
    username : str
    password : str
