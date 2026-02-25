#from ponto_mais.auth.logout import logout
from gsheets import Gsheets
import os
from pathlib import Path
#from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.ponto_mais.utilities.operation.operations import Operations
from src.ponto_mais.utilities.operation.operations_manager import OperationsManager
from src.ponto_mais.utilities.delete.folders.delete_folders import delete_folders
# from src.ponto_mais.analysis.Analise_Excel import analise_file
from src.ponto_mais.utilities.email.email_manager import EmailSender
from src.teste_sirtec import pdf_to_images
import pandas as pd
from functions.drive_utils import download_docx_from_drive

test_list = ["ricardo.souza@sirtec.com.br"]




# Caminho da pasta e Integração API Google Drive
folder_id_docx = "0AAf8OZuFlhHdUk9PVA" # Folder Inovação - RH com os templates .docx
path_script = os.path.dirname(os.path.abspath(__file__))
docx_dir = os.path.join(path_script, "downloads", "docx_templates")

# Baixar os templates do drive 
download_docx_from_drive(folder_id_docx, docx_dir)

operations_list = [
    Operations("RS", "","", os.path.join(docx_dir, "RS.docx"), os.path.join("downloads", "images", "RS")),
    Operations("CE", "","", os.path.join(docx_dir, "CEARÁ.docx"), os.path.join("downloads", "images", "CE")),
    Operations("VTC","","", os.path.join(docx_dir, "SUDOESTE VDC.docx"), os.path.join("downloads", "images", "BA Sudoeste")),
    Operations("BAR","","", os.path.join(docx_dir, "EXTREMO OESTE BAR.docx"), os.path.join("downloads", "images", "BA Barreiras")),
    Operations("FRS","","", os.path.join(docx_dir, "CENTRO FRS.docx"), os.path.join("downloads", "images", "BA Centro")),
    Operations("PEL","","", os.path.join(docx_dir, "PELOTAS.docx"), os.path.join("downloads", "images", "PEL")),
    Operations("BJL","" ,"", os.path.join(docx_dir, "OESTE GUA-BJL.docx"), os.path.join("downloads", "images", "BA Bom Jesus da Lapa")),
    Operations("POA","", "", os.path.join(docx_dir, "POA.docx"), os.path.join("downloads", "images", "POA")),
    Operations("SP", "", "", os.path.join(docx_dir, "SP.docx"), os.path.join("downloads", "images", "OURINHOS"))
]

manager = OperationsManager(operations_list)
manager.process_images('downloads/images/')


sender = EmailSender()

for op in operations_list:
    nome_unidade = os.path.basename(op.images_path)
    
    sender.send_email(
        to_list=test_list,
        cc_list=[],            # Cópia
        image_path=os.path.join('imagem', f'imagens_{op.operation}'),      # ← Imagens dos PDFs
        image_base_path_downloads=os.path.join('downloads', 'images', op.operation),  # ← Imagens do .docx
        subject=f'Ocorrências de ponto Sirtec - {nome_unidade}'
    )