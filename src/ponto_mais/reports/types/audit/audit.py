
import pyperclip

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from src.ponto_mais.reports.modal import modal
from src.ponto_mais.utilities.operation import operations
from src.ponto_mais.auth.logout import logout
from src.ponto_mais.downloads import download_xlsx
from src.ponto_mais.reports.types.audit import columns
from src.ponto_mais.reports.period import getPeriod

def reports_audit(operation: operations.Operations, data_in, data_fi, driver):
    try:
        print("INICIANDO DOWNLOAD DO RELATÓRIO DE AUDITORIA. OPERAÇÃO: " + operation.operation)
        getPeriod.writeDate("audit")

        if(operation.operation == "PEL"):
            print("última operação sendo executada, iniciando salvamento da data: " + data_in + " : " + data_fi)
            getPeriod.writeDate("audit")

        print(data_in, data_fi)

        today = data_in
        today_f = data_fi
        print(today, today_f)

        # Adiciona data do filtro
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/app-root/app-side-nav-outer-toolbar/dx-drawer/div/div[2]/dx-scroll-view/div[1]/div/div[1]/div[2]/div[1]/app-container/reports/div/div[1]/div/pm-card/div/div[2]/pm-form/form/div[2]/div/div[3]/pm-input/div/div/pm-date-range/div/input"))).clear()
        pyperclip.copy(f'{today}-{today_f}')
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/app-root/app-side-nav-outer-toolbar/dx-drawer/div/div[2]/dx-scroll-view/div[1]/div/div[1]/div[2]/div[1]/app-container/reports/div/div[1]/div/pm-card/div/div[2]/pm-form/form/div[2]/div/div[3]/pm-input/div/div/pm-date-range/div/input"))).send_keys(Keys.CONTROL, 'v')
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/app-root/app-side-nav-outer-toolbar/dx-drawer/div/div[2]/dx-scroll-view/div[1]/div/div[1]/div[2]/div[1]/app-container/reports/div/div[1]/div/pm-card/div/div[2]/pm-form/form/div[2]/div/div[3]/pm-input/div/div/pm-date-range/div/input"))).send_keys(Keys.CONTROL, 'a')
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/app-root/app-side-nav-outer-toolbar/dx-drawer/div/div[2]/dx-scroll-view/div[1]/div/div[1]/div[2]/div[1]/app-container/reports/div/div[1]/div/pm-card/div/div[2]/pm-form/form/div[2]/div/div[3]/pm-input/div/div/pm-date-range/div/input"))).send_keys(Keys.CONTROL, 'v')
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/app-root/app-side-nav-outer-toolbar/dx-drawer/div/div[2]/dx-scroll-view/div[1]/div/div[1]/div[2]/div[1]/app-container/reports/div/div[1]/div/pm-card/div/div[2]/pm-form/form/div[2]/div/div[3]/pm-input/div/div/pm-date-range/div/input"))).send_keys(Keys.ENTER)

        driver.find_element(By.CSS_SELECTOR, ".ng-invalid > .form-group .ng-input").click()
        # pyautogui.write('auditoria')
        element = driver.find_element(By.XPATH, "/html/body/ng-dropdown-panel/div[2]/div[2]/div[8]/div/div/div[2]/span")
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()


    except: 
        print("Ocorreu algum erro durante a filtragem em auditoria. (Pode não ser nada e reiniciar pode resolver)")

    modal.close(driver)
    columns.columns(driver)
    download_xlsx.download(driver, "audit", operation.operation)
    logout(driver)
