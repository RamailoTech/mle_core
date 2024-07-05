import json
import language_tool_python

class JsonGrammarChecker:
    def __init__(self, json_data, keywords=None):
        if isinstance(json_data, str):
            self.data = json.loads(json_data)
        elif isinstance(json_data, dict) or isinstance(json_data, list):
            self.data = json_data
        else:
            raise ValueError("json_data must be a string, dictionary, or list")
        
        self.keywords = keywords if keywords is not None else []
        self.tool = language_tool_python.LanguageTool('en-US')

    def check_text(self, text):
        matches = self.tool.check(text)
        filtered_matches = [m for m in matches if not any(kw.lower() in m.context.lower() for kw in self.keywords)]
        return filtered_matches

    def check_json_for_errors(self):
        errors = self._check_recursive(self.data)
        return errors

    def _check_recursive(self, data):
        errors = {}

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    matches = self.check_text(value)
                    if matches:
                        errors[key] = [{
                            "message": m.message,
                            "context": m.context,
                            "offset": m.offset,
                            "category": m.category,
                            "ruleIssueType": m.ruleIssueType,
                            "sentence": m.sentence,
                            "replacements": m.replacements
                        } for m in matches]
                elif isinstance(value, (dict, list)):
                    nested_errors = self._check_recursive(value)
                    if nested_errors:
                        errors[key] = nested_errors

        elif isinstance(data, list):
            for index, item in enumerate(data):
                if isinstance(item, str):
                    matches = self.check_text(item)
                    if matches:
                        errors[index] = [{
                            "message": m.message,
                            "context": m.context,
                            "offset": m.offset,
                            "category": m.category,
                            "ruleIssueType": m.ruleIssueType,
                            "sentence": m.sentence,
                            "replacements": m.replacements
                        } for m in matches]
                elif isinstance(item, (dict, list)):
                    nested_errors = self._check_recursive(item)
                    if nested_errors:
                        errors[index] = nested_errors

        return errors

    def close(self):
        self.tool.close()
