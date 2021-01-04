from typing import Optional
from datetime import datetime

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fake_db = {} #assume a fake db

class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Optional[str] = None

app =FastAPI()

@app.put("/items/{id}")
def update_item(id: str,item: Item):
    json_compatible_item_data = jsonable_encoder(item) #把Item的類型轉換成json，datetime的資料類型會變字串
    fake_db[id] = json_compatible_item_data

