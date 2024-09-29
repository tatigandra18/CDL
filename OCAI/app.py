import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Função para carregar e preparar os dados
def load_and_prepare_data(url):
    data = pd.read_csv(url)
    columns_clan = [col for col in data.columns if 'Clã' in col]
    columns_adhocracy = [col for col in data.columns if 'Adhocracia' in col]
    columns_market = [col for col in data.columns if 'Mercado' in col]
    columns_hierarchy = [col for col in data.columns if 'Hierarquia' in col]
    
    clean_data = data.iloc[1:]  # Ignorar a primeira linha de textos explicativos
    
    clean_data['Clã_atual'] = clean_data[columns_clan[0:6]].astype(float).mean(axis=1)
    clean_data['Adhocracia_atual'] = clean_data[columns_adhocracy[0:6]].astype(float).mean(axis=1)
    clean_data['Mercado_atual'] = clean_data[columns_market[0:6]].astype(float).mean(axis=1)
    clean_data['Hierarquia_atual'] = clean_data[columns_hierarchy[0:6]].astype(float).mean(axis=1)
    
    clean_data['Clã_desejado'] = clean_data[columns_clan[6:]].astype(float).mean(axis=1)
    clean_data['Adhocracia_desejado'] = clean_data[columns_adhocracy[6:]].astype(float).mean(axis=1)
    clean_data['Mercado_desejado'] = clean_data[columns_market[6:]].astype(float).mean(axis=1)
    clean_data['Hierarquia_desejado'] = clean_data[columns_hierarchy[6:]].astype(float).mean(axis=1)
    
    return clean_data

# Função para criar gráfico de radar
def radar_chart(culture_current, culture_desired, labels, title):
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    culture_current += culture_current[:1]
    culture_desired += culture_desired[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, culture_current, color='blue', alpha=0.25, label='Atual')
    ax.plot(angles, culture_current, color='blue', linewidth=2)

    ax.fill(angles, culture_desired, color='green', alpha=0.25, label='Desejado')
    ax.plot(angles, culture_desired, color='green', linewidth=2)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    plt.legend(loc='upper right')
    plt.title(title, size=20, color='blue', y=1.1)

    st.pyplot(fig)


# URL do arquivo raw no GitHub
file_url = 'https://raw.githubusercontent.com/tatigandra18/CDL/refs/heads/main/OCAI/censo-estagios-2024-2.csv'

# Carregar e preparar os dados
data = load_and_prepare_data(file_url)

# Título do app
st.title('Análise de Cultura Organizacional')

# Filtros
empresas = st.selectbox("Selecione a Empresa", data['Empresas'].unique())
funcionarios = st.selectbox("Selecione o Funcionário", data[data['Empresas'] == empresas]['Unnamed: 0'])

# Filtrar os dados
filtro = data[(data['Empresas'] == empresas) & (data['Unnamed: 0'] == funcionarios)]

if not filtro.empty:
    # Valores de cultura para gráfico
    culture_current = [
        filtro.iloc[0]['Clã_atual'], 
        filtro.iloc[0]['Adhocracia_atual'], 
        filtro.iloc[0]['Mercado_atual'], 
        filtro.iloc[0]['Hierarquia_atual']
    ]
    
    culture_desired = [
        filtro.iloc[0]['Clã_desejado'], 
        filtro.iloc[0]['Adhocracia_desejado'], 
        filtro.iloc[0]['Mercado_desejado'], 
        filtro.iloc[0]['Hierarquia_desejado']
    ]
    
    labels = ['Clã', 'Adhocracia', 'Mercado', 'Hierarquia']
    title = f"Cultura Organizacional - {empresas}"

    radar_chart(culture_current, culture_desired, labels, title)

# Exibir gráfico geral para empresa
st.subheader('Média Geral da Empresa')

empresa_filtro = data[data['Empresas'] == empresas]
if not empresa_filtro.empty:
    culture_current_avg = [
        empresa_filtro['Clã_atual'].mean(),
        empresa_filtro['Adhocracia_atual'].mean(),
        empresa_filtro['Mercado_atual'].mean(),
        empresa_filtro['Hierarquia_atual'].mean()
    ]
    
    culture_desired_avg = [
        empresa_filtro['Clã_desejado'].mean(),
        empresa_filtro['Adhocracia_desejado'].mean(),
        empresa_filtro['Mercado_desejado'].mean(),
        empresa_filtro['Hierarquia_desejado'].mean()
    ]
    
    radar_chart(culture_current_avg, culture_desired_avg, labels, f"Média Geral - {empresas}")
