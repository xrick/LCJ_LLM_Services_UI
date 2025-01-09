from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse
from fastapi.responses import JSONResponse
from openai import AsyncOpenAI
import json
import logging
import uuid
from typing import Dict, List

logger = logging.getLogger(__name__)

class AIChatService:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.conversations: Dict[str, List[dict]] = {}


    async def create_thread(self):
        thread_id = str(uuid.uuid4())
        self.conversations[thread_id] = []
        return {"thread_id": thread_id}

    async def chat_message(self, thread_id: str, message: str):
        try:
            if thread_id not in self.conversations:
                self.conversations[thread_id] = []

            self.conversations[thread_id].append({"role": "user", "content": message})

            completion = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.conversations[thread_id],
                stream=True
            )

            async def event_generator():
                assistant_message = ""
                async for chunk in completion:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        assistant_message += content
                        yield {
                            "event": "message",
                            "data": json.dumps({
                                "content": content
                            })
                        }
                
                self.conversations[thread_id].append({
                    "role": "assistant",
                    "content": assistant_message
                })

            return EventSourceResponse(event_generator())

        except Exception as e:
            logger.error(f"Error in chat_message: {str(e)}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={"error": str(e)}
            )
