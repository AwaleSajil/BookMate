from abc import ABC, abstractmethod


class BaseModel(ABC):
    @abstractmethod
    def save(self):
        """Save the object to the database."""
        pass

    @abstractmethod
    def delete(self):
        """Delete the object from the database."""
        pass
