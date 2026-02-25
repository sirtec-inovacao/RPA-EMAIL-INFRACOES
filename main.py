import os
import glob
import time
import logging
import gspread
from gsheets import Gsheets
# import xlwings as xw
from time import sleep

import numpy as np
import pandas as pd
from colorama import Fore, init
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright
from google.oauth2.service_account import Credentials
import google.auth.transport.requests
import io

from functions.delete_folders import delete_folders
from functions.clear_terminal import clear_terminal
from functions.drive_utils import download_latest_csvs_from_drive, upload_file_to_drive

from src.main_etp2 import main_etapa2

if os.name == 'nt':
    os.system('title ROBÔ - EMAIL INFRAÇÕES') 

"""
Config
"""


path_script = os.path.dirname(os.path.abspath(__file__))
gsheets = Gsheets()

acessos = gsheets.pegar_dados_aba_access()
df_acessos = pd.DataFrame(acessos)
df_acessos.columns = df_acessos.iloc[0]

for index, row in df_acessos.iterrows():
    local = str(row['local'])
    login = str(row['login'])
    senha = str(row['passw'])

    if local == 'pontomaisRS':
        login_pontomaisRS = login
        senha_pontomaisRS = senha

    # if local == 'pontomaisCE':
    #     login_pontomaisCE = login
    #     senha_pontomaisCE = senha

    if local == 'pontomaisVTC':
        login_pontomaisVTC = login
        senha_pontomaisVTC = senha

    if local == 'pontomaisBAR':
        login_pontomaisBAR = login
        senha_pontomaisBAR = senha

    if local == 'pontomaisFRS':
        login_pontomaisFRS = login
        senha_pontomaisFRS = senha

    if local == 'pontomaisPEL':
        login_pontomaisPEL = login
        senha_pontomaisPEL = senha

    if local == 'pontomaisPOA':
        login_pontomaisPOA = login
        senha_pontomaisPOA = senha

    if local == 'pontomaisBJL':
        login_pontomaisBJL = login
        senha_pontomaisBJL = senha

    if local == 'pontomaisSP':
        login_pontomaisSP = login
        senha_pontomaisSP = senha

init(autoreset=True)
clear_terminal()

