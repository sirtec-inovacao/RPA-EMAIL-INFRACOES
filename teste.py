#from ponto_mais.auth.logout import logout
from gsheets import Gsheets
import os
from pathlib import Path
#from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.ponto_mais.utilities.operation.operations import Operations
from src.ponto_mais.utilities.operation.operations_manager import OperationsManager
from src.ponto_mais.utilities.delete.folders.delete_folders import delete_folders
from src.ponto_mais.analysis.Analise_Excel import analise_file
from src.ponto_mais.utilities.email.email_manager import EmailSender
from src.teste_sirtec import pdf_to_images
import pandas as pd

test_list = ["ricardo.souza@sirtec.com.br"]




operations_list = [
    Operations("RS", "","", "G:/Drives compartilhados/Inovação - RH/RS.docx", "downloads/images/RS"),
    Operations("CE", "","",  "G:/Drives compartilhados/Inovação - RH/CEARÁ.docx", "downloads/images/CE"),
    Operations("VTC","","", "G:/Drives compartilhados/Inovação - RH/SUDOESTE VDC.docx", "downloads/images/VTC"),
    Operations("BAR","","", "G:/Drives compartilhados/Inovação - RH/EXTREMO OESTE BAR.docx", "downloads/images/BAR"),
    Operations("FRS","","", "G:/Drives compartilhados/Inovação - RH/CENTRO FRS.docx", "downloads/images/FRS"),
    Operations("PEL","","", "G:/Drives compartilhados/Inovação - RH/PELOTAS.docx", "downloads/images/PEL"),
    Operations("BJL","" ,"", "G:/Drives compartilhados/Inovação - RH/OESTE GUA-BJL.docx", "downloads/images/BJL"),
    Operations("POA","", "", "G:/Drives compartilhados/Inovação - RH/POA.docx", "downloads/images/POA"),
    Operations("SP", "", "", "G:/Drives compartilhados/Inovação - RH/SP.docx", "downloads/images/SP")
]

manager = OperationsManager(operations_list)
manager.process_images('downloads/images/')


sender = EmailSender()

for op in operations_list:
    sender.send_email(
        to_list=test_list,
        cc_list=[],            # Cópia
        image_path=rf'imagem\imagens_{op.operation}',      # ← Imagens dos PDFs
        image_base_path_downloads=rf'downloads\images\{op.operation}',  # ← Imagens do .docx
        subject=f'Ocorrências de ponto Sirtec - {op.operation} V3'
    )