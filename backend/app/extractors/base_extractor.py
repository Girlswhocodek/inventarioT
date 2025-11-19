from abc import ABC, abstractmethod

class BaseExtractor(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def extract_databases(self):
        """Lista de bases de datos del servidor."""
        pass

    @abstractmethod
    def extract_tables(self, database_name: str):
        pass

    @abstractmethod
    def extract_columns(self, database_name: str, table_name: str):
        pass

    @abstractmethod
    def extract_storage(self):
        """Tamaño del servidor, tablas, índices… dependiendo del gestor."""
        pass
