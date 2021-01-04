# get username&password
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel

# userdata from db
fake_users_db = { 
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()

def fake_hash_password(password: str):
    return "fakehashed" + password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel): #request body
    username: str
    email: Optional[str]=None
    full_name: Optional[str]=None
    disabled: Optional[bool]=None

class UserInDb(User): 
    # check user by password. we always use hashed password to comfirm whether password is right
    # never use plaintext password which ez to stolen
    # If the passwords don't match, we return the same error.
    hashed_password: str

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDb(**user_dict)

def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user

async def get_current_user(token: str= Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}, 
        )
    return user
    #The additional header WWW-Authenticate with value Bearer we are returning here is also part of the spec.
    #Any HTTP (error) status code 401 "UNAUTHORIZED" is supposed to also return a WWW-Authenticate header.
    #In the case of bearer tokens (our case), the value of that header should be Bearer.
    
async def get_current_active_user(current_user: User= Depends(get_current_user)): 
    # we want to get the current user only if user is active
    # So, we create an additional dependency get_current_active_user that in turn uses get_current_user as a dependency.
    # Both of these dependencies will just return an HTTP error if the user doesn't exist, or if is inactive.
    # So, in our endpoint, we will only get a user if the user exists, was correctly authenticated, and is active:
    if current_user.disabled:
        raise HTTPException(
            status_code=400,
            detail="Inactive user",
        )
    return current_user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username) # form field login's username
    if not user_dict:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )
    user = UserInDb(**user_dict) # login's username and his values
    hashed_password = fake_hash_password(form_data.password) # hash password
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            )

    return {"access_token":user.username,"token_type":"bearer"} 
    # return token must be json type
    # It should have a token_type. In our case, as we are using "Bearer" tokens, the token type should be "bearer".
    # And it should have an access_token, with a string containing our access token.
    

@app.get("/users/me")
async def read_users_me(current_user: User=Depends(get_current_active_user)):
    return current_user





