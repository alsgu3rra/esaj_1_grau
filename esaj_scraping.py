from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from tkinter import filedialog, Tk
from datetime import datetime
import re
import time

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

        time.sleep(3)

        mais_detalhes_element = driver.find_element(By.ID, 'maisDetalhes')
        driver.execute_script("arguments[0].setAttribute('class', 'collapse show')", mais_detalhes_element)

        time.sleep(1)

        try:
            link_partes = driver.find_element(By.ID, 'linkpartes')
            driver.execute_script("arguments[0].click();", link_partes)
            time.sleep(2)
        except:
            print('Não foi possível expandir a seção de partes.')

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
            indiciado_element = driver.find_element(By.XPATH, '//span[contains(@class, "tipoDeParticipacao") and contains(text(), "Indiciado")]/../following-sibling::td[@class="nomeParteEAdvogado"]')
            indiciado_text = indiciado_element.text.strip()
            indiciado = indiciado_text.replace('\n', ', ')
            print(f'Encontrado o Indiciado: {indiciado}')
        except:
            print('Não Encontrado o Indiciado do processo')

        driver.quit()

def Main():
    root = Tk()
    root.withdraw()

    file = filedialog.askopenfilename(title='Selecione o arquivo texto ou csv com os números dos processos', initialdir='.')

    lista_arquivos = ler_arquivo(file)

    extrai_dados(lista_arquivos)

if __name__ == '__main__':
    Main()
