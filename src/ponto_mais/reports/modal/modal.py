from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException


def close(driver):
    # add cookies
    # cookie to remove pop up de pesquisa de satisfação
    try:
        modal = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'wootric-desktop-modal'))
        )

        botao = modal.find_element(By.CLASS_NAME, 'wootric-close-right')
        botao.click()
        sleep(10)
    except Exception as e:
        print(f"Erro ao clicar no botão do modal. Pode ser que o modal não esteja mais sendo exibido!")