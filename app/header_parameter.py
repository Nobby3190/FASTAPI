from fastapi import FastAPI, Header
from typing import Optional, List

app = FastAPI()

@app.get("/header_items/")
async def read_items(user_agent: Optional[str] = Header(None)):
    return {"user-agent":user_agent}

# ----- strange version -------- 
# 通常header都是以'-'分離的，但python只能允許'_'，所以Header模組提供自動轉換的功能
# 就算參數設user_agent，Header會自動轉換成user-agent

@app.get("/strange_items/") # 如果不想自動轉換 convert_underscores設成False就好
async def read_strange_items(strange_header: Optional[str] = Header(None, convert_underscores=False)):
    return {"strange_header":strange_header}

# Before setting convert_underscores to False, bear in mind that some HTTP proxies and servers disallow the usage of headers with underscores.


@app.get("/duplicate_header_items/")
async def read_duplicate_items(x_token: Optional[List[str]] = Header(None)):
    return {"x-token values":x_token}
    