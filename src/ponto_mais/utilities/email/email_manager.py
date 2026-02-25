import os
import logging
from pathlib import Path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from typing import List
import mimetypes
from datetime import datetime, timedelta

class EmailSender:
    def __init__(self, smtp_server: str = 'smtp.sirtec.com.br', smtp_port: int = 465,
                 username: str = 'time.inovacao@sirtec.com.br', password: str = '=rnzg21k:-:-@eVZcy+D'):
        """Initialize EmailSender with SMTP configuration."""
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.setup_logging()
        
        # Calcula as datas automaticamente
        self.yesterday = datetime.now() - timedelta(days=1)
        self.last_month = self.yesterday - timedelta(days=30)

        self.hoje = datetime.today()

        # Verifica se o dia atual é maior ou igual a 16 para definir o início do ciclo
        if self.hoje.day >= 16:
            self.data_ini_ciclo = self.hoje.replace(day=16).strftime('%d/%m/%Y')
        else:
            # Se for menor que 16, ajusta para o mês anterior
            self.mes_anterior = self.hoje.month - 1 if self.hoje.month > 1 else 12
            self.ano_relativo = self.hoje.year if self.hoje.month > 1 else self.hoje.year - 1
            self.data_ini_ciclo = datetime(self.ano_relativo, self.mes_anterior, 16).strftime('%d/%m/%Y')

    def setup_logging(self):
        """Configure logging for the email sender."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('email_sender.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def get_date_range_text(self) -> tuple:
        """Return formatted dates for the email template."""
        hoje = datetime.today()
        yesterday_text = self.yesterday.strftime('%d/%m/%Y')
        last_month_text = self.last_month.strftime('01/%m/%Y')

        if hoje.day >= 16:
            data_ini_ciclo = hoje.replace(day=16).strftime('%d/%m/%Y')
        else:
            # Se for menor que 16, ajusta para o mês anterior
            mes_anterior = hoje.month - 1 if hoje.month > 1 else 12
            ano_relativo = hoje.year if hoje.month > 1 else hoje.year - 1
            data_ini_ciclo = datetime(ano_relativo, mes_anterior, 16).strftime('%d/%m/%Y')

        return yesterday_text, last_month_text, yesterday_text, data_ini_ciclo
    
    

    def attach_image(self, image_path: str, cid: str, msg: MIMEMultipart) -> str:
        """Attach an image to the email message as inline-only and return its HTML tag."""
        try:
            image_path = Path(image_path).resolve()
            if not image_path.exists():
                self.logger.warning(f"Image not found: {image_path}")
                return ""

            with open(image_path, 'rb') as img:
                mime_image = MIMEImage(img.read())
                mime_image.add_header('Content-ID', f'<{cid}>')
                mime_image.add_header('Content-Disposition', 'inline', filename=image_path.name)
                mime_image.add_header('X-Attachment-Id', cid)
                mime_image.add_header('Content-Type', f'image/{image_path.suffix[1:]}')
                msg.attach(mime_image)
                return f'<img src="cid:{cid}" style="max-width:100%;" /><br/>'
                
        except Exception as e:
            self.logger.error(f"Error attaching image {image_path}: {str(e)}")
            return ""

    def attach_excel(self, excel_path: str, msg: MIMEMultipart) -> bool:
        """Attach an Excel file to the email message."""
        try:
            excel_path = Path(excel_path).resolve()
            if not excel_path.exists():
                self.logger.warning(f"Excel file not found: {excel_path}")
                return False

            # Determine the correct MIME type for Excel files
            mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            if excel_path.suffix.lower() == '.xls':
                mime_type = 'application/vnd.ms-excel'

            with open(excel_path, 'rb') as excel:
                attachment = MIMEBase('application', 'octet-stream')
                attachment.set_payload(excel.read())
                encoders.encode_base64(attachment)
                
                # Add headers
                attachment.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=excel_path.name
                )
                attachment.add_header('Content-Type', mime_type)
                msg.attach(attachment)
                return True

        except Exception as e:
            self.logger.error(f"Error attaching Excel file {excel_path}: {str(e)}")
            return False

    def send_email(self, to_list: List[str], cc_list: List[str], 
               image_path: str, image_base_path_downloads: str, subject: str = 'Informativo das Ocorrências do Ponto') -> bool:
        """Send email with attachments and inline images."""
        try:
            image_base_path = Path(image_path).resolve()
            if not image_base_path.exists():
                self.logger.error(f"Base image path does not exist: {image_base_path}")
                return False

            msg = MIMEMultipart('related')
            msg['From'] = self.username
            msg['To'] = ", ".join(to_list)
            if cc_list:
                msg['CC'] = ", ".join(cc_list)
            msg['Subject'] = subject
            msg['MIME-Version'] = '1.0'
            
            msgAlternative = MIMEMultipart('alternative')
            msg.attach(msgAlternative)

            try:
                # Prepare image substitutions
                image_mappings = {
                    'evolucao_semanal': 'grafico_geral.png',
                    'ranking_02': 'ocorrencia_pontos.png',
                    'ranking_03': ['ocorrencia_pontos_mensal.png', 'quadro_geral.png'],
                    'resumo': ['quadro_detalhado.png', 'quadro_equipes.png']
                }

                image_replacements = {}
                for section, images in image_mappings.items():
                    if isinstance(images, list):
                        section_html = ""
                        for img in images:
                            img_path = image_base_path / img
                            cid = img.split('.')[0]
                            result = self.attach_image(str(img_path), cid, msg)
                            section_html += result
                        image_replacements[section] = section_html
                    else:
                        img_path = image_base_path / images
                        cid = images.split('.')[0]
                        image_replacements[section] = self.attach_image(str(img_path), cid, msg)

                # Process inconsistency images
                inconsistency_html = ""
                image_base_path_downloads = Path(image_base_path_downloads).resolve()
                print(f"Looking for image files in: {image_base_path_downloads}")

                if image_base_path_downloads.exists():
                    print(f"Directory exists: {image_base_path_downloads}")
                    idx = 0
                    valid_extensions = ['.jpg', '.jpeg', '.png']
                    files_in_directory = list(image_base_path_downloads.iterdir())
                    print(f"Files in directory: {[file.name for file in files_in_directory]}")

                    for file in sorted(files_in_directory):
                        print(f"Processing file: {file.name}")
                        if file.suffix.lower() in valid_extensions:
                            cid = f'inconsistency_{idx}'
                            print(f"Attaching image: {file.name} with cid: {cid}")
                            result = self.attach_image(str(file), cid, msg)
                            if result:
                                inconsistency_html += result
                                idx += 1
                            else:
                                print(f"Failed to attach image: {file.name}")
                        else:
                            print(f"Skipping unsupported file: {file.name}")
                else:
                    self.logger.error(f"The folder {image_base_path_downloads} does not exist.")
                    print(f"The folder {image_base_path_downloads} does not exist.")
                    return False  # Early exit since the directory doesn't exist

                image_replacements['imagens_inconsistencias'] = inconsistency_html
                print(f"Generated HTML for inconsistency images: {inconsistency_html}")

                # Get formatted dates
                yesterday_date, start_date, end_date, data_ini_ciclo = self.get_date_range_text()

                # Combine all substitutions
                all_replacements = {
                    **image_replacements,
                    'yesterday_date': yesterday_date,
                    'start_date': start_date,
                    'end_date': end_date,
                    'data_ini_ciclo': data_ini_ciclo
                }

                # Format the template with all replacements
                email_body = self.get_email_template().format(**all_replacements)
                
                # Attach both plain text and HTML versions
                text_part = MIMEText(self.get_plain_text_content(), 'plain', 'utf-8')
                html_part = MIMEText(email_body + self.get_signature(), 'html', 'utf-8')
                
                msgAlternative.attach(text_part)
                msgAlternative.attach(html_part)

            except KeyError as e:
                self.logger.error(f"Template formatting error: {str(e)}")
                return False
            except Exception as e:
                self.logger.error(f"Error preparing email content: {str(e)}")
                return False

            # Attach Excel file
            excel_path = image_base_path / 'inconsistencias.xlsx'
            if not self.attach_excel(str(excel_path), msg):
                self.logger.warning(f"Excel file not found at {excel_path}, continuing without attachment.")
            
            # Send the email
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.username, self.password)
                all_recipients = to_list + cc_list
                server.sendmail(self.username, all_recipients, msg.as_string())
                
            self.logger.info(f"Email successfully sent to: {', '.join(to_list)}")
            return True

        except Exception as e:
            self.logger.error(f"Error sending email: {str(e)}")
            return False


    def get_plain_text_content(self) -> str:
        """Return plain text version of the email content."""
        yesterday_date, start_date, end_date, data_ini_ciclo = self.get_date_range_text()
        return f"""
        Prezados,

        Segue informativo das ocorrências do ponto, destacando o top 5 do dia {yesterday_date}, 
        acumulado do período de {start_date} até {end_date}, além do anexo com todos 
        os colaboradores da operação.

        Em complemento segue anexo com todos os colaboradores da operação. 
        Ressaltamos que tratam-se de informações sensíveis da empresa, 
        portanto devem compartilhadas a nível gerencial.

        Qualquer dúvida ficaremos à disposição!

        Atenciosamente,
        Sirtec Sistemas Elétricos
        """

    def get_email_template(self) -> str:
        """Return the email template with placeholders for dynamic content."""
        return """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                     body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.5;
                        margin: 0;
                        padding: 0;
                     }}
                     .imagem {{
                        margin-bottom: 10px;
                     }}
                     .container {{
                        margin: 20px;
                     }}
                     img {{
                        max-width: 100%;
                        height: auto;
                     }}
                </style>
            </head>
            <body>
               <div class="container">
                     <p>Prezados, boa tarde!</p>
                     <p>Segue informativo das ocorrências do ponto, destacando o top 5 do dia anterior, acumulado do período, além do anexo com todos os colaboradores da operação:</p>
                     <p>1) Evolução semanal das infrações:</p>
                     {evolucao_semanal}
                     <p>2) Ranking Top 5 do dia {yesterday_date}:</p>
                     {ranking_02}
                     <p>3) Ranking Top 5 do dia {data_ini_ciclo} até {end_date}:</p>
                     {ranking_03}
                     <p>4) Resumo das infrações de +10 horas trabalhadas e -11 entre jornada:</p>
                     {resumo}
                     <p>5) Inconsistências no registro fotográfico do ponto:</p>
                     {imagens_inconsistencias}
                     <p>Em complemento segue anexo com todos os colaboradores da operação. Também ressaltamos que tratam-se de informações sensíveis da empresa, portanto devem compartilhadas a nível gerencial.</p>
                     <p>Qualquer dúvida ficaremos à disposição!</p>
               </div>
            </body>
            </html>
            """

    def get_signature(self) -> str:
        """Return the email signature."""
        return """
            <div style="margin-top: 20px; font-family: Arial, sans-serif; color: #555;">
               <p>Atenciosamente,</p>
               <p> </p>
               <p><b>-- </b></p>
               <p><b>Sirtec Sistemas Elétricos</b></p>
               <p> </p>
               <p>Fone: (55) 3431-3195</p>
               <p><a href="http://www.sirtec.com.br" target="_blank">www.sirtec.com.br</a></p>
               <p>NOSSA MISSÃO: Contribuir para o bem-estar e o desenvolvimento da humanidade.</p>
               <p> </p>
               <p style="font-size: 10px; color: #666;">Esta mensagem, incluindo seus eventuais anexos, é somente para uso do destinatário informado e pode conter informações privilegiadas, confidenciais, proprietárias de uso restrito e/ou legalmente protegidas. Se você recebeu esta mensagem por engano, por favor, notifique o remetente imediatamente e apague a original. Qualquer outro uso deste e-mail é proibido. Se tiver alguma dúvida, entre em contato conosco pelo endereço sirtec.com.br/contato.</p>
            </div>
         """