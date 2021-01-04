# the file schemas.py with the Pydantic models for reading data when returning it from the API.

from typing import List, Optional
from pydantic import BaseModel

# Create an ItemBase and UserBase Pydantic models (or let's say "schemas") to have common attributes while creating or reading data.


class ItemBase(BaseModel):
    title:str
    description: Optional[str] = None

class ItemCreate(BaseModel):
    pass

class Item(BaseModel):
    id: int
    owner_id: int

    class Config:  # config class is used to configure Pydantic models
        orm_mode=True #Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).
 

class UserBase(BaseModel):
    email: str

class UserCreate(BaseModel):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config: # config class is used to configure Pydantic models
        orm_mode=True  #Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).

    # pydantic model要跟資料庫互動要在設定檔加上orm_mode=true and you can just declare it in the response_model argument in your path operations.



