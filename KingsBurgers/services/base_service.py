class BaseService:
    """Base service class following Single Responsibility Principle"""
    
    def __init__(self, repository):
        """Dependency Injection of repository"""
        self.repository = repository
