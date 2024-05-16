import os
import requests
from .base import BaseLLMConnector

class AzureAIConnector(BaseLLMConnector):
    def __init__(self, endpoint=None, api_key=None, deployment_name=None):
        self.endpoint = endpoint or os.environ.get("AZURE_ENDPOINT")
        self.api_key = api_key or os.environ.get("AZURE_API_KEY")
        self.deployment_name = deployment_name or os.environ.get("AZURE_DEPLOYMENT_NAME")

    def get_connection(self):
        # No explicit connection needed for Azure API
        return {"endpoint": self.endpoint, "api_key": self.api_key}

    def get_model_response(self, user_prompt, system_prompt, temperature=0, max_tokens=100, **kwargs):
        '''
        Function to get model response
        '''
        url = f"{self.endpoint}/openai/deployments/{self.deployment_name}/chat/completions?api-version=2023-05-15"
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }
        data = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        data.update(kwargs)

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
