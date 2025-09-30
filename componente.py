# componente.py
from abc import ABC, abstractmethod

class ComponenteCadastro(ABC):
    """
    Interface comum (Componente) para o padrão Composite.
    """
    
    @abstractmethod
    def exibir(self, profundidade=0) -> str:
        """Retorna a representação textual hierárquica do componente.

        profundidade: nível de indentação usado internamente pelo composite.
        """
        raise NotImplementedError("Subclasse deve implementar 'exibir'.")
