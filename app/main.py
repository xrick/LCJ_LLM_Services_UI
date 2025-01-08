from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

# 設置模板目錄
templates = Jinja2Templates(directory="templates")

# 設置靜態文件目錄（如果需要）
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def home(request: Request):
    # 正確的方式是將 request 作為參數傳遞給 template
    return templates.TemplateResponse("index0108_2.html", {"request": request})

@app.get("/chat")
async def chat(request: Request):
    return templates.TemplateResponse("ai-chat.html", {"request": request})

# 其他路由
@app.get("/writing")
async def writing(request: Request):
    return templates.TemplateResponse("writing.html", {"request": request})

@app.get("/regulations")
async def regulations(request: Request):
    return templates.TemplateResponse("regulations.html", {"request": request})

@app.get("/ebook")
async def ebook(request: Request):
    return templates.TemplateResponse("ebook.html", {"request": request})

# API 路由
@app.post("/api/chat")
async def api_chat(request: Request):
    data = await request.json()
    # 處理聊天邏輯
    return {"response": "這是 AI 的回應"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
