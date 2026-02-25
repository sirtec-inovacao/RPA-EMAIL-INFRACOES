import pandas as pd
import numpy as np
import glob
import os
from datetime import date, timedelta
from functions.drive_utils import download_all_csvs_from_drive

def hhmm_para_hhmmss(x):
    if pd.isna(x):
        return "00:00:00"
    s = str(x).strip()
    if s == "":
        return "00:00:00"
    # se vier HH:MM, adiciona segundos
    if s.count(":") == 1:
        return s + ":00"
    return s  # já é HH:MM:SS

def weeknum_tipo1(d: date) -> int:
    """Equivalente ao Excel NÚMSEMANA(data;1): semana começa no domingo, semana 1 contém 1º de janeiro."""
    jan1 = date(d.year, 1, 1)
    # Python: Monday=0..Sunday=6  -> queremos Sunday=1..Saturday=7
    weekday_jan1 = ((jan1.weekday() + 1) % 7) + 1
    doy = d.timetuple().tm_yday
    return ((doy + weekday_jan1 - 2) // 7) + 1




dtypes = {
    "Nome da Origem": "string",
    "Nome": "string",
    "Matrícula": "Int64",   
    "Equipe": "string",
    "Ocorrência": "string",
    "Operação": "string",
    "Valor": "string",     
}
parse_dates = ["Data"]  

cols = [
    "+10hrs trabalhadas",
    "-11hrs_entrejornada",
    "Batidas de ponto errados",
    "intervalo menos 30 min",
    "+7dias_infracao",
]

cols_entrada_saida = [
    "1ª Entrada", "1ª Saída",
    "2ª Entrada", "2ª Saída",
    "3ª Entrada", "3ª Saída",
    "4ª Entrada", "4ª Saída",
    "5ª Entrada", "5ª Saída",
]

ordem = [
    "Data", "Nome", "Cargo", "Equipe", "Turno",
    "1ª Entrada", "1ª Saída", "2ª Entrada", "2ª Saída", "3ª Entrada", "3ª Saída",
    "Crédito", "Débito", "H. intervalo", "Horas normais",
    "Horas extras fator 1", "Horas extras fator 2", "Horas extras fator 3",
    "Horas totais", "Horas previstas", "Horas intrajornada", "Matrícula", "Feriado",
    "Total de horas em sobreaviso", "Motivo/Observação", "+10hrs trabalhadas",
    "Deveria trabalhar", "Batidas de ponto errados", "intervalo menos 30 min",
    "Intervalos.Ocorrência", "erro contabilização intervalo", "trabalhou", "Ajustes",
    "Ajuste+48hrs", "priemira_entrada_dia", "ultima_saida_dia", "aux", "extra",
    "entrejornada", "-11hrs_entrejornada", "+7dias_infracao", "Operação_SemTratar",
    "4ª Entrada", "5ª Entrada", "6ª Entrada", "4ª Saída", "5ª Saída", "6ª Saída",
    "Atraso", "Semana do Ano", "Infrações S/ Atraso", "Qtd. Registros","Infrações C/ Atraso"
]

order = [
    'Data', 'Nome', 'Cargo', 'Equipe', 'Turno', '1ª Entrada', '1ª Saída', '2ª Entrada', '2ª Saída', '3ª Entrada', '3ª Saída', 
    'Crédito', 'Débito', 'H. intervalo', 'Horas normais', 'Horas extras fator 1', 'Horas extras fator 2', 'Horas extras fator 3', 
    'Horas totais', 'Horas previstas', 'Horas intrajornada', 'Matrícula', 'Feriado', 'Total de horas em sobreaviso', 
    'Motivo/Observação', '+10hrs trabalhadas', 'Deveria trabalhar', 'Batidas de ponto errados', 'intervalo menos 30 min', 
    'erro contabilização intervalo', 'trabalhou', 'Ajustes', 'Ajuste+48hrs', 'priemira_entrada_dia', 'ultima_saida_dia', 
    'aux', 'extra', 'entrejornada', '-11hrs_entrejornada', '+7dias_infracao', 'Operação_SemTratar', '4ª Entrada', 
    '5ª Entrada', '6ª Entrada', '4ª Saída', '5ª Saída', 'Saldo', 'Adicional noturno', '6ª Saída', 'Atraso', 
    'Semana do Ano', 'Infrações S/ Atraso', 'Qtd. Registros', 'Infrações C/ Atraso', 'Meta Infração', 'Filtra Semana', 
    'Dia Anterior', 'Inicio Período', 'Valida Período', 'Horas entrejornada', 'Operação'
]

colmuns_trata = [
    '-11hrs_entrejornada', '+10hrs trabalhadas','+7dias_infracao'
    
]

def gerar_bd_completo():
    limit = "00:05:00"

    # Verificar se final.csv existe
    #if not os.path.exists('final.csv'):
    #     print("Erro: Arquivo final.csv não encontrado.")
    #     return None

    df_final = pd.read_csv('final.csv', sep=';', encoding='utf-8-sig')
    #df_final = pd.read_excel("final_teste.xlsx")
    

    # Caminho da pasta de rede e Integração API Google Drive
    folder_id = "10EBQJVYN_MRxd0rQtBOKB7kwb0Ngu0-R"
    path_script = os.path.dirname(os.path.abspath(__file__))
    download_dir = os.path.join(path_script, "downloads", "bases_intervalos")
    
    folder_path = download_all_csvs_from_drive(folder_id, download_dir)
    
    if folder_path is None:
        fallback_path = r"G:\Drives compartilhados\PCP\Time Inovação\Soluções\BI - Painel RH\Bases\Intervalos"
        if os.path.exists(fallback_path):
            print("Aviso: Falha ao baixar bases de Intervalos do Drive. Usando caminho de rede como fallback.")
            folder_path = fallback_path
        else:
            print(f"Erro crítico: Falha ao baixar bases de Intervalos do Drive e fallback {fallback_path} inacessível.")
            folder_path = "" # Evita erro path vazio no os.path.join
            
    all_files = glob.glob(os.path.join(folder_path, "*.csv"))

    df_list = []
    print(f"Lendo {len(all_files)} arquivos de intervalos...")

    for filename in all_files:
        try:
            temp_df = pd.read_csv(filename, dtype=dtypes, parse_dates=parse_dates, sep=';', encoding='utf-8-sig') # ou latin1 se der erro
            df_list.append(temp_df)
        except Exception as e:
            print(f"Erro ao ler {filename}: {e}")

    if df_list:
        df_intervalo = pd.concat(df_list, ignore_index=True)
    else:
        print("Nenhum arquivo CSV encontrado ou erro na leitura.")
        df_intervalo = pd.DataFrame() # evitar erro nas proximas linhas


    df_intervalo["Valor_Tempo"] = pd.to_timedelta(
        df_intervalo["Valor"].apply(hhmm_para_hhmmss),
        errors="coerce"
    )

    limit_td = pd.to_timedelta(limit)

    df_intervalo = df_intervalo[df_intervalo["Valor_Tempo"] > limit_td].copy()

    df_intervalo["Valor"] = df_intervalo["Valor_Tempo"].astype(str).str.replace(r"^0 days ", "", regex=True)
    # Converte para texto e pega tudo depois de " days "
    df_intervalo["Valor_Tempo"] = df_intervalo["Valor_Tempo"].astype(str).str.split(' days ').str[-1]
    df_intervalo = df_intervalo.drop(columns=["Valor"])
    df_intervalo = df_intervalo.rename(columns={"Valor_Tempo": "Valor"})


    df_final_filtro = df_final[(df_final["Matrícula"] != "Não") & (df_final["Horas intrajornada"] == "00:00")].copy()
    df_final_filtro = df_final_filtro[~df_final_filtro["Matrícula"].astype(str).str.contains("Sim", na=False)].copy()
    # Converte coluna Data para datetime temporariamente para aplicar a funcao
    df_temp_data = pd.to_datetime(df_final_filtro["Data"], dayfirst=True, errors="coerce")
    df_final_filtro["Semana do Ano"] = df_temp_data.apply(lambda x: weeknum_tipo1(x.date()) if pd.notnull(x) else 0).astype("int64")

    df_final_filtro[cols] = (
        df_final_filtro[cols]
        .astype(str)
        .apply(lambda x: x.str.replace(',', '.', regex=False))
        .apply(pd.to_numeric, errors="coerce")
        .fillna(0)
    )

    # soma linha a linha e grava como inteiro
    df_final_filtro["Infrações S/ Atraso"] = df_final_filtro[cols].sum(axis=1).astype("int64")

    cols_com_atraso = cols + ["Atraso"]

    df_final_filtro[cols_com_atraso] = df_final_filtro[cols_com_atraso].apply(pd.to_numeric, errors="coerce").fillna(0)

    df_final_filtro["Infrações S/ Atraso"] = df_final_filtro[cols].sum(axis=1).astype("int64")
    df_final_filtro["Infrações C/ Atraso"] = df_final_filtro[cols_com_atraso].sum(axis=1).astype("int64")
    df_final_filtro = df_final_filtro.rename(columns={"Operação": "Operação_SemTratar"})

    df_final_filtro["Qtd. Registros"] = (
        df_final_filtro[cols_entrada_saida]
          .replace(r"^\s*$", np.nan, regex=True)  # trata "" ou só espaços como vazio
          .notna()
          .sum(axis=1)
          .astype("int64")
    )

    print(df_final_filtro.info())
    print(df_intervalo.info())

    keys = ["Data","Nome", "Matrícula"]

    # Garantir que a chave Data seja do mesmo tipo (datetime) para o merge funcionar
    df_final_filtro["Data"] = pd.to_datetime(df_final_filtro["Data"], dayfirst=True, errors="coerce")
    df_intervalo["Data"] = pd.to_datetime(df_intervalo["Data"], dayfirst=True, errors="coerce")
    # Garantir Matrícula int64
    df_final_filtro["Matrícula"] = pd.to_numeric(df_final_filtro["Matrícula"], errors="coerce").fillna(0).astype("int64")
    df_intervalo["Matrícula"] = pd.to_numeric(df_intervalo["Matrícula"], errors="coerce").fillna(0).astype("int64")

    # Remove duplicatas para evitar explosão de linhas no merge
    #df_intervalo = df_intervalo.drop_duplicates(subset=["Data", "Matrícula"], keep="first")


    df_BD = df_final_filtro.merge(
        df_intervalo[keys + ["Ocorrência"]],
        on=keys,
        how="left"
    ).rename(columns={"Ocorrência": "Intervalos.Ocorrência"})

    df_BD["Intervalos.Ocorrência"] = (
        df_BD["Intervalos.Ocorrência"]
          .astype("string")  # preserva NA como <NA>
          .str.replace("Intervalo menor do que o previsto", "1", regex=False)
    )

    df_BD["Intervalos.Ocorrência"] = pd.to_numeric(df_BD["Intervalos.Ocorrência"], errors="coerce").fillna(0).astype("int64")


    df_BD["Intervalo Corrigido"] = np.where(
        df_BD["Qtd. Registros"].eq(4),
        pd.to_numeric(df_BD["Intervalos.Ocorrência"], errors="coerce").fillna(0),
        0
    ).astype("int64")

    df_BD.drop(columns=["Intervalos.Ocorrência"], inplace=True)
    df_BD = df_BD.rename(columns={"Intervalo Corrigido": "Intervalos.Ocorrência"})

    #resto = [c for c in df_BD.columns if c not in ordem]
    #df_BD = df_BD.loc[:, ordem + resto]
    
    # Atualiza lista order para colunas existentes
    cols_existentes = [c for c in order if c in df_BD.columns]

    df_BD = df_BD.loc[:, cols_existentes]

    #df_BD.drop(columns=["intervalo menos 30 min"], inplace=True)

    df_BD = df_BD.rename(columns={"Intervalos.Ocorrência": "intervalo menos 30 min"})
    df_BD["intervalo menos 30 min"] = df_BD["intervalo menos 30 min"].astype(int)

       ############################# 
    ## FORMULAS DO EXCEL PARA PYTHON ##
       #############################

    hoje = date.today()


    df_BD["Meta Infração"] = np.where(
        pd.to_numeric(df_BD["trabalhou"], errors="coerce").fillna(0).eq(1),
        0.025,
        0
    ).astype(float)


    semana_atual = weeknum_tipo1(date.today())

    df_BD["Semana do Ano"] = pd.to_numeric(df_BD["Semana do Ano"], errors="coerce")

    df_BD["Filtra Semana"] = np.where(
        (df_BD["Semana do Ano"] >= (semana_atual - 3)) & (df_BD["Semana do Ano"] <= semana_atual),
        1, 0
    ).astype("int64")


    eh_segunda = (hoje.isoweekday() == 1)
    dia_ref = hoje - timedelta(days=3 if eh_segunda else 1)

    df_BD["Data"] = pd.to_datetime(df_BD["Data"], errors="coerce").dt.date
    print(f"DEBUG: Hoje: {hoje}, Dia Ref (Anterior/Util): {dia_ref}")
    df_BD["Dia Anterior"] = np.where(df_BD["Data"] == dia_ref, 1, 0).astype("int64")
    print(f"DEBUG: Registros com Dia Anterior=1: {df_BD['Dia Anterior'].sum()}")

    hoje = date.today()

    if hoje.day < 16:
        # volta 1 mês (tratando janeiro)
        ano = hoje.year
        mes = hoje.month - 1
        if mes == 0:
            mes = 12
            ano -= 1
        inicio_periodo = date(ano, mes, 16)
        inicio_periodo = inicio_periodo.strftime("%d/%m/%Y")
    else:
        inicio_periodo = date(hoje.year, hoje.month, 16)

    df_BD["Inicio Período"] = inicio_periodo


    df_BD["Data"] = pd.to_datetime(df_BD["Data"], errors="coerce")
    df_BD["Inicio Período"] = pd.to_datetime(df_BD["Inicio Período"], errors="coerce")

    df_BD["Valida Período"] = np.where(df_BD["Data"] >= df_BD["Inicio Período"], 1, 0).astype("int64")



    df_BD["entrejornada"] = (
        df_BD["entrejornada"].astype(str).str.strip()
          .str.replace(".", "", regex=False)   # se vier "62.820,0"
          .str.replace(",", ".", regex=False)  # "62820,0" -> "62820.0"
    )

    df_BD["entrejornada"] = pd.to_numeric(df_BD["entrejornada"], errors="coerce").fillna(0)
    df_BD["Horas entrejornada"] = df_BD["entrejornada"] / 3600 / 24

    df_BD["Horas entrejornada"] = pd.to_timedelta(df_BD["entrejornada"], unit="s")
    df_BD["Horas entrejornada"] = df_BD["Horas entrejornada"].astype(str).str.replace("0 days ", "", regex=False)

    df_BD["Operação"] = df_BD["Operação_SemTratar"].copy()

    df_BD[colmuns_trata] = (
        df_BD[colmuns_trata].astype(str)
            .apply(lambda s: s.astype(str).str.replace("\u00a0"," ",regex=False).str.strip())
            .apply(pd.to_numeric, errors="coerce")
            .fillna(0)
            .astype(int)
    )

    df_BD["entrejornada"] = np.where(
                            df_BD["entrejornada"].astype(str).str.strip().str.startswith("0.0"),
                            "Sem registro",
                            df_BD["entrejornada"]
    )

    df_BD["Data"] = pd.to_datetime(df_BD["Data"], dayfirst=True, errors="coerce").dt.strftime("%d/%m/%Y")
    df_BD["Inicio Período"] = pd.to_datetime(df_BD["Inicio Período"], errors="coerce").dt.strftime("%d/%m/%Y")
    df_BD["Batidas de ponto errados"] = df_BD["Batidas de ponto errados"].astype(int)


    print(df_BD.info())
    print(df_BD)

    df_BD.to_csv("BD.csv", sep=';', index=False, encoding='utf-8-sig')
    print("Arquivo BD.csv gerado com sucesso!")
    return df_BD

if __name__ == "__main__":
    gerar_bd_completo()

