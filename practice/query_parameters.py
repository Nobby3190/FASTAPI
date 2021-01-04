from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

@app.get("/items/")
async def read_items(q:Optional[str]=None): #查詢參數是optional的，因此可加可不加
    results = {'items':[{'item_id':"Foo","item_id":"Bar"}]}
    if q:
        results.update({'q':q})
    return results

@app.get("/50words_limited_items/") #fastapi提供的query方法添加參數限制條件
async def words_limited_items(q:Optional[str]=Query(None,max_length=50,min_length=3)): 
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/regex_added_items/") #可以直接在Query加上正則表達式
async def regex_added_items(q:Optional[str]=Query(None,min_length=3,max_length=50,regex="^fixedquery$")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/default_items/") #也可以在Query的第一個參數加上預設的默認值，q為默認值為最小長度為3的fixedquery 
async def default_items(q: str = Query("fixedquery",min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/required_in_query_items/") #如果需要在Query宣告必加參數而非預設值則在第一個參數使用...，
async def required_in_query_items(q:str = Query(...,min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/multiple_items/") #查詢參數列表、複數值
async def multiple_items(q:Optional[List[str]] = Query(None)): #用list來接query出來的複數值，List是typing裡的model要先import
    query_items = {"q":q} #因此query出來的結果會是{"q":['a','b','c']}
    return query_items
# @app.get('/multiple_items/') 
# async def multiple_items(q: list = Query([])): #不限定list型態的話可以這麼用
#     query_items = {'q':q}
#     return query_items

@app.get("/default_multiple_items/")
async def default_multiple_items(q: Optional[List[str]] = Query(['bar','Foo'])):
    query_items = {'q':q}
    return query_items


@app.get("/title_description_added_items/")
async def title_description_added_items(
    q: Optional[str] = Query(
        None,
        min_length=3,
        title="Query String",
        description="Query string for the items to search in the database that have a good match"
        )  #添加title跟description在query裡，訊息會生成在openapi裡，由文檔跟用戶介面跟外部工具所使用
    ):
    results = {"items":[{'user_id':"Foo",'item_id':"Bar"}]}
    if q:
        results.update({'q':q})
    return results

@app.get("/alias_items/")
async def alias_items(
    q: Optional[str] = Query(
        None,
        alias="item-query"
    ) # alias參數在url上添加別名用於查詢參數數值
):
    results = {"items":[{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({'q':q})
    return results

@app.get("/abandoned_items/")
async def abandoned_items(
    q: Optional[str] = Query(
        None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        deprecated=True
    )
):
    results = {"items":[{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results