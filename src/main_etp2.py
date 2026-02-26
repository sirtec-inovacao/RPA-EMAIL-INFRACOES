#from ponto_mais.auth.logout import logout
from gsheets import Gsheets
import os
from pathlib import Path
#from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.ponto_mais.utilities.operation.operations import Operations
from src.ponto_mais.utilities.operation.operations_manager import OperationsManager
from src.ponto_mais.utilities.delete.folders.delete_folders import delete_folders
#from src.ponto_mais.analysis.Analise_Excel import analise_file
from src.ponto_mais.utilities.email.email_manager import EmailSender
from src.teste_sirtec import pdf_to_images
import pandas as pd

# Caminho do script atual
path_script = os.path.dirname(os.path.abspath(__file__))

# Subir um nível na hierarquia de diretórios
path_parent = os.path.dirname(path_script)

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

list_todas_operacoes = gsheets.pegar_lista_emails(coluna_ref=1)
list_rs = gsheets.pegar_lista_emails(coluna_ref=2)
list_pel_poa = gsheets.pegar_lista_emails(coluna_ref=3)
list_ce = gsheets.pegar_lista_emails(coluna_ref=4)
list_ourinhos = gsheets.pegar_lista_emails(coluna_ref=5)
list_sudoeste = gsheets.pegar_lista_emails(coluna_ref=6)
list_oeste = gsheets.pegar_lista_emails(coluna_ref=7)
list_extremo_oeste = gsheets.pegar_lista_emails(coluna_ref=8)
list_centro = gsheets.pegar_lista_emails(coluna_ref=9)

operations_list = [
    Operations("RS", login_pontomaisRS, senha_pontomaisRS, "G:/Drives compartilhados/Inovação - RH/RS.docx", "downloads/images/RS"),
    # Operations("CE", login_pontomaisCE, senha_pontomaisCE,  "G:/Drives compartilhados/Inovação - RH/CEARÁ.docx", "downloads/images/CE"),
    Operations("VTC", login_pontomaisVTC, senha_pontomaisVTC, "G:/Drives compartilhados/Inovação - RH/SUDOESTE VDC.docx", "downloads/images/VTC"),
    Operations("BAR", login_pontomaisBAR, senha_pontomaisBAR, "G:/Drives compartilhados/Inovação - RH/OESTE BAR-IBO.docx", "downloads/images/BAR"),
    Operations("FRS", login_pontomaisFRS, senha_pontomaisFRS, "G:/Drives compartilhados/Inovação - RH/CENTRO FRS.docx", "downloads/images/FRS"),
    Operations("PEL", login_pontomaisPEL, senha_pontomaisPEL, "G:/Drives compartilhados/Inovação - RH/PELOTAS.docx", "downloads/images/PEL"),
    Operations("FRS", login_pontomaisFRS, senha_pontomaisFRS, "G:/Drives compartilhados/Inovação - RH/CENTRO FRS.docx", "downloads/images/FRS"),
    Operations("BJL", login_pontomaisBJL, senha_pontomaisBJL, "G:/Drives compartilhados/Inovação - RH/OESTE GUA-BJL.docx", "downloads/images/BJL"),
    Operations("POA", login_pontomaisPOA, senha_pontomaisPOA, "G:/Drives compartilhados/Inovação - RH/POA.docx", "downloads/images/POA"),
    Operations("SP", login_pontomaisSP, senha_pontomaisSP, "G:/Drives compartilhados/Inovação - RH/SP.docx", "downloads/images/SP")
]

