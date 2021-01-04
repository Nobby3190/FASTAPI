from fastapi import FastAPI
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class ModelName(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'

app = FastAPI()

# ------------------ #
# 路徑參數
@app.get("/modelname/{model_name}")
async def get_model(model_name: ModelName): # model_name: ModelName 這裡的model_name參數代表ModelName物件裡的objects
    if model_name == ModelName.alexnet:
        return {'model_name':model_name,'message':'Deep Learning FTW'}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

 # --------------- #
 # 查詢參數

fake_item_db = [{"item_name":"foo","item_name":"bar","item_name":"baz"}]

@app.get("/items/")
async def read_item(skip: int=0,limit: int=10):
    return fake_item_db[skip:skip+limit]

@app.get("/items/{items_id}")
async def read_item_id(items_id: str, q: Optional[str]=None):
    if q:
        return {'item_id':items_id,'q':q}
    return {'item_id',items_id}

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int,item_id: str,q: Optional[str]=None,short: bool=False):
    item = {'item_id': item_id,'owner_id':user_id}
    if q:
        item.update({'q':q})
    if not short:
        item.update({'description':"his is an amazing item that has a long description"})
    return item

# @app.get("/items/{item_id}")
# async def read_another_user_item(item_id:str,needy:str): 
#     item = {'item_id':item_id,'needy':needy} # needy為必須參數，如果在url上沒加needy會報錯，因此要在url上設置needy的值
#     return item
    
@app.get("items/{item_id}")
async def read_another_user_item(
    item_id: str, needy: str, skip:int = 0, limit: Optional[int]=None
    ):
    item = {"item_id":item_id,"needy":needy,"skip":skip,"limit":limit}
    return item
    


