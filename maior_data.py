import pandas as pd
import numpy as np

# Função para carregar e limpar os dados do CSV
def carregar_e_limpar_dados(caminho_csv):
    # Carregar o CSV com a codificação correta e remover espaços nas colunas
    df = pd.read_csv(caminho_csv, delimiter=';', encoding='latin1')
    df.columns = df.columns.str.strip()  # Remover espaços em branco dos nomes das colunas
    
    # Converter colunas numéricas e tratar valores inválidos
    df['Quantidade (kg)'] = pd.to_numeric(df['Quantidade (kg)'], errors='coerce')
    df['Preço Total (R$)'] = pd.to_numeric(df['Preço Total (R$)'], errors='coerce')
    df['Data da Compra'] = pd.to_datetime(df['Data da Compra'], format='%d/%m/%Y')
    
    return df

# Função para calcular o valor de revenda com margem de lucro
def calcular_valor_revenda(df):
    # Gerar uma margem de lucro aleatória entre 30% e 45% para cada produto
    df['Margem de Lucro (%)'] = np.random.uniform(0.30, 0.45, len(df))
    
    # Calcular o valor de revenda
    df['Valor de Revenda (R$)'] = df['Preço Total (R$)'] * (1 + df['Margem de Lucro (%)'])
    
    # Arredondar a margem de lucro e o valor de revenda para 2 casas decimais
    df['Margem de Lucro (%)'] = df['Margem de Lucro (%)'].round(2)
    df['Valor de Revenda (R$)'] = df['Valor de Revenda (R$)'].round(2)
    
    return df

# Função para salvar os dados em um novo arquivo CSV
def salvar_csv(df, caminho_novo_csv):
    # Selecionar as colunas necessárias
    df_selecionado = df[['Data da Compra', 'Quantidade (kg)', 'Nome do Material', 'Margem de Lucro (%)', 'Valor de Revenda (R$)']]
    
    # Salvar os dados em um novo arquivo CSV
    df_selecionado.to_csv(caminho_novo_csv, index=False, sep=';', encoding='latin1')


def data_maior_valor(df):
    # Agrupar por data e somar as quantidades e valores
    vendas_por_data = df.groupby('Data da Compra').agg({
        'Quantidade (kg)': 'sum',
        'Preço Total (R$)': 'sum'
    }).reset_index()

    # Encontrar a data com maior valor arrecadado
    data_maior_valor = vendas_por_data.loc[vendas_por_data['Preço Total (R$)'].idxmax()]
    
    return data_maior_valor

# Função para encontrar os produtos mais vendidos por ano
def produtos_mais_vendidos_por_ano(df):
    # Criar uma nova coluna 'Ano' extraindo o ano da 'Data da Compra'
    df['Ano'] = df['Data da Compra'].dt.year
    
    # Agrupar por ano e material, somando as quantidades
    agrupado_ano = df.groupby(['Ano', 'Nome do Material'])['Quantidade (kg)'].sum()

def calcular_valor_revenda(df):
    # Gerar uma margem de lucro aleatória entre 30% e 45% para cada produto
    df['Margem de Lucro (%)'] = np.random.uniform(0.30, 0.45, len(df))
    
    # Calcular o valor de revenda
    df['Valor de Revenda (R$)'] = df['Preço Total (R$)'] * (1 + df['Margem de Lucro (%)'])
    
    return df[['Nome do Material', 'Preço Total (R$)', 'Margem de Lucro (%)', 'Valor de Revenda (R$)']]

    
    # Encontrar o produto mais vendido por ano
    mais_vendidos_por_ano = agrupado_ano.groupby(level=0).idxmax()
    quantidade_mais_vendidos_por_ano = agrupado_ano.groupby(level=0).max()

    # Exibir resultados para cada ano
    for ano in mais_vendidos_por_ano.index:
        print(f"\nNo ano {ano}, o item mais vendido foi {mais_vendidos_por_ano[ano][1]} com {quantidade_mais_vendidos_por_ano[ano]} kg vendidos.")

# Função principal que carrega o CSV e chama as outras funções
def main():
    caminho_novo_csv = r"F:\coisas de bigdata\outro projeto\vendas_com_valor_revenda.csv"
    
    # Caminho do arquivo CSV
    caminho_csv = r"F:\coisas de bigdata\outro projeto\vendas.csv"
    
    # Carregar e limpar os dados
    df = carregar_e_limpar_dados(caminho_csv)

    # Calcular o valor de revenda e salvar em um novo arquivo CSV
    df_revenda = calcular_valor_revenda(df)
    salvar_csv(df_revenda, r"F:\coisas de bigdata\outro projeto\vendas_revenda.csv")

    # Analisar produtos mais vendidos por ano
    produtos_mais_vendidos_por_ano(df)

    data_valor = data_maior_valor(df)
    print("\n\nData com o maior valor arrecadado:")
    print(data_valor)

    df_revenda = calcular_valor_revenda(df)
    print("\nValores de Revenda calculados:")
    print(df_revenda.head())

    # Salvar os dados com o valor de revenda em um novo arquivo CSV
    salvar_csv(df_revenda, caminho_novo_csv)

# Verificação se o arquivo está sendo executado diretamente
if __name__ == "__main__":
    main()
