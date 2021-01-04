from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login/")
async def login(username: str = Form(...),password: str = Form(...)): #form屬於
    return {"username":username,"password":password}