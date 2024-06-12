from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from tkinter import filedialog, Tk
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import re
import time

print ('\nBem vindo ao eSAJ Scraping 2.0 do Pimentel & AlanGuerra!')
print ('-------------------------------------------\n')

ano = input('Entre com o ano de referência: ')
nome_pj = input('Entre com o nome do Procurador/PJ/Grupo/Foro/Vara: ')

data_e_hora_em_texto = datetime.now().strftime('%Y-%m-%d_%Hh%Mmin')

lista_consulta = []
lista_resultados = []
lista_erros = []
lista_inconclusivos = []
lista_arquivos = []

def encontra_processos(linha_de_texto):
    resultado = re.findall(r'[0-9]{7}[-][0-9]{2}[.][0-9]{4}[.][8][.][2][6][.][0-9]{4}', linha_de_texto)

    for r in resultado:
        if r not in lista_arquivos:
            lista_arquivos.append(r) 

def ler_arquivo(path_do_arquivo):
    with open(path_do_arquivo, encoding='latin-1') as file:
        for line in file:
            encontra_processos(line)

    print(f'Encontrei {len(lista_arquivos)} processos únicos.')

    print('Aguarde o processamento e a criação dos arquivos...')

    return lista_arquivos

def extrai_dados(lista_consulta):
    for n_processo in lista_consulta: 
        firefox_service = Service(GeckoDriverManager().install())
        firefox_options = Options()
        firefox_options.headless = True

        driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
        driver.get(f'https://esaj.tjsp.jus.br/cpopg/show.do?processo.codigo=9A0001V5X0000&processo.foro=334&processo.numero={n_processo}')

        time.sleep(2)

        mais_detalhes_element = driver.find_element(By.ID, 'maisDetalhes')
        
        driver.execute_script("arguments[0].setAttribute('class', 'collapse show')", mais_detalhes_element)

        assunto = "Não Encontrado"
        foro = "Não Encontrado"
        classe = "Não Encontrado"
        vara = "Não Encontrado"
        juiz = "Não Encontrado"
        distribuicao = "Não Encontrado"
        controle = "Não Encontrado"
        area = "Não Encontrado"
        valor_acao = "Não Encontrado"
        requerentes = "Não Encontrado"
        requeridos = "Não Encontrado"
        autor = "Não Encontrado"
        indiciado = "Não Encontrado"
        averiguado = "Não Encontrado"
        exeqte = "Não Encontrado"
        exectda = "Não Encontrado"

        try:
            assunto = driver.find_element(By.ID, 'assuntoProcesso').text
            print(f'Encontrado o Assunto do Processo: {assunto}')
        except:
            print('Não Encontrado o Assunto do Processo')

        try:
            foro = driver.find_element(By.ID, 'foroProcesso').text
            print(f'Encontrado o foro: {foro}')
        except:
            print('Não Encontrado o foro do Processo')

        try:
            classe = driver.find_element(By.ID, 'classeProcesso').text
            print(f'Encontrado a classe: {classe}')
        except:
            print('Não Encontrado a classe do processo')

        try:
            vara = driver.find_element(By.ID, 'varaProcesso').text
            print(f'Encontrado o vará : {vara}')
        except:
            print('Não Encontrado o vará do processo ')

        try:
            juiz = driver.find_element(By.ID, 'juizProcesso').text
            print(f'Encontrado o Juiz: {juiz}')
        except:
            print('Não Encontrado o Juiz do processo')

        try:
            distribuicao = driver.find_element(By.ID, 'dataHoraDistribuicaoProcesso').text
            print(f'Encontrado a Distribuição : {distribuicao}')
        except:
            print('Não Encontrado a Distribuição do processo ')

        try:
            controle = driver.find_element(By.ID, 'numeroControleProcesso').text
            print(f'Encontrado o número de controle: {controle}')
        except:
            print('Não Encontrado o número de controle do Processo')

        try:
            area_element = driver.find_element(By.ID, 'areaProcesso')
            area = area_element.find_element(By.TAG_NAME, 'span').get_attribute('title')
            print(f'Encontrado a Área do Processo: {area}')
        except:
            print('Não Encontrado a Área do Processo')

        try:
            valor_acao_element = driver.find_element(By.ID, 'valorAcaoProcesso')
            valor_acao = valor_acao_element.text.strip()
            print(f'Encontrado o valor da ação: {valor_acao}')
        except:
            print('Não Encontrado o valor da ação')

        try:
            requerentes_element = driver.find_element(By.XPATH, '//span[contains(@class, "tipoDeParticipacao") and contains(text(), "Reqte")]/../../following-sibling::td[@class="nomeParteEAdvogado"]')
            requerentes_text = requerentes_element.text.strip()
            requerentes = requerentes_text.replace('\n', ', ')
            print(f'Encontrado os requerentes: {requerentes}')
        except:
            print('Não Encontrado os requerentes do processo')

        try:
            requeridos_element = driver.find_element(By.XPATH, '//span[contains(@class, "tipoDeParticipacao") and contains(text(), "Reqdo")]/../../following-sibling::td[@class="nomeParteEAdvogado"]')
            requeridos_text = requeridos_element.text.strip()
            requeridos = requeridos_text.replace('\n', ', ')
            print(f'Encontrado os requeridos: {requeridos}')
        except:
            print('Não Encontrado os requeridos do processo')
            
        try:
            autor_element = driver.find_element(By.XPATH, '//span[contains(@class, "tipoDeParticipacao") and contains(text(), "Autor")]/../following-sibling::td[@class="nomeParteEAdvogado"]')
            autor_text = autor_element.text.strip()
            autor = autor_text.replace('\n', ', ')
            print(f'Encontrado o Autor: {autor}')
        except:
            print('Não Encontrado o Autor do processo')

        try:
            link_partes = driver.find_element(By.ID, 'linkpartes')
            driver.execute_script("arguments[0].click();", link_partes)
        except:
            pass

        try:
            indiciado_element = driver.find_element(By.XPATH, '//span[contains(@class, "tipoDeParticipacao") and contains(text(), "Indiciado")]/../following-sibling::td[@class="nomeParteEAdvogado"]')
            indiciado_text = indiciado_element.text.strip()
            indiciado = indiciado_text.replace('\n', ', ')
            print(f'Encontrado o Indiciado: {indiciado}')
        except:
            print('Não Encontrado o Indiciado do processo')

        try:
            averiguado_element = driver.find_element(By.XPATH, '//span[contains(@class, "tipoDeParticipacao") and contains(text(), "Averiguado")]/../following-sibling::td[@class="nomeParteEAdvogado"]')
            averiguado_text = averiguado_element.text.strip()
            averiguado = averiguado_text.replace('\n', ', ')
            print(f'Encontrado o Averiguado: {averiguado}')
        except:
            print('Não Encontrado o Averiguado do processo')

        try:
            exeqte_element = driver.find_element(By.XPATH, '//span[contains(@class, "tipoDeParticipacao") and contains(text(), "Exeqte")]/../following-sibling::td[@class="nomeParteEAdvogado"]')
            exeqte_text = exeqte_element.text.strip()
            exeqte = exeqte_text.replace('\n', ', ')
            print(f'Encontrado o Exeqte: {exeqte}')
        except:
            print('Não Encontrado o Exeqte do processo')

        try:
            exectda_element = driver.find_element(By.XPATH, '//span[contains(@class, "tipoDeParticipacao") and contains(text(), "Exectda")]/../following-sibling::td[@class="nomeParteEAdvogado"]')
            exectda_text = exectda_element.text.strip()
            exectda = exectda_text.replace('\n', ', ')
            print(f'Encontrado o Exectda: {exectda}')
        except:
            print('Não Encontrado o Exectda do processo')

        lista_resultados.append([n_processo, assunto, foro, classe, vara, juiz, distribuicao, controle, area, valor_acao, requerentes, requeridos, autor, indiciado, averiguado, exeqte, exectda])

        driver.quit()

