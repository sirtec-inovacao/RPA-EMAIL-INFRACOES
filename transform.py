import os
from multiprocessing.sharedctypes import copy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configurar pandas para mostrar todas as colunas e linhas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

operacao_regiao = [
    "BAR",
    "CE",
    "VTC",
    "FRS",
    "PEL",
    "BJL",
    "POA",
    "SP",
    "RS"
]

##BD
COL_DIA_ANTERIOR = "Dia Anterior"
COL_OPER = "Operação"
COL_MATRICULA = "Matrícula"
COL_NAME = "Nome"
COL_DATE = "Data"
COL_10_TRABALHO = "+10hrs trabalhadas"
COL_11_ENTREJORNADA = "-11hrs_entrejornada" #-11hrs entre jornada
COL_MENOR_PREVISTO = "intervalo menos 30 min" #intervalo menor que o previsto
COL_7_INFRACAO = "+7dias_infracao" #+7 dias trabalhados
COL_BATIDAS_PONTOS_ERRADOS = "Batidas de ponto errados" #Batidas ímpares
COL_ATRASOS = "Atraso" #Atraso abertura de turno > 10 min
COL_INFR_C_ATRASO = "Infrações C/ Atraso"  #Qtd total
COL_VALIDA_PERIODO = "Valida Período"
COL_INICIO_PERIODO = "Inicio Período"
COL_SEMANA = "Semana do Ano"
COL_INFR_S_ATRASO = "Infrações S/ Atraso"
COL_META_INFRA = "Meta Infração"
COL_FILTRA_SEMANA = "Filtra Semana"

##BD_RES
COL_NAME_BD_RES = "Nome"
COL_PERIODO = "Periodo"
COL_EQUIPE = "Equipe"
COL_MENOR20 = "MENOR 10H"
COL_DATE_RES = "Data"
COL_OCORRENCIA = "Ocorrência"
COL_HORA = "Hora"




def gerar_pivot(df, operacao, filtra_semana=1):
    
    # Filtrar por Operação e Filtra Semana
    df_filtro = df[
        (df[COL_OPER] == operacao) &
        (df[COL_FILTRA_SEMANA] == filtra_semana)
    ].copy()


    #print(df_filtro)


    # Garantir que as colunas numéricas estão corretas
    df_filtro[COL_INFR_S_ATRASO] = pd.to_numeric(df_filtro[COL_INFR_S_ATRASO], errors='coerce').fillna(0)
    df_filtro[COL_META_INFRA] = pd.to_numeric(df_filtro[COL_META_INFRA], errors='coerce').fillna(0)

    # Agrupamento (Pivot)
    resumo = (
        df_filtro
        .groupby(COL_SEMANA, as_index=False)[[COL_INFR_S_ATRASO, COL_META_INFRA]]
        .sum()
        .sort_values(COL_SEMANA)
    )

    resumo = resumo.rename(columns={
        COL_INFR_S_ATRASO: "Infrações S/ Atraso",
        COL_META_INFRA: "Meta Infrações 0,25%"
    })

    resumo["Meta Infrações 0,25%"] = resumo["Meta Infrações 0,25%"].round(0).astype(int)

    total_infracoes = resumo["Infrações S/ Atraso"].sum()
    total_meta = resumo["Meta Infrações 0,25%"].sum()

    linha_total = pd.DataFrame([{
        COL_SEMANA: "Total Geral",
        "Infrações S/ Atraso": total_infracoes,
        "Meta Infrações 0,25%": total_meta
    }])

    resumo_final = pd.concat([resumo, linha_total], ignore_index=True)

    return resumo_final


