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

# Função para calcular z-scores globais
def calculate_global_z_scores(data, columns_current, columns_desired):
    all_aspects = columns_current + columns_desired
    
    # Calcular a média global para todos os aspectos
    mean_global = data[all_aspects].mean().mean()
    
    # Calcular o desvio padrão global para todos os aspectos
    std_global = data[all_aspects].stack().std()
    
    # Calcular z-scores globais para atual e desejado
    z_scores_current = (data[columns_current] - mean_global) / std_global
    z_scores_desired = (data[columns_desired] - mean_global) / std_global
    
    return z_scores_current, z_scores_desired

# Função para criar gráfico de radar com Plotly
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
            radialaxis=dict(visible=True, range=[-3, 3], tickvals=np.arange(-3, 3.5, 0.5))
        ),
        title=title,
        showlegend=True
    )

    st.plotly_chart(fig)

# Título do app
st.title('Análise de Cultura Organizacional com Z-Scores Globais')

# URL do arquivo raw no GitHub
file_url = 'https://raw.githubusercontent.com/tatigandra18/CDL/refs/heads/main/OCAI/censo-estagios-2024-2.csv'

# Carregar e preparar os dados
data = load_and_prepare_data(file_url)

# Definir as colunas dos aspectos
columns_current = ['Clã_atual', 'Adhocracia_atual', 'Mercado_atual', 'Hierarquia_atual']
columns_desired = ['Clã_desejado', 'Adhocracia_desejado', 'Mercado_desejado', 'Hierarquia_desejado']

# Calcular z-scores globais
z_scores_current, z_scores_desired = calculate_global_z_scores(data, columns_current, columns_desired)

# Implementando as abas
tab1, tab2 = st.tabs(["Análise Individual", "Comparação entre Empresas"])

# Aba 1: Análise Individual
with tab1:
    st.subheader('Análise por Empresa e Funcionário')

    # Filtros
    empresas = sorted(data['Empresas'].unique())  # Ordena as empresas em ordem alfabética
    selected_empresa = st.selectbox("Selecione a Empresa", empresas)
    funcionarios = st.selectbox("Selecione o Funcionário", data[data['Empresas'] == selected_empresa]['Unnamed: 0'])

    # Filtrar os dados
    filtro = data[(data['Empresas'] == selected_empresa) & (data['Unnamed: 0'] == funcionarios)]

    if not filtro.empty:
        # Pegar z-scores para o funcionário selecionado
        z_scores_current_funcionario = z_scores_current.loc[filtro.index].values.flatten().tolist()
        z_scores_desired_funcionario = z_scores_desired.loc[filtro.index].values.flatten().tolist()
        
        labels = ['Clã', 'Adhocracia', 'Mercado', 'Hierarquia']
        title = f"Cultura Organizacional - {selected_empresa} (Z-Scores Globais)"

        radar_chart(z_scores_current_funcionario, z_scores_desired_funcionario, labels, title)

    # Exibir gráfico geral para empresa
    st.subheader('Diferença em Z-Scores - Média Geral da Empresa')

    empresa_filtro = data[data['Empresas'] == selected_empresa]
    if not empresa_filtro.empty:
        z_scores_current_avg = z_scores_current.loc[empresa_filtro.index].mean().values.tolist()
        z_scores_desired_avg = z_scores_desired.loc[empresa_filtro.index].mean().values.tolist()
        
        radar_chart(z_scores_current_avg, z_scores_desired_avg, labels, f"Média Geral - {selected_empresa} (Z-Scores Globais)")

# Aba 2: Comparação entre Empresas
with tab2:
    st.subheader('Comparação entre Empresas')

    empresas_unicas = sorted(data['Empresas'].unique())  # Ordena as empresas em ordem alfabética

    for empresa in empresas_unicas:
        empresa_filtro = data[data['Empresas'] == empresa]
        
        if not empresa_filtro.empty:
            z_scores_current_avg = z_scores_current.loc[empresa_filtro.index].mean().values.tolist()
            z_scores_desired_avg = z_scores_desired.loc[empresa_filtro.index].mean().values.tolist()
            
            st.markdown(f"### {empresa}")
            radar_chart(z_scores_current_avg, z_scores_desired_avg, labels, f"Média Geral - {empresa} (Z-Scores Globais)")
