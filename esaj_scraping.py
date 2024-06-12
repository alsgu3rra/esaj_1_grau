from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from tkinter import filedialog, Tk
from datetime import datetime
import time


data_e_hora_em_texto = datetime.now().strftime('%Y-%m-%d_%Hh%Mmin')

lista_consulta = []
lista_resultados = []
lista_erros = []
lista_inconclusivos = []
lista_arquivos = []

url = "https://esaj.tjsp.jus.br/cpopg"

def abrir_navegador(url_site):
  firefox_service = Service(GeckoDriverManager().install())

  firefox_options = Options()
  
  firefox_options.headless = True

  driver = webdriver.Firefox(service=firefox_service, options=firefox_options)

  driver.get(url_site)

  time.sleep(5)

  driver.quit()

def Main():
  root = Tk()
  root.withdraw()

  file = filedialog.askopenfilename(title = 'Selecione o arquivo texto ou csv com os números dos processos', initialdir = '.')

  abrir_navegador(url)

if __name__ == '__main__':
  Main()
