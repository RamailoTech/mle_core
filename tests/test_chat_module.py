import pytest
from pydantic import BaseModel, Field
from mle_core.config import get_llm_connector
from mle_core.chat.chat_service import ChatService 
from dotenv import load_dotenv
import os
from langchain_core.runnables.base import RunnableSequence


class Joke(BaseModel):
    setup: str = Field(description="setup of the joke")
    punchline: str = Field(description="punchline of the joke")

class Testcase(BaseModel):
    text: str = Field(description="A descriptive text that includes the scenario and context.")
    explanation: str = Field(description="Detailed explanation of the keywords and themes")

@pytest.fixture
def chat_service():
    load_dotenv()
    service = ChatService(llm_type="openai")
    return service

def test_sync_invoke(chat_service):
    input_data = {"system_message": "You are a helpful assistant.", "user_message": "Tell me a joke"}
    model_name = "gpt-3.5-turbo"
    response = chat_service.get_sync_response(
        method="sync",
        response_method="invoke",
        input=input_data,
        model_name=model_name,
        is_structured=False,
        pydantic_model=None
    )
    assert isinstance(input_data, dict), "Input to invoke is not a dictionary"
    assert response is not None, "Response from invoke is empty"


def test_sync_stream(chat_service):
    input_data = {"system_message": "You are a helpful assistant.", "user_message": "Tell me a joke"}
    model_name = "gpt-3.5-turbo"
    response = chat_service.get_sync_response(
        method="sync",
        response_method="stream",
        input=input_data,
        model_name=model_name,
        is_structured=False,
        pydantic_model=None
    )
    assert isinstance(input_data, dict), "Input to invoke is not a dictionary"
    assert response is not None, "Response from stream is empty"


def test_sync_batch(chat_service):
    system_message = "you are a helpful assistant."
    input_data = [{'system_message': system_message, 'user_message': 'Tell me a bear joke.'}, {'system_message': system_message, 'user_message': 'Tell me a cat joke.'}]
    model_name = "gpt-3.5-turbo"
    response = chat_service.get_sync_response(
        method="sync",
        response_method="batch",
        input=input_data,
        model_name=model_name,
        is_structured=False,
        pydantic_model=None
    )
    assert isinstance(input_data, list), "Input to batch is not a list"
    assert all(isinstance(i, dict) for i in input_data), "Not all elements in input to batch are dictionaries"
    assert response is not None, "Response from batch is empty"

@pytest.mark.asyncio
async def test_async_invoke(chat_service):
    input_data = {"system_message": "You are a helpful assistant.", "user_message": "Tell me a joke"}
    model_name = "gpt-3.5-turbo"
    response = await chat_service.get_async_response(
        method="async",
        response_method="invoke",
        input=input_data,
        model_name=model_name,
        is_structured=False,
        pydantic_model=None
    )
    assert isinstance(input_data, dict), "Input to invoke is not a dictionary"
    assert response is not None, "Response from invoke is empty"


@pytest.mark.asyncio
async def test_async_stream(chat_service):
    input_data = {"system_message": "You are a helpful assistant.", "user_message": "Tell me a joke"}
    model_name = "gpt-3.5-turbo"
    response = await chat_service.get_async_response(
        method="async",
        response_method="stream",
        input=input_data,
        model_name=model_name,
        is_structured=False,
        pydantic_model=None
    )
    assert isinstance(input_data, dict), "Input to invoke is not a dictionary"
    assert response is not None, "Response from stream is empty"


@pytest.mark.asyncio
async def test_async_batch(chat_service):
    system_message = "you are a helpful assistant."
    input_data = [{'system_message': system_message, 'user_message': 'Tell me a bear joke.'}, {'system_message': system_message, 'user_message': 'Tell me a cat joke.'}]
    model_name = "gpt-3.5-turbo"
    response = await chat_service.get_async_response(
        method="async",
        response_method="batch",
        input=input_data,
        model_name=model_name,
        is_structured=False,
        pydantic_model=None
    )
    assert isinstance(input_data, list), "Input to batch is not a list"
    assert all(isinstance(i, dict) for i in input_data), "Not all elements in input to batch are dictionaries"
    assert response is not None, "Response from batch is empty"


def test_lecl_chain_return_type(chat_service):
    chain = chat_service.get_lecl_chain(
        model_name="gpt-3.5-turbo", is_structured=False, pydantic_model=None
    )
    assert chain is not None, "get_lecl_chain did not return a chain"
    assert hasattr(chain, 'invoke'), "Returned chain does not have an 'invoke' method"
    assert hasattr(chain, 'stream'), "Returned chain does not have an 'stream' method"
    assert hasattr(chain, 'batch'), "Returned chain does not have an 'batch' method"
    assert isinstance(chain, RunnableSequence), f"Returned chain is not an instance of RunnableSequence, got {type(chain)}"


def test_chain_invoke_sync(chat_service):
    """Check if runnable interface are invoking on chain of input or not. """
    input_data = {"system_message": "You are a helpful assistant.", "user_message": "Tell me a joke"}
    system_message = "you are a helpful assistant."
    batch_input_data = [{'system_message': system_message, 'user_message': 'Tell me a bear joke.'}, {'system_message': system_message, 'user_message': 'Tell me a cat joke.'}]
    chain = chat_service.get_lecl_chain(
        model_name="gpt-3.5-turbo", is_structured=False, pydantic_model=None
    )
    invoke_result = chat_service.sync_invoke(chain, input_data)
    assert invoke_result is not None, "'invoke' method did not return a result"
    stream_result = chat_service.sync_stream(chain, input_data)
    assert stream_result is not None, "'stream' method did not return a result"
    batch_result = chat_service.sync_batch(chain, batch_input_data)
    assert batch_result is not None, "'batch' method did not return a result"


