import json
from datetime import datetime, timedelta

def writeDate(update_type):
    config_path = "ponto_mais/reports/period/period.json"
    now = datetime.now()

    if update_type == "journey":

        journey_initial = now
        journey_final = (journey_initial - timedelta(days=1)).strftime("%Y-%m-%dT00:00:00")
    
    elif update_type == "records":
        # Records: initial e final são hoje
        records_initial = now.strftime("%Y-%m-%dT00:00:00")
        records_final = now.strftime("%Y-%m-%dT23:59:59")
        
    
    elif update_type == "audit":
        now = datetime.now()
        
        if now.day >= 16:
            audit_initial = now.replace(day=15).strftime("%Y-%m-%dT00:00:00")
        else:
            last_month = now - timedelta(days=now.day)  # Vai para o mês anterior
            audit_initial = last_month.replace(day=15).strftime("%Y-%m-%dT00:00:00")

        audit_final = now.strftime("%Y-%m-%dT23:59:59")
    
    try:
        with open(config_path, "r+") as json_file:
            data = json.load(json_file)

            # Atualizar a data conforme o tipo especificado
            if update_type == "journey":
                data[0]["journey_initial"] = journey_final
                data[0]["journey_final"] = journey_final
            elif update_type == "records":
                data[1]["records_initial"] = records_initial
                data[1]["records_final"] = records_final
            elif update_type == "audit":
                data[2]["audit_initial"] = audit_initial
                data[2]["audit_final"] = audit_final
            else:
                print("Tipo de atualização inválido. Use 'journey', 'records' ou 'audit'.")
                return

            json_file.seek(0)
            json.dump(data, json_file, indent=4)
            json_file.truncate()

            print(f"Datas de '{update_type}' atualizadas com sucesso no arquivo JSON.")
    except FileNotFoundError:
        print("Arquivo JSON não encontrado para atualizar as datas.")
    except json.JSONDecodeError:
        print("Erro ao decodificar o JSON para atualizar as datas.")
    except Exception as e:
        print("Ocorreu um erro ao atualizar as datas:", e)

def getInitialDate(reports):
    config_path = "ponto_mais/reports/period/period.json"
    try:
        with open(config_path, "r") as json_file:
            data = json.load(json_file)
            if(reports == "journey"):
                initial_date = data[0].get("journey_initial")
            elif(reports == "records"):
                initial_date = data[1].get("records_initial")
            elif(reports == "audit"):
                initial_date = data[2].get("audit_initial")
        if initial_date is not None:
            print("O valor de 'last_date' é:", initial_date)
            # Converter a string para objeto datetime
            data_objeto = datetime.strptime(initial_date, "%Y-%m-%dT%H:%M:%S")
            # Formatar para o formato desejado
            data_formatada = data_objeto.strftime("%d/%m/%Y")
            return data_formatada
        else:
            print("O campo 'initial_date' não foi encontrado no arquivo JSON.")
    except FileNotFoundError:
        print("Arquivo JSON não encontrado.")
    except json.JSONDecodeError:
        print("Erro ao decodificar o JSON.")
    except Exception as e:
        print("Ocorreu um erro:", e)

    return initial_date

def getFinalDate(reports):
    config_path = "ponto_mais/reports/period/period.json"
    try:
        with open(config_path, "r") as json_file:
            data = json.load(json_file)
            if(reports == "journey"):
                final_date = data[0].get("journey_final")
            elif(reports == "records"):
                final_date = data[1].get("records_final")
            elif(reports == "audit"):
                final_date = data[2].get("audit_final")
        if final_date is not None:
            print("O valor de 'final_date' é:", final_date)
            data_objeto = datetime.strptime(final_date, "%Y-%m-%dT%H:%M:%S")
            # Formatar para o formato desejado
            data_formatada = data_objeto.strftime("%d/%m/%Y")
            return data_formatada
        else:
            print("O campo 'final_date' não foi encontrado no arquivo JSON.")
    except FileNotFoundError:
        print("Arquivo JSON não encontrado.")
    except json.JSONDecodeError:
        print("Erro ao decodificar o JSON.")
    except Exception as e:
        print("Ocorreu um erro:", e)

    return final_date
