from fastapi import FastAPI, Query, Path
from typing import Optional

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(...,title="The Id of the item to get"), #Path因為是必須的所以就算第一個參數放None或其他默認值也不會有影響
    q: Optional[str] = Query(None,alias="query string"),
):
    results = {"item_id":item_id}
    if q:
        results.update({'q':q})
    return results
    
@app.get("/unsorted_items/{unsorted_item_id}")
async def unsorted_items(
    q:str, #如果將帶有「默认值」的参数放在没有「默认值」的参数之前，Python 将会报错。
    sorted_item_id:int=Path(..., title="The ID of the item to get"), 
):
    results = {'unsorted_item_id':unsorted_item_id}
    if q:
        results.update({'q':q})
    return results

@app.get("/sorted_items/{sorted_items}") #如果想不按順序必須要在首個參數定義為多參數，Python不會對*做任何事情
async def sorted_items(
    *, #調用kwargs關鍵字參數
    item_id: int = Path(..., title="The ID of the item to get"),
    q:str
):
    results = {'unsorted_item_id':unsorted_item_id}
    if q:
        results.update({'q':q})
    return results

@app.get("/greater_than_items/{ge_item_id}") #限定路徑參數數值
async def greater_than_items(
    *,
    ge_item_id:int = Path(...,title="this is a greater than item",ge=1,le=1000), #ge=1 表示ge_item_id數值至少大於等於1
    q:str                                                                        #le=1000 表示小於等於1000
):
    results = {"ge_item_id":ge_item_id}
    if q:
        results.update({'q':q})
    return results

@app.get("/greater_than_float_items/{ge_float_item_id}") # 限定路徑參數浮點數的數值
async def greater_than_float_items(
    *,
    ge_float_item_id:int=Path(...,title=None,gt=1,le=100),
    q:str,
    size: float=Query(...,gt=0,le=10.5) # 預設一定放第一個參數
):
    results = {'ge_float_item_id':ge_float_item_id}
    if q:
        results.update({'q':q})
    return results
