from abc import ABC, abstractmethod

class BaseFileHandler(ABC):
    @abstractmethod
    def extract_text(self, file_path: str) -> str:
        pass