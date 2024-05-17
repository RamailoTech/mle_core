import json
import pandas as pd
from abc import ABC, abstractmethod
from utility_functions import f_similarity_search

class f_evaluate(ABC):
    def __init__(self, input_path, function, output_path):
        self.input_path = input_path
        self.function = function
        self.output_path = output_path
        self.data = None

    def load_and_validate_json(self):
        with open(self.input_path, 'r') as file:
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
        # Assuming the function expects a list of dictionaries (from JSON) and returns a DataFrame
        if not callable(self.function):
            raise ValueError("Provided function is not callable.")
        
        try:
            
            if not all(isinstance(test, dict) for test in self.data["tests"]):
                  raise ValueError("test_cases should be a list of dictionaries")
            # Convert the list of tests to a DataFrame for processing
            tests_df = pd.DataFrame(self.data["tests"])
            processed_data = self.function(tests_df)
            if not isinstance(processed_data, pd.DataFrame):
                raise ValueError("The function should return a pandas DataFrame.")
            return processed_data
        except Exception as e:
            raise ValueError(f"Error processing data: {str(e)}")

    def output_data(self, data_frame):
        # Determine file extension to decide format
        if self.output_path.endswith('.csv'):
            data_frame.to_csv(self.output_path, index=False)
        elif self.output_path.endswith('.xlsx'):
            data_frame.to_excel(self.output_path, index=False)
        else:
            raise ValueError("Output file must be a .csv or .xlsx")

    def execute(self):
        self.load_and_validate_json()
        processed_data = self.process_data()
        self.output_data(processed_data)



if __name__=='__main__':
    # Execute the workflow
    input_path = 'test_case.json'
    output_path = 'output_file.csv'  

    # Create an instance of the class
    evaluator = f_evaluate(input_path, f_similarity_search, output_path)
    try:
        evaluator.execute()
        print("Processing completed successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")