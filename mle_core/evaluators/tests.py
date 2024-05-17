import json
import pandas as pd
from abc import ABC
from functions import f_similarity_search

class Evaluator(ABC):
    def __init__(self, input_file_path,test_function, output_file_path, output_file_type):
        self.input_file_path = input_file_path
        self.test_function = test_function
        self.output_file_path = output_file_path
        self.output_file_type = output_file_type
        self.data = None
        
        self.load_and_validate_json()
        

    def load_and_validate_json(self):
        with open(self.input_file_path, 'r') as file:
            try:
                self.data = json.load(file)
                assert isinstance(self.data, dict), "JSON must be a dictionary."
                assert "tests" in self.data, '"tests" key not found in JSON.'
                for test in self.data["tests"]:
                    assert "expected_output" in test and "predicted_output" in test, 'Missing "expected_output" or "predicted_output" in one of the tests.'
            except json.JSONDecodeError:
                raise ValueError("File is not a valid JSON.")
            except AssertionError as e:
                raise ValueError(str(e))

    def process_data(self):
        if not all(isinstance(test, dict) for test in self.data["tests"]):
            raise ValueError("test_cases should be a list of dictionaries")

        results = []
        for test in self.data["tests"]:
            # Here we expect that each test dict contains 'expected_output' and 'predicted_output'.
            if "expected_output" not in test or "predicted_output" not in test:
                raise ValueError("Test cases must contain 'expected_output' and 'predicted_output' keys.")
            
            result = self.test_function(test["expected_output"], test["predicted_output"])
            results.append(result)
            
        if not results:
            raise ValueError("No valid test cases processed.")

        # Concatenate all result dataframes into a single dataframe
        processed_data = pd.concat(results, ignore_index=True)
        if not isinstance(processed_data, pd.DataFrame):
            raise ValueError("The function should return a pandas DataFrame.")
        return processed_data

    

    def output_data(self):
        self.processed_data = self.process_data()
        if self.output_file_type == "csv":
            self.processed_data.to_csv(self.output_file_path, index=False)
        elif self.output_file_type == 'xlsx':
            self.processed_data.to_excel(self.output_file_path, index=False)
        else:
            raise ValueError("Output file type must be 'csv' or 'xlsx'")

    def execute(self):
        self.output_data()

if __name__ == '__main__':
    input_file_path = 'test_case.json'
    output_file_path = 'output_file.csv'
    output_file_type = 'csv'

    try:
        evaluator = Evaluator(input_file_path,f_similarity_search, output_file_path, output_file_type.lower())
        evaluator.execute()
        print("Processing completed successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
