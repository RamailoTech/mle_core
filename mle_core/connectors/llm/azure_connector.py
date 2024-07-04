import os
from .base import BaseLLMConnector
from langchain_openai import AzureChatOpenAI


class AzureAIConnector(BaseLLMConnector):
    def __init__(self, endpoint=None, api_key=None, deployment_name=None):
        self.endpoint = endpoint or os.environ.get("AZURE_ENDPOINT")
        self.api_key = api_key or os.environ.get("AZURE_API_KEY")
        self.deployment_name = deployment_name or os.environ.get("AZURE_DEPLOYMENT_NAME")
        
    def get_connection(self, api_version = "2024-05-01-preview", **kwargs):
        """function to return model"""
        params = {
            "azure_deployment":self.deployment_name,
            "api_version":api_version
        }
        params.update(kwargs)
        llm = AzureChatOpenAI(**kwargs)
        return llm

    