import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import seaborn as sns
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

# Função para criar um heatmap
def plot_heatmap(data):
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.heatmap(data, annot=True, cmap="coolwarm", center=0, fmt=".2f", linewidths=0.5, ax=ax)
    plt.title("Mapa de Calor das Preferências (Médias)")
    st.pyplot(fig)

# Título do app
st.title('Análise de Cultura Organizacional com Z-Scores')

# URL do arquivo raw no GitHub
file_url = 'https://raw.githubusercontent.com/tatigandra18/CDL/refs/heads/main/OCAI/censo-estagios-2024-2.csv'

# Carregar e preparar os dados
data = load_and_prepare_data(file_url)

# Implementando as abas
tab1, tab2, tab3 = st.tabs(["Análise Individual", "Comparação entre Empresas", "Top 10 Empresas"])

# Aba 3: Top 10 Empresas + Heatmap Geral
with tab3:
    st.subheader('Top 10 Empresas por Dimensões')

    # Calculando a média de cada dimensão
    media_empresas = data.groupby('Empresas')[['Clã_atual', 'Adhocracia_atual', 'Mercado_atual', 'Hierarquia_atual',
                                               'Clã_desejado', 'Adhocracia_desejado', 'Mercado_desejado', 'Hierarquia_desejado']].mean()

    # Encontrando as 10 maiores empresas para cada dimensão
    top_10_cla = media_empresas['Clã_atual'].nlargest(10)
    top_10_adh = media_empresas['Adhocracia_atual'].nlargest(10)
    top_10_mer = media_empresas['Mercado_atual'].nlargest(10)
    top_10_hie = media_empresas['Hierarquia_atual'].nlargest(10)

    # Plotando os gráficos de barras
    st.subheader("Top 10 Empresas - Clã")
    st.bar_chart(top_10_cla)

    st.subheader("Top 10 Empresas - Adhocracia")
    st.bar_chart(top_10_adh)

    st.subheader("Top 10 Empresas - Mercado")
    st.bar_chart(top_10_mer)

    st.subheader("Top 10 Empresas - Hierarquia")
    st.bar_chart(top_10_hie)

    # Mapa de Calor Geral
    st.subheader("Mapa de Calor - Preferências Gerais do Grupo")

    # Criar DataFrame com as médias gerais
    media_geral = data[['Clã_atual', 'Adhocracia_atual', 'Mercado_atual', 'Hierarquia_atual',
                         'Clã_desejado', 'Adhocracia_desejado', 'Mercado_desejado', 'Hierarquia_desejado']].mean()

    # Converter para DataFrame para melhor visualização no heatmap
    heatmap_data = pd.DataFrame(media_geral).T  # Transformar em tabela para heatmap

    plot_heatmap(heatmap_data)
