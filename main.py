# main.py
# Importações de composicao.py
from composicao import (
    DadosPessoais, DadosAdmissional, Endereco, Documentos, ComposicaoCadastro,
    Contatos, Dependentes, InformacoesCargo
)
# Importações de folha.py
from folha import ID, DataCadastro, FolhaCadastro, Nome, Telefone, DataAdmissao, Salario, RG, CPF, CNH, CTPS

def construir_cadastro_colaborador():
    """Monta a estrutura Composite do cadastro do colaborador."""
    
    # Folhas que vão para a raiz (ID e DataCadastro)
    id_colaborador = ID("C001")
    data_cadastro = DataCadastro("2024-01-01")

    # Documentos
    documentos = Documentos()
    documentos.adicionar(RG("MG-12.345.678"))
    documentos.adicionar(CPF("123.456.789-00"))
    documentos.adicionar(CNH("00000000000"))
    documentos.adicionar(CTPS("987654"))

    # Endereco
    endereco = Endereco()
    # Adicionando as folhas de endereço
    endereco.adicionar(FolhaCadastro("Residencial", "Rua das Flores, 100"))
    endereco.adicionar(FolhaCadastro("Comercial", "Av. Brasil, 500"))

    # Dados Admissional
    informacoes_cargo = InformacoesCargo()
    informacoes_cargo.adicionar(FolhaCadastro("Função", "Analista de RH"))
    
    dados_admissional = DadosAdmissional()
    dados_admissional.adicionar(DataAdmissao("2024-01-15"))
    dados_admissional.adicionar(Salario("R$ 5.000,00"))
    dados_admissional.adicionar(informacoes_cargo) 

    # Dados Pessoais
    dependentes = Dependentes()
    dependentes.adicionar(FolhaCadastro("Dependente 1", "João Silva"))
    
    contatos = Contatos()
    contatos.adicionar(FolhaCadastro("Email", "colaborador@empresa.com.br"))

    dados_pessoais = DadosPessoais()
    # Adicionando Nome e Telefone (Folhas)
    dados_pessoais.adicionar(Nome("Fulano de Tal"))
    dados_pessoais.adicionar(Telefone("(31) 98765-4321"))
    
    # Adicionando os sub-Composites
    dados_pessoais.adicionar(contatos) 
    dados_pessoais.adicionar(dependentes)

    # Colaborador (Composição Raiz)
    colaborador = ComposicaoCadastro("CADASTRO COMPLETO DO COLABORADOR") 
    
    colaborador.adicionar(id_colaborador)
    colaborador.adicionar(data_cadastro)
    
    colaborador.adicionar(dados_pessoais)
    colaborador.adicionar(dados_admissional)
    colaborador.adicionar(endereco)
    colaborador.adicionar(documentos)
    
    return colaborador

if __name__ == "__main__":
    cadastro = construir_cadastro_colaborador()
    
    print("--- Chamada Única do método exibir() (Estrutura Fiel ao Diagrama) ---")
    print(cadastro.exibir())
    print("--------------------------------------------------------------------")
    
    # --- Testando a restrição de Dados Pessoais (Agora exclui ID e DataCadastro) ---
    print("\n--- TESTANDO RESTRIÇÕES DE TIPO EM DADOS PESSOAIS ---")
    dados_pessoais = cadastro.getFilho(2) 
    
    # 1. Tenta adicionar ID (Deve falhar)
    try:
        print("1. Tentando adicionar ID em Dados Pessoais...")
        dados_pessoais.adicionar(ID("INV")) 
    except TypeError as e:
        print(f"   [OK] Restrição aplicada: {e}")
        
    # 2. Tenta adicionar Nome (Deve ter sucesso, mas não faremos para manter o teste limpo)
    
    # 3. Tenta adicionar Salario (Deve falhar)
    try:
        print("\n3. Tentando adicionar Salário em Dados Pessoais...")
        dados_pessoais.adicionar(Salario("R$ 10.000"))
    except TypeError as e:
        print(f"   [OK] Restrição aplicada: {e}")