import pytest
from mle_core.config import get_llm_connector
from mle_core.chat.chat_service import ChatService 
from dotenv import load_dotenv
import os
from langchain_core.runnables.base import RunnableSequence


@pytest.fixture
def chat_service_openai():
    load_dotenv()
    service = ChatService(llm_type="openai")
    return service

@pytest.fixture
def chat_service_anthropic():
    load_dotenv()
    service = ChatService(llm_type="anthropic")
    return service

@pytest.mark.parametrize("fixture_name, model_name", [
    ("chat_service_openai", "gpt-3.5-turbo"),
    ("chat_service_anthropic", "claude-3-5-sonnet-20240620"),
])
def test_sync_invoke(request,fixture_name, model_name):
    chat_service = request.getfixturevalue(fixture_name)
    input_data = {"system_message": "You are a helpful assistant.", "user_message": "Tell me a joke"}
    response = chat_service.get_sync_response(
        response_method="invoke",
        input=input_data,
        model_name=model_name,
        temperature=0.2,
        max_tokens=200,
        is_structured=False,
        pydantic_model=None
    )
    assert isinstance(input_data, dict), "Input to invoke is not a dictionary"
    assert response is not None, "Response from invoke is empty"


@pytest.mark.parametrize("fixture_name, model_name", [
    ("chat_service_openai", "gpt-3.5-turbo"),
    ("chat_service_anthropic", "claude-3-5-sonnet-20240620"),
])
def test_sync_stream(request, fixture_name, model_name):
    chat_service = request.getfixturevalue(fixture_name)
    input_data = {"system_message": "You are a helpful assistant.", "user_message": "Tell me a joke"}
    response = chat_service.get_sync_response(
        response_method="stream",
        input=input_data,
        model_name=model_name,
        temperature=0.2,
        max_tokens=200,
        is_structured=False,
        pydantic_model=None
    )
    assert isinstance(input_data, dict), "Input to invoke is not a dictionary"
    assert response is not None, "Response from stream is empty"


@pytest.mark.parametrize("fixture_name, model_name", [
    ("chat_service_openai", "gpt-3.5-turbo"),
    ("chat_service_anthropic", "claude-3-5-sonnet-20240620"),
])
def test_sync_batch(request,fixture_name,model_name):
    chat_service = request.getfixturevalue(fixture_name)
    system_message = "you are a helpful assistant."
    input_data = [{'system_message': system_message, 'user_message': 'Tell me a bear joke.'}, {'system_message': system_message, 'user_message': 'Tell me a cat joke.'}]
    response = chat_service.get_sync_response(
        response_method="batch",
        input=input_data,
        model_name=model_name,
        is_structured=False,
        pydantic_model=None
    )
    assert isinstance(input_data, list), "Input to batch is not a list"
    assert all(isinstance(i, dict) for i in input_data), "Not all elements in input to batch are dictionaries"
    assert response is not None, "Response from batch is empty"


@pytest.mark.parametrize("fixture_name, model_name", [
    ("chat_service_openai", "gpt-3.5-turbo"),
    ("chat_service_anthropic", "claude-3-5-sonnet-20240620"),
])
@pytest.mark.asyncio
async def test_async_invoke(request,fixture_name,model_name):
    chat_service = request.getfixturevalue(fixture_name)
    input_data = {"system_message": "You are a helpful assistant.", "user_message": "Tell me a joke"}
    response = await chat_service.get_async_response(
        response_method="invoke",
        input=input_data,
        model_name=model_name,
        is_structured=False,
        pydantic_model=None
    )
    assert isinstance(input_data, dict), "Input to invoke is not a dictionary"
    assert response is not None, "Response from invoke is empty"


@pytest.mark.parametrize("fixture_name, model_name", [
    ("chat_service_openai", "gpt-3.5-turbo"),
    ("chat_service_anthropic", "claude-3-5-sonnet-20240620"),
])
@pytest.mark.asyncio
async def test_async_stream(request,fixture_name, model_name):
    chat_service = request.getfixturevalue(fixture_name)
    input_data = {"system_message": "You are a helpful assistant.", "user_message": "Tell me a joke"}
    response = await chat_service.get_async_response(
        response_method="stream",
        input=input_data,
        model_name=model_name,
        is_structured=False,
        pydantic_model=None
    )
    assert isinstance(input_data, dict), "Input to invoke is not a dictionary"
    assert response is not None, "Response from stream is empty"


