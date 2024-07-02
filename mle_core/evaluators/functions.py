from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util

load_dotenv()


def f_clean_text_for_comparison(text):
    """
    Function to clean text for comparison
    """
    return (
        str(text)
        .lower()
        .replace(" ", "")
        .replace("\n", "")
        .replace("\t", "")
        .replace('"', "")
        .replace("'", "")
        .replace(".toarray()", "")
    )


def f_similarity_search(expected_output, predicted_output):
    """Process test cases to compare expected and predicted outputs."""

    model = SentenceTransformer("all-MiniLM-L6-v2")

    try:
        embeddings1 = model.encode(expected_output)
        embeddings2 = model.encode(predicted_output)
        similarity = util.cos_sim(embeddings1, embeddings2)
        similarity_score = similarity.item()  # Convert tensor to float
        output_match = True if similarity_score > 0.75 else False

        results = {
            "similarity_score": round(similarity_score, 2),
            "output_match": output_match,
        }

    except Exception as exc:
        error = str(exc)
        results = {"similarity_score": None, "output_match": False}

    return results
