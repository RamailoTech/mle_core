from mle_core.config import get_llm_connector
from mle_core.utils import setup_logging
from langchain_core.prompts import ChatPromptTemplate
from typing import List

logger = setup_logging()

class ChatService:
    def __init__(self, llm_type):
        self.llm_connector = get_llm_connector(llm_type)

    def get_lecl_chain(self, model_name, is_structured=False, pydantic_model=None,**kwargs):
        if is_structured and pydantic_model is None:
            raise ValueError("pydantic_model cannot be None when is_structured is True")
        
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                ("human", "{user_message}")
            ]
        )
        llm = self.llm_connector.get_connection(model_name=model_name,**kwargs)
        
        if is_structured and pydantic_model is not None:
            llm = llm.with_structured_output(pydantic_model)
        
        
        chain = prompt | llm
        return chain
    
    async def async_invoke(self, chain, input):
        return await chain.ainvoke(input)

    async def async_stream(self, chain, input):
        async for s in chain.astream(input):
            yield s     

    async def async_batch(self, chain, inputs: List[dict]):
        return await chain.abatch(inputs)

    def sync_batch(self, chain, inputs: List[dict]):
        return chain.batch(inputs)

    def sync_invoke(self, chain, input):
        return chain.invoke(input)

    def sync_stream(self, chain, input):
        for s in chain.stream(input):
            yield s   

    def get_sync_response(self, method, response_method, input, model_name, is_structured=False, pydantic_model=None, **kwargs):
        chain = self.get_lecl_chain(model_name=model_name, is_structured=is_structured, pydantic_model=pydantic_model, **kwargs)
        if response_method == "invoke":
            response = self.sync_invoke(chain, input)
            if not is_structured:
                response = response.content
            return response
        elif response_method == "batch":
            response = self.sync_batch(chain, input)
            if not is_structured:
                response = [msg.content for msg in response]
            return response
        elif response_method == "stream":
            output_content = []
            for s in self.sync_stream(chain, input):
                if not is_structured:
                    output_content.append(s.content)
                else:
                    output_content=s
            if not is_structured:
                return "".join(output_content)
            return output_content
        else:
            raise ValueError("Invalid response_method for sync")


    async def get_async_response(self, method, response_method, input, model_name, is_structured=False, pydantic_model=None,  **kwargs):
        chain = self.get_lecl_chain(model_name=model_name, is_structured=is_structured, pydantic_model=pydantic_model,**kwargs)
        if response_method == "invoke":
            response = await self.async_invoke(chain, input)
            if not is_structured:
                response = response.content
            return response
        elif response_method == "batch":
            response = await self.async_batch(chain, input)
            if not is_structured:
                response = [msg.content for msg in response]
            return response

        elif response_method == "stream":
            output_content = []
            async for s in self.async_stream(chain, input):
                if not is_structured:
                    output_content.append(s.content)
                else:
                    output_content=s      
            if not is_structured:
                return "".join(output_content)    
            return output_content
        else:
            raise ValueError("Invalid response_method for async")
