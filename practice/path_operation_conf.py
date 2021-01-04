from typing import Optional, Set

from fastapi import FastAPI, status
from pydantic import BaseModel

app =FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = []

@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED) #status code添加在路由器上會返回到前端
async def create_itema(item: Item):
    return item

# --------------
# add tags
@app.post("/itemsb/", response_model=Item, tags=['items'])
async def create_itemb(item: Item):
    return item

@app.get("/itemsb/", tags=["items"])
async def read_items():
    return [{"name":"foo", "price":42}]

@app.get("/usersb/", tags=["users"])
async def read_users():
    return [{"username":"johndoe"}]

# --------------
# add summary&dexcription
@app.post(
    "/itemsc/",
    response_model=Item,
    summary="Create an Item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_itemc(item: Item):
    return item

# -------------
# add docstring
@app.post(
    "/itemsd/",
    response_model=Item,
    summary="Create a item"
    )
async def create_itemd(item: Item):
    """
    Create an item with all the information:
    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item

# -----------
# add deprecated = eliminated 
@app.post(
    "/itemse/",
    response_model=Item,
    summary="Create a item",
    response_description="The created item",
)
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item

# -------------

@app.get("/elements/", tags=["needless"], deprecated=True)
async def read_elements():
    return [{"item_id":"Foo"}]
