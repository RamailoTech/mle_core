from .connectors.db import PostgresConnector, MongoConnector
from mle_core.connectors.llm.openai_connector import OpenAIConnector
from mle_core.connectors.llm.azure_connector import AzureAIConnector
from mle_core.connectors.llm.anthropic_connector import AnthropicConnector


def get_db_connector(db_type):
    if db_type == "postgres":
        return PostgresConnector()
    elif db_type == "mongo":
        return MongoConnector()
    else:
        raise ValueError("Unsupported database type")

def get_llm_connector(llm_type):
    if llm_type == "openai":
        return OpenAIConnector()
    elif llm_type == "azure":
        return AzureAIConnector()
    elif llm_type == "anthropic":
        return AnthropicConnector()
    else:
        raise ValueError("Unsupported LLM type")
