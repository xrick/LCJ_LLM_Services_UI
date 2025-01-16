import openai
from typing import List, Dict, AsyncGenerator


class AIChatService:
    def __init__(self, api_key: str):
        # 初始化 OpenAI API 密鑰
        openai.api_key = api_key

    #ref: https://stackoverflow.com/questions/77505030/openai-api-error-you-tried-to-access-openai-chatcompletion-but-this-is-no-lon
    async def generate(self, message: str, history: List[Dict[str, str]] = None, model: str = "gpt-4") -> str:
        """
        使用 OpenAI ChatCompletion API 生成 AI 回應（非流式）
        :param message: 用戶當前輸入的消息
        :param history: 聊天歷史（默認為空）
        :param model: 使用的模型（默認為 "gpt-4"）
        :return: AI 的回應
        """
        try:
            # 構建消息列表
            messages = [{"role": "system", "content": "You are a helpful assistant."}]
            if history:
                messages.extend(history)
            messages.append({"role": "user", "content": message})

            # 調用 ChatCompletion API
            #{"detail":"Error generating AI response: Missing required arguments; Expected either ('messages' and 'model') or ('messages', 'model' and 'stream') arguments to be given"}(
            response = openai.chat.completions.create(
                model="gpt-4",#"gpt-3.5-turbo",
                messages=messages,
                # content= messages,
                # role= "user",
                temperature=0.7,
                max_tokens=500,
            )
            # response = await openai.ChatCompletion.acreate(
            #     #model=model,
            #     model="gpt-3.5-turbo-1106",
            #     messages=messages,
            #     temperature=0.7,  # 可調整生成文本的隨機性
            #     max_tokens=500,  # 限制生成的最大 token 數
            # )

            # 提取回應文本
            # return response["choices"][0]["message"]["content"].strip()
            #{"detail":"Error generating AI response: Error code: 400 - {'error': {'message': \"Missing required parameter: 'messages[0].content[0].type'.\", 'type': 'invalid_request_error', 'param': 'messages[0].content[0].type', 'code': 'missing_required_parameter'}}"}(
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"Error generating AI response: {e}")

    async def generate_stream(self, message: str, history: List[Dict[str, str]] = None, model: str = "gpt-4") -> AsyncGenerator[str, None]:
        """
        使用 OpenAI ChatCompletion API 生成流式 AI 回應

        :param message: 用戶當前輸入的消息
        :param history: 聊天歷史（默認為空）
        :param model: 使用的模型（默認為 "gpt-4"）
        :return: 逐步生成的回應（生成器）
        """
        try:
            # 構建消息列表
            messages = [{"role": "system", "content": "You are a helpful assistant."}]
            if history:
                messages.extend(history)
            messages.append({"role": "user", "content": message})

            # 調用流式 ChatCompletion API
            response = await openai.ChatCompletion.acreate(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
                stream=True,  # 啟用流式回應
            )

            # 流式回應生成器
            async for chunk in response:
                yield chunk["choices"][0]["delta"]["content"]
        except Exception as e:
            raise RuntimeError(f"Error generating AI response: {e}")
