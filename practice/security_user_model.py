from typing import Optional

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # frontend via username&password to get a token 

class User(BaseModel): #create a request's user model
     username: str
     email: Optional[str] = None
     full_name: Optional[str] = None
     disabled: Optional[bool] = None

def fake_decode_token(token): # add fake decode on original user
    return User(
        username=token+"fakedecoded", 
        email="john@example.com",
        full_name="John Doe"
    )

async def get_current_user(token: str=Depends(oauth2_scheme)): #token inherit from oauth2_scheme
    user = fake_decode_token(token) # this token via fake decode function decode and return data
    return user

@app.get("/users/me") # request via this route trigger function beneath
async def read_users_me(current_user: User=Depends(get_current_user)): # current_user inherit from user and return 
    return current_user


    
