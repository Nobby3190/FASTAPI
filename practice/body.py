from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str
    description: Optional[str]=None
    price: float
    tax: Optional[float]=None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price+item.tax
        item_dict.update({'price_with_tax':price_with_tax})
    return item_dict

@app.put("/items/{item_id}")
async def create_another_item(item_id:int, item:Item):
    return {'item_id':item_id,**item.dict()}
    
@app.put("/another_items/{item_id}")
async def create_another_item(item_id: int, item: Item,q: Optional[str]=None): #item被宣告request的載體，就能從client端收到request接到api
    result = {'item_id':item_id,**item.dict()}
    if q:
        result.update({'q':q}) #update方法 = dictionary版的append
    return result



