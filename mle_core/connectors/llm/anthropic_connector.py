import os
import openai
from .base import BaseLLMConnector
from langchain_anthropic import ChatAnthropic


class AnthropicConnector(BaseLLMConnector):
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        openai.api_key = self.api_key

    def get_connection(
        self, model_name="claude-3-5-sonnet-20240620",**kwargs
    ):
        """function to return model"""
        params = {
            "model": model_name
        }
        params.update(kwargs)
        llm = ChatAnthropic(**params)
        return llm
