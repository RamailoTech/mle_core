import os 
from dotenv import load_dotenv
import openai
from sentence_transformers import SentenceTransformer, util
import pandas as pd

load_dotenv()

# Load OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.api_type = os.environ.get("OPENAI_API_TYPE")



def f_clean_text_for_comparison(text):
    '''
    Function to clean text for comparison
    '''
    return str(text).lower().replace(" ", "").replace("\n", "").replace("\t", "").replace('"','').replace("'","").replace('.toarray()','')

def f_similarity_search(test_cases:list):
    """Process test cases to compare expected and predicted outputs."""
    
    # headers = ['test_id','difficulty', 'expected_output', 'predicted_output', 'output_match_score', 'output_match', 'error']
    # results = []
    # model = SentenceTransformer('all-MiniLM-L6-v2')

    # for test_case in test_cases:
    #     test_id = test_case['test_id']
    #     difficulty = test_case['difficulty']
    #     expected_output = test_case['expected_output']
    #     predicted_output = test_case['predicted_output']

    #     try:
    #         embeddings1 = model.encode(expected_output)
    #         embeddings2 = model.encode(predicted_output)
    #         similarity = util.cos_sim(embeddings1, embeddings2)
    #         similarity_score = similarity.item()  # Convert tensor to float
    #         output_match = True if similarity_score > 0.75 else False

    #         results.append([test_id,  difficulty, expected_output, predicted_output, round(similarity_score, 2), output_match, None])
    #     except Exception as exc:
    #         error = str(exc)
    #         results.append([test_id, difficulty, expected_output, predicted_output, None, False, error])

    return pd.DataFrame(test_cases)