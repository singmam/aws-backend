from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str


class UserSignup(BaseModel):
    username: str
    password: str
    email: str
