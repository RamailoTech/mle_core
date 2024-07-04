
# MLE Core

## Overview

Welcome to the MLE Core repository, maintained by the ML Experts team. This repository contains core modules and utilities necessary for application development. It includes connectors for databases and language model services, a chat service for interacting with LLMs, and various utility functions to aid in development.

## Directory Structure

```
mle_core/
├── __init__.py
├── chat/
│   ├── __init__.py
│   └── chat_service.py
├── connectors/
│   ├── __init__.py
│   ├── base.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── postgres_connector.py
│   │   └── mongo_connector.py
│   └── llm/
│       ├── __init__.py
│       ├── base.py
│       ├── openai_connector.py
│       └── azure_connector.py
├── utils/
│   ├── __init__.py
│   ├── formatting.py
│   ├── logging.py
│   └── response_handling.py
├── config.py
└── main.py
```

## Modules

### Chat

The `chat` module provides a `ChatService` class that simplifies interaction with different language model (LLM) connectors.

- `chat_service.py`: Contains the `ChatService` class for interacting with LLMs.

### Connectors

The `connectors` module includes connectors for various databases and LLMs.

- `base.py`: Defines the abstract base class for connectors.
- `db/`: Contains database connectors.
  - `postgres_connector.py`: Connector for PostgreSQL.
  - `mongo_connector.py`: Connector for MongoDB.
- `llm/`: Contains LLM connectors.
  - `openai_connector.py`: Connector for OpenAI API.
  - `azure_connector.py`: Connector for Azure AI API.

### Utils

The `utils` module contains utility functions that are commonly used across different modules.

- `formatting.py`: Functions for formatting prompts.
- `logging.py`: Functions for setting up logging.
- `response_handling.py`: Functions for handling LLM responses.

### Config

The `config.py` file contains configuration logic to select the appropriate connectors based on the environment or other criteria.



### Installing the Repository

To install the repository, run the following command in the root directory of the project:

```sh
python3 setup.py install
```

## Usage

### Setting Up Environment Variables

Ensure you have the following environment variables set for database and LLM connectors:

For PostgreSQL:
```
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=your_db_host
DATABASE_PORT=your_db_port
DATABASE_NAME=your_db_name
```

For MongoDB:
```
MONGO_URI=your_mongo_uri
MONGO_DB_NAME=your_mongo_db_name
```

For OpenAI:
```
OPENAI_API_KEY=your_openai_api_key
```

For ChatAnthropic:
```
ANTHROPIC_API_KEY=your_anthropic_api_key
```

For Azure AI:
```
AZURE_ENDPOINT=your_azure_endpoint
AZURE_API_KEY=your_azure_api_key
AZURE_DEPLOYMENT_NAME=your_azure_deployment_name
```

### Using the Chat Service

```python
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
```

### Using the Chat Service for structured output

```python
from mle_core.chat import ChatService
import asyncio
from dotenv import load_dotenv
from mle_core.chat.chat_service import ChatService
from langchain_core.pydantic_v1 import BaseModel, Field

load_dotenv()

#create a pydnatic model
class Joke(BaseModel):
    setup: str = Field(description="setup of the joke")
    punchline: str = Field(description="punchline of the joke")

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
            is_structured=True, 
            pydantic_model=Joke)
        print(response)

    elif method == "async":
        response = await chat_service.get_async_response(
            response_method, 
            input, 
            model_name=model_name, 
            temperature=0.2, 
            max_tokens=1000,
            is_structured=True, 
            pydantic_model=Joke)
        print(response)


asyncio.run(main())
```


### Note: Using Chat Service

1. If response_method is "batch" the input should be list of input. 

Example: 
```
system_message = 'You are a helpful assistant.'
input = [{'system_message': system_message, 'user_message': 'Tell me a bear joke.'}, {'system_message': system_message, 'user_message': 'Tell me a cat joke.'}]
```


### Using Database Connectors

```python
from mle_core.config import get_db_connector

def main():
    db_type = "postgres"  # or "mongo"
    db_connector = get_db_connector(db_type)
    db_connection = db_connector.get_connection()
    print(db_connection)

if __name__ == "__main__":
    main()
```

## Contributing

Feel free to contribute by making a pull request. Please ensure your code follows the style guidelines and includes appropriate tests.

## License

This repository is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
