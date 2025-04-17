from abc import ABC, abstractmethod

class BaseRepository(ABC):
    """Interface for repository pattern following Dependency Inversion Principle"""
    
    @abstractmethod
    def get_all(self):
        pass
    
    @abstractmethod
    def get_by_id(self, id):
        pass
    
    @abstractmethod
    def create(self, entity):
        pass
    
    @abstractmethod
    def update(self, entity):
        pass
    
    @abstractmethod
    def delete(self, id):
        pass
