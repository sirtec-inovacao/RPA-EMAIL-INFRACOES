import pandas as pd
import numpy as np
import os
  

COL_HORA = "10:20:00"
def processar_bd(arquivo):
    # Ler o CSV
    print("Lendo CSV...")
    # Ajuste o caminho conforme necessário
    if os.path.exists(arquivo):
        #df = pd.read_csv(arquivo, sep=";", encoding="utf-8-sig", low_memory=False, skiprows=1)
        df = pd.read_csv(arquivo, sep=";", encoding="utf-8-sig", low_memory=False)
    else:
        print("Arquivo BD.csv não encontrado.")
        return

    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df

def processar_10hrs(df):
    if df is None:
        print("DataFrame vazio ou não carregado.")
        return

    df["Semana do Ano"] = pd.to_numeric(df["Semana do Ano"], errors='coerce')
    df["+10hrs trabalhadas"] = pd.to_numeric(df["+10hrs trabalhadas"], errors='coerce')

    print("Filtrando dados...")
    mask = (df["Semana do Ano"] >= 1) & (df["+10hrs trabalhadas"] == 1)
        
    df_resultado = df[mask].copy()

    if df_resultado.empty:
        print("Nenhum registro encontrado com os filtros aplicados.")
        return pd.DataFrame()
    else:
        df_final = pd.DataFrame()
        df_final["Nome"] = df_resultado["Nome"]
        df_final["Equipe"] = df_resultado["Equipe"]
        df_final["Data"] = df_resultado["Data"]
        df_final["Ocorrência"] = "+10hrs trabalhadas"
        df_final["Horas totais"] = df_resultado["Horas totais"]
        df_final["Operação"] = df_resultado["Operação"]
        #df_final["Periodo"] = df_resultado["Valida Período"]
        df_final["Periodo"] = df_resultado["Filtra Semana"]

        s = df_final["Horas totais"].astype(str).str.strip()
        s = s.replace({"": np.nan, "nan": np.nan, "-": np.nan})

        s = np.where(pd.Series(s).str.count(":") == 1, pd.Series(s) + ":00", s)

        td = pd.to_timedelta(s, errors="coerce")

        df_final["Horas totais"] = td.where(td.notna(), "Data Inválida") 

        df_final["Horas totais"] = df_final["Horas totais"].astype(str).str.split(' days ').str[-1]

        df_final.rename(columns={"Horas totais": "Hora"}, inplace=True)


        #hora_num = pd.to_numeric(df_final["Horas"], errors="coerce")

        df_final["MENOR 10H"] = np.where(
        (df_final["Ocorrência"].astype(str).str.strip() == "+10hrs trabalhadas") &
        (df_final["Hora"] <= COL_HORA),   # 10h20 (em fração de dia)
        1, 0
            ).astype("int64")


        df1 = df_final
        print(df_final)

        return df1

