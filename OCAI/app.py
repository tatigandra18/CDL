import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

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

# Função para calcular desvios padrões
def calculate_z_scores(data, columns):
    mean_values = data[columns].mean()
    std_values = data[columns].std()
    
    z_scores = (data[columns] - mean_values) / std_values
    return z_scores

# Função para criar gráfico de radar
def radar_chart(z_scores_current, z_scores_desired, labels, title):
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=z_scores_current,
        theta=labels,
        fill='toself',
        name='Atual',
        line=dict(color='blue')
    ))

    fig.add_trace(go.Scatterpolar(
        r=z_scores_desired,
        theta=labels,
        fill='toself',
        name='Desejado',
        line=dict(color='green')
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[-3, 3],
                dtick=0.5
            )
        ),
        title=title,
        showlegend=True
    )

    return fig

# Título do app
st.title('Análise de Cultura Organizacional com Z-Scores')

# URL do arquivo raw no GitHub
file_url = 'https://raw.githubusercontent.com/tatigandra18/CDL/refs/heads/main/OCAI/censo-estagios-2024-2.csv'

# Carregar e preparar os dados
data = load_and_prepare_data(file_url)

# Calcular z-scores globais (média de todos os funcionários e empresas)
columns_current = ['Clã_atual', 'Adhocracia_atual', 'Mercado_atual', 'Hierarquia_atual']
columns_desired = ['Clã_desejado', 'Adhocracia_desejado', 'Mercado_desejado', 'Hierarquia_desejado']

z_scores_current = calculate_z_scores(data, columns_current)
z_scores_desired = calculate_z_scores(data, columns_desired)

# Implementando as abas
tab1, tab2 = st.tabs(["Análise Individual", "Comparação entre Empresas"])

# Aba 1: Análise Individual
with tab1:
    st.subheader('Análise por Empresa e Funcionário')

    # Filtros
    empresas = st.selectbox("Selecione a Empresa", sorted(data['Empresas'].unique()))
    funcionarios = st.selectbox("Selecione o Funcionário", data[data['Empresas'] == empresas]['Unnamed: 0'])

    # Filtrar os dados
    filtro = data[(data['Empresas'] == empresas) & (data['Unnamed: 0'] == funcionarios)]

    if not filtro.empty:
        # Pegar z-scores para o funcionário selecionado
        z_scores_current_funcionario = z_scores_current.loc[filtro.index].values.flatten().tolist()
        z_scores_desired_funcionario = z_scores_desired.loc[filtro.index].values.flatten().tolist()
        
        labels = ['Clã', 'Adhocracia', 'Mercado', 'Hierarquia']
        title = f"Cultura Organizacional - {empresas} (Z-Scores)"

        fig = radar_chart(z_scores_current_funcionario, z_scores_desired_funcionario, labels, title)
        st.plotly_chart(fig)

    # Exibir gráfico geral para empresa
    st.subheader('Diferença em Z-Scores - Média Geral da Empresa')

    empresa_filtro = data[data['Empresas'] == empresas]
    if not empresa_filtro.empty:
        z_scores_current_avg = z_scores_current.loc[empresa_filtro.index].mean().values.tolist()
        z_scores_desired_avg = z_scores_desired.loc[empresa_filtro.index].mean().values.tolist()
        
        fig = radar_chart(z_scores_current_avg, z_scores_desired_avg, labels, f"Média Geral - {empresas} (Z-Scores)")
        st.plotly_chart(fig)

# Aba 2: Comparação entre Empresas
with tab2:
    st.subheader('Comparação entre Empresas')

    empresas_unicas = sorted(data['Empresas'].unique())  # Ordena as empresas em ordem alfabética

    for i, empresa in enumerate(empresas_unicas):  # Adicionar índice para chave única
        empresa_filtro = data[data['Empresas'] == empresa]
        
        if not empresa_filtro.empty:
            z_scores_current_avg = z_scores_current.loc[empresa_filtro.index].mean().values.tolist()
            z_scores_desired_avg = z_scores_desired.loc[empresa_filtro.index].mean().values.tolist()
            
            st.markdown(f"### {empresa}")
            fig = radar_chart(z_scores_current_avg, z_scores_desired_avg, labels, f"Média Geral - {empresa} (Z-Scores Globais)")
            
            # Adicionando uma chave única ao gráfico
            st.plotly_chart(fig, key=f"radar_chart_{i}")
