from mongoManager import MongoManager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import User
from auth import verify_password, get_password_hash, create_access_token, decode_access_token, pwd_context

app = FastAPI()

# Initialize the MongoManager
db_password = "0o31l4nD7w5Iz3iy"
db_name = "recyclya"
collection_name = "users"
mongo_manager = MongoManager(db_password, db_name)
mongo_manager.connect()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Define the API endpoints
@app.get("/")
def read_root():
    """
    Root endpoint that returns a simple greeting message.
    Usage: Send a GET request to the root URL.
    """
    return {"Recyclya backend running": "OK"}, 200


@app.post("/create_user")
def create_user(user: User):
    """
    Endpoint to create a new user in the MongoDB collection.
    Accepts a User model as input and inserts it into the database.
    Usage: Send a POST request to /users with a JSON body containing user details.
    """
    user.password = get_password_hash(user.password)
    data = user.model_dump()
    mongo_manager.write_to_db(collection_name, [data])
    return data, 201


@app.post("/delete_user")
def delete_users(username: str):
    """
    Endpoint to delete user from the MongoDB collection.
    Usage: Send a POST request to /delete_user with a JSON body containing user details.
    """
    deleted_count = mongo_manager.delete_user_from_db(collection_name, username)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"{username} deleted!"}, 200


@app.post("/update_user")
def update_user(username: str, update_data: dict):
    """
    Endpoint to update a user in the MongoDB collection.
    Usage: Send a POST request to /update_user with a JSON body containing user details.
    """
    result = mongo_manager.update_user_in_db(collection_name, username, update_data)
    if result == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"{result} user updated!"}, 200


@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint to login a user and return an access token.
    Usage: Send a POST request to /token with form data containing username and password.
    """
    user = mongo_manager.find_one(collection_name, {"username": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
def read_users_me(token: str = Depends(oauth2_scheme)):
    """
    Endpoint to get the current logged-in user's information.
    Usage: Send a GET request to /users/me with a valid access token.
    """
    username = decode_access_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = mongo_manager.find_one(collection_name, {"username": username})
    return user


