import os
import openai
from .base import BaseLLMConnector
from langchain_openai import ChatOpenAI

class OpenAIConnector(BaseLLMConnector):
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def get_connection(self, model_name="gpt-3.5-turbo", **kwargs):
        '''function to return model'''
        params = {
            "model":model_name
        }
        params.update(kwargs)
        llm = ChatOpenAI(**params)
        return llm
