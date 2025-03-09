from pydantic import BaseModel

# Define the User model
class User(BaseModel):
    usename: str
    password: str