def processar_11hrs(df):
    if df is None:
        print("DataFrame vazio ou não carregado.")
        return

    df["Semana do Ano"] = pd.to_numeric(df["Semana do Ano"], errors='coerce')
    df["-11hrs_entrejornada"] = pd.to_numeric(df["-11hrs_entrejornada"], errors='coerce')

    print("Filtrando dados...")
    mask = (df["Semana do Ano"] >= 1) & (df["-11hrs_entrejornada"] == 1)
        
    df_resultado = df[mask].copy()


    if df_resultado.empty:
        print("Nenhum registro encontrado com os filtros aplicados.")
        return pd.DataFrame()
    else:
        df_final = pd.DataFrame()
        df_final["Nome"] = df_resultado["Nome"]
        df_final["Equipe"] = df_resultado["Equipe"]
        df_final["Data"] = df_resultado["Data"]
        df_final["Ocorrência"] = "-11hrs entrejornada"
        df_final["Horas entrejornada"] = "00:00:00"
        df_final["Operação"] = df_resultado["Operação"]
        #df_final["Periodo"] = df_resultado["Valida Período"]
        df_final["Periodo"] = df_resultado["Filtra Semana"]


        #col_horas = "Horas entrejornada"
        #if col_horas not in df_resultado.columns:
           # if "entrejornada" in df_resultado.columns:
                #col_horas = "entrejornada"
           # else:
            #    print("Coluna de horas entrejornada não encontrada!")
                #col_horas = None
        
       # if col_horas:
            #df_final["Horas entrejornada"] = df_resultado[col_horas]
            #df_final = df_final[df_final["Horas entrejornada"].astype(str).str.strip().eq("00:00:00")].copy()
        #else:
        #     df_final["Horas entrejornada"] = "N/A"
        
        df_final.rename(columns={"Horas entrejornada": "Hora"}, inplace=True)

        #hora_num = pd.to_numeric(df_final["Horas"], errors="coerce")

        df_final["MENOR 10H"] = np.where(
        (df_final["Ocorrência"].astype(str).str.strip() == "+10hrs trabalhadas") &
        (df_final["Hora"] <= COL_HORA),   # 10h20 (em fração de dia)
        1, 0
            ).astype("int64")

        df2 = df_final
        print(df_final)

        return df2

def processar_7dias(df):
    if df is None:
        print("DataFrame vazio ou não carregado.")
        return

    df["Semana do Ano"] = pd.to_numeric(df["Semana do Ano"], errors='coerce')
    df["+7dias_infracao"] = pd.to_numeric(df["+7dias_infracao"], errors='coerce')
    print("Filtrando dados...")
    mask = (df["Semana do Ano"] >= 1) & (df["+7dias_infracao"] == 1)
        
    df_resultado = df[mask].copy()


    if df_resultado.empty:
        print("Nenhum registro encontrado com os filtros aplicados.")
        return pd.DataFrame()
    else:
        df_final = pd.DataFrame()
        df_final["Nome"] = df_resultado["Nome"]
        df_final["Equipe"] = df_resultado["Equipe"]
        df_final["Data"] = df_resultado["Data"]
        df_final["Ocorrência"] = "+7dias_infracao"
        df_final["Horas totais"] = "N/A"
        df_final["Operação"] = df_resultado["Operação"]
        #df_final["Periodo"] = df_resultado["Valida Período"]
        df_final["Periodo"] = df_resultado["Filtra Semana"]
        df_final.rename(columns={"Horas totais": "Hora"}, inplace=True)

        #hora_num = pd.to_numeric(df_final["Horas"], errors="coerce")

        df_final["MENOR 10H"] = np.where(
        (df_final["Ocorrência"].astype(str).str.strip() == "+10hrs trabalhadas") &
        (df_final["Hora"] <= COL_HORA),   # 10h20 (em fração de dia)
        1, 0
            ).astype("int64")

    
        df3 = df_final
        print(df_final)

        return df3

def concat_dfs(df1, df2, df3):
    df_final = pd.concat([df1, df2, df3], ignore_index=True)

    return df_final


def gerar_bd_res():
    try:
        df = processar_bd("BD.csv")
        if df is None:
             print("Erro: Não foi possível processar BD.csv")
             return None

        df1 = processar_10hrs(df)
        df2 = processar_11hrs(df)
        df3 = processar_7dias(df)
        df_final = concat_dfs(df1, df2, df3)
        
        output_file = "BD_RES.csv"
        df_final.to_csv(output_file, sep=';', index=False, encoding='utf-8-sig')
        print(f"Arquivo {output_file} gerado com sucesso!")
        return df_final
    except PermissionError:
        print(f"Erro: Não foi possível salvar BD_RES.csv. O arquivo pode estar aberto.")
        return None
    except Exception as e:
        print(f"Erro inesperado em gerar_bd_res: {e}")
        return None

if __name__ == "__main__":
    gerar_bd_res()