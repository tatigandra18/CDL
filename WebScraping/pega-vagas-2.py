from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
from datetime import date
import pandas as pd

# Função para apertar o botão de 'mais vagas'
def continuar_pesquisa():
    proxima_pagina = driver.find_element(By.XPATH, '//*[@id="left-column"]/div[2]/div/button')
    proxima_pagina.click()

# Função para criar arquivo .csv com as vagas
def cria_csv(lista, nome_arquivo):
    df = pd.DataFrame(lista)
    df.to_csv(nome_arquivo, index=False)

# Função para descobrir que horas são
def que_horas_sao():
    hora_atual = datetime.datetime.now()
    return hora_atual.time()

######################## INICIANDO O WEB SCRAPING ############################

#Abre o glassdoor
driver = webdriver.Chrome()
driver.get('https://www.glassdoor.com.br/index.htm')

# Credenciais de entrada
usuario = 'azevedogandratatiane@gmail.com'
senha = 'tati24Xumf'

try:
    # Preencher o campo de e-mail
    campo_usuario = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="inlineUserEmail"]'))
    )
    campo_usuario.send_keys(usuario)

    # Esperar até que o botão esteja clicável e então clicar nele
    enviar = driver.find_element(By.XPATH, '//*[@id="InlineLoginModule"]/div/div[1]/div/div/div/div/form/div[2]/button')
    enviar.click()

    print("Botão 'Entrar com e-mail' clicado.")
    time.sleep(3)

except Exception as e:
    print("Erro:", e)

# Preenchendo o campo de senha e efetuando o login
campo_senha = driver.find_element(By.XPATH, '//*[@id="inlineUserPassword"]')
campo_senha.send_keys(senha)
enviar = driver.find_element(By.XPATH, '//*[@id="InlineLoginModule"]/div/div[1]/div/div/div/div/form/div[4]/button')
enviar.click()
time.sleep(5)

# Lista de localizações a serem pesquisadas
localizacoes = [ "AC", "AL", "AP", "AM", "SP","BA","CE","ES", "GO","MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SE", "TO", "DF", "Brasil" ]
 # ALETERE AQUI - Digite a função (categoria) da busca
categoria = "Dados"

