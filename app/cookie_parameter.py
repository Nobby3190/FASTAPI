from fastapi import FastAPI, Cookie
from typing import Optional

app = FastAPI()

@app.get("/items/")
async def read_items(ads_id: Optional[str] = Cookie(None)): # 定義cookie參數的方法跟path、query雷同
    return {"ads_id":ads_id}


