import pandas as pd

# Carregar o CSV com a codificação correta e converter colunas numéricas
df = pd.read_csv(r"F:\coisas de bigdata\outro projeto\vendas.csv", delimiter=';', encoding='latin1')

# Remover espaços em branco dos nomes das colunas
df.columns = df.columns.str.strip()

df['Quantidade (kg)'] = pd.to_numeric(df['Quantidade (kg)'], errors='coerce')
df['Preço Total (R$)'] = pd.to_numeric(df['Preço Total (R$)'], errors='coerce')

# Agrupar por data e somar as quantidades e valores
vendas_por_data = df.groupby('Data da Compra').agg({
    'Quantidade (kg)': 'sum',
    'Preço Total (R$)': 'sum'
}).reset_index()

# Encontrar a data com maior valor arrecadado
data_maior_valor = vendas_por_data.loc[vendas_por_data['Preço Total (R$)'].idxmax()]

#data com maior numero de vendas
data_maior_vendas = vendas_por_data.loc[vendas_por_data['Quantidade (kg)'].idxmax()]
print("Data com o maior valor arrecadado:")
print(data_maior_valor)

print("\n\nData com maior registo de vendas:")
print(data_maior_vendas)
