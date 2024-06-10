import json
import language_tool_python

def check_json_for_errors(json_data, keywords=None):

    if isinstance(json_data, str):
        data = json.loads(json_data)
    elif isinstance(json_data, dict):
        data = json_data
    else:
        raise ValueError("json_data must be a string or a dictionary")
    
    if keywords is None:
        keywords = []
    tool = language_tool_python.LanguageTool('en-US')

    def check_text(text):
        """Check spelling and grammar for a given text, ignoring specified keywords."""
        matches = tool.check(text)
        filtered_matches = [m for m in matches if not any(kw.lower() in m.context.lower() for kw in keywords)]
        return filtered_matches

    errors = {}

    # Check each value in the JSON document
    for key, value in data.items():
        if isinstance(value, str):
            matches = check_text(value)
            if matches:
                errors[key] = [{"message": m.message, "offset": m.offset} for m in matches]

    # Close the LanguageTool instance
    tool.close()

    return errors
