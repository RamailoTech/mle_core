import os
import openai
from .base import BaseLLMConnector

class OpenAIConnector(BaseLLMConnector):
    def __init__(self, api_key=None, model_name="gpt-3.5-turbo"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model_name = model_name
        openai.api_key = self.api_key

    def get_connection(self):
        # No explicit connection needed for OpenAI API
        return openai

    def get_model_response(self, user_prompt, system_prompt, temperature=0, max_tokens=100,stream= False, **kwargs):
        '''
        Function to get model response
        '''
        params = {
            "model": self.model_name,
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": max_tokens,
            "stream": stream
        }
        params.update(kwargs)
        
        response = openai.ChatCompletion.create(**params)
        return response.choices[0].message["content"].strip()
