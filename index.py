from mle_core.chat import ChatService

import asyncio
from dotenv import load_dotenv
from mle_core.chat.chat_service import ChatService

load_dotenv()


async def main():
    chat_service = ChatService(
        'openai', # or "azure" or "anthropic", 
    )

    model_params = {
        "model_name": "gpt-3.5-turbo",
        "pydantic_model": None,
        "method": "sync",
    }

    input_params = {
        "system_message": 'You are a helpful assistant.',
        "user_message": '''
            What is the weather like today? 
            Ouptut should be in only one word that describes the weather.
        ''',
    }

    output_params = {
        "response_method": 'invoke',
        "is_structured": False,
        "temperature": 0.2,
        "max_tokens": 1000
    }

    options = {
        "grammar_check": True,
        "keyword_check": True,
        "optimize_prompt": True,
        "validate_example": True,
        "validate_tests": True
    }

    tests = [{
        "input": "What is the weather like today?",
        "expected_output": "SUNNY"
    }]

    examples = [
        f"If weather is clear, bright, hot, output should be 'SUNNY'",
        f"If weather is wet, damp, drizzly, output should be 'RAINY'",
    ]

    response = chat_service.get_response(model_params, input_params, output_params,  options, tests, examples)    
    print(response)

asyncio.run(main())
