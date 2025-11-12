import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service



# Caminho correto do chromedriver
service = Service(
    log_path=os.devnull,
    executable_path="{{ "{{ cookiecutter.project_slug }}" }}/bin/chromedriver.exe",    
)

# Configurar navegador (sem headless para você visualizar)
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--start-maximized")  # Abrir em tela cheia para ver tudo
chrome_options.binary_location = "{{ "{{ cookiecutter.project_slug }}" }}/bin/chrome-win32/chrome.exe" # Você precisa extrair o bin para usar isso

driver = webdriver.Chrome(service=service, options=chrome_options)

