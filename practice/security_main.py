from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") #提供前端使用者透過username&password拿token的url

@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {'token':token}