@pytest.mark.parametrize("fixture_name, model_name", [
    ("chat_service_openai", "gpt-3.5-turbo"),
    ("chat_service_anthropic", "claude-3-5-sonnet-20240620"),
])
@pytest.mark.asyncio
async def test_async_batch(request, fixture_name, model_name):
    chat_service = request.getfixturevalue(fixture_name)
    system_message = "you are a helpful assistant."
    input_data = [{'system_message': system_message, 'user_message': 'Tell me a bear joke.'}, {'system_message': system_message, 'user_message': 'Tell me a cat joke.'}]
    response = await chat_service.get_async_response(
        response_method="batch",
        input=input_data,
        model_name=model_name,
        temperature=0.2,
        max_tokens=300,
        is_structured=False,
        pydantic_model=None
    )
    assert isinstance(input_data, list), "Input to batch is not a list"
    assert all(isinstance(i, dict) for i in input_data), "Not all elements in input to batch are dictionaries"
    assert response is not None, "Response from batch is empty"


@pytest.mark.parametrize("fixture_name, model_name", [
    ("chat_service_openai", "gpt-3.5-turbo"),
    ("chat_service_anthropic", "claude-3-5-sonnet-20240620"),
])
def test_lecl_chain_return_type(request, fixture_name, model_name):
    chat_service = request.getfixturevalue(fixture_name)
    chain = chat_service.get_lecl_chain(
        model_name=model_name, is_structured=False, pydantic_model=None
    )
    assert chain is not None, "get_lecl_chain did not return a chain"
    assert hasattr(chain, 'invoke'), "Returned chain does not have an 'invoke' method"
    assert hasattr(chain, 'stream'), "Returned chain does not have an 'stream' method"
    assert hasattr(chain, 'batch'), "Returned chain does not have an 'batch' method"
    assert isinstance(chain, RunnableSequence), f"Returned chain is not an instance of RunnableSequence, got {type(chain)}"


@pytest.mark.parametrize("fixture_name, model_name", [
    ("chat_service_openai", "gpt-3.5-turbo"),
    ("chat_service_anthropic", "claude-3-5-sonnet-20240620"),
])
def test_chain_invoke_sync(request,fixture_name, model_name):
    """Check if runnable interface are invoking on chain of input or not. """
    chat_service = request.getfixturevalue(fixture_name)
    input_data = {"system_message": "You are a helpful assistant.", "user_message": "Tell me a joke"}
    system_message = "you are a helpful assistant."
    batch_input_data = [{'system_message': system_message, 'user_message': 'Tell me a bear joke.'}, {'system_message': system_message, 'user_message': 'Tell me a cat joke.'}]
    chain = chat_service.get_lecl_chain(
        model_name=model_name, is_structured=False, pydantic_model=None
    )
    invoke_result = chat_service.sync_invoke(chain, input_data)
    assert invoke_result is not None, "'invoke' method did not return a result"
    stream_result = chat_service.sync_stream(chain, input_data)
    assert stream_result is not None, "'stream' method did not return a result"
    batch_result = chat_service.sync_batch(chain, batch_input_data)
    assert batch_result is not None, "'batch' method did not return a result"


@pytest.mark.parametrize("fixture_name, model_name", [
    ("chat_service_openai", "gpt-3.5-turbo"),
    ("chat_service_anthropic", "claude-3-5-sonnet-20240620"),
])
@pytest.mark.asyncio
async def test_chain_invoke_async(request,fixture_name, model_name):
    """Check if runnable interface are invoking on chain of input or not. """
    chat_service = request.getfixturevalue(fixture_name)
    input_data = {"system_message": "You are a helpful assistant.", "user_message": "Tell me a joke"}
    system_message = "you are a helpful assistant."
    batch_input_data = [{'system_message': system_message, 'user_message': 'Tell me a bear joke.'}, {'system_message': system_message, 'user_message': 'Tell me a cat joke.'}]
    chain = chat_service.get_lecl_chain(
        model_name=model_name, is_structured=False, pydantic_model=None
    )
    invoke_result = await chat_service.async_invoke(chain, input_data)
    assert invoke_result is not None, "'invoke' method did not return a result"
    stream_result = []
    async for item in chat_service.async_stream(chain, input_data):
        stream_result.append(item)
    assert stream_result, "'stream' method did not return a result"
    batch_result = await chat_service.async_batch(chain, batch_input_data)
    assert batch_result is not None, "'batch' method did not return a result"


