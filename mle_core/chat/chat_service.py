from mle_core.config import get_llm_connector
from mle_core.utils import format_prompt, handle_llm_response, setup_logging

logger = setup_logging()

class ChatService:
    def __init__(self, llm_type):
        self.llm_connector = get_llm_connector(llm_type)

    def get_response(self, user_prompt, system_prompt, temperature=0, max_tokens=100, **kwargs):
        formatted_prompt = format_prompt(system_prompt, user_prompt)
        logger.info(f"Formatted prompt: {formatted_prompt}")

        response = self.llm_connector.get_model_response(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        logger.info(f"Raw response: {response}")
        return handle_llm_response(response)
