import os
import json
import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, HTMLResponse
from app.ai_chat_service import AIChatService
from pathlib import Path
from dotenv import load_dotenv

app = FastAPI()

# 設置模板目錄
templates = Jinja2Templates(directory="templates")

# 設置靜態文件目錄
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize AI-Chatservice
load_dotenv()
_api_key = os.getenv("OPENAI_API_KEY")
if not _api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")
print(f"api_key is {_api_key}")
ai_chat_service = None

@app.on_event("startup")
async def startup_event():
    global ai_chat_service
    try:
        # 如果 AIChatService 是同步初始化，直接實例化
        ai_chat_service = AIChatService(_api_key)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize AIChatService: {e}")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/ai-chat", response_class=HTMLResponse)
async def get_chat_template(request: Request):
    return templates.TemplateResponse("ai-chat.html", {"request": request})

@app.get("/chat-content", response_class=HTMLResponse)
async def get_chat_content(request: Request):
    # 返回聊天框模板
    return templates.TemplateResponse("chat-content.html", {"request": request})

@app.post("/api/ai-chat")
async def api_ai_chat(request: Request):
    try:
        # 從請求中提取用戶消息
        data = await request.json()
        message = data.get("message")
        thread_id = data.get("thread_id")  # 可選的 thread_id，用於多線程支持

        if not message:
            raise HTTPException(status_code=400, detail="Message is required")

        # 如果沒有 thread_id，創建一個新的對話線程
        if not thread_id:
            thread_id = await ai_chat_service.create_thread()

        # 調用 AIChatService 的生成方法
        ai_response = await ai_chat_service.generate(thread_id, message)

        # 返回 AI 的回應
        return {
            "thread_id": thread_id,
            "response": ai_response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat/thread")
async def create_thread():
    try:
        thread_id = await ai_chat_service.create_thread()
        return {"thread_id": thread_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chat/history/{thread_id}")
async def get_chat_history(thread_id: str):
    try:
        messages = await ai_chat_service.get_messages(thread_id)
        return {"messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add new endpoints for run status and cancellation
@app.get("/api/chat/status/{thread_id}")
async def get_run_status(thread_id: str):
    try:
        status = await ai_chat_service.get_run_status(thread_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat/cancel/{thread_id}")
async def cancel_run(thread_id: str):
    try:
        result = await ai_chat_service.cancel_run(thread_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
