def handle_llm_response(response):
    """
    Handle the LLM response, extracting the relevant information.
    If the expected message content is not found, return the entire response.
    """
    try:
        if "choices" in response and response["choices"] and "message" in response["choices"][0] and "content" in response["choices"][0]["message"]:
            return response["choices"][0]["message"]["content"].strip()
        else:
            return response
    except Exception as e:
        raise ValueError("Unexpected response format") from e