# Configurar o logger
logging.basicConfig(
    filename='main.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Operações PontoMais
operations = [
    ["BJL", login_pontomaisBJL, senha_pontomaisBJL, "G:/Drives compartilhados/Inovação - RH/OESTE GUA-BJL.docx", "downloads/images/BJL"],
    ["RS", login_pontomaisRS, senha_pontomaisRS, "G:/Drives compartilhados/Inovação - RH/RS.docx", "downloads/images/RS"],
    ["PEL", login_pontomaisPEL, senha_pontomaisPEL, "G:/Drives compartilhados/Inovação - RH/PELOTAS.docx", "downloads/images/PEL"],
    # ["CE", login_pontomaisCE, senha_pontomaisCE, "G:/Drives compartilhados/Inovação - RH/CEARÁ.docx", "downloads/images/CE"],
    ["VTC", login_pontomaisVTC, senha_pontomaisVTC, "G:/Drives compartilhados/Inovação - RH/SUDOESTE VDC.docx", "downloads/images/VTC"],
    ["BAR", login_pontomaisBAR, senha_pontomaisBAR, "G:/Drives compartilhados/Inovação - RH/OESTE BAR-IBO.docx", "downloads/images/BAR"],
    ["FRS", login_pontomaisFRS, senha_pontomaisFRS, "G:/Drives compartilhados/Inovação - RH/CENTRO FRS.docx", "downloads/images/FRS"],
    ["POA", login_pontomaisPOA, senha_pontomaisPOA, "G:/Drives compartilhados/Inovação - RH/POA.docx", "downloads/images/POA"],
    ["SP", login_pontomaisSP, senha_pontomaisSP, "G:/Drives compartilhados/Inovação - RH/SP.docx", "downloads/images/SP"],
]

# Verificar se a pasta dowloads já existe
downloads_folder = os.path.join(path_script, 'downloads', 'fotos')
delete_folders(downloads_folder)

# Verificar se a pasta dowloads já existe
downloads_folder = os.path.join(path_script, 'downloads', 'jornadas')
delete_folders(downloads_folder)

# Criar pasta de downloads se não existir
download_dir = os.path.join(path_script, "downloads")
os.makedirs(download_dir, exist_ok=True)
os.makedirs(os.path.join(download_dir, "jornadas"), exist_ok=True)
os.makedirs(os.path.join(download_dir, "fotos"), exist_ok=True)


"""
#Config
"""

# Iniciando Downloads dos relatórios
print(Fore.CYAN + "############### INICIANDO DOWNLOAD DOS RELATORIOS ###############")

x = 0
for i in operations:
    while True:
        print(f"Operação: {i[0]}")
        if x == 10:
            x = 0
            break

        try:
            with sync_playwright() as p:
                today = datetime.now()

                # Início: dia 16 do mês anterior
                start = (today.replace(day=16) - timedelta(days=121)).strftime('%d/%m/%Y')
                end = (today - timedelta(days=1)).strftime('%d/%m/%Y')

                # Fim: dia atual
                # if today.day > 15:
                #     end = today.strftime('15/%m/%Y')
                # else:
                #     end = today.strftime('%d/%m/%Y')

                date = f"{start} - {end}"

                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    accept_downloads=True
                )
                page = context.new_page()

                # Configurar tela cheia antes de começar a navegação
                page.set_viewport_size({"width": 1820, "height": 980})
                page.goto("https://app2.pontomais.com.br/login")

                # OTIMIZAÇÃO 1: Espera campo de email aparecer de forma mais específica
                page.wait_for_selector("//*[@id='container-login']/div[1]/div/div[4]/div[1]/login-form/pm-form/form/div/div/div[1]/pm-input/div/div/pm-text/div/input", timeout=15000)

                page.fill("//*[@id='container-login']/div[1]/div/div[4]/div[1]/login-form/pm-form/form/div/div/div[1]/pm-input/div/div/pm-text/div/input", i[1])
                page.fill("//*[@id='container-login']/div[1]/div/div[4]/div[1]/login-form/pm-form/form/div/div/div[2]/pm-input/div/div/pm-password/div/input", i[2])
                page.click("//*[contains(text(), 'Entrar')]")

                page.wait_for_timeout(20000)

                page.goto("https://app2.pontomais.com.br/relatorios")

                while True:
                    try:
                        page.click('//*[@id="undefined"]/div/div/div[2]')
                        break
                    except:
                        pass
                sleep(2)
                page.click("//*[contains(text(), 'Atrasos')]")
                
                # # Selecionar o tipo de relarorio
                time.sleep(5)
                # page.fill('//*[@id=\"a34f79967bfa\"]/div[1]/div/input', 'Atrasos') # Jornada
                
                # page.keyboard.press('Enter')
                # time.sleep(5)
                # page.click('//*[@id="a34f79967bfa-6"]/div/div/div[2]/span')

                page.wait_for_timeout(5000)

                # Selecionar o periodo
                page.click('xpath=/html/body/app-mfe-remote/app-side-nav-outer-toolbar/dx-drawer/div/div[2]/dx-scroll-view/div[1]/div/div[1]/div[2]/div[1]/app-container/reports/div/div[1]/div/pm-card/div/div[2]/pm-form/form/div[2]/div/div[3]/pm-input/div/div/pm-date-range/div/input')
                page.wait_for_timeout(5000)
                page.click('xpath=/html/body/app-mfe-remote/app-side-nav-outer-toolbar/dx-drawer/div/div[2]/dx-scroll-view/div[1]/div/div[1]/div[2]/div[1]/app-container/reports/div/div[1]/div/pm-card/div/div[2]/pm-form/form/div[2]/div/div[3]/pm-input/div/div/pm-date-range/div/input')
                page.keyboard.down('Control')
                page.keyboard.press('A') 
                page.keyboard.up('Control')
                page.keyboard.type(date)
                page.keyboard.press('Enter')

                page.wait_for_timeout(5000)

                # Clicar no botão colunas
                page.click('xpath=/html/body/app-mfe-remote/app-side-nav-outer-toolbar/dx-drawer/div/div[2]/dx-scroll-view/div[1]/div/div[1]/div[2]/div[1]/app-container/reports/div/div[2]/div[1]/div/div[1]/pm-button/button')

                page.wait_for_timeout(5000)

                # Adicionar equipes
                #page.click('span:text("Equipe")')
                if i[0] == 'FRS':
                    page.click('xpath=/html/body/ngb-modal-window/div/div/pm-modal-multi-select-modal/div[2]/div/div/div[1]/pm-form/form/div[8]/div/div[1]/pm-input/div/div/pm-checkbox/ul/li/label/span')
                else:
                    page.click('span:text("Equipe")')

                page.wait_for_timeout(10000)

                page.click('xpath=/html/body/ngb-modal-window/div/div/pm-modal-multi-select-modal/div[2]/div/div/div[2]/pm-button/button') #btn salvar

                page.wait_for_timeout(10000)

                page.click('//*[@id="relatorios-baixar"]/pm-drop-down/a/div/pm-button/button/span[1]') #btn baixar

                page.mouse.wheel(0, 9999)  # Scroll 500 pixels para baixo

                # Aguardar um momento para o scroll completar
                page.wait_for_timeout(5000)

                # Lidar com downloads
                with page.expect_download(timeout=180000) as download_info:
                    #page.click("//html/body/app-root/app-side-nav-outer-toolbar/dx-drawer/div/div[2]/dx-scroll-view/div[1]/div/div[1]/div[2]/div[1]/app-container/reports/div/div[2]/div[2]/div/div[2]/pm-drop-down/a/div/div/a[3]")
                    page.click("//*[contains(text(), 'CSV')]")
                download = download_info.value
            
                # Salvar na pasta downloads
                download.save_as(os.path.join(download_dir, f'jornadas/{i[0]}.csv'))
                
                browser.close()
                break
        except Exception as e:
            try:
                browser.close()
            except:
                pass
            x += 1
            print(Fore.RED + f"Erro ao baixar o relatório: {i[0]}")
            print(e)
            pass


