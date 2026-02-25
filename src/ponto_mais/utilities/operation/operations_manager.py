import os
from docx import Document
from PIL import Image
import io
from src.ponto_mais.auth.login import login
from src.ponto_mais.auth.logout import logout

from src.ponto_mais.reports.types.journey import journey
from src.ponto_mais.reports.types.audit import audit
from src.ponto_mais.reports.types.records import records
from src.ponto_mais.reports.period import getPeriod

class OperationsManager:
    def __init__(self, operations_list):
        self.operations_list = operations_list

    def process_images(self, output_folder):
        for operation in self.operations_list:
            current_output_folder = os.path.join(output_folder, operation.operation)
            print("Obtendo imagens do world e salvando em: " + current_output_folder)

            if not os.path.exists(current_output_folder):
                os.makedirs(current_output_folder)
            else:
                for file_name in os.listdir(current_output_folder):
                    file_path = os.path.join(current_output_folder, file_name)
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
            
            doc = Document(operation.docx_path)
            image_counter = 1

            for rel in doc.part.rels.values():
                if "image" in rel.target_ref:
                    
                    image_blob = rel.target_part.blob
                    image_format = rel.target_part.content_type.split('/')[1] 
                    image_temp = io.BytesIO(image_blob)
                    image_name = f"imagem_{image_counter}.png"
                    image_path = os.path.join(current_output_folder, image_name)

                    try:
                        with Image.open(image_temp) as img:
                            img.save(image_path, 'PNG')
                        print(f"Imagem salva em: {image_path}")
                        image_counter += 1
                    except Exception as e:
                        print(f"Erro ao salvar a imagem: {e}")

    def process_operation_journey(self, output_folder, driver):
        for operation in self.operations_list:
            print("############### INICIANDO PROCESSO DE DOWNLOAD DO RELATORIO JORNADA ###############")
            print(f'Operação: {operation.operation}')
            login(driver, operation)
            journey.reports_journey(
                operation, 
                getPeriod.getInitialDate("journey"), 
                getPeriod.getFinalDate("journey"), 
                driver
            )
        print("--------------- DOWNLOAD DO RELATORIO JORNADA FINALIZADO ---------------")

    def process_operation_audit(self, output_folder, driver):
        for operation in self.operations_list:
            print("############### INICIANDO PROCESSO DE DOWNLOAD DO RELATORIO DE AUDITORIA ###############")
            print(f'Operação: {operation.operation}')
            login(driver,operation)
            audit.reports_audit(operation, getPeriod.getInitialDate("audit"), getPeriod.getFinalDate("audit"), driver)
        print("--------------- DOWNLOAD DO RELATORIO DE AUDITORIA FINALIZADO ---------------")

    def process_operation_records(self, driver):
        for operation in self.operations_list:
            print("############### INICIANDO PROCESSO DE DOWNLOAD DO RELATORIO DE REGISTRO DE PONTOS ###############")
            print(f'Operação: {operation.operation}')
            login(driver,operation)
            records.reports_records(operation, getPeriod.getInitialDate("records"), getPeriod.getFinalDate("records"), driver)
        print("--------------- DOWNLOAD DO RELATORIO DE REGISTRO DE PONTOS ---------------")