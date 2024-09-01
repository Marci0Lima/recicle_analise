import csv
import random
from datetime import datetime, timedelta

# Dados iniciais
materiais = {
    'latinha': 8.4,
    'cobre': 44.2,
    'aluminio': 7.0,
    'aço': 5.4,
    'PET PEAD': 2.5,
    'PP BRANCO': 2.25,
    'PP PRETO': 1.3,
    'PP COLORIDO': 1.5,
    'PP CRISTAL': 2.9,
    'alto impacto': 1.0,
    'PVC vidro': 80.0,
    'bateria': 5.0,
    'arquivo': 0.8,
    'chumbo': 7.5,
    'óleo': 2.0,
    'ferro': 1.2,
    'placa eletronica': 40.0,
    'bloco': 7.9,
    'vidro': 1.0,
    'papelão': 0.8
}

def gerar_precos_variados(preco_base):
    """ Gera um preço variado com margem de lucro entre 30% e 40%. """
    margem = random.uniform(0.3, 0.4)
    preco_lucro = preco_base * (1 + margem)
    return round(preco_lucro, 2)

def gerar_vendas_inicio_fim(data_inicio, data_fim, num_registros_desejados):
    """ Gera um número específico de registros de vendas entre duas datas, incluindo sábados e domingos. """
    vendas = []
    id_compra = 1  # Começa com o ID 1
    data_atual = data_inicio
    total_vendas = 0

    while total_vendas < num_registros_desejados:
        # Determina o número de vendas para o dia atual, de 1 a 30
        num_vendas_dia = random.randint(1, 30)
        
        for _ in range(num_vendas_dia):
            if total_vendas >= num_registros_desejados:
                break
            material = random.choice(list(materiais.keys()))
            preco_por_kg = gerar_precos_variados(materiais[material])
            quantidade_kg = round(random.uniform(0.1, 50.0), 2)  # Quantidade aleatória entre 0.1 e 50 kg
            preco_total = round(preco_por_kg * quantidade_kg, 2)

            vendas.append([id_compra, data_atual.strftime('%Y-%m-%d'), material, quantidade_kg, preco_por_kg, preco_total])
            total_vendas += 1
            id_compra += 1
        
        if total_vendas >= num_registros_desejados:
            break
        data_atual += timedelta(days=1)  # Passa para o próximo dia

    return vendas

# Define o intervalo de datas para 2021, 2022 e 2023
data_inicio = datetime(2021, 1, 1)
data_fim = datetime(2023, 12, 31)

# Número de registros desejados
num_registros_desejados = 20000

# Gera as vendas
vendas = gerar_vendas_inicio_fim(data_inicio, data_fim, num_registros_desejados)

# Salva as vendas em um arquivo CSV
with open('vendas.csv', 'w', newline='') as arquivo_csv:
    writer = csv.writer(arquivo_csv)
    writer.writerow(['ID da Compra', 'Data da Compra', 'Nome do Material', 'Quantidade (kg)', 'Preço por kg (R$)', 'Preço Total (R$)'])
    writer.writerows(vendas)

print(f"Arquivo 'vendas.csv' com {len(vendas)} registros gerado com sucesso.")
