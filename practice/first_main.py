from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"hello world!"}

@app.get("/say/{data}")
async def say(data: str,q: int):
    return {"data":data,"item":q}

# --------------------------------------- #

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/{item_id}")
async def readItems(item_id: str,q: str=None,short: bool=False): #short參數不能沒有默認值，不然會報錯
    item = {"item_id":item_id}
    if q:
        item.update({"q":q})
    if not short:
        item.update({
            "description":"this is an amazing item which has long description"
        })
    return item
    