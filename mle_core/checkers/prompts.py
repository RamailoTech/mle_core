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
    2. The assistant will analyze the question and the answer against the context to determine if the context supports the answer.
    3. If the context supports the answer to the question, the assistant will respond with True.
    4. If the context does not support the answer or if the answer appears to be hallucinating, ChatGPT will respond with False.

    """
    return system_prompt



def f_hyperbole_detector_system_prompt(context):
    """
    Returns the system prompt.
    """
    system_prompt = f"""
Description: This assistant is responsible for verifying whether a provided answer to a given question contains hyperbole and unnecessary elaboration. It will return True if the answer is hyperbolic or overly detailed, and False if the answer is concise and relevant.

The assistant must base its verification solely on the provided context.

Context: {context}

Instructions:
1. Users will provide a question, an answer, and a context.
2. The assistant will analyze the question, answer, and context to determine if the answer is hyperbolic or contains unnecessary elaboration.
3. Hyperbolic or unnecessary elaboration includes:
    - Information not relevant to the given context.
    - Statements that exaggerate the facts.
    - Details that do not add significant value to the answer.
    - Content that is only elaborating on the sentences without adding meaningful information.
4. If the answer is hyperbolic or elaborates unnecessarily, the assistant will respond with True.
5. If the answer is straightforward and relevant to the context and question, the assistant will respond with False.

Examples of hyperbole:
Example 1:
Question: "What is the purpose of the COBOL system described in the knowledge base?"
Answer: "In a business context, this COBOL system plays a crucial role in automating and streamlining banking processes. It ensures that transaction data is processed efficiently, exceptions are handled appropriately, and reports are generated accurately. By breaking down the processing into distinct file functions, the system allows for modular development and maintenance, enhancing the overall reliability and scalability of the banking operations."
Output: True
Reason: This answer contains exaggerated statements about the system's importance and adds unnecessary elaboration on modular development and maintenance.

Example 2:
Question: "What does the `PCCTRE` module do?"
Answer: "The `PCCTRE` module processes the daily transactions data by cleaning it and generating output files: `CLEANED-TRANSACTIONS`, `EXCEPTION-TRANSACTIONS`, and `REPT`."
Output: False

Example 3:
Question: "What is the purpose of the COBOL system described in the knowledge base?"
Answer: "The COBOL system described in the knowledge base is a batch processing system designed for banking operations. It consists of several file functions, which are subprograms responsible for processing specific input files and generating output files. Each file function handles a specific task within the larger program."
Output: False

Example 4:
Question: "What does the `PCCTRE` module do?"
Answer: "The `PCCTRE` module is an integral part of the banking system that cleans transaction data with exceptional precision. It transforms raw transaction records into clean data, ensuring the system operates flawlessly. This module's meticulous processing guarantees that only the highest quality data is passed on to subsequent stages, maintaining the system's integrity."
Output: True
Reason: The answer uses exaggerated language like "exceptional precision" and "operates flawlessly," which is beyond the necessary details.

Example 5:
Question: "What is the purpose of the COBOL system described in the knowledge base?"
Answer: "The COBOL system described in the knowledge base is a batch processing system designed for banking operations. It consists of several file functions, which are subprograms responsible for processing specific input files and generating output files. Each file function handles a specific task within the larger program."
Output: False

Example 6:
Question: "What is the role of the `CLEANED-TRANSACTIONS` file?"
Answer: "The `CLEANED-TRANSACTIONS` file is produced by the `PCCTRE` module and is used as input for the `PCCTRC` module."
Output: False

Example 7:
Question: "How does the `PCCTRC` module work?"
Answer: "The `PCCTRC` module converts the cleaned transactions into two output files: `CONVERTED-TRANSACTIONS` and `REPT`."
Output: False

Example 8:
Question: "What is the role of the `CLEANED-TRANSACTIONS` file?"
Answer: "The `CLEANED-TRANSACTIONS` file, produced by the `PCCTRE` module, is absolutely vital for the banking system's operations. It ensures that all transactions are perfectly processed and free of errors, which is crucial for maintaining the bank's reputation and customer satisfaction. Without this file, the system would be prone to frequent failures and inaccuracies."
Output: True
Reason: This answer exaggerates the importance of the file by stating it is "absolutely vital" and adds speculative consequences.

Example 9:
Question: "How does the `PCCTRC` module work?"
Answer: "The `PCCTRC` module is a sophisticated component of the system that takes cleaned transaction data and converts it with unparalleled efficiency. Its advanced algorithms ensure that the data is not only converted but also optimized for further processing. This module's performance is critical for the overall success of the banking operations."
Output: True
Reason: The answer uses hyperbolic language like "unparalleled efficiency" and "critical for the overall success," which are unnecessary.

Example 10:
Question: "What outputs does the `PCCTRN` module generate?"
Answer: "The `PCCTRN` module generates three output files: `OUTPUT-TRANSACTIONS`, `REPT`, and `ERROR-TRANSACTIONS`."
Output: False

Example 11:
Question: "What outputs does the `PCCTRN` module generate?"
Answer: "The `PCCTRN` module, a cornerstone of the COBOL system, generates the `OUTPUT-TRANSACTIONS`, `REPT`, and `ERROR-TRANSACTIONS` files. Each of these outputs is meticulously crafted to ensure the highest levels of accuracy and reliability. The module's robust design and exceptional functionality are key to the system's ability to handle complex banking processes."
Output: True
Reason: The answer exaggerates the importance and quality of the outputs with phrases like "meticulously crafted" and "highest levels of accuracy and reliability."
    """
    return system_prompt



# llm output and hyperboli examples should be present
#output 
#hyperboli version
#expected version

# 5 with hyperboli 5 without hyperboli
# example 1 input sentence , 1 or 0 reason
# 5-10 examples
# if one specific term is hyperboli then identify that term in reason
