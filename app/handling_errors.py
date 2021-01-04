from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

class UnicornException(Exception): #定義unicorn的exception
    def __init__(self, name: str):
        self.name = name


app = FastAPI()

items = {"foo":'The Foo Wrestlers'}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404, 
            detail="Item not found",
            headers={"X-factor":"There goes my error"} #exception裡根據不同狀況也能自訂header
        ) # raise目的在於舉報異常狀況，不需加參數。這裡的狀況在於舉報httpexception異常就丟404出來
    return {"item":items[item_id]}

# ------------

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):  #
    return JSONResponse(
        status_code=418,
        content={"message":f"Oops!{exc.name} did something. There goes rainbow...."}
    )
    
@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yoro":
        raise UnicornException(name = name)
    return {"unicorn_name": name}


# --------------
# override request validation exceptions

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {'item_id':item_id}
