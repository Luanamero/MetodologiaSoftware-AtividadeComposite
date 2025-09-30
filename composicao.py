# composicao.py
from typing import List, Iterable
from componente import ComponenteCadastro
# Importa TODAS as folhas para uso nas restrições de tipo
from folha import FolhaCadastro, ID, DataCadastro, Nome, Telefone, DataAdmissao, Salario, RG, CPF, CNH, CTPS


# ----------------------------------------------------
# ComposicaoCadastro (O COMPOSITE Base)
# ----------------------------------------------------

class ComposicaoCadastro(ComponenteCadastro):
    """
    Representa uma seção ou subseção (Composite).
    Define o comportamento de gerenciamento de filhos.
    """
    def __init__(self, nome: str):
        self.nome = nome
        self.filhos: List[ComponenteCadastro] = [] 

    # Métodos obrigatórios para o Composite
    def adicionar(self, componente: ComponenteCadastro) -> None:
        """Adiciona um componente filho ao composite."""
        self.filhos.append(componente)

    def remover(self, componente: ComponenteCadastro) -> bool:
        """Remove um filho se existir. Retorna True se removeu, False caso contrário."""
        if componente in self.filhos:
            self.filhos.remove(componente)
            return True
        return False
        
    def getFilho(self, indice: int) -> ComponenteCadastro:
        """Retorna o filho pelo índice com mensagem clara em caso de erro."""
        try:
            return self.filhos[indice]
        except IndexError as e:
            raise IndexError(f"Índice {indice} inválido para '{self.nome}', total de filhos: {len(self.filhos)}") from e

    # Alias em estilo PEP8 sem quebrar código existente.
    get_filho = getFilho

    def iter_filhos(self) -> Iterable[ComponenteCadastro]:
        """Iterador somente leitura dos filhos (não expõe a lista interna)."""
        return iter(self.filhos)

    def exibir(self, profundidade=0) -> str:
        indent = '    ' * profundidade
        resultado = f"{indent}* {self.nome.upper()} *"
        
        for componente in self.filhos:
            resultado += "\n" + componente.exibir(profundidade + 1)
            
        return resultado

# ----------------------------------------------------
# CLASSES DE COMPOSIÇÃO PRINCIPAIS (Com Validação de Tipo)
# ----------------------------------------------------

class DadosPessoais(ComposicaoCadastro):
    """
    Restrição: Aceita Nome, Telefone e os Composites Dependentes/Contatos.
    Não aceita ID ou DataCadastro (conforme a estrutura estrita).
    """
    def __init__(self):
        super().__init__("Dados Pessoais")
        
    TIPOS_PERMITIDOS = (Nome, Telefone, 'Dependentes', 'Contatos')  
    def adicionar(self, componente: ComponenteCadastro):
        tipos_permitidos_resolvidos = (Nome, Telefone, Dependentes, Contatos)
        if not isinstance(componente, tipos_permitidos_resolvidos):
            raise TypeError(f"Erro: Componente de tipo {type(componente).__name__} não pode ser adicionado à seção Dados Pessoais.")
        super().adicionar(componente)

class DadosAdmissional(ComposicaoCadastro):
    """
    Restrição: Aceita DataAdmissao, Salario e InformacoesCargo.
    """
    def __init__(self):
        super().__init__("Dados Admissional")
        
    TIPOS_PERMITIDOS = (DataAdmissao, Salario, 'InformacoesCargo')

    def adicionar(self, componente: ComponenteCadastro):
        tipos_permitidos_resolvidos = (DataAdmissao, Salario, InformacoesCargo)
        if not isinstance(componente, tipos_permitidos_resolvidos):
            raise TypeError(f"Erro: Componente de tipo {type(componente).__name__} não pode ser adicionado à seção Dados Admissional.")
        super().adicionar(componente)

class Endereco(ComposicaoCadastro):
    """
    Restrição: Aceita apenas itens FolhaCadastro nomeados 'Residencial' ou 'Comercial'.
    """
    def __init__(self):
        super().__init__("Endereço")
        
    TIPOS_PERMITIDOS_NOMES = {"Residencial", "Comercial"}

    def adicionar(self, componente: ComponenteCadastro):
        if isinstance(componente, FolhaCadastro) and componente.nome in self.TIPOS_PERMITIDOS_NOMES:
            super().adicionar(componente)
            return
        raise TypeError(
            f"Erro: A seção Endereço só aceita 'Residencial' ou 'Comercial'. Recebido: {getattr(componente, 'nome', type(componente).__name__)}"
        )

class Documentos(ComposicaoCadastro):
    """
    Restrição: Aceita apenas RG, CPF, CNH, CTPS.
    """
    def __init__(self):
        super().__init__("Documentos")
        
    TIPOS_PERMITIDOS = (RG, CPF, CNH, CTPS)

    def adicionar(self, componente: ComponenteCadastro):
        if not isinstance(componente, self.TIPOS_PERMITIDOS):
            raise TypeError(f"Erro: Componente de tipo {type(componente).__name__} não pode ser adicionado à seção Documentos.")
            
        super().adicionar(componente)

# ----------------------------------------------------
# CLASSES DE COMPOSIÇÃO ANINHADA (Subseções com Sobrescrita de Restrição)
# ----------------------------------------------------

class Dependentes(DadosPessoais):
    """
    Extends DadosPessoais. Sobrescreve 'adicionar' para aceitar FolhaCadastro.
    """
    def __init__(self):
        ComposicaoCadastro.__init__(self, "Dependentes")
        
    def adicionar(self, componente: ComponenteCadastro):
        """Aceita apenas FolhaCadastro genérico para os dependentes."""
        tipos_permitidos = (FolhaCadastro,) 
        if not isinstance(componente, tipos_permitidos):
            raise TypeError(f"Erro: Componente de tipo {type(componente).__name__} não pode ser adicionado à seção {self.nome}.")
        # Bypass: Chama o adicionar da classe avô (ComposicaoCadastro)
        ComposicaoCadastro.adicionar(self, componente)

class Contatos(DadosPessoais):
    """
    Extends DadosPessoais. Sobrescreve 'adicionar' para aceitar FolhaCadastro.
    """
    def __init__(self):
        ComposicaoCadastro.__init__(self, "Contatos") 
        
    def adicionar(self, componente: ComponenteCadastro):
        """Aceita apenas FolhaCadastro genérico para os contatos (email, etc.)."""
        tipos_permitidos = (FolhaCadastro,) 
        if not isinstance(componente, tipos_permitidos):
            raise TypeError(f"Erro: Componente de tipo {type(componente).__name__} não pode ser adicionado à seção {self.nome}.")
        # Bypass: Chama o adicionar da classe avô (ComposicaoCadastro)
        ComposicaoCadastro.adicionar(self, componente)

class InformacoesCargo(DadosAdmissional):
    """
    Extends DadosAdmissional. Sobrescreve 'adicionar' para aceitar FolhaCadastro.
    """
    def __init__(self):
        ComposicaoCadastro.__init__(self, "Informações de Cargo")
        
    def adicionar(self, componente: ComponenteCadastro):
        """Aceita apenas FolhaCadastro genérico para a função/departamento."""
        tipos_permitidos = (FolhaCadastro,) 
        
        if not isinstance(componente, tipos_permitidos):
            raise TypeError(f"Erro: Componente de tipo {type(componente).__name__} não pode ser adicionado à seção {self.nome}.")
            
        # Bypass: Chama o adicionar da classe avô (ComposicaoCadastro)
        ComposicaoCadastro.adicionar(self, componente)