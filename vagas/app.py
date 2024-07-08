
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import requests
from io import StringIO
from collections import Counter

# Lista de URLs dos arquivos CSV no GitHub
urls = [
    'https://raw.githubusercontent.com/tatigandra18/CDL/main/vagas/arquivo_correto1.csv',
    'https://raw.githubusercontent.com/tatigandra18/CDL/main/vagas/arquivo_correto2.csv',
    'https://raw.githubusercontent.com/tatigandra18/CDL/main/vagas/arquivo_correto3.csv',
    'https://raw.githubusercontent.com/tatigandra18/CDL/main/vagas/arquivo_correto4.csv',
    'https://raw.githubusercontent.com/tatigandra18/CDL/main/vagas/arquivo_correto5.csv'
]

urls_2 =[
    'https://github.com/tatigandra18/CDL/raw/main/vagas/vagas_classificadas_part1.csv',
    'https://github.com/tatigandra18/CDL/raw/main/vagas/vagas_classificadas_part2.csv',
    'https://github.com/tatigandra18/CDL/raw/main/vagas/vagas_classificadas_part3.csv',
    'https://github.com/tatigandra18/CDL/raw/main/vagas/vagas_classificadas_part4.csv',
    'https://github.com/tatigandra18/CDL/raw/main/vagas/vagas_classificadas_part5.csv',
] 

# Função para ler e combinar os arquivos CSV
def load_and_combine_csvs(urls):
    dataframes = []
    for url in urls:
        df = pd.read_csv(url)
        dataframes.append(df)
    combined_df = pd.concat(dataframes, ignore_index=True)
    return combined_df

# Carregar e combinar os arquivos CSV
df_tech = load_and_combine_csvs(urls)
df_nao_rotulados = load_and_combine_csvs(urls_2)

df_merged = pd.merge(df_tech, df_nao_rotulados[['Localização', 'Skills Necessarias', 'Média Salarial', 'Cargo', 'ver_cargo', 'palavra_chave', 'Nome Vaga Normalizado']], on=['Localização', 'Skills Necessarias', 'Média Salarial', 'Cargo', 'ver_cargo', 'palavra_chave'], how='left')

# Criar guias
titulos_guias = ['Pesquisa','Etapas','Análises', 'Próximos passos']
guia1, guia2, guia3, guia4 = st.tabs(titulos_guias)

