import os
from .connectors.db import PostgresConnector, MongoConnector
from .connectors.llm import OpenAIConnector, AzureAIConnector

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
    else:
        raise ValueError("Unsupported LLM type")
