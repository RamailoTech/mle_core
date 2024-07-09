from mle_core.chat import ChatService

import asyncio
from dotenv import load_dotenv
from mle_core.chat.chat_service import ChatService

load_dotenv()


async def main():
    llm_type='openai' # or "azure" or "anthropic"
    chat_service = ChatService(llm_type)

    method = 'sync'  # or async
    response_method = 'invoke'  # or "batch" or "stream"
    system_message = 'You are a helpful assistant.'
    user_message = 'What is the weather like today?'
    model_name = "gpt-3.5-turbo"
    input = {
        "system_message": system_message,
        "user_message": user_message
    }
    if method == "sync":
        response = chat_service.get_sync_response(
        response_method, 
        input, 
        model_name=model_name, 
        temperature=0.2, 
        max_tokens=1000, 
        is_structured=False, 
        pydantic_model=None)
        print(response)

    elif method == "async":
        response = await chat_service.get_async_response(
        response_method, 
        input, 
        model_name=model_name, 
        temperature=0.2, 
        max_tokens=1000,
        is_structured=False, 
        pydantic_model=None)
        print(response)


asyncio.run(main())
