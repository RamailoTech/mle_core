from mle_core.checkers.prompts import f_hyperbole_detector_system_prompt
from loguru import logger
from mle_core.chat.chat_service import ChatService
from langchain_core.pydantic_v1 import BaseModel, Field
import os 


class HyperboleOutput(BaseModel):
    output: bool = Field(description='Returns boolean')



def f_hyperbole_detector(query, context,answer,llm_type='openai', model='gpt-3.5-turbo', method = 'llm') -> bool: 

    chat_service = ChatService(llm_type)
    if method == 'llm':
        user_prompt = f"question: ```{query} \n answer: {answer}```"
        system_prompt = f_hyperbole_detector_system_prompt(context)
        input = {
                "system_message": system_prompt,
                "user_message": user_prompt 
            }
        llm_response = chat_service.get_sync_response(
            "invoke", 
            input, 
            model_name="gpt-3.5-turbo",
            temperature=0.2, 
            max_tokens=1000, 
            is_structured=True, 
            pydantic_model=HyperboleOutput)
        return llm_response.output

    elif method == 'similarity_check':
        return True



 