def gerar_raking_top5_ontem(df, operacao):    
    
    df = df[
        (df[COL_OPER] == operacao) &
        (df[COL_DIA_ANTERIOR] == 1)
    ].copy()

    df_ranking = (
        df
        .groupby([COL_OPER, COL_MATRICULA, COL_NAME, COL_DATE], as_index=False)
        [[COL_10_TRABALHO, COL_11_ENTREJORNADA, COL_MENOR_PREVISTO, COL_7_INFRACAO, COL_BATIDAS_PONTOS_ERRADOS, COL_ATRASOS, COL_INFR_C_ATRASO]]
        .sum()
        .sort_values(by=[COL_INFR_C_ATRASO,COL_MATRICULA, COL_NAME, COL_DATE], ascending=[False, True, True,True])
        )

    df_filtrado = df_ranking[df_ranking[COL_INFR_C_ATRASO] != 0].copy()

    df_ranking = df_filtrado.rename(columns={
        COL_11_ENTREJORNADA: "-11hrs entre jornada",
        COL_MENOR_PREVISTO: "intervalo menor que o previsto",
        COL_7_INFRACAO: "+7 dias trabalhados",
        COL_BATIDAS_PONTOS_ERRADOS: "Batidas ímpares",
        COL_ATRASOS: "Atraso abertura de turno > 10 min",
        COL_INFR_C_ATRASO: "Qtd total"
    })

    #df_ranking = df_ranking.sort_values(by=["Qtd total",COL_MATRICULA, COL_NAME,], ascending=[True, True, True,True]).head(5)

    return df_ranking

def gerar_raking_top5_mensal(df, operacao):

    
    df[COL_INICIO_PERIODO] = pd.to_datetime(df[COL_INICIO_PERIODO], dayfirst=True, errors="coerce")
    

    hoje = pd.Timestamp.today().normalize()
    ontem = hoje - pd.Timedelta(days=1)
    ontem_str = ontem.strftime('%d/%m/%Y')
    df[COL_INICIO_PERIODO]= df[COL_INICIO_PERIODO].dt.strftime('%d/%m/%Y')

    print(df[COL_INICIO_PERIODO])
    print(ontem)
    print(ontem_str,"data normal")

    df_dia_anterior = df[
        (df[COL_OPER] == operacao) &
        (df[COL_VALIDA_PERIODO] == 1) &
        (df[COL_INICIO_PERIODO] <= ontem_str)
    ].copy()

    df_ranking = (
        df_dia_anterior
        .groupby([COL_OPER, COL_MATRICULA, COL_NAME], as_index=False)[[COL_10_TRABALHO, COL_11_ENTREJORNADA, COL_MENOR_PREVISTO, COL_7_INFRACAO, COL_BATIDAS_PONTOS_ERRADOS, COL_ATRASOS, COL_INFR_C_ATRASO]]
        .sum()
        .sort_values(by= COL_INFR_C_ATRASO, ascending=False)
        .head(5)
    )

    df_ranking = df_ranking.rename(columns={
        COL_11_ENTREJORNADA: "-11hrs entre jornada",
        COL_MENOR_PREVISTO: "intervalo menor previsto",
        COL_7_INFRACAO: "+7 dias trabalhados",
        COL_BATIDAS_PONTOS_ERRADOS: "Batidas Ímpares",
        COL_ATRASOS: "Atraso abertura de turno > 10 min",
        COL_INFR_C_ATRASO: "Qtd Total"
    })
    
    df_ranking = df_ranking.sort_values(by=[COL_MATRICULA, COL_NAME], ascending=[True ,False, False])

    return df_ranking

def resumo_infrações_10hrs_11entrejornada(df, operacao):

    df_filtro = df[
        (df[COL_OPER] == operacao) &
        (df[COL_PERIODO] == 1)
    ].copy()

    df_resumo = (
        df_filtro
        .groupby([COL_EQUIPE], as_index=False)
        .agg({COL_NAME_BD_RES: 'count', COL_MENOR20: 'sum'})
        .sort_values(by=COL_EQUIPE, ascending=False)
    )

    df_resumo = df_resumo.rename(columns={
        COL_MENOR20: "Qtd 10:01 - 10:20",
        COL_NAME_BD_RES: "Qtd Ocorrencias"
    })

    total_ocorrencias = df_resumo["Qtd Ocorrencias"].sum()
    total_10_20 = df_resumo["Qtd 10:01 - 10:20"].sum()

    linha_total = pd.DataFrame([{
        COL_EQUIPE: "Total Geral",
        "Qtd Ocorrencias": total_ocorrencias,
        "Qtd 10:01 - 10:20": total_10_20
    }])

    df_resumo = pd.concat([df_resumo, linha_total], ignore_index=True)
    
    #df_resumo = df_resumo.sort_values(COL_EQUIPE, ascending=False)
    
    return df_resumo

