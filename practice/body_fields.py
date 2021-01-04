from fastapi import FastAPI, Body
from typing import Optional
from pydantic import Field, BaseModel

app = FastAPI()

class Item(BaseModel): #Field 能定義模型屬性裡的條件，使用方法跟query、body、path在參數上的方法雷同
    name: str
    description: Optional[str] = Field(
        None,
        title="The description of the item",
        max_length=300
    )
    price: float= Field(
        ...,
        gt = 0,
        description="The price must be greater than zero"
    )
    tax: Optional[float] = None

@app.put("/items/{item_id}")
async def update_items(item_id: int,item: Item = Body(...,embed=True)):
    results = {'item_id':item_id,"item":item}
    return results