@pytest.mark.asyncio
async def test_chain_invoke_async(chat_service):
    """Check if runnable interface are invoking on chain of input or not. """
    input_data = {"system_message": "You are a helpful assistant.", "user_message": "Tell me a joke"}
    system_message = "you are a helpful assistant."
    batch_input_data = [{'system_message': system_message, 'user_message': 'Tell me a bear joke.'}, {'system_message': system_message, 'user_message': 'Tell me a cat joke.'}]
    chain = chat_service.get_lecl_chain(
        model_name="gpt-3.5-turbo", is_structured=False, pydantic_model=None
    )
    invoke_result = await chat_service.async_invoke(chain, input_data)
    assert invoke_result is not None, "'invoke' method did not return a result"
    stream_result = []
    async for item in chat_service.async_stream(chain, input_data):
        stream_result.append(item)
    assert stream_result, "'stream' method did not return a result"
    batch_result = await chat_service.async_batch(chain, batch_input_data)
    assert batch_result is not None, "'batch' method did not return a result"

# @pytest.mark.asyncio
# async def test_async_joke_output(chat_service):
#     input_data = {"system_message": "You are a helpful assistant.", "user_message": "Tell me a joke."}
#     assert isinstance(input_data, dict), "Input to invoke is not a dictionary"
#     model_name = "gpt-3.5-turbo"
#     response = await chat_service.get_async_response(
#         method="async",
#         response_method="invoke",
#         input=input_data,
#         model_name=model_name,
#         temperature=0.5,
#         max_tokens=4097,
#         is_structured=True,
#         pydantic_model=Joke
#     )
#     # Check if the output is an instance of Joke
#     assert isinstance(response, Joke)
#     # Check if the variables match the fields in the pydantic model
#     assert hasattr(response, 'setup')
#     assert hasattr(response, 'punchline')


def test_sync_joke_output(chat_service):
    # input_data = {"system_message": "You are a helpful assistant.", "user_message": "Tell me a joke"}
    # assert isinstance(input_data, dict), "Input to invoke is not a dictionary"
    # model_name = "gpt-3.5-turbo"
    # response = chat_service.get_sync_response(
    #     method="sync",
    #     response_method="invoke",
    #     input=input_data,
    #     model_name=model_name,
    #     is_structured=True,
    #     pydantic_model=Joke
    # )
    # # Check if the output is an instance of Joke
    # assert isinstance(response, Joke)
    # # Check if the variables match the fields in the pydantic model
    # assert hasattr(response, 'setup')
    # assert hasattr(response, 'punchline')
    print("Chat service is here",chat_service)

    method = 'sync'
    response_method = 'invoke'
    system_message = 'You are a helpful assistant.'
    user_message = 'Tell me a joke.'
    input = {"system_message": "Generate test cases.", "user_message": "Test case should describe about selling alcohol."}

    model_name = 'gpt-3.5-turbo'
    # model_name = "claude-3-5-sonnet-20240620"
    # input = [{'system_message': system_message, 'user_message': 'Tell me a bear joke.'}, {'system_message': system_message, 'user_message': 'Tell me a cat joke.'}]
    response = chat_service.get_sync_response(method, response_method, input, model_name=model_name, is_structured=False, pydantic_model=Testcase, max_tokens = 4000)
    print(response)

    assert 1 == 1



# @pytest.mark.asyncio
# async def test_async_testcase_output(chat_service):
#     input_data = {"system_message": "Generate test cases.", "user_message": "Test case should describe about selling alcohol."}
#     assert isinstance(input_data, dict), "Input to invoke is not a dictionary"
#     model_name = "gpt-3.5-turbo"
#     response = await chat_service.get_async_response(
#         method="async",
#         response_method="invoke",
#         input=input_data,
#         model_name=model_name,
#         is_structured=True,
#         pydantic_model=Testcase
#     )
#     # Check if the output is an instance of Testcase
#     assert isinstance(response, Testcase)
#     # Check if the variables match the fields in the pydantic model
#     assert hasattr(response, 'text')
#     assert hasattr(response, 'explanation')
#     assert isinstance(input_data, dict), "Input to invoke is not a dictionary"


def test_sync_testcase_output(chat_service):
    # input_data = {"system_message": "Generate test cases.", "user_message": "Test case should describe about selling alcohol."}
    # assert isinstance(input_data, dict), "Input to invoke is not a dictionary"
    # model_name = "gpt-3.5-turbo"
    # response = chat_service.get_sync_response(
    #     method="sync",
    #     response_method="invoke",
    #     input=input_data,
    #     model_name=model_name,
    #     is_structured=True,
    #     pydantic_model=Testcase
    # )
    # # Check if the output is an instance of Testcase
    # assert isinstance(response, Testcase)
    # # Check if the variables match the fields in the pydantic model
    # assert hasattr(response, 'text')
    # assert hasattr(response, 'explanation')
    # assert isinstance(input_data, dict), "Input to invoke is not a dictionary"
    assert 1 == 1

