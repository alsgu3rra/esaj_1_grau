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

root = Tk()
root.withdraw()

def Main():
  firefox_service = Service(GeckoDriverManager().install())

  firefox_options = Options()
  
  firefox_options.headless = True

  driver = webdriver.Firefox(service=firefox_service, options=firefox_options)

  url = "https://esaj.tjsp.jus.br/cpopg/show.do?processo.codigo=9A0001VSZ0000&processo.foro=334&processo.numero=1000664-45.2024.8.26.0334"

  driver.get(url)

  time.sleep(5)

  driver.quit()

if __name__ == '__main__':
  Main()
