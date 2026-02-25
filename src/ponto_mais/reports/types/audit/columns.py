from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def columns(driver):
    # Novo método criando o layut através das colunas (sem modelo de relatório)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(
        (By.XPATH, "//span[contains(.,' Colunas ')]"))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(
        (By.XPATH, "//span[contains(.,' Equipe ')]"))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(
        (By.XPATH, "//span[contains(.,' Cargo ')]"))).click()
    sleep(3)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(
        (By.XPATH, "//span[contains(.,' Salvar ')]"))).click()