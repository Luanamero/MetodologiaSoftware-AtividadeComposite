# folha.py
from componente import ComponenteCadastro

class FolhaCadastro(ComponenteCadastro):
    """
    Componente Folha Base (Leaf).
    """
    def __init__(self, nome: str, valor=None):
        self.nome = nome
        self.valor = valor

    def exibir(self, profundidade=0) -> str:
        """Implementação do exibir() para itens finais (folhas)."""
        indent = '    ' * profundidade
        info = f"{self.nome}"
        if self.valor is not None:
            info += f": {self.valor}"
        
        return f"{indent}- {info}"

# ----------------------------------------------------
# TODAS AS CLASSES CONCRETAS (Folhas) HERDAM DE FolhaCadastro
# ----------------------------------------------------

class ID(FolhaCadastro):
    def __init__(self, valor):
        super().__init__("ID do Cliente", valor)

class DataCadastro(FolhaCadastro):
    def __init__(self, valor):
        super().__init__("Data de Cadastro", valor)

class Nome(FolhaCadastro):
    def __init__(self, valor):
        super().__init__("Nome Completo", valor)

class Telefone(FolhaCadastro):
    def __init__(self, valor):
        super().__init__("Telefone", valor)

class DataAdmissao(FolhaCadastro):
    def __init__(self, valor):
        super().__init__("Data de Admissão", valor)

class Salario(FolhaCadastro):
    def __init__(self, valor):
        super().__init__("Salário Base", valor)

class RG(FolhaCadastro):
    def __init__(self, numero):
        super().__init__("RG", numero)

class CPF(FolhaCadastro):
    def __init__(self, numero):
        super().__init__("CPF", numero)
        
class CNH(FolhaCadastro):
    def __init__(self, numero):
        super().__init__("CNH", numero)

class CTPS(FolhaCadastro):
    def __init__(self, numero):
        super().__init__("CTPS", numero)