import json
import language_tool_python

class JsonGrammarChecker:
    def __init__(self, json_data, keywords=None):
        if isinstance(json_data, str):
            self.data = json.loads(json_data)
        elif isinstance(json_data, dict):
            self.data = json_data
        else:
            raise ValueError("json_data must be a string or a dictionary")
        
        self.keywords = keywords if keywords is not None else []
        self.tool = language_tool_python.LanguageTool('en-US')

    def check_text(self, text):
        """Check spelling and grammar for a given text, ignoring specified keywords."""
        matches = self.tool.check(text)
        filtered_matches = [m for m in matches if not any(kw.lower() in m.context.lower() for kw in self.keywords)]
        return filtered_matches

    def check_json_for_errors(self):
        errors = {}

        for key, value in self.data.items():
            if isinstance(value, str):
                matches = self.check_text(value)
                if matches:
                    errors[key] = [{"message": m.message, "offset": m.offset} for m in matches]

        return errors

    def close(self):
        self.tool.close()

