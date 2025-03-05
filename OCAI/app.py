import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Função para carregar e preparar os dados
def load_and_prepare_data(url):
    data = pd.read_csv(url)
    columns_clan = [col for col in data.columns if 'Clã' in col]
    columns_adhocracy = [col for col in data.columns if 'Adhocracia' in col]
    columns_market = [col for col in data.columns if 'Mercado' in col]
    columns_hierarchy = [col for col in data.columns if 'Hierarquia' in col]

    clean_data = data.iloc[1:]

    clean_data['Clã_atual'] = clean_data[columns_clan[0:6]].astype(float).mean(axis=1)
    clean_data['Adhocracia_atual'] = clean_data[columns_adhocracy[0:6]].astype(float).mean(axis=1)
    clean_data['Mercado_atual'] = clean_data[columns_market[0:6]].astype(float).mean(axis=1)
    clean_data['Hierarquia_atual'] = clean_data[columns_hierarchy[0:6]].astype(float).mean(axis=1)

    clean_data['Clã_desejado'] = clean_data[columns_clan[6:]].astype(float).mean(axis=1)
    clean_data['Adhocracia_desejado'] = clean_data[columns_adhocracy[6:]].astype(float).mean(axis=1)
    clean_data['Mercado_desejado'] = clean_data[columns_market[6:]].astype(float).mean(axis=1)
    clean_data['Hierarquia_desejado'] = clean_data[columns_hierarchy[6:]].astype(float).mean(axis=1)

    return clean_data

# Função para criar gráfico de densidade Kernel 2D
def kde_density_plot(data, x_col, y_col, title):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.kdeplot(
        x=data[x_col], y=data[y_col], cmap="coolwarm", fill=True, thresh=0, levels=100, ax=ax
    )
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(title)
    st.pyplot(fig)

# Título do app
st.title('Análise de Cultura Organizacional com Z-Scores')

# URL do arquivo raw no GitHub
file_url = 'https://raw.githubusercontent.com/tatigandra18/CDL/refs/heads/main/OCAI/censo-estagios-2024-2.csv'

# Carregar e preparar os dados
data = load_and_prepare_data(file_url)

# Implementando as abas
tab1, tab2, tab3 = st.tabs(["Análise Individual", "Comparação entre Empresas", "Top 10 Empresas & Mapa de Calor"])

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

      # Aba 3: Top 10 Empresas & Mapa de Calor
      with tab3:
          st.subheader('Top 10 Empresas com Maiores Índices')
      
          elements = ['Clã_atual', 'Adhocracia_atual', 'Mercado_atual', 'Hierarquia_atual']
          for element in elements:
              top_10 = data.groupby('Empresas')[element].mean().nlargest(10)
              
              fig = px.bar(top_10, x=top_10.index, y=top_10.values, labels={'y': 'Média', 'x': 'Empresa'},
                           title=f'Top 10 Empresas com Maiores Índices de {element.split("_")[0]}')
              
              fig.update_layout(
                  width=800,
                  height=500
              )
              
              st.plotly_chart(fig, use_container_width=True)
          
          st.subheader("Distribuição das Preferências dos Alunos - Mapa de Calor")
          kde_density_plot(data, "Clã_atual", "Adhocracia_atual", "Distribuição Clã vs Adhocracia")
