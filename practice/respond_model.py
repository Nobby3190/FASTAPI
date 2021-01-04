from fastapi import FastAPI
from typing import Optional, List
from pydantic import BaseModel, EmailStr

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []

class UserIn(BaseModel): #輸入使用者的模型物件，用此模型輸入數據
    username: str
    password: str
    email: EmailStr 
    full_name: Optional[str] = None

class UserOut(BaseModel): #輸出使用者的模型物件，用此模型輸出數據
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class Default_Items(BaseModel): #含有默認值的model
    name: str
    description: Optional[str] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []


    
@app.post("/items/", response_model= Item) # respond_model屬於http method的參數，不屬於路徑函數的參數
async def create_item(item: Item):
    return item

# 返回輸入的模型數據
# @app.post("/user/", response_model= UserIn) 
# async def create_user(user: UserIn):
#     return user

@app.post("/user/", response_model= UserOut)
async def create_user(user: UserIn):
    return user

# ------------------------ #

default_items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

@app.get("/default_items/{default_item_id}", response_model=Default_Items, response_model_exclude_unset=True)
async def read_items(default_item_id: str):
    return default_items[default_item_id]

# ーーーーーーーーーーーーーーーーーーーーーーー#

# 你还可以使用路径操作装饰器的 response_model_include 和 response_model_exclude 参数。

# 它们接收一个由属性名称 str 组成的 set 来包含（忽略其他的）或者排除（包含其他的）这些属性。

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}

@app.get(
    "/items/{item_id}/name",
    response_model=Default_Items,
    response_model_include={"name","description"} # response_model參數接收資料結構是set，如果誤用list，fastapi可以自動轉成set
)
async def read_item_name(item_id: str):
    return items[item_id]
    
@app.get("/items/{item_id}/public", response_model=Default_Items, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]