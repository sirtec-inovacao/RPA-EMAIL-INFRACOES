import os
from gsheets import Gsheets

def testar_atualizacao():
    print("Iniciando teste de atualização no Google Sheets...")
    
    path_script = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(path_script, "chaveGoogle.json")
    
    if not os.path.exists(json_path):
        print(f"ERRO: Arquivo de credenciais não encontrado em: {json_path}")
        return

    # Dados usados no main.py
    id_plan_att = "1lM8Q3NIUrDsdR8OD_6RG0wAddXvq1PpWczuOUeOyivE"
    aba_att = "Att_email_infracoes"
    
    gsheets = Gsheets()
    
    try:
        print(f"Tentando atualizar a planilha ID: {id_plan_att}, Aba: {aba_att}")
        gsheets.attsheets(json_path, id_plan_att, aba_att)
        print("Sucesso: A planilha foi atualizada sem erros (verifique no Google Sheets).")
    except Exception as e:
        print(f"Erro durante a atualização: {e}")

if __name__ == "__main__":
    testar_atualizacao()
