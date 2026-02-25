from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.ponto_mais.downloads.rename_move_xlsx import xlsx_move

def download(driver, report, operation):
    # Baixa o relatório em xls
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/app-root/app-side-nav-outer-toolbar/dx-drawer/div/div[2]/dx-scroll-view/div[1]/div/div[1]/div[2]/div[1]/app-container/reports/div/div[2]/div[2]/div/div[2]/pm-drop-down/a/div/pm-button/button"))).click()
    button = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/app-root/app-side-nav-outer-toolbar/dx-drawer/div/div[2]/dx-scroll-view/div[1]/div/div[1]/div[2]/div[1]/app-container/reports/div/div[2]/div[2]/div/div[2]/pm-drop-down/a/div/div/a[3]")))
    # Da Scroll até a posicao do botao
    button.location_once_scrolled_into_view
    # Clica no botão
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/app-root/app-side-nav-outer-toolbar/dx-drawer/div/div[2]/dx-scroll-view/div[1]/div/div[1]/div[2]/div[1]/app-container/reports/div/div[2]/div[2]/div/div[2]/pm-drop-down/a/div/div/a[3]"))).click()

    # Aguarda realizar download
    sleep(40)
    xlsx_move(report, operation)
