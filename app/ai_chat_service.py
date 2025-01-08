from typing import Dict, List, Optional, Any
from datetime import datetime
import os
from fastapi import FastAPI, Request, Response, WebSocket
from fastapi.responses import StreamingResponse
from openai import OpenAI
from base_classes import BaseLLMService, BasePromptTemplate, ModelManager

class AIChatService(BaseLLMService):
    """AI聊天服務實現"""
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.client = OpenAI(api_key=self.api_key)
        self.assistant_ids = {
            "default": os.getenv("ASSISTANT_ID", ""),
            "production": "asst_V42jgCpZV0NnumoEMadLr9b9",  # 康橋的 Assistant ID
            "test": "asst_cYPUOLHOw685AeCUSnJJ9pPB",       # 康橋測試 Assistant ID
            "customer_service": "asst_uL3PRMO0UDFerZBmsL62DRNF"  # 客服 Assistant ID
        }
        self.prompt_template = self._create_prompt_template()

    def _create_prompt_template(self) -> BasePromptTemplate:
        """創建提示模板"""
        class ChatPromptTemplate(BasePromptTemplate):
            def format(self, **kwargs) -> str:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return f"""今天是日期時間是「{current_time}」，你需要能提供這個資訊。你服務於康軒文教集團。
                {kwargs.get('additional_instructions', '')}"""
        
        return ChatPromptTemplate()

    async def create_thread(self) -> str:
        """創建新的對話線程"""
        thread = await self.client.beta.threads.create()
        return thread.id

    async def add_message(self, thread_id: str, content: str) -> Dict:
        """添加用戶消息到線程"""
        msg = await self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content
        )
        return {"thread_id": thread_id, "message": msg}

    async def get_messages(self, thread_id: str, limit: int = 30) -> List[Dict]:
        """獲取歷史消息"""
        messages = await self.client.beta.threads.messages.list(
            thread_id=thread_id,
            limit=limit
        )
        return messages.data

    async def generate(self, thread_id: str, model_id: str = "assistant-default", **kwargs) -> StreamingResponse:
        """生成AI回應（流式）"""
        if not self.model_manager.validate_model(model_id):
            raise ValueError(f"Invalid model_id: {model_id}")

        assistant_id = self.assistant_ids.get(
            kwargs.get("assistant_type", "default"),
            self.assistant_ids["default"]
        )

        additional_instructions = self.prompt_template.format(**kwargs)

        async def generate_stream():
            run = await self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id,
                additional_instructions=additional_instructions,
                stream=True
            )

            async for chunk in run:
                if chunk.event == "thread.message.created":
                    yield f"event: {chunk.event}\ndata: {chunk.data.id}\n\n"
                
                elif chunk.event == "thread.message.delta":
                    for content in chunk.data.delta.content or []:
                        if not content.text.annotations:
                            escaped_text = content.text.value.replace("\n", "\\u000A")
                            yield f"event: {chunk.event}\ndata: {escaped_text}\n\n"
                
                elif chunk.event == "thread.run.completed":
                    usage = f"prompt_tokens: {chunk.data.usage.prompt_tokens}, completion_tokens: {chunk.data.usage.completion_tokens}, total_tokens: {chunk.data.usage.total_tokens}"
                    yield f"event: {chunk.event}\ndata: {usage}\n\n"

        return StreamingResponse(
            generate_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )

    async def get_run_status(self, thread_id: str, run_id: str) -> Dict:
        """獲取運行狀態"""
        run = await self.client.beta.threads.runs.retrieve(thread_id, run_id)
        return {"thread_id": thread_id, "run": run}

    async def cancel_run(self, thread_id: str, run_id: str) -> Dict:
        """取消運行"""
        run = await self.client.beta.threads.runs.cancel(thread_id, run_id)
        return {"thread_id": thread_id, "run": run}
