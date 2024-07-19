from __future__ import print_function
import json
import language_tool_python
import ProWritingAidSDK
from ProWritingAidSDK.rest import ApiException
import os


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





def check_grammar_prowriter(json_data):
    configuration = ProWritingAidSDK.Configuration()
    configuration.host = 'https://api.prowritingaid.com'
    configuration.api_key['licenseCode'] = os.environ.get('PROWRITINGAID_API_KEY')
    api_instance = ProWritingAidSDK.TextApi(ProWritingAidSDK.ApiClient('https://api.prowritingaid.com'))
    
    def extract_text(data):
        if isinstance(data, dict):
            for value in data.values():
                yield from extract_text(value)
        elif isinstance(data, list):
            for item in data:
                yield from extract_text(item)
        elif isinstance(data, str):
            yield data

    # Extract text values
    text_values = list(extract_text(json_data))
    
    results = []
    
    for text in text_values:
        try:
            api_request = ProWritingAidSDK.TextAnalysisRequest(
                text,["grammar"],"General","en"
            )
            api_response = api_instance.post(api_request)
            for tag in api_response.result.tags:
                results.append({
                    "sentence": text,
                    "hint": tag.hint,
                    "error_location": f"Start: {tag.start_pos}, End: {tag.end_pos}",
                    "subcategory": tag.subcategory,
                    "suggestions": tag.suggestions,
                    "report": tag.report,
                })
        except ApiException as e:
            print("Exception when calling API: %s\n" % e)
            results.append({
                "sentence": text,
                "hint": "API call failed",
                "error_location": ""
            })

    return results