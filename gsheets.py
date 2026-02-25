
from time import sleep
import os
import gspread
from google.oauth2.service_account import Credentials
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

path_script = os.path.dirname(os.path.abspath(__file__))
path_credenciais_json = os.path.join(path_script, "chaveGoogle.json")


class Gsheets:
    def __init__(self):
        
        # ID da planilha do Drive 
        #self.id_planilha_gsheet = "1gv-8nnlNnchPGE-FnCqxOLPVkd2ygXUn_nJZd5nqaLc" # planilha "bd_config_SESMT"
        self.planilha_emails = '12OAPj75aCww6DDHTfN07reVvlB-GqIob5HbwD0JHN1Q'
        
        self.escopo = ["https://www.googleapis.com/auth/spreadsheets",
                        "https://www.googleapis.com/auth/drive"]
        
        # Inicializar como None para evitar AttributeError
        self.planilhaGSheet = None
        self.credenciais = None
        self.cliente = None
        
        # Acessar planilha do Drive
        try:
            self.credenciais = Credentials.from_service_account_file(path_credenciais_json,scopes=self.escopo)
            self.cliente = gspread.authorize(self.credenciais)
            self.planilhaGSheet = self.cliente.open_by_key(self.planilha_emails)
            print("Conectado ao Google Sheets com sucesso!")
            
        except Exception as e:
            print(f"Erro ao conectar com o Google Sheets: {e}")
            print("Sistema continuara sem funcionalidades do Google Sheets")

            
    def attsheets(self, chave_json, planilha_id, aba_nome):
        # Defina o escopo e as credenciais
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(chave_json, scope)

        # Autentique e abra a planilha
        client = gspread.authorize(credentials)
        planilha = client.open_by_key(planilha_id)
        aba = planilha.worksheet(aba_nome)

        # Obtenha a data e hora atual
        data_hora_atual = datetime.now().strftime('%d/%m/%Y %H:%M')

        # Atualize a célula A2 com a data e hora atual
        aba.update_cell(2, 1, data_hora_atual)  
        

    def pegar_dados_aba_access(self):
        if self.planilhaGSheet is None:
            print("AVISO: Google Sheets nao conectado. Retornando lista vazia.")
            return []
        
        try:
            aba_planilha_GSheet = self.planilhaGSheet.worksheet("access")  # Pegar abas da planilha no Drive
            valores_aba = aba_planilha_GSheet.get_all_values()         # Pegar células com valores (não vazias)
            return valores_aba
        except Exception as e:
            print(f"Erro ao ler aba 'access': {e}")
            return []
    
    def pegar_celula_gsheets(self, celula):
        if self.planilhaGSheet is None:
            print("AVISO: Google Sheets nao conectado. Retornando None.")
            return None
        
        try:
            aba_planilha_GSheet = self.planilhaGSheet.worksheet("access")  # Pegar abas da planilha no Drive
            valor_celula = aba_planilha_GSheet.acell(celula).value
            return valor_celula
        except Exception as e:
            print(f"Erro ao ler celula {celula}: {e}")
            return None
    
    def pegar_lista_emails(self, coluna_ref: int) -> list:
        if self.planilhaGSheet is None:
            print("AVISO: Google Sheets nao conectado. Retornando lista vazia.")
            return []
        
        try:
            aba = self.planilhaGSheet.worksheet('lista_emails')
            col = aba.col_values(coluna_ref)  
            col.pop(0) 
            return col
        except Exception as e:
            print(f"Erro ao ler lista de emails: {e}")
            return []
        
if __name__ == "__main__":
    gsheets = Gsheets()
    


