from abc import ABC, abstractmethod

class BaseConnector(ABC):
    @abstractmethod
    def get_connection(self):
        pass