# Encontrando barra de pesquisa de categoria e enviando as chaves
pesquisa_categoria = driver.find_element(By.XPATH, '//*[@id="searchBar-jobTitle"]')
pesquisa_categoria.send_keys(categoria)
# Loop para pesquisar em cada localização
for localizacao in localizacoes:
    # Nesta lista armazenaremos todas as vagas e mais tarde criaremos um csv
    vagas = []

    # Encontrando barra de pesquisa de localidade e enviando chaves
    pesquisa_estado = driver.find_element(By.XPATH, '//*[@id="searchBar-location"]')
    pesquisa_estado.send_keys(localizacao)

    # Iniciando a pesquisa
    pesquisa_estado.send_keys(Keys.ENTER)
    time.sleep(2)

    # Fechando o pop-up de notificações
    verifica_pop_up = driver.find_elements(By.XPATH, '//*[@id="JAModal"]/div/div[2]/span')

    if verifica_pop_up:
        pop_up = driver.find_element(By.XPATH, '//*[@id="JAModal"]/div/div[2]/span')
        pop_up.click()
        time.sleep(2)

    # Variável para controle de parada
    card_not_found = False

    # Contador do While
    contador_vaga = 0
    while True:
        contador_vaga += 1
        #Dicionário inidividual para cada vaga 
        vaga = {}
        
        #Este número é utilizado para formar o XPATH do card de cada vaga
        numero_card = str(contador_vaga)
        
        #XPATH é o ID de cada card que é gerado de acordo com a posição do card na lista (1, 2, 3, 4...)
        xpath_card = '//*[@id="left-column"]/div[2]/ul/li[' + numero_card + ']'  
        
        #Esta é uma lista que é preenchida se o card for encontrado, caso não torna-se uma lista vazia
        verificacao_card = driver.find_elements(By.XPATH, xpath_card)
        
        #Se a lista tiver elementos, entra no if, caso não, vamos direto para o else
        if verificacao_card:
            
            #dado que o card existe, vamos armazená-lo nesta variavel
            card = driver.find_element(By.XPATH, xpath_card)
            
            #tenta o click no card 
            try:
                verifica_pop_up = driver.find_elements(By.XPATH, '//*[@id="JAModal"]/div/div[2]/span')
                if verifica_pop_up:
                    pop_up = driver.find_element(By.XPATH, '//*[@id="JAModal"]/div/div[2]/span')
                    pop_up.click()
                    time.sleep(2)
                card.click()
                time.sleep(3)
                
            #caso não seja possivel entrar no card isto é executado para evitar erros quando o programa chegar ao fim das vagas
            except:
                #Informa qual card não é clicável
                print(f"Card is not clickable at job opportunity:  {contador_vaga}")
                
                #A variavel de controle é inicialmente False, para que rode mais uma vez e verifique que realmente é o último 
                if card_not_found:
                    break
                #Agora transformamos em True para que se o mesmo ocorra no próximo card o loop possa ser encerrado
                card_not_found = True
                continue
            
            
            
            #Tenta Encontrar o cargo
            try:
                vaga['Funcao'] = driver.find_element(By.CLASS_NAME, 'JobDetails_jobDetailsHeader__Hd9M3').text
            #Caso não ache imprime uma mensagem 
            except:
                print('Function not found')

            
            #Tenta encontrar a localização
            try:
                vaga['Localização'] = driver.find_element(By.CLASS_NAME, 'JobDetails_location__mSg5h').text
            
            #Caso não ache imprime uma mensagem 
            except:
                print("Location Not Found")
            
            #Armazenando a seção do card em uma variável
            secao_vaga_lista = driver.find_elements(By.XPATH, '//*[@id="app-navigation"]/div[3]/div/div[2]/div/header/div[1]')
            
            if secao_vaga_lista:
                secao_vaga = driver.find_element(By.XPATH, '//*[@id="app-navigation"]/div[3]/div/div[2]/div/header/div[1]')
                #A partir da seção buscamos o nome da empresa - que vem acompanhada de avaliação
                vaga['Empresa'] = secao_vaga.find_element(By.CSS_SELECTOR, '.EmployerProfile_employerInfo__d8uSE').text

                #Descobrindo o ID da data de maneira dinâmica
                xpath_data = '//*[@id="left-column"]/div[2]/ul/li[' +str(contador_vaga) + ']/div/div/div[1]/div[2]'
                #Acha a data de publicação
                vaga['Data de Publicacao'] = driver.find_element(By.XPATH, xpath_data).text
                
            
            
            #Tenta encontrar a descrição
            try:
                vaga['Skills Necessarias'] = driver.find_element(By.CLASS_NAME, 'JobDetails_jobDetailsSection__y_xa6').text
                
            #Caso não ache imprime uma mensagem
            except: 
                print("Resumo não encontrado")
                vaga['Skills Necessarias'] = "NF"

            

            #Tenta encontrar o salario
            try:
                salario = driver.find_element(By.XPATH, '//*[@id="app-navigation"]/div[3]/div[2]/div[2]/div/div[1]/section/section[1]/div/div[1]/div[1]/div[2]')
                
                vaga['Média Salarial'] = salario.text
                
            #Caso não ache imprime uma mensagem
            except:
                print('Salário Não declarado')
                vaga['Média Salarial'] = 'NF'
            
            #Adicionamos o dict à lista criada no escopo mais amplo
            vagas.append(vaga)  
                # Se atingir a cada 30 vagas, clique no botão para ir para a próxima página
            if contador_vaga % 30 == 0:
                elemento = driver.find_elements(By.XPATH, '//*[@id="left-column"]/div[2]/div/button')
                if elemento:
                    continuar_pesquisa()
                    time.sleep(5)
                    verifica_pop_up = driver.find_elements(By.XPATH, '//*[@id="JAModal"]/div/div[2]/span')
                    if verifica_pop_up:
                        pop_up = driver.find_element(By.XPATH, '//*[@id="JAModal"]/div/div[2]/span')
                        pop_up.click()
                        time.sleep(2)
                else:
                    break

        #A lista estava vazia, então quebramos o loop
        else:
            
            #limpa o campo de localização
            limpa_localizacao = driver.find_element(By.XPATH, '//*[@id="searchBar-location"]')
            limpa_localizacao.send_keys(Keys.CONTROL + 'a')
            limpa_localizacao.send_keys(Keys.BACK_SPACE)
            
            break
            # Verificar se o card está presente
        xpath_card = f'//*[@id="left-column"]/div[2]/ul/li[{contador_vaga}]'
        verificacao_card = driver.find_elements(By.XPATH, xpath_card)
        
        # Se atingir o limite de vagas por localização ou não encontrar mais vagas, saia do loop
        if contador_vaga >= 1000 or not verificacao_card:
            break
            
        # Criar um arquivo CSV com as vagas coletadas da localização atual
        cria_csv(vagas, f"{categoria}_{localizacao.replace(' ', '_')}.csv")
        # Resto do seu código para coletar informações das vagas

        print(contador_vaga)


# Finalizar o navegador
driver.quit()