def criar_planilha():
    columns = ['Número do processo', 'Assunto', 'Foro', 'Classe', 'Varé', 'Juiz', 'Distribuição', 'Controle', 'Área', 'Valor da Ação', 'Requerentes', 'Requeridos', 'Autor', 'Indiciado', 'Averiguado', 'Exeqte', 'Exectda'] 

    df = pd.DataFrame(lista_resultados, columns=columns)

    columns = ['Número do processo', 'Erro']
    
    df_erros = pd.DataFrame(lista_erros, columns=columns)

    with pd.ExcelWriter(f'{nome_pj}_{ano}_resultado_dos_recursos_{data_e_hora_em_texto}.xlsx') as writer:  
        df.to_excel(writer, sheet_name='resultados')
        df_erros.to_excel(writer, sheet_name='erros ou não processados')

def criar_arquivo_texto():
    nome_arquivo_texto = f'{nome_pj}_{ano}_resultado_dos_recursos_{data_e_hora_em_texto}.txt'

    with open(nome_arquivo_texto, 'w', encoding='utf-8') as arquivo_texto:
        arquivo_texto.write(f'Resultado dos processos recebidos por/pelo {nome_pj} no ano {ano} julgados pelo TJSP\n\n')

        for resultado in lista_resultados:
            numero_processo = resultado[0]
            assunto = resultado[1]
            foro = resultado[2]
            classe = resultado[3]
            vara = resultado[4]
            juiz = resultado[5]
            distribuicao = resultado[6]
            controle = resultado[7]
            area = resultado[8]
            valor_acao = resultado[9]
            requerentes = resultado[10]
            requeridos = resultado[11]
            autor = resultado[12]
            indiciado = resultado[13]
            averiguado = resultado[14]
            exeqte = resultado[15]
            exectda = resultado[16]

            arquivo_texto.write(f'Número do processo: {numero_processo}\n')
            arquivo_texto.write(f'Assunto: {assunto}\n')
            arquivo_texto.write(f'Foro: {foro}\n')
            arquivo_texto.write(f'Classe: {classe}\n')
            arquivo_texto.write(f'Vara: {vara}\n')
            arquivo_texto.write(f'Juiz: {juiz}\n')
            arquivo_texto.write(f'Distribuição: {distribuicao}\n')
            arquivo_texto.write(f'Controle: {controle}\n')
            arquivo_texto.write(f'Área: {area}\n')
            arquivo_texto.write(f'Valor da Ação: {valor_acao}\n')
            arquivo_texto.write(f'Requerentes: {requerentes}\n')
            arquivo_texto.write(f'Requeridos: {requeridos}\n')
            arquivo_texto.write(f'Autor: {autor}\n')
            arquivo_texto.write(f'Indiciado: {indiciado}\n')
            arquivo_texto.write(f'Averiguado: {averiguado}\n')
            arquivo_texto.write(f'Exeqte: {exeqte}\n')
            arquivo_texto.write(f'Executada: {exectda}\n')
            arquivo_texto.write('======================================================')

def Main():
    root = Tk()
    root.withdraw()

    file = filedialog.askopenfilename(title='Selecione o arquivo texto ou csv com os números dos processos', initialdir='.')

    lista_arquivos = ler_arquivo(file)

    extrai_dados(lista_arquivos)

    criar_planilha()

    criar_arquivo_texto()

if __name__ == '__main__':
    Main()

    print('Programa concluído!')
