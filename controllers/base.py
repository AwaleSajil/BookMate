from abc import ABC, abstractmethod


class BaseModel(ABC):
    """
    Abstract base class for all models in the application.

    This class enforces the implementation of `save` and `delete` methods in
    derived classes. These methods are essential for managing the persistence
    of objects in the SQLite database.

    Methods:
        - save(): Abstract method to save the object to the database.
        - delete(): Abstract method to delete the object from the database.
    """

    @abstractmethod
    def save(self):
        """
        Save the object to the database.

        Each subclass must implement this method to define how the object
        should be persisted in the database.
        """
        pass

    @abstractmethod
    def delete(self):
        """
        Delete the object from the database.

        Each subclass must implement this method to define how the object
        should be removed from the database.
        """
        pass