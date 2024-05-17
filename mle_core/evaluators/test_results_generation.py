import json
import pandas as pd
from abc import ABC


class Evaluator(ABC):
    def __init__(self, input_file_path,evaluator_function, output_file_path, output_file_type):
        self.input_file_path = input_file_path
        self.evaluator_function = evaluator_function
        self.output_file_path = output_file_path
        self.output_file_type = output_file_type
        self.data = None
        
        self._load_and_validate_json()
        self._validate_evaluator_function()
        
        
    def _load_and_validate_json(self):
        with open(self.input_file_path, 'r') as file:
            try:
                self.data = json.load(file)
                assert isinstance(self.data, dict), "JSON must be a dictionary."
                assert "tests" in self.data, '"tests" key not found in JSON.'
                if not all(isinstance(test, dict) for test in self.data["tests"]):
                    raise ValueError("Test cases should be a list of dictionaries")

                for test in self.data["tests"]:
                    assert "test_id" in test and "difficulty" in test, 'Missing "test_id" or "difficulty" in one of the tests.'
            except json.JSONDecodeError:
                raise ValueError("File is not a valid JSON.")
            except AssertionError as e:
                raise ValueError(str(e))

    def _validate_evaluator_function(self):
        """ The output of the evaluator function should be a pandas DataFrame """
        
        # check if self.evaluator_function is a function
        if not callable(self.evaluator_function):
            raise ValueError("Evaluator function must be a function")
        

    def _export_output(self):
        if self.output_file_type == "csv":
            self.processed_data.to_csv(self.output_file_path, index=False)
        elif self.output_file_type == 'xlsx':
            self.processed_data.to_excel(self.output_file_path, index=False)
        else:
            raise ValueError("Output file type must be 'csv' or 'xlsx'")

    def execute(self):
        try:
            processed_data = self.evaluator_function(self.data)
            # check if the output of the evaluator function is a pandas dataframe
            assert isinstance(self.processed_data, pd.DataFrame), "Evaluator function must return a pandas DataFrame"
            self.processed_data = processed_data
        except AssertionError as e:
            raise ValueError(str(e))
        self._export_output()

