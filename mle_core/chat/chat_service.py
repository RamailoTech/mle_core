from mle_core.config import get_llm_connector
from mle_core.utils import format_prompt, handle_llm_response, setup_logging
from langchain_core.prompts import ChatPromptTemplate

logger = setup_logging()

class ChatService:
    def __init__(self, llm_type):
        self.llm_connector = get_llm_connector(llm_type)

    
    def get_lecl_chain(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system","{system_message}"),
                ("human","{user_message}")
            ]
        )
        llm = self.llm_connector.get_connection()
        chain = prompt | llm #structured output
        return chain
    
    async def async_invoke(self,chain,input):
        return await chain.ainvoke(input)

    async def async_stream(self, chain, input):
        stream_output = await chain.astream(input)
        output_content = []
        async for s in stream_output:
            output_content.append(s.content)
        return output_content


    async def async_batch(self,chain,input):
        return await chain.abatch(input)
    
    def sync_batch(self,chain,input):
        return chain.batch(input)
    
    def sync_invoke(self,chain,input):
        return chain.invoke(input)
    
    def sync_stream(self,chain,input):
        output_content = []
        for s in chain.stream(input):
            output_content.append(s.content)
        return output_content
    
    async def get_response(self,method, response_method, input):
        chain = self.get_lecl_chain()

        if method == "sync":
            if response_method == "invoke":
                response =  self.sync_invoke(chain, input)
                return response.content
            elif response_method == "batch":
                response = self.sync_batch(chain, input)
                return response.content
            elif response_method == "stream":
                return self.sync_stream(chain, input)
            else:
                raise ValueError("Invalid response_method for sync")
        elif method == "async":
            if response_method == "invoke":
                response = await self.async_invoke(chain, input)
                return response.content
            elif response_method == "stream":
                return await self.async_stream(chain, input)
            elif response_method == "batch":
                response = await self.async_batch(chain, input)
                return response.content
            else:
                raise ValueError("Invalid response_method for async")
        
    