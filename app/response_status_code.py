from fastapi import FastAPI, status #status module提供所有status code會自動補全
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.post("/items/", status_code = 201) #successful response -> 201
async def create_item(name: str):
    return {"name":name}

@app.post("/items/", status_code = status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name":name}