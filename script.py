import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# Funções de Manipulação de Dados
# ---------------------------

def carregar_dados(caminho_arquivo: str, nome_planilha: str) -> pd.DataFrame:
    """Carrega dados de um arquivo Excel e substitui NaN por zero."""
    df = pd.read_excel(caminho_arquivo, sheet_name=nome_planilha)
    df.fillna(0, inplace=True)
    return df

def preparar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """Converte data e padroniza nomes de colunas, apenas se ainda não estiverem formatadas."""
    colunas_esperadas = ['DATA', 'LOCAL', 'REFERENCIA', 'SENTIDO', 'INICIO', 'FIM', 'SITUACAO', 'SUB']
    if list(df.columns) != colunas_esperadas:
        df = df.copy()
        df[df.columns[0]] = pd.to_datetime(df[df.columns[0]], errors='coerce')
        df.columns = colunas_esperadas
    return df

def gerar_tabela_enchentes(df: pd.DataFrame) -> pd.DataFrame:
    """Gera tabela com contagem de enchentes por local, ordenada por recorrência e data mais recente."""
    df = preparar_dados(df)
    agrupado = df.groupby('LOCAL').agg({'DATA': ['count', 'max']})
    agrupado.columns = ['OCORRENCIAS', 'DATA_RECENTE']
    agrupado.sort_values(by=['OCORRENCIAS', 'DATA_RECENTE'], ascending=[False, False], inplace=True)
    return agrupado[['OCORRENCIAS']].reset_index()

def filtrar_dados_por_local(df: pd.DataFrame, local: str) -> pd.DataFrame:
    """Filtra os dados para um local específico e adiciona a coluna ANO."""
    df = preparar_dados(df)
    df['ANO'] = df['DATA'].dt.year
    return df[df['LOCAL'] == local]

# ---------------------------
# Funções de Exibição
# ---------------------------

def exibir_tabela_com_indices(tabela: pd.DataFrame, limite: int = 15):
    """Exibe tabela dos locais com maior número de ocorrências."""
    print("\n📊 LOCAIS COM MAIOR NÚMERO DE ENCHENTES (2007–2016)")
    print("-" * 50)
    print(f"{'ÍNDICE':<7} {'LOCAL':<30} OCORRÊNCIAS")
    print("-" * 50)
    for idx, row in tabela.head(limite).iterrows():
        print(f"{idx:<7} {row['LOCAL']:<30} {row['OCORRENCIAS']}")
    print("-" * 50)

def gerar_grafico_ocorrencias(df: pd.DataFrame, local: str):
    """Gera gráfico de ocorrências por ano para um local específico."""
    df_filtrado = filtrar_dados_por_local(df, local)
    ocorrencias_por_ano = df_filtrado.groupby('ANO').size()

    plt.figure(figsize=(10, 5))
    plt.plot(ocorrencias_por_ano.index, ocorrencias_por_ano.values,
             marker='o', linestyle='-', color='royalblue')
    plt.title(f'Ocorrências de Enchentes em "{local}" por Ano')
    plt.xlabel('Ano')
    plt.ylabel('Número de Ocorrências')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# ---------------------------
# Funções de Entrada do Usuário
# ---------------------------

def perguntar_sim_ou_nao(msg: str) -> str:
    """Pergunta sim ou não até resposta válida."""
    while True:
        resposta = input(msg).strip().lower()
        if resposta in ['y', 'n']:
            return resposta
        print("❌ Entrada inválida. Digite 'y' para sim ou 'n' para não.")

def perguntar_indice_valido(max_indice: int) -> int:
    """Pergunta índice numérico válido dentro de um intervalo."""
    while True:
        entrada = input(f"Escolha o índice do local (0 a {max_indice}): ").strip()
        if entrada.isdigit():
            indice = int(entrada)
            if 0 <= indice <= max_indice:
                return indice
        print(f"❌ Índice inválido. Digite um número entre 0 e {max_indice}.")

# ---------------------------
# Código Principal
# ---------------------------

def main():
    caminho = 'C:\\Users\\labsfiap\\Desktop\\NoéEnchentes\\Alagamentos em São Paulo 2007 a 2016.xlsx'
    planilha = 'Plan1'

    df = carregar_dados(caminho, planilha)
    tabela_enchentes = gerar_tabela_enchentes(df)

    exibir_tabela_com_indices(tabela_enchentes, limite=15)

    while True:
        resposta = perguntar_sim_ou_nao("\n🔍 Deseja gerar um gráfico de ocorrências por ano para algum local? (y/n): ")
        if resposta == 'n':
            print("\n✅ Encerrando o programa. Obrigado!")
            break
        indice = perguntar_indice_valido(14)
        local_escolhido = tabela_enchentes.iloc[indice]['LOCAL']
        print(f"\n📈 Gerando gráfico para: {local_escolhido}...\n")
        gerar_grafico_ocorrencias(df, local_escolhido)

# Execução principal
if __name__ == "__main__":
    main()
