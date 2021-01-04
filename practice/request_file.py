from fastapi import FastAPI, File, UploadFile
from typing import List
from fastapi.responses import HTMLResponse

app = FastAPI()

# @app.post("/files/")
# async def create_files(file: bytes = File(...)): #跟query、path相同從fastapi繼承的function，要宣告成file bodies要用函數File不然會變查詢參數
#     return {"file_size":len(file)} #fastapi接收到資料會轉換成bytes格式的資料

# @app.post("/uploadfile/")
# async def create_upload_files(file: UploadFile = File(...)): #UploadFile比起bytes有更大的好處在於資料容量大的情況下
#     return {"filename":file.filename}


# --------------------

@app.post("/files/")
async def create_files(files: List[bytes] = File(...)): #files參數以bytes類型的file回傳給server
    return {"file_size":[len(file) for file in files]}

@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)): #files參數以uploadfile方法處理的file回傳給server
    return {"filenames":[file.filename for file in files]}
# ----
# bytes跟uploadfile差異在於，bytes會大量消耗內存，然而uploadfile在處理上更適合大文件，且可以支持異步
# ----
@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)




