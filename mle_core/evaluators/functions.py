import os 
from dotenv import load_dotenv
import openai
from sentence_transformers import SentenceTransformer, util
import pandas as pd

load_dotenv()


def f_clean_text_for_comparison(text):
    '''
    Function to clean text for comparison
    '''
    return str(text).lower().replace(" ", "").replace("\n", "").replace("\t", "").replace('"','').replace("'","").replace('.toarray()','')


def f_similarity_search(expected_output, predicted_output):
    """Process test cases to compare expected and predicted outputs."""
    
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    openai.api_type = os.environ.get("OPENAI_API_TYPE")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    results = []

    try:
        embeddings1 = model.encode(expected_output)
        embeddings2 = model.encode(predicted_output)
        similarity = util.cos_sim(embeddings1, embeddings2)
        similarity_score = similarity.item()  # Convert tensor to float
        output_match = True if similarity_score > 0.75 else False

        results.append({
            "Expected Output": expected_output,
            "Predicted Output": predicted_output,
            "Similarity Score": round(similarity_score, 2),
            "Output Match": output_match
        })
    except Exception as exc:
        error = str(exc)
        results.append({
            "Expected Output": expected_output,
            "Predicted Output": predicted_output,
            "Similarity Score": None,
            "Output Match": False,
            "Error": error
        })

    return pd.DataFrame(results)