from typing import List, Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: float = 10.5
    tags: List[str] = []

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

# ------ put 全部更新

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded

# -------- patch 部份更新
# 如果只想更新items裡"bar"的name、description、price
# Using Pydantic's exclude_unset parameter

@app.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data) # items[item_id]之下多個值，回傳的類型應該是dict
    update_item = item.dict(exclude_unset = True) # exclude_unset不會回傳包含有設default的值
    updated_item = stored_item_model.copy(update=update_item) # 把update_item更新的值設成update複製到stored_item_model
    items[item_id] = jsonable_encoder(updated_item) # 在編碼成json回傳
    return updated_item
    

