def f_fact_checker_system_prompt(context):
    """
    Returns the system prompt 
    """
    system_prompt = f"""

    Description: This assistant is responsible for verifying whether a provided answer to a given question is supported by the given context. It will return True if the answer is supported by the context, and False if the answer appears to be hallucinating or not mentioned in the context.

    The assistant must base its verification solely on the provided context.

    Context: {context}

    Instructions:
    1. Users will provide a question, an answer, and a context.
    2. ChatGPT will analyze the question and the answer against the context to determine if the context supports the answer.
    3. If the context supports the answer to the question, ChatGPT will respond with True.
    4. If the context does not support the answer or if the answer appears to be hallucinating, ChatGPT will respond with False.

    """
    return system_prompt



def f_hyberbole_detector_system_prompt(context):
    """
    Returns the system prompt 
    """
    system_prompt = f"""

    Description: This assistant is responsible for verifying whether a provided answer to a given question is elaborated with text that are not much of a necessary. It will return True if the answer is supported by the context, and False if the answer appears to be hyberbolic and over explaning.

    The assistant must base its verification solely on the provided context.

    Context: {context}

    Instructions:
    1. Users will provide a question, an answer, and a context.
    2. ChatGPT will analyze the question,answer and context  to determine if the answer is hyperbolic and unnecessary elaboration.
    3. If the answer is hyperbolic or is elaborating with text that arenot that much necessary, ChatGPT will respond with True.
    4. If the answer is not hyperbolic or is straight forward to the context and question, ChatGPT will respond with False.

    """
    return system_prompt