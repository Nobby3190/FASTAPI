from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import Optional, Union, List

app = FastAPI()

class UserIn(BaseModel): #數據輸入者輸入模型
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None

class UserOut(BaseModel): #數據輸出模型
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserInDb(BaseModel): #數據存入DB模型
    username: str
    hashed_password: str
    email: EmailStr
    full_name: Optional[str] = None

def fake_password_hasher(raw_password: str): #hash成亂碼的模型
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password) #把原密碼透過Fake_Password_Hasher的function hash成亂碼
    user_in_db = UserInDb(**user_in.dict(), hashed_password=hashed_password) # user的資料丟進db裡，因密碼要用hash過的不然駭客就能透過原密碼取得db裡的資料所以要再hash一遍
    print("user saved!.. not really") # 通过以**开头传递给 UserInDB 来使 Python「解包」它
    return user_in_db

@app.post("/user/", response_model = UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

# ---------------------------- #
#減少代碼重複

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserIn(BaseModel):
    password: str

class UserOut(BaseModel):
    pass

class UserInDb(UserBase):
    hashed_password: str

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDb(**user_in.dict(),hashed_password = hashed_password)
    print("User saved! ..not really")
    return user_in_db

@app.get("/user/", response_model= UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved
    
# ---------------------- #
# typing.Union union表示不是a就是b
# union[int,str] 

class BaseItem(BaseModel):
    description: str
    type: str

class CarItem(BaseItem):
    type = "car"

class PlaneItem(BaseItem):
    type = "plane"
    size: int

items = {
    "item1": {"description":"All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}

@app.get("/items/{item_id}", response_model= Union[PlaneItem,CarItem])
async def read_item(item_id: str):
    return items[item_id]
# -----------------------
# 也可以用list包住response的物件傳送

class Item(BaseModel):
    name: str
    description: str


items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]


@app.get("/items/", response_model=List[Item])
async def read_items():
    return items