def get_files(path, extension=None):
    files = []
    for f in os.listdir(path):
        file_path = os.path.join(path, f)
        if os.path.isfile(file_path):
            if extension:
                if f.endswith(extension):
                    files.append(file_path)
            else:
                files.append(file_path)
    return files

def process_delays(excel_files):
    all_dfs = []

    for excel_file in excel_files:
        time.sleep(1)
        print(f"Processando arquivo: {excel_file}")
        try:
            #operacao = excel_file.split('/')[-1].split('.')[0]
            # Mudança de read_excel para read_csv com separador correto
            df = pd.read_csv(excel_file, sep=',', header=3, encoding="utf-8-sig")
            print(df)
            print(df.columns.to_list())
            operacao = excel_file.split('/')[-1].split('.')[0]
            df['Operação'] = operacao
            df = df[df['Nome'].notna()]

            df["Operação"] = np.where(
                df["Equipe"].astype(str)
                .str.strip().str.startswith("CE -"),
                "CE",
                operacao
            )

            def convert_to_timedelta(time_str):
                try:
                    if isinstance(time_str, timedelta):
                        return time_str
                    time_str = str(time_str).strip()
                    if ':' in time_str:
                        parts = time_str.split(':')
                        hours = int(parts[0])
                        minutes = int(parts[1])
                        return timedelta(hours=hours, minutes=minutes)
                    return pd.to_timedelta(time_str)
                except:
                    return pd.NaT

            df['Tempo de atraso'] = df['Tempo de atraso'].apply(convert_to_timedelta)

            # Converter data para o formato 'dd/mm/yyyy', extraindo a parte relevante
            df['Data'] = df['Data'].apply(lambda x: datetime.strptime(x.split(', ')[1], '%d/%m/%Y') if isinstance(x, str) else pd.NaT)
            df['Data'] = df['Data'].dt.strftime('%Y-%m-%d')
            print(df["Data"])

            all_dfs.append(df)
            
        except Exception as e:
            print(f"Erro ao processar arquivo {excel_file}: {str(e)}")

    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        df_atraso_maior_30min = combined_df[combined_df['Tempo de atraso'] > timedelta(minutes=10)]
        return df_atraso_maior_30min  # Retorna apenas colunas relevantes

    return pd.DataFrame()

