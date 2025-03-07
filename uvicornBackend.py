from mongoManager import MongoManager
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Initialize the MongoManager
db_password = "0o31l4nD7w5Iz3iy"
db_name = "recyclya"
collection_name = "users"
mongo_manager = MongoManager(db_password, db_name)
mongo_manager.connect()

# Define the User model
class User(BaseModel):
    name: str
    email: str
    age: int

# Define the API endpoints
@app.get("/")
def read_root():
    """
    Root endpoint that returns a simple greeting message.
    """
    return {"Hello": "World"}


@app.get("/users")
def read_users():
    """
    Endpoint to read all users from the MongoDB collection.
    """
    return mongo_manager.read_from_db(collection_name)


@app.post("/users")
def create_user(user: User):
    """
    Endpoint to create a new user in the MongoDB collection.
    Accepts a User model as input and inserts it into the database.
    """
    data = user.model_dump()
    mongo_manager.write_to_db(collection_name, [data])
    return data


@app.delete("/users")
def delete_users():
    """
    Endpoint to delete all users from the MongoDB collection.
    """
    mongo_manager.delete_from_db(collection_name)
    return {"message": "All users deleted!"}


# Run the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

