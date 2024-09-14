import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def carregar_e_limpar_dados(caminho_csv):
    try:
        df = pd.read_csv(caminho_csv, delimiter=';', encoding='latin1')
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.columns = df.columns.str.strip()
        
        expected_columns = ['ID da Compra', 'Data da Compra', 'Nome do Material', 'Quantidade (kg)', 'Preço por kg (R$)']
        missing_columns = [col for col in expected_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Colunas esperadas não encontradas: {missing_columns}")
        
        df['Quantidade (kg)'] = pd.to_numeric(df['Quantidade (kg)'], errors='coerce')
        df['Preço por kg (R$)'] = pd.to_numeric(df['Preço por kg (R$)'], errors='coerce')
        df['Preço Total (R$)'] = df['Quantidade (kg)'] * df['Preço por kg (R$)']
        df['Data da Compra'] = pd.to_datetime(df['Data da Compra'], errors='coerce')
        
        return df
    except Exception as e:
        messagebox.showerror("Erro ao carregar os dados", str(e))
        return None


def valor_total_por_mes(df):
    df['Ano-Mês'] = df['Data da Compra'].dt.to_period('M')
    vendas_por_mes = df.groupby('Ano-Mês').agg({
        'Quantidade (kg)': 'sum',
        'Preço Total (R$)': 'sum'
    }).reset_index()
    return vendas_por_mes


def exibir_grafico(df):
    vendas_por_mes = valor_total_por_mes(df)
    
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(vendas_por_mes['Ano-Mês'].astype(str), vendas_por_mes['Preço Total (R$)'], color='blue')
    ax.set_title("Valor Total por Mês")
    ax.set_ylabel("Preço Total (R$)")
    
    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack()

def exibir_tabela(df):
    tabela_frame = ttk.Treeview(janela)
    tabela_frame['columns'] = list(df.columns)
    tabela_frame.column("#0", width=0, stretch=tk.NO)
    
    for col in tabela_frame['columns']:
        tabela_frame.heading(col, text=col)
    
    for index, row in df.iterrows():
        tabela_frame.insert("", "end", values=list(row))
    
    tabela_frame.pack()


def produtos_mais_vendidos_por_mes(df):
    df['Ano-Mês'] = df['Data da Compra'].dt.to_period('M')
    agrupado_mes = df.groupby(['Ano-Mês', 'Nome do Material'])['Quantidade (kg)'].sum()
    
    mais_vendidos_por_mes = agrupado_mes.groupby(level=0).idxmax()
    quantidade_mais_vendidos_por_mes = agrupado_mes.groupby(level=0).max()
    
    resultados = mais_vendidos_por_mes.map(lambda x: f"{x[1]} ({quantidade_mais_vendidos_por_mes[x[0]]:.2f} kg)")
    
    return resultados


def exibir_produtos_mais_vendidos(df):
    mais_vendidos = produtos_mais_vendidos_por_mes(df)
    resultados_texto = "\n".join([f"Mês {periodo}: {info}" for periodo, info in mais_vendidos.items()])
    
    messagebox.showinfo("Produtos Mais Vendidos", resultados_texto)


def abrir_arquivo():
    caminho_arquivo = filedialog.askopenfilename(title="Selecione o arquivo CSV", filetypes=(("Arquivo CSV", "*.csv"),))
    if caminho_arquivo:
        df = carregar_e_limpar_dados(caminho_arquivo)
        if df is not None:
            exibir_grafico(df)
            exibir_tabela(df)
            exibir_produtos_mais_vendidos(df)


janela = tk.Tk()
janela.title("Análise de Vendas de Materiais Recicláveis")
janela.geometry("800x600")


btn_carregar_dados = tk.Button(janela, text="Carregar e Analisar CSV", command=abrir_arquivo)
btn_carregar_dados.pack(pady=20)


janela.mainloop()
