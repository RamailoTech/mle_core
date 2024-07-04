import pytest
import os
from mle_core.connectors.llm.openai_connector import OpenAIConnector
from mle_core.connectors.llm.azure_connector import AzureAIConnector
from mle_core.connectors.llm.anthropic_connector import AnthropicConnector
from unittest.mock import patch, MagicMock

mock_model = MagicMock()

@pytest.fixture
def set_env_vars():
    """Fixture to set environment variables for testing"""
    os.environ["ANTHROPIC_API_KEY"] = "test-anthropic-api-key"
    os.environ["OPENAI_API_KEY"] = "test-openai-api-key"
    os.environ['AZURE_API_KEY'] = 'test-azure-api-key'


# Test for API key correctness from environment
@pytest.mark.parametrize("connector_class, env_var, env_value", [
    (AnthropicConnector, "ANTHROPIC_API_KEY", "test-anthropic-api-key"),
    (AzureAIConnector, "AZURE_API_KEY", "test-azure-api-key"),
    (OpenAIConnector, "OPENAI_API_KEY", "test-openai-api-key")
])
def test_api_key_from_env(connector_class, env_var, env_value, set_env_vars):
    connector = connector_class()
    assert connector.api_key == env_value, f"Expected API key {env_value} from environment, got {connector.api_key}"

# Test for model return
@pytest.mark.parametrize("connector_class", [
    AnthropicConnector,
    AzureAIConnector,
    OpenAIConnector
])
def test_model_return(connector_class, set_env_vars):
    with patch.object(connector_class, 'get_connection', return_value=mock_model) as mock_get_model:
        connector = connector_class()
        model = connector.get_connection()
        mock_get_model.assert_called_once()
        assert model == mock_model, "Expected the mocked model to be returned"



