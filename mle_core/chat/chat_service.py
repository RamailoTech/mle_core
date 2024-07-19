from mle_core.config import get_llm_connector
from mle_core.utils import setup_logging
from langchain_core.prompts import ChatPromptTemplate
from typing import List

# from prompt_optimizer.metric import TokenMetric
# from prompt_optimizer.poptim import EntropyOptim
from langchain.schema import (
    HumanMessage,
    SystemMessage
)

logger = setup_logging()

#TODO add exp handling
class ChatService:
    def __init__(self, llm_type):
        self.llm_connector = get_llm_connector(llm_type)


    def grammar_check(self, prompt):
        """
        Check the grammar of the prompt.
        """
        # Placeholder for grammar check logic
        # This could be an integration with a grammar check API or library
        # apply only if it crossess some threshold value
        return True
    
    def check_keywords(self, prompt):
        # get all the keywords expected in the output
        # check if the keywords are properly defined in the prompt
        # return any(keyword in prompt for keyword in keywords)
        # raise ValueError("Prompt does not contain required keywords.")
        return True
    
    def optimize_prompt(self, prompt):
        """
            Optimize the prompt for the LLM.
            Reduce the number of tokens in the prompt.
            Add more keywords to the prompt.
        """
        optimized_prompt = prompt.strip()
        return optimized_prompt
    
    def validate_prompt(self, prompt):
        """
            Validate the prompt structure or content.
        """
        if not prompt:
            raise ValueError("Prompt cannot be empty.")
        return True

    def validate_example(self, prompt, examples):
        """
            Validate the examples provided.
        """
        if not examples or len(examples) == 0:
            raise ValueError("Cannot accept prompt with examples")
        
        prompt += f"""
            Examples:
            {examples}
        """
        return prompt
    
    def check_test_suite(self, prompt, test_suites):
        """
        Check if a test suite exists for the prompt or example.
        Execute llm using the test suite and fail if it doesn't match with the expected output.
        """
        if not test_suites or len(test_suites) == 0:
            raise ValueError("No test suite provided.")
        return True
    
    def ensure_llm_ready(self, prompt, options={}, tests=[], examples=[]):
        """
            Block LLM calls if the system is not ready.
        """
        grammar_check = options.get("grammar_check", True)
        keyword_check = options.get("keyword_check", True)
        optimize_prompt = options.get("optimize_prompt", True)
        validate_example = options.get("validate_example", True)
        validate_tests = options.get("validate_tests", True)

        try:
            if grammar_check:
                self.grammar_check(prompt)

            if optimize_prompt:
                prompt = self.optimize_prompt(prompt)

            if keyword_check:
                self.check_keywords(prompt)

            if validate_example:
                prompt = self.validate_example(prompt, examples)

            if validate_tests:
                self.check_test_suite(prompt, tests)

            self.validate_prompt(prompt)
        except Exception as e:
            raise RuntimeError("LLM is not ready.", e)
        
        return prompt

    def get_lecl_chain(self, model_name, is_structured=False, pydantic_model=None, **kwargs):
        if is_structured and pydantic_model is None:
            raise ValueError("pydantic_model cannot be None when is_structured is True")

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                ("human", "{user_message}")
            ]
        )
        llm = self.llm_connector.get_connection(model_name=model_name, **kwargs)

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

    def get_response(self, model_params={}, input_params={}, output_params={},options={},  tests=[], examples=[], **kwargs):
        # Extracting input parameters
        system_message = input_params.get("system_message", "")
        user_message = input_params.get("user_message", "")

        # Ensure prompt is ready for llm call
        user_message = self.ensure_llm_ready(user_message, options, tests, examples)

        # Extracting model parameters
        model_name = model_params.get("model_name", "")
        pydantic_model = model_params.get("pydantic_model", None)
        method = model_params.get("method", None)

        # Extracting output parameters
        response_method = output_params.get("response_method", "invoke")
        is_structured = output_params.get("is_structured", False)
        temperature = output_params.get("temperature", 0)
        max_tokens = output_params.get("max_tokens", 1000)

        messages = { "user_message": user_message, "system_message": system_message }
        if method == "sync":
            return self.get_sync_response(
            response_method, 
            messages, 
            model_name, 
            is_structured,
            pydantic_model,
        )
        elif method == "async":
            return self.get_async_response(
                response_method, 
                messages,
                model_name, 
                is_structured, 
                pydantic_model,
            )
        
    def get_sync_response(self, response_method, input, model_name, is_structured=False, pydantic_model=None, **kwargs):
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
                    output_content = s
            if not is_structured:
                return "".join(output_content)
            return output_content
        else:
            raise ValueError("Invalid response_method for sync")

    async def get_async_response(self, response_method, input, model_name, is_structured=False, pydantic_model=None, **kwargs):
        chain = self.get_lecl_chain(model_name=model_name, is_structured=is_structured, pydantic_model=pydantic_model, **kwargs)
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
                    output_content = s      
            if not is_structured:
                return "".join(output_content)    
            return output_content
        else:
            raise ValueError("Invalid response_method for async")
