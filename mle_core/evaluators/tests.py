import json
import pandas as pd
from abc import ABC, abstractmethod
from mle_core.evaluators.functions import f_similarity_search

class Evaluator(ABC):
    def __init__(self, input_file_path, function, output_file_path,output_file_type):
        self.input_file_path = input_file_path
        self.function = function
        self.output_file_path = output_file_path
        self.output_file_type = output_file_type
        self.data = None
        
        # Load and validate the JSON upon instantiation
        self.load_and_validate_json()
        
        # Process data right after loading and validation
        self.processed_data = self.process_data()

    def load_and_validate_json(self):
        with open(self.input_file_path, 'r') as file:
            try:
                self.data = json.load(file)
                
                # Validation checks
                assert isinstance(self.data, dict), "JSON must be a dictionary."
                assert "tests" in self.data, '"tests" key not found in JSON.'
                for test in self.data["tests"]:
                    assert "test_id" in test, '"test_id" missing in one of the tests.'
                    assert "difficulty" in test, '"difficulty" missing in one of the tests.'
                
            except json.JSONDecodeError:
                raise ValueError("File is not a valid JSON.")
            except AssertionError as e:
                raise ValueError(str(e))

    def process_data(self):
        if not callable(self.function):
            raise ValueError("Provided function is not callable.")
        
        try:
            if not all(isinstance(test, dict) for test in self.data["tests"]):
                raise ValueError("test_cases should be a list of dictionaries")
            tests_df = pd.DataFrame(self.data["tests"])
            processed_data = self.function(tests_df)
            if not isinstance(processed_data, pd.DataFrame):
                raise ValueError("The function should return a pandas DataFrame.")
            return processed_data
        except Exception as e:
            raise ValueError(f"Error processing data: {str(e)}")

    def output_data(self, data_frame):
        if self.output_file_type == "csv":
            data_frame.to_csv(self.output_file_path, index=False)
        elif self.output_file_type == 'xlsx':
            data_frame.to_excel(self.output_file_path, index=False)
        else:
            raise ValueError("Output file type be a csv or xlsx")

    def execute(self):
        self.output_data(self.processed_data)

if __name__=='__main__':
    input_file_path = 'test_case.json'
    output_file_path = 'output_file.csv'  
    output_file_type = 'csv'

    # Create an instance of the class
    try:
        evaluator = Evaluator(input_file_path, f_similarity_search, output_file_path,output_file_type.lower())
        evaluator.execute()
        print("Processing completed successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
