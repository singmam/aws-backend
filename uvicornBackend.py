from mongoManager import MongoManager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import User, UserSignup
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
def create_user(user: UserSignup):
    """
    Endpoint to create a new user in the MongoDB collection.
    Accepts a User model as input and inserts it into the database.
    Usage: Send a POST request to /users with a JSON body containing user details.
    """
    user.password = get_password_hash(user.password)
    data = user.model_dump()
    ret = mongo_manager.write_to_db(collection_name, [data])
    if ret == "200":
        return {"message": "User created"}, 200
    else:
        raise HTTPException(status_code=500, detail="Failed to create user")


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
def update_user(username: str, update_data: dict, token: str = Depends(oauth2_scheme)):
    """
    Endpoint to update a user in the MongoDB collection.
    Usage: Send a POST request to /update_user with a JSON body containing user details.
    """
    token_username = decode_access_token(token)
    if token_username is None or token_username != username:
        raise HTTPException(status_code=401, detail="Invalid token or unauthorized")
    
    result = mongo_manager.update_user_in_db(collection_name, username, update_data)
    if result == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"{result} user updated!"}, 200


@app.post("/token") # login endpoint
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


@app.post("/forgot_password")
def forgot_password(username: str, current_password: str, new_password: str):
    """
    Endpoint to reset a user's password.
    Usage: Send a POST request to /forgot_password with a JSON body containing username, current password, and new password.
    """
    user = mongo_manager.find_one(collection_name, {"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(current_password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect current password")
    
    hashed_password = get_password_hash(new_password)
    result = mongo_manager.update_user_in_db(collection_name, username, {"password": hashed_password})
    if result == 0:
        raise HTTPException(status_code=500, detail="Failed to update password")
    
    return {"message": "Password updated successfully!"}, 200