def resumo_bd_res(df,operacao):

    df_select = df[
        (df[COL_OPER] == operacao) &
        (df[COL_PERIODO] == 1)
    ].copy()

    df_select = df_select[[COL_NAME,COL_EQUIPE,COL_DATE_RES,COL_OCORRENCIA,COL_HORA]]

    df_select = df_select.sort_values(by=[COL_NAME, COL_DATE_RES], ascending=[True, False])

    return df_select


    
if __name__ == "__main__":
    print("Lendo CSV...")
    df_bd = pd.read_csv("BD.csv", sep=";", encoding="utf-8-sig", low_memory=False)
    df_db_res = pd.read_csv("BD_RES.csv", sep=";", encoding="utf-8-sig", low_memory=False)

    # Garantir que não existam nomes duplicados na lista para evitar reprocessamento
    operacoes_unicas = list(dict.fromkeys(operacao_regiao))

    for operacao in operacoes_unicas:
        print(f"\n--- Processando operação: {operacao} ---")
        
        pasta_operacao = str(operacao).strip()
        pasta_operacao = f"docs/{pasta_operacao}"
        os.makedirs(pasta_operacao, exist_ok=True)

        # Gráfico Semanal
        #try:
            #df_grafico = gerar_grafico(df_bd, operacao)
            #caminho_grafico = os.path.join(pasta_operacao, 'grafico_geral.png')
            #plt.savefig(caminho_grafico, dpi=300, bbox_inches='tight')
            #plt.close() # Fechar para não sobrepor aos próximos
        #except Exception as e:
            #print(f"Erro ao gerar gráfico para {operacao}: {e}")

        # Pivot
        try:
            df_filtro = gerar_pivot(df_bd, operacao)
            caminho_pivot = os.path.join(pasta_operacao, 'pivot_infracoes.csv')
            df_filtro.to_csv(caminho_pivot, sep=";", index=False, encoding="utf-8-sig")
        except Exception as e:
            pass

        # Top 5
        try:
            df_ranking = gerar_raking_top5_ontem(df_bd, operacao)
            caminho_top5 = os.path.join(pasta_operacao, 'ocorrencia_pontos.csv')
            df_ranking.to_csv(caminho_top5, sep=";", index=False, encoding="utf-8-sig")
        except Exception as e:
            pass

        # Dia Anterior
        try:
            df_anterior = gerar_raking_top5_mensal(df_bd, operacao)
            caminho_dia_anterior = os.path.join(pasta_operacao, 'ocorrencia_pontos_mensal.csv')
            df_anterior.to_csv(caminho_dia_anterior, sep=";", index=False, encoding="utf-8-sig")
        except Exception as e:
            pass

        # Resumo Infrações 10hrs 11entrejornada
        if df_db_res is not None:
            try:
                df_resumo = resumo_infrações_10hrs_11entrejornada(df_db_res, operacao)
                caminho_resumo = os.path.join(pasta_operacao, 'quadro_detalhado.csv')
                df_resumo.to_csv(caminho_resumo, sep=";", index=False, encoding="utf-8-sig")
            except Exception as e:
                pass

        # Resumo BD RES
        if df_db_res is not None:
            try:
                df_resumo_bd = resumo_bd_res(df_db_res, operacao)
                caminho_bd_res = os.path.join(pasta_operacao, 'quadro_equipes.csv')
                df_resumo_bd.to_csv(caminho_bd_res, sep=";", index=False, encoding="utf-8-sig")
            except Exception as e:
                pass