def combine_latest_csvs(folder_path):
    def get_latest_csvs(folder_path):
        current_date = datetime.now()
        csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
        valid_files = []

        for file in csv_files:
            filename = os.path.basename(file)
            try:
                # Extrai a data do nome do arquivo (formato YYYY-MM)
                date = datetime.strptime(filename.split('.')[0], '%Y-%m')
                if date <= current_date:
                    # Adiciona à lista de arquivos válidos com o nome do arquivo e a data
                    valid_files.append((date, file))
            except ValueError:
                # Ignora arquivos com nomes que não seguem o formato esperado
                continue

        # Ordena os arquivos por data em ordem decrescente
        valid_files.sort(reverse=True, key=lambda x: x[0])

        # Retorna os dois arquivos mais recentes, ou None se não houver suficientes
        if len(valid_files) >= 2:
            return valid_files[0][1], valid_files[1][1]
        elif len(valid_files) == 1:
            return valid_files[0][1], None
        else:
            return None, None

    file1, file2 = get_latest_csvs(folder_path)
    print(f"Arquivo 1: {file1}")
    print(f"Arquivo 2: {file2}")
    if file1 is None:
        print("Nenhum arquivo CSV válido encontrado.")
        return None

    try:
        df1 = pd.read_csv(file1, sep=';', engine='python', on_bad_lines='warn')
        if file2 is not None:
            df2 = pd.read_csv(file2, sep=';', engine='python', on_bad_lines='warn')
            combined_df = pd.concat([df1, df2], ignore_index=True)
        else:
            combined_df = df1

        return combined_df
    except pd.errors.ParserError as e:
        print("Erro ao ler CSV:", e)
        return None

# Função principal para marcar atrasos no df_csvs
def mark_delays_in_csv(df_csvs, df_delays):
    df_csvs['Atraso'] = 0
    for _, row in df_delays.iterrows():
        print(row)
        data = row['Data']
        nome = row['Nome']
        mask = (df_csvs['Data'] == data) & (df_csvs['Nome'] == nome)
        df_csvs.loc[mask, 'Atraso'] = 1
    return df_csvs

# Uso do código
excel_files = get_files("downloads/jornadas/", ".csv")
df_delays = process_delays(excel_files)
df_delays.to_csv("atrasos.csv", index=False, sep=';')  # CSV é ~15x mais rápido que XLSX

folder_id = "1fDcVXWg1YJ3xlAer0JmOD59XtryiWR1N"
download_dir = os.path.join(path_script, "downloads", "bases_geral")
folder_path = download_latest_csvs_from_drive(folder_id, download_dir)

if folder_path is None:
    fallback_path = r"G:\Drives compartilhados\PCP\Time Inovação\Soluções\BI - Painel RH\Bases\Geral"
    if os.path.exists(fallback_path):
        print("Aviso: Falha ao baixar bases do Drive. Usando caminho de rede como fallback.")
        folder_path = fallback_path
    else:
        print(f"Erro crítico: Falha ao baixar bases do Drive e fallback {fallback_path} inacessível.")
        folder_path = None

df_csvs = combine_latest_csvs(folder_path)
df_csvs.to_csv("csvs.csv", index=False)  # CSV é ~15x mais rápido que XLSX
print(df_csvs)



