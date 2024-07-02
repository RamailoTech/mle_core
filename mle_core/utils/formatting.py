def format_prompt(system_prompt, user_prompt):
    """
    Format the system and user prompts into a structured format for LLM input.
    """
    return {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }
