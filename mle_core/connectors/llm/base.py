from abc import ABC, abstractmethod

class BaseLLMConnector(ABC):
    @abstractmethod
    def get_connection(self):
        pass

