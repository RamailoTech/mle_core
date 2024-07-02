from abc import ABC, abstractmethod

class BaseLLMConnector(ABC):
    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def get_model_response(self, *args, **kwargs):
        pass