if df_csvs is not None and not df_delays.empty:
    df_csvs = mark_delays_in_csv(df_csvs, df_delays)
    df_csvs.to_csv("final.csv", index=False, sep=';') # Salva para o processar_infracoes.py
    df_csvs.to_excel("final_TESTE.xlsx", index=False)
    
    # Salvar localmente e fazer upload final_TESTE.xlsx para o drive
    file_teste_path = "final_TESTE.xlsx"
    df_csvs.to_excel(file_teste_path, index=False)
    folder_id_email = "15CIGno6aVWxS1bwLktXelmFY-WGXdv3R"
    upload_file_to_drive(file_teste_path, folder_id_email)
    
    print(df_csvs)
else:
    print("Erro: Arquivo CSV ou dados de atraso não encontrados.")

# # Configurar as credenciais e a autorização
# scope = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive"
# ]
# creds = Credentials.from_service_account_file("service_account.json", scopes=scope)
# client = gspread.authorize(creds)

# # Abrir a planilha e selecionar a aba
# spreadsheet = client.open_by_key('1H1Mk2K3U_c-szdoAIllrd7gi2XWgTnPqLF9gjSesVrk')
# sheet = spreadsheet.worksheet("BD")

# # Excluir colunas A até N (A = 1, N = 14)
# start_column = 1  # Coluna A
# end_column = 14   # Coluna N

# spreadsheet.batch_update({
#     "requests": [
#         {
#             "deleteDimension": {
#                 "range": {
#                     "sheetId": sheet.id,
#                     "dimension": "COLUMNS",
#                     "startIndex": start_column - 1,  # Zero-indexed, então A é 0
#                     "endIndex": end_column           # N é 14
#                 }
#             }
#         }
#     ]
# })

# # Preparar dados para atualização
# dados = [df_csvs.columns.tolist()] + df_csvs.values.tolist()

# # Atualizar a faixa de dados a partir de A1 sem limpar a aba inteira
# sheet.update("A1", dados)  # Insere os dados a partir de A1

# ================================
# ANTIGO: Execução da Macro Excel (DESATIVADO)
# ================================
# path_arquivo = r'C:\\Users\\Sirtec\\arquivos_teste\\Gerador\\Geral_v2.5.2.xlsm'
# nome_macro = 'CriarResumoDeInfracoesTeste2'
# 
# try:
#     print("Executando macro, atualizando excel e gerando arquivos...")
#     arquivo = xw.Book(path_arquivo)
#     arquivo.app.api.WindowState = xw.constants.WindowState.xlMaximized
#     arquivo.app.api.Application.Calculation = xw.constants.Calculation.xlCalculationAutomatic
#     arquivo.app.activate(steal_focus=True) 
#     sleep(3)
#     executar_macro = arquivo.macro(nome_macro)
#     executar_macro()
#     arquivo.app.api.Application.Calculate()
#     sleep(3)
#     arquivo.app.quit()
# except Exception as e:
#     print(f"Erro ao executar a macro {nome_macro}: {e}")



from gerar_BD import gerar_bd_completo
from gerar_BD_RES import gerar_bd_res

try:
    print("\n" + "="*70)
    print("PROCESSANDO INFRAÇÕES E GERANDO RELATÓRIOS")
    print("="*70)
    
    # 1. Gerar BD.csv
    print("\n📊 Etapa 1: Gerando BD completo...")
    gerar_bd_completo()

    # 2. Gerar BD_RES.csv
    print("\n� Etapa 2: Gerando BD RES...")
    gerar_bd_res()
    

    
except Exception as e:
    print(f"\n❌ Erro ao processar: {e}")
    import traceback
    traceback.print_exc()


# executar envio dos emails  
#main_etapa2()


# atualizar planilha robos
#try:  
    # Atualizar planilha de robôs no drive
#    print("#Atualizando planilha de robôs no drive")
#    json = os.path.join(path_script, "chaveGoogle.json")
#    id_plan_att = "1lM8Q3NIUrDsdR8OD_6RG0wAddXvq1PpWczuOUeOyivE" # planilha de robôs no drive
#    aba_att = "Att_email_infracoes"
    
#    gsheets.attsheets(json, id_plan_att, aba_att)
#    att = True

#except Exception as e:
#    print(f"#Erro ao atualizar planilha de robôs no drive: {e}")