def main_etapa2():
    while True:
        downloads_folder = 'downloads/'
        delete_folders(downloads_folder)

        print("############### INICIANDO DOWNLOAD DOS RELATORIOS ###############")

        # options = Options()
        # options.add_experimental_option("excludeSwitches",["enable-automation"])
        # options.add_experimental_option('detach', True)
        # options.add_argument('--start-maximized')
        # driver = webdriver.Chrome(options=options)

        # driver.get("https://app2.pontomais.com.br/login")

        # logout(driver)

        output_folder = 'downloads/images/'

        # #Iniciando processo de download do registro de ponto
        # recordsManager = OperationsManager(operations_list)
        # recordsManager.process_operation_records(driver)

        #Iniciando processo para obter imagens dos documentos world
        """
        manager = OperationsManager(operations_list)
        manager.process_images(output_folder)

        # BAR
        pdf_to_images("grafico_geral", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/BAR/grafico_geral.pdf', 'ponto_mais/analysis/BAR', 1, zoom=3.0)

        pdf_to_images("ocorrencia_pontos", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/BAR/ocorrencia_pontos.pdf', 'ponto_mais/analysis/BAR', 1, zoom=3.0)

        pdf_to_images("ocorrencia_pontos_mensal", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/BAR/ocorrencia_pontos_mensal.pdf', 'ponto_mais/analysis/BAR', 1, zoom=3.0)

        pdf_to_images("quadro_detalhado", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/BAR/quadro_detalhado.pdf', 'ponto_mais/analysis/BAR', 1, zoom=3.0)

        pdf_to_images("quadro_equipes", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/BAR/quadro_equipes.pdf', 'ponto_mais/analysis/BAR', 1, zoom=3.0)

        # BJL
        pdf_to_images("grafico_geral", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/BJL/grafico_geral.pdf', 'ponto_mais/analysis/BJL', 1, zoom=3.0)

        pdf_to_images("ocorrencia_pontos", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/BJL/ocorrencia_pontos.pdf', 'ponto_mais/analysis/BJL', 1, zoom=3.0)

        pdf_to_images("ocorrencia_pontos_mensal", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/BJL/ocorrencia_pontos_mensal.pdf', 'ponto_mais/analysis/BJL', 1, zoom=3.0)

        pdf_to_images("quadro_detalhado", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/BJL/quadro_detalhado.pdf', 'ponto_mais/analysis/BJL', 1, zoom=3.0)

        pdf_to_images("quadro_equipes", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/BJL/quadro_equipes.pdf', 'ponto_mais/analysis/BJL', 1, zoom=3.0)

        # CE
        # pdf_to_images("grafico_geral", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/CE/grafico_geral.pdf', 'ponto_mais/analysis/CE', 1, zoom=3.0)

        # pdf_to_images("ocorrencia_pontos", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/CE/ocorrencia_pontos.pdf', 'ponto_mais/analysis/CE', 1, zoom=3.0)

        # pdf_to_images("ocorrencia_pontos_mensal", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/CE/ocorrencia_pontos_mensal.pdf', 'ponto_mais/analysis/CE', 1, zoom=3.0)

        # pdf_to_images("quadro_detalhado", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/CE/quadro_detalhado.pdf', 'ponto_mais/analysis/CE', 1, zoom=3.0)

        # pdf_to_images("quadro_equipes", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/CE/quadro_equipes.pdf', 'ponto_mais/analysis/CE', 1, zoom=3.0)

        # FRS
        pdf_to_images("grafico_geral", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/FRS/grafico_geral.pdf', 'ponto_mais/analysis/FRS', 1, zoom=3.0)

        pdf_to_images("ocorrencia_pontos", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/FRS/ocorrencia_pontos.pdf', 'ponto_mais/analysis/FRS', 1, zoom=3.0)

        pdf_to_images("ocorrencia_pontos_mensal", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/FRS/ocorrencia_pontos_mensal.pdf', 'ponto_mais/analysis/FRS', 1, zoom=3.0)

        pdf_to_images("quadro_detalhado", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/FRS/quadro_detalhado.pdf', 'ponto_mais/analysis/FRS', 1, zoom=3.0)

        pdf_to_images("quadro_equipes", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/FRS/quadro_equipes.pdf', 'ponto_mais/analysis/FRS', 1, zoom=3.0)

        # PEL
        pdf_to_images("grafico_geral", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/PEL/grafico_geral.pdf', 'ponto_mais/analysis/PEL', 1, zoom=3.0)

        pdf_to_images("ocorrencia_pontos", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/PEL/ocorrencia_pontos.pdf', 'ponto_mais/analysis/PEL', 1, zoom=3.0)

        pdf_to_images("ocorrencia_pontos_mensal", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/PEL/ocorrencia_pontos_mensal.pdf', 'ponto_mais/analysis/PEL', 1, zoom=3.0)

        pdf_to_images("quadro_detalhado", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/PEL/quadro_detalhado.pdf', 'ponto_mais/analysis/PEL', 1, zoom=3.0)

        pdf_to_images("quadro_equipes", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/PEL/quadro_equipes.pdf', 'ponto_mais/analysis/PEL', 1, zoom=3.0)

        # RS
        pdf_to_images("grafico_geral", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/RS/grafico_geral.pdf', 'ponto_mais/analysis/RS', 1, zoom=3.0)

        pdf_to_images("ocorrencia_pontos", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/RS/ocorrencia_pontos.pdf', 'ponto_mais/analysis/RS', 1, zoom=3.0)

        pdf_to_images("ocorrencia_pontos_mensal", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/RS/ocorrencia_pontos_mensal.pdf', 'ponto_mais/analysis/RS', 1, zoom=3.0)

        pdf_to_images("quadro_detalhado", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/RS/quadro_detalhado.pdf', 'ponto_mais/analysis/RS', 1, zoom=3.0)

        pdf_to_images("quadro_equipes", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/RS/quadro_equipes.pdf', 'ponto_mais/analysis/RS', 1, zoom=3.0)

        # VTC
        pdf_to_images("grafico_geral", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/VTC/grafico_geral.pdf', 'ponto_mais/analysis/VTC', 1, zoom=3.0)

        pdf_to_images("ocorrencia_pontos", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/VTC/ocorrencia_pontos.pdf', 'ponto_mais/analysis/VTC', 1, zoom=3.0)

        pdf_to_images("ocorrencia_pontos_mensal", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/VTC/ocorrencia_pontos_mensal.pdf', 'ponto_mais/analysis/VTC', 1, zoom=3.0)

        pdf_to_images("quadro_detalhado", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/VTC/quadro_detalhado.pdf', 'ponto_mais/analysis/VTC', 1, zoom=3.0)

        pdf_to_images("quadro_equipes", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/VTC/quadro_equipes.pdf', 'ponto_mais/analysis/VTC', 1, zoom=3.0)

        # SP
        pdf_to_images("grafico_geral", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/SP/grafico_geral.pdf', 'ponto_mais/analysis/SP', 1, zoom=3.0)

        pdf_to_images("ocorrencia_pontos", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/SP/ocorrencia_pontos.pdf', 'ponto_mais/analysis/SP', 1, zoom=3.0)

        pdf_to_images("ocorrencia_pontos_mensal", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/SP/ocorrencia_pontos_mensal.pdf', 'ponto_mais/analysis/SP', 1, zoom=3.0)

        pdf_to_images("quadro_detalhado", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/SP/quadro_detalhado.pdf', 'ponto_mais/analysis/SP', 1, zoom=3.0)

        pdf_to_images("quadro_equipes", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/SP/quadro_equipes.pdf', 'ponto_mais/analysis/SP', 1, zoom=3.0)


        # #Iniciando processo de download do jornada
        # journeyManager = OperationsManager(operations_list)
        # journeyManager.process_operation_journey(output_folder, driver)

        # # Iniciando processo de download de auditoria
        # auditManager = OperationsManager(operations_list)
        # auditManager.process_operation_audit(output_folder, driver)

        # # Iniciando processo de analise
        # analise_file.analise_main
        """
        # ---------------------------------------------------------------------
        # NOVA LOGICA: Processamento de infracoes e geracao de imagens em Python
        # Substitui a conversao de PDF para imagens
        # ---------------------------------------------------------------------
        from processar_infracoes import processar_infracoes, gerar_relatorios, salvar_resumo
        
        print("\n>> Iniciando processamento de infracoes (Python)...")
        # Caminho do arquivo final (ajuste conforme necessario, assumindo raiz do projeto)
        arquivo_final_xlsx = os.path.join(path_parent, 'final.xlsx')
        arquivo_final_csv = os.path.join(path_parent, 'final.csv')
        
        df_resumo = pd.DataFrame()
        
        if os.path.exists(arquivo_final_xlsx):
            df_resumo = processar_infracoes(arquivo_final_xlsx)
        elif os.path.exists(arquivo_final_csv):
             df_resumo = processar_infracoes(arquivo_final_csv)
        else:
            print(">> ERRO: Arquivo final.xlsx/csv nao encontrado na raiz.")
            
        if not df_resumo.empty:
            salvar_resumo(df_resumo, os.path.join(path_parent, 'BD_RES.csv'))
            
            print(">> Gerando imagens dos relatorios...")
            # Gera imagens em downloads/images/{SIGLA}/...
            gerar_relatorios(df_resumo, base_output_dir=os.path.join(path_parent, 'downloads/images'))
        else:
            print(">> Nenhuma infracao encontrada ou erro ao processar.")

        # COMENTADO: Antiga logica de converter PDF (nao usada mais)
        # ----------------------------------------------------------
        # # BAR
        # pdf_to_images("grafico_geral", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/BAR/grafico_geral.pdf', 'ponto_mais/analysis/BAR', 1, zoom=3.0)
        # ... (restante dos pdf_to_images comentado) ...


        # Initialize the email sender
        sender = EmailSender()

        # Defining test list
        test_list = ["ricardo.souza@sirtec.com.br"]

        # Send emails
        # ORIGINAL:
        # success = sender.send_email(
        #     to_list=list_rs,
        #     cc_list=list_todas_operacoes,
        #     image_path='ponto_mais/analysis/RS',
        #     image_base_path_downloads=Path(os.path.join(path_parent, r'downloads\images\RS')),
        #     subject = 'Ocorrências de ponto Sirtec - RS V3'
        # )
        success = sender.send_email(
            to_list=test_list,
            cc_list=[], # Clearing CC list as requested "unico email"
            image_path='ponto_mais/analysis/RS',
            image_base_path_downloads=Path(os.path.join(path_parent, r'downloads\images\RS')),
            subject = 'Ocorrências de ponto Sirtec - RS V3'
        )

        if not success:
            print("Check email_sender.log for error details")


        # Send emails
        # ORIGINAL:
        # success = sender.send_email(
        #     to_list=list_pel_poa,
        #     cc_list=list_todas_operacoes,
        #     image_path='ponto_mais/analysis/PEL',
        #     image_base_path_downloads=Path(os.path.join(path_parent, r'downloads\images\PEL')),
        #     subject = 'Ocorrências de ponto Sirtec - POA/PEL V3'
        # )
        success = sender.send_email(
            to_list=test_list,
            cc_list=[],
            image_path='ponto_mais/analysis/PEL',
            image_base_path_downloads=Path(os.path.join(path_parent, r'downloads\images\PEL')),
            subject = 'Ocorrências de ponto Sirtec - POA/PEL V3'
        )

        if not success:
            print("Check email_sender.log for error details")



        # # Send emails
        # success = sender.send_email(
        #     to_list=list_ce,
        #     cc_list=list_todas_operacoes,
        #     image_path='ponto_mais/analysis/CE',
        #     image_base_path_downloads=Path(os.path.join(path_parent, r'downloads\images\RSCE')),
        #     subject = 'Ocorrências de ponto Sirtec - CE V3'
        # )

        if not success:
            print("Check email_sender.log for error details")


        # Send emails
        # ORIGINAL:
        # success = sender.send_email(
        #     to_list=list_sudoeste,
        #     cc_list=list_todas_operacoes,
        #     image_path='ponto_mais/analysis/VTC',
        #     image_base_path_downloads=Path(os.path.join(path_parent, r'downloads\images\VTC')),
        #     subject = 'Ocorrências de ponto Sirtec - BA Sudoeste'
        # )
        success = sender.send_email(
            to_list=test_list,
            cc_list=[],
            image_path='ponto_mais/analysis/VTC',
            image_base_path_downloads=Path(os.path.join(path_parent, r'downloads\images\VTC')),
            subject = 'Ocorrências de ponto Sirtec - BA Sudoeste'
        )

        if not success:
            print("Check email_sender.log for error details")


        # Send emails
        # ORIGINAL:
        # success = sender.send_email(
        #     to_list=list_oeste,
        #     cc_list=list_todas_operacoes,
        #     image_path='ponto_mais/analysis/BJL',
        #     image_base_path_downloads=Path(os.path.join(path_parent, r'downloads\images\BJL')),
        #     subject = 'Ocorrências de ponto Sirtec - BA Bom Jesus da Lapa V3'
        # )
        success = sender.send_email(
            to_list=test_list,
            cc_list=[],
            image_path='ponto_mais/analysis/BJL',
            image_base_path_downloads=Path(os.path.join(path_parent, r'downloads\images\BJL')),
            subject = 'Ocorrências de ponto Sirtec - BA Bom Jesus da Lapa V3'
        )

        if not success:
            print("Check email_sender.log for error details")


        # Send emails
        # ORIGINAL:
        # success = sender.send_email(
        #     to_list=list_extremo_oeste,
        #     cc_list=list_todas_operacoes,
        #     image_path='ponto_mais/analysis/BAR',
        #     image_base_path_downloads=Path(os.path.join(path_parent, r'downloads\images\BAR')),
        #     subject = 'Ocorrências de ponto Sirtec - BA Barreiras V3'
        # )
        success = sender.send_email(
            to_list=test_list,
            cc_list=[],
            image_path='ponto_mais/analysis/BAR',
            image_base_path_downloads=Path(os.path.join(path_parent, r'downloads\images\BAR')),
            subject = 'Ocorrências de ponto Sirtec - BA Barreiras V3'
        )


        if not success:
            print("Check email_sender.log for error details")


        # Send emails
        # ORIGINAL:
        # success = sender.send_email(
        #     to_list=list_centro,
        #     cc_list=list_todas_operacoes,
        #     image_path='ponto_mais/analysis/FRS',
        #     image_base_path_downloads=Path(os.path.join(path_parent, r'downloads\images\FRS')),
        #     subject = 'Ocorrências de ponto Sirtec - BA Centro V3'
        # )
        success = sender.send_email(
            to_list=test_list,
            cc_list=[],
            image_path='ponto_mais/analysis/FRS',
            image_base_path_downloads=Path(os.path.join(path_parent, r'downloads\images\FRS')),
            subject = 'Ocorrências de ponto Sirtec - BA Centro V3'
        )

        if not success:
            print("Check email_sender.log for error details")

        # Send emails
        # ORIGINAL:
        # success = sender.send_email(
        #     to_list=list_ourinhos,
        #     cc_list=list_todas_operacoes,
        #     image_path='ponto_mais/analysis/SP',
        #     image_base_path_downloads=Path(os.path.join(path_parent, r'downloads\images\SP')),
        #     subject = 'Ocorrências de ponto Sirtec - OURINHOS'
        # )
        success = sender.send_email(
            to_list=test_list,
            cc_list=[],
            image_path='ponto_mais/analysis/SP',
            image_base_path_downloads=Path(os.path.join(path_parent, r'downloads\images\SP')),
            subject = 'Ocorrências de ponto Sirtec - OURINHOS'
        )
        
        if not success:
            print("Check email_sender.log for error details")
        
        break


if __name__ == "__main__":
    main_etapa2()