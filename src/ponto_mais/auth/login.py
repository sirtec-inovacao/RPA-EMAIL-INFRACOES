from selenium import webdriver
from time import sleep 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.ponto_mais.utilities.operation import operations
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def login(driver, operation: operations.Operations):
    try:
        login = str(operation.email)
        pswd = str(operation.password)

        # Login
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "//*[@id='container-login']/div[1]/div/div[4]/div[1]/login-form/pm-form/form/div/div/div[1]/pm-input/div/div/pm-text/div/input"))).send_keys(login)
        # Senha
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "//*[@id='container-login']/div[1]/div/div[4]/div[1]/login-form/pm-form/form/div/div/div[2]/pm-input/div/div/pm-password/div/input"))).send_keys(pswd)
        # Clicar no entrar
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Entrar')]"))).click()
        # # Dá enter para entrar
        # WebDriverWait(driver, 20).until(EC.presence_of_element_located(
        #     (By.XPATH, "/html/body/app-root/dx-drawer/div/div[2]/div[2]/div/app-container/login/div/div[1]/div/div[4]/div[1]/login-form/pm-form/form/div/div/div[2]/pm-input/div/div/pm-text/div/input"))).send_keys(Keys.ENTER)
        # Aguarda carregar
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/app-root/app-side-nav-outer-toolbar/app-header/header/dx-toolbar/div/div[1]/div/dxi-item/a/img[1]")))

        # Carrega a pág de relatórios
        driver.get("https://app2.pontomais.com.br/relatorios")
        sleep(10)
    except Exception as e:
        Error(driver, operation)
        

def Error(driver, operation: operations.Operations):
    print("Ocorreu algum erro no login, vamos aguardar 3min e tentar novamente!")
    sleep(180)
    print("Tentando logar novamente")
    login(driver, operation)
