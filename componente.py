# componente.py
from abc import ABC, abstractmethod

class ComponenteCadastro(ABC):
    """
    Interface comum (Componente) para o padrão Composite.
    """
    
    @abstractmethod
    def exibir(self, profundidade=0) -> str:
        pass