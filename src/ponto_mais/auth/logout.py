from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def logout(driver):
    try:
        # Aguarda carregar e checa se já existe um login e deslogar
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/app-root/app-side-nav-outer-toolbar/app-header/header/dx-toolbar/div/div[1]/div/dxi-item/a/img[1]")))
        print('Login encontrado, deslogando')
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "//app-user-panel/div/div/div/div"))).click()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Sair')]"))).click()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(.,'Sim')]"))).click()
    except:
        print("fechou aqui 1")
        pass
