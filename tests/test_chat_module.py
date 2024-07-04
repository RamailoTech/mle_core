import pytest
from pydantic import BaseModel, Field
from mle_core.config import get_llm_connector
from mle_core.chat.chat_service import ChatService 
from dotenv import load_dotenv
import os

load_dotenv()

class Joke(BaseModel):
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")

class Testcase(BaseModel):
    text: str = Field(description="A descriptive text that includes the scenario and context, clearly containing the instruction.")
    explanation: str = Field(description="Detailed explanation of how the keywords relate to the themes in the given text.")

@pytest.fixture
def chat_service():
    return ChatService(llm_type="openai")

@pytest.mark.asyncio
async def test_async_joke_output(chat_service):
    input_data = {"system_message": "You are a helpful assistant.", "user_message": "Tell me a joke."}
    assert isinstance(input_data, dict), "Input to invoke is not a dictionary"
    model_name = "gpt-3.5-turbo"
    response = await chat_service.get_async_response(
        method="async",
        response_method="invoke",
        input=input_data,
        model_name=model_name,
        temperature=0.5,
        max_tokens=4097,
        is_structured=True,
        pydantic_model=Joke
    )
    # Check if the output is an instance of Joke
    assert isinstance(response, Joke)
    # Check if the variables match the fields in the pydantic model
    assert hasattr(response, 'setup')
    assert hasattr(response, 'punchline')


def test_sync_joke_output(chat_service):
    input_data = {"system_message": "You are a helpful assistant.", "user_message": "Tell me a joke"}
    assert isinstance(input_data, dict), "Input to invoke is not a dictionary"
    model_name = "gpt-3.5-turbo"
    response = chat_service.get_sync_response(
        method="sync",
        response_method="invoke",
        input=input_data,
        model_name=model_name,
        is_structured=True,
        pydantic_model=Joke
    )
    # Check if the output is an instance of Joke
    assert isinstance(response, Joke)
    # Check if the variables match the fields in the pydantic model
    assert hasattr(response, 'setup')
    assert hasattr(response, 'punchline')



@pytest.mark.asyncio
async def test_async_testcase_output(chat_service):
    input_data = {"system_message": "Generate test cases.", "user_message": "Explain the scenario"}
    assert isinstance(input_data, dict), "Input to invoke is not a dictionary"
    model_name = "gpt-3.5-turbo"
    response = await chat_service.get_async_response(
        method="async",
        response_method="invoke",
        input=input_data,
        model_name=model_name,
        is_structured=True,
        pydantic_model=Testcase
    )
    # Check if the output is an instance of Testcase
    assert isinstance(response, Testcase)
    # Check if the variables match the fields in the pydantic model
    assert hasattr(response, 'text')
    assert hasattr(response, 'explanation')
    assert isinstance(input_data, dict), "Input to invoke is not a dictionary"


def test_sync_testcase_output(chat_service):
    input_data = {"system_message": "Generate test cases.", "user_message": "Explain the scenario"}
    assert isinstance(input_data, dict), "Input to invoke is not a dictionary"
    model_name = "gpt-3.5-turbo"
    response = chat_service.get_sync_response(
        method="sync",
        response_method="invoke",
        input=input_data,
        model_name=model_name,
        is_structured=True,
        pydantic_model=Testcase
    )
    # Check if the output is an instance of Testcase
    assert isinstance(response, Testcase)
    # Check if the variables match the fields in the pydantic model
    assert hasattr(response, 'text')
    assert hasattr(response, 'explanation')
    assert isinstance(input_data, dict), "Input to invoke is not a dictionary"

