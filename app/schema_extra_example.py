from typing import Optional
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()

# 添加額外信息

class BasicItem(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    class Config: # 1.把添加的信息額外寫個設定檔，此用法常用的慣例是寫於文檔的範例
        schema_extra = {
            "example":{
                "name":"Foo",
                "dexcription":"A very nice Item",
                "price":35.4,
                "tax":3.2,
            }
        }

class FieldItem(BaseModel): # 2.把添加的信息利用Field模組添加進屬性裡
    name: str = Field(...,example="Foo")
    description: Optional[str] = Field(None, example="A very nice Item")
    price: float = Field(...,example=35.4)
    tax: Optional[float] = Field(None, example=3.2)

@app.put("/items/{item_id}") # 1
async def update_item(item_id: int,item: Item):
    results = {"item_id":item_id,"item":item}
    return results

@app.put("/field_items/{field_item_id}") # 2
async def update_field_item(field_item_id: int,fielditem: FieldItem):
    results = {'field_item_id':field_item_id,"fielditem":fielditem}
    return results

@app.put("/body_items/{body_item_id}")
async def body_items(
    body_item_id: int,
    basicitem: BasicItem = Body(
        ...,
        example={
            "name":"Foo",
            "description":"A very nice team",
            "price": 35.4,
            "tax":3.2,
        },
        ) # 3.也可以在body裡額外新增example
    ):
    results = {"body_item_id":body_item_id,"basicitem":basicitem}
    return results

