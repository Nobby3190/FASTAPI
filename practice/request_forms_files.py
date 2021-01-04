from fastapi import FastAPI, UploadFile, File, Form

app = FastAPI()

@app.post("/files/")
async def create_files(
    file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...)
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }
    