with guia1:
    st.header('Pesquisa de carreiras')
    
    st.markdown('<hr style="border-top: 2px solid blue;">', unsafe_allow_html=True)
     
    st.subheader('Reports:')

    st.markdown("- Como começar a carreira tecnologia?")
    st.markdown("- Top profissões")
    st.markdown("- Como está o mercado de tecnologia no Brasil?")
    st.markdown("- Tipos de carreira em tecnologia")
    st.markdown("- Carreira acadêmica")
    st.markdown("- Carreira empreendedora")
    st.markdown("- Mitos e Verdades sobre carreira (input das entrevistas dos alunos)")
    st.markdown("- Startups x Bigtechs (diferenças e prós e contras)")
    st.markdown("- Carreira dos Sonhos Inteli")
    st.markdown("- Porque seguir carreira em tecnologia?")    
   
    with guia2:
        st.header('Etapas:')
    
        st.markdown('<hr style="border-top: 2px solid blue;">', unsafe_allow_html=True)
        
        st.subheader('Extração de dados:')

        img_caged = 'https://raw.githubusercontent.com/tatigandra18/CDL/main/vagas/caged 2023.png'
        img_miro = 'https://raw.githubusercontent.com/tatigandra18/CDL/main/vagas/descrição áreas.png'
        img_fontes = 'https://raw.githubusercontent.com/tatigandra18/CDL/main/vagas/fontes.png'
        img_webscrapping = 'https://raw.githubusercontent.com/tatigandra18/CDL/main/vagas/webscrapping.png'
        img_tratamento = 'https://raw.githubusercontent.com/tatigandra18/CDL/main/vagas/tratamento.png'

        st.image(img_webscrapping, caption = 'Extração de dados das vagas da glassdoor abril/2023', use_column_width=True)
        st.markdown("Essa busca coletou mais de 38.000 vagas de todo o Brasil.")
        #incluir as palavras chaves
        st.subheader('Busca de fontes:')

        st.image(img_fontes, caption = 'Lista de fontes relacionadas à pesquisa', use_column_width=True)
        st.markdown("Essas fontes foram classificadas em tipos de dados que poderíamos buscar.")

        st.subheader('Análise das fontes:')

        st.image(img_miro, caption = 'Descrições de cada área da tecnologia com base nas fontes citadas acima', use_column_width=True)

        st.markdown("Hora de processar as informações encontradas no estudos selecionados. WKS está focada nessa atividade no momento.")

        st.subheader('Análises Caged')

        st.image(img_caged, caption = 'quantidade de vagas criadas em 2023 na área de tecnologia', use_column_width=True)

        st.markdown("Fizemos também análises na base do caged, que serão incorporadas nesse relatório. A imagem ilustra um exemplo.")

        st.subheader('Tratamento das vagas')

        st.markdown("Processo de normalização dos cargos, uma vez que em cada vaga eles são escritos de formas diferentes. A partir disso, conseguimos até o momento:")
        st.markdown(" - Excluir vagas que não são de tecnologia")
        st.markdown(" - Definir a área de cada vaga")
        st.markdown(" - Definir as vags que são de início de carreira")
        st.image(img_tratamento, caption = 'Exemplo de como é feito o tratamento', use_column_width=True)

        with guia3:
            st.header('Análises:')

            st.markdown('<hr style="border-top: 2px solid blue;">', unsafe_allow_html=True)
        
            st.subheader('Áreas com mais vagas')

            contagem_areas_individual = Counter()
            for areas in df_tech['macro_area']:
                for area in areas.split(', '):
                    contagem_areas_individual[area] += 1

            if 'Indefinida' in contagem_areas_individual:
                del contagem_areas_individual['Indefinida']
            # Converter o contador para um DataFrame
            df_contagem_areas = pd.DataFrame(contagem_areas_individual.items(), columns=['Área', 'Quantidade'])

            # Calcular percentual
            total = df_contagem_areas['Quantidade'].sum()
            df_contagem_areas['Percentual'] = (df_contagem_areas['Quantidade'] / total) * 100

            # Ordenar do menor para o maior
            df_contagem_areas = df_contagem_areas.sort_values(by='Quantidade')

            # Gráfico de barras com Plotly
            fig = px.bar(df_contagem_areas, x='Quantidade', y='Área', text='Percentual',
                        labels={'Quantidade': 'Quantidade', 'Área': 'Áreas'})

            fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
            fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', yaxis={'categoryorder':'total ascending'})

            fig.update_layout(margin=dict(l=200, r=50, b=50, t=50), yaxis_tickangle=0)

            st.plotly_chart(fig)

            st.subheader("Tipos de cargos que mais aparecem")
            # Contabilizar combinações de áreas
            contagem_combinacoes_tipo_cargo = Counter(df_tech['tipo_cargo'])

            # Converter o contador para um DataFrame
            df_contagem_combinacoes_tipo_cargo = pd.DataFrame(contagem_combinacoes_tipo_cargo.items(), columns=['Combinação de Áreas', 'Quantidade'])

            # Calcular percentual
            total_combinacoes = df_contagem_combinacoes_tipo_cargo['Quantidade'].sum()
            df_contagem_combinacoes_tipo_cargo['Percentual'] = (df_contagem_combinacoes_tipo_cargo['Quantidade'] / total_combinacoes) * 100

            # Ordenar do menor para o maior
            df_contagem_combinacoes_tipo_cargo = df_contagem_combinacoes_tipo_cargo.sort_values(by='Quantidade')

            # Gráfico de barras com Plotly
            fig2 = px.bar(df_contagem_combinacoes_tipo_cargo, x='Quantidade', y='Combinação de Áreas', text='Percentual',
                        labels={'Quantidade': 'Quantidade', 'Combinação de Áreas': 'Combinações de Áreas'})

            fig2.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
            fig2.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', yaxis={'categoryorder':'total ascending'})

            # Ajuste da margem e espaçamento
            fig2.update_layout(margin=dict(l=200, r=50, b=50, t=50), yaxis_tickangle=0)

            st.plotly_chart(fig2)
            st.subheader("Quantidade de cargos iniciais")

            # Contabilizar combinações de áreas
            contagem_combinacoes_momento_carreira = Counter(df_tech['momento_carreira'])

            # Converter o contador para um DataFrame
            df_contagem_combinacoes_momento_carreira = pd.DataFrame(contagem_combinacoes_momento_carreira.items(), columns=['Combinação de Áreas', 'Quantidade'])

            # Calcular percentual
            total_combinacoes = df_contagem_combinacoes_momento_carreira['Quantidade'].sum()
            df_contagem_combinacoes_momento_carreira['Percentual'] = (df_contagem_combinacoes_momento_carreira['Quantidade'] / total_combinacoes) * 100

            # Ordenar do menor para o maior
            df_contagem_combinacoes_momento_carreira = df_contagem_combinacoes_momento_carreira.sort_values(by='Quantidade')

            # Gráfico de barras com Plotly
            fig3 = px.bar(df_contagem_combinacoes_momento_carreira, x='Quantidade', y='Combinação de Áreas', text='Percentual',
                        labels={'Quantidade': 'Quantidade', 'Combinação de Áreas': 'Combinações de Áreas'})

            fig3.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
            fig3.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', yaxis={'categoryorder':'total ascending'})

            # Ajuste da margem e espaçamento
            fig3.update_layout(margin=dict(l=200, r=50, b=50, t=50), yaxis_tickangle=0)

            st.plotly_chart(fig3)

            st.subheader("Quantidade de cargos iniciais por área")

            df_tech = df_tech.assign(Área=df_tech['macro_area'].str.split(', ')).explode('Área')

            # Filtrar os dados para vagas em início de carreira e não início de carreira
            df_inicio_carreira = df_tech[df_tech['momento_carreira'] == 'inicio de carreira']
            df_nao_inicio_carreira = df_tech[df_tech['momento_carreira'] == 'carreira avançada']

            # Contar as vagas em início de carreira e não início de carreira por Área
            contagem_inicio_carreira = df_inicio_carreira['Área'].value_counts().reset_index()
            contagem_inicio_carreira.columns = ['Área', 'Quantidade']
            contagem_inicio_carreira['Tipo'] = 'Início de Carreira'

            contagem_nao_inicio_carreira = df_nao_inicio_carreira['Área'].value_counts().reset_index()
            contagem_nao_inicio_carreira.columns = ['Área', 'Quantidade']
            contagem_nao_inicio_carreira['Tipo'] = 'Não Início de Carreira'

            # Concatenar os dois DataFrames
            df_comparacao_carreira = pd.concat([contagem_inicio_carreira, contagem_nao_inicio_carreira])
            fig4 = px.bar(df_comparacao_carreira, x='Área', y='Quantidade', color='Tipo',
              labels={'Quantidade': 'Quantidade de Vagas', 'Área': 'Áreas', 'Tipo': 'Tipo de Carreira'},
              barmode='stack')
            
            st.plotly_chart(fig4)

            st.subheader('Quantidade de vagas em início de carreira por Área')

            fig5 = px.bar(contagem_inicio_carreira, x='Área', y='Quantidade',
              labels={'Quantidade': 'Quantidade de Vagas', 'Área': 'Áreas'})
            st.plotly_chart(fig5)

            # Analisar as áreas e cargos
            area_cargo_count = df_merged.groupby(['Área', 'Nome Vaga Normalizado']).size().reset_index(name='counts')

            # Lista suspensa para selecionar a área
            areas = area_cargo_count['Área'].unique()
            area_selecionada = st.selectbox('Selecione a Área', areas)

            # Filtrar dados para a área selecionada
            df_area_selecionada = area_cargo_count[area_cargo_count['Área'] == area_selecionada].sort_values(by='counts', ascending=False).head(10)

            # Criar gráfico para a área selecionada
            fig_area_selecionada = px.bar(
                df_area_selecionada,
                x='Nome Vaga Normalizado',
                y='counts',
                title=f'Cargos na Área: {area_selecionada}',
                labels={'counts': 'Número de Vagas', 'Nome Vaga Normalizado': 'Cargo'},
                template='plotly_white'
            )
            fig_area_selecionada.update_layout(xaxis_tickangle=-45)

            # Exibir o gráfico
            st.plotly_chart(fig_area_selecionada)

            # Analisar as vagas de início de carreira
            df_inicio_carreira = df_merged[df_merged['momento_carreira'] == 'inicio de carreira']  # Certifique-se de que o filtro está correto
            area_inicio_carreira_count = df_inicio_carreira.groupby(['Área', 'Nome Vaga Normalizado']).size().reset_index(name='counts')

            # Lista suspensa para selecionar a área para vagas de início de carreira
            st.header('Vagas de Início de Carreira por Área')
            area_selecionada_inicio_carreira = st.selectbox('Selecione a Área', areas, key='inicio_carreira')

            # Filtrar dados para a área selecionada
            df_area_inicio_carreira_selecionada = area_inicio_carreira_count[area_inicio_carreira_count['Área'] == area_selecionada_inicio_carreira].sort_values(by='counts', ascending=False).head(10)

            # Criar gráfico para a área selecionada de início de carreira
            fig_area_inicio_carreira_selecionada = px.bar(
                df_area_inicio_carreira_selecionada,
                x='Nome Vaga Normalizado',
                y='counts',
                title=f'Vagas de Início de Carreira na Área: {area_selecionada_inicio_carreira}',
                labels={'counts': 'Número de Vagas', 'Nome Vaga Normalizado': 'Cargo'},
                template='plotly_white'
            )
            fig_area_inicio_carreira_selecionada.update_layout(xaxis_tickangle=-45)

            # Exibir o gráfico
            st.plotly_chart(fig_area_inicio_carreira_selecionada)

            with guia4:

                st.header('Próximos passos:')

                st.markdown('<hr style="border-top: 2px solid blue;">', unsafe_allow_html=True)
            
                st.markdown(' - Normalizar os nomes das vagas')
                st.markdown(' - Nomear vagas em início de carreira dentro de cada área')
                st.markdown(' - Descobrir palavras-chave para cada vaga')
                st.markdown(' - Análisar bases de salário para incluir valores em cada vaga')
                st.markdown(' - Incluir análises do Caged')
                st.markdown(' - Incluir esses dados no texto da WKS')