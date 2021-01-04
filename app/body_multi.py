from fastapi import FastAPI, Path, Body
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

# ----------------------

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[str]= None

class User(BaseModel):
    username: str
    full_name: Optional[str] = None

# -----------------------
@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(...,title="The ID of the item to get",ge=0,le=1000),
    q: Optional[str] = None,
    item: Optional[Item] = None #通过将默认值设置为 None 来将request参数定義为可选参数
):
    results = {"item_id":item_id}
    if q:
        results.update({'q':q})
    if item:
        results.update({'item':item})
    return results

@app.put("/multi_items/{multi_item_id}")
async def multi_items(multi_item_id:int,item: Item,user: User): # 接收兩個request物件，
    result = {"multi_item_id":multi_item_id,"item": item,"user":user}
    return result
    
@app.put("/importance_items/{importance_item_id}")
async def update_more_items(importance_item_id: int,item: Item,user: User,importance: int= Body(...) ): #額外多增加一個request
    results = {"importance_item_id":importance_item_id,"item": item,"user":user,"importance":importance}
    return results
# 为了扩展先前的模型，你可能决定除了 item 和 user 之外，还想在同一请求体中具有另一个键 importance。
# 如果你就按原样声明它，因为它是一个单一值，FastAPI 将假定它是一个查询参数。
# 但是你可以使用 Body 指示 FastAPI 将其作为请求体的另一个键进行处理。

@app.put("/added_query_request_items/{query_request_item_id}") #同時增加查詢參數&request物件
async def added_query_request_items(
    *,
    query_request_item_id: int,
    item: Item,
    user: User,
    importance: int=Body(...), # 額外增加一個額外的request
    q: Optional[str] = None
):
    results = {'query_request_item_id':query_request_item_id,"item":item,"user":user,"importance":importance}
    if q:
        results.update({'q':q}) # 再新增一個query參數
    return results

@app.put("/embed_items/{embed_item_id}")
async def embed_items(embed_item_id: int,item: Item = Body(...,embed=True)): # 替request物件添加key值
    results = {'embed_item_id':embed_item_id,"item":item}
    return results
    
