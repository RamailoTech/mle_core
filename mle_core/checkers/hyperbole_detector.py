from mle_core.checkers.prompts import f_hyberbole_detector_system_prompt
from loguru import logger
from mle_core.chat.chat_service import ChatService
import os 


def f_hyperbole_detector(query, context,answer,llm_type='openai', model='gpt-3.5-turbo', method = 'llm') -> bool: 
    """
    Function to check the fact of the query
    Input Args : 
    query : str : The user query
    context : str : The context of the query
    model : str : The model to be used for the fact checking
    method : str : The method to be used for the fact checking. Methods available are 'llm' and 'similarity_check'
    """
    chat_service = ChatService(llm_type)
    if method == 'llm':
        user_prompt = f"question: ```{query} \n answer: {answer}```"
        system_prompt = f_hyberbole_detector_system_prompt(context)
        llm_response =  chat_service.get_response(
                    user_prompt= user_prompt,
                    system_prompt= system_prompt,
                    max_tokens=1000
                    )
        if 'True' in llm_response:
            return True
        else:
            return False

    elif method == 'similarity_check':
        return True
    
    
    
