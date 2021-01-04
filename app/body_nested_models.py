from fastapi import FastAPI, Body
from pydantic import BaseModel, HttpUrl #The string will be checked to be a valid URL, and documented in JSON Schema / OpenAPI as such.
from typing import Optional, List, Set, Dict #從typing導入List、Set

app = FastAPI()

# 
class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = set()
    item: Optional[Image] = None

class NestedItems(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = set()
    items: Optional[List[Image]] = None #把image包成list，items變數就成了key值

class Offer(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    big_items: List[NestedItems] #把進一步把nestedItems包起來


# ---- List --------
class List_Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = [] #將屬性定義為list字段並限定資料類型，也可不限定

# ---- Set ----------
class Set_Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = set() #这样，即使你收到带有重复数据的请求，这些数据也会被转换为一组唯一项。而且，每当你输出该数据时，即使源数据有重复，它们也将作为一组唯一项输出。


@app.put("/list_items/{list_item_id}")
async def list_items(list_item_id: int,List_item: List_Item):
    results = {"list_item_id":list_item_id,"List_item":List_item}
    return results

@app.put("/submodel/{submodel_id}")
async def submodel(submodel_id: int,item: Item):
    results = {"submodel_id":submodel_id,"item":item}
    return results

@app.put("/nested_items/{nested_item_id}")
async def nested_items(nested_item_id: int, nesteditems: NestedItems):
    results = {"nested_item_id":nested_item_id,"nesteditems":nesteditems}
    return results

@app.post("/offer/")
async def create_offer(offer: Offer):
    return offer

@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image]): # 把image包進list做處理
    return images

@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]): #dict的key值為int,value的值為float
    return weights
# 请记住 JSON 仅支持将 str 作为键。

# 但是 Pydantic 具有自动转换数据的功能。

# 这意味着，即使你的 API 客户端只能将字符串作为键发送，只要这些字符串内容仅包含整数，Pydantic 就会对其进行转换并校验。

# 然后你接收的名为 weights 的 dict 实际上将具有 int 类型的键和 float 类型的值。