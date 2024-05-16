def handle_llm_response(response):
    """
    Handle the LLM response, extracting the relevant information.
    """
    try:
        return response["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError) as e:
        raise ValueError("Unexpected response format") from e
