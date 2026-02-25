import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt


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




def gerar_grafico(df, operacao):
    
    df_filtro = df[
        (df[COL_OPER] == operacao) &
        (df[COL_FILTRA_SEMANA] == 1)
    ].copy()

    resumo = (
        df_filtro
        .groupby(COL_SEMANA, as_index=False)[[COL_INFR_S_ATRASO, COL_META_INFRA]]
        .sum()
        .sort_values(COL_SEMANA)
    )
    resumo[COL_META_INFRA] = resumo[COL_META_INFRA].round(0).astype(int)

    fig, ax = plt.subplots(figsize=(6, 4))

    # 1. Barras (Qtd Total de Infrações)
    bars = ax.bar(resumo[COL_SEMANA], resumo[COL_INFR_S_ATRASO], color='firebrick', width=0.4, label='Infrações')

    # 2. Linha (Meta ou Evolução)
    line = ax.plot(resumo[COL_SEMANA], resumo[COL_META_INFRA], color='#004c6d', marker='s', linewidth=3, markersize=10, label='Meta')

    # Calcular o limite superior dinâmico (com uma margem de 20% para caber os textos)
    y_max = 0
    if not resumo.empty:
        val1 = dict(resumo[COL_INFR_S_ATRASO]).values()
        val2 = dict(resumo[COL_META_INFRA]).values()
        m1 = max(val1) if val1 else 0
        m2 = max(val2) if val2 else 0
        y_max = max(m1, m2)

    if pd.isna(y_max) or y_max == 0:
        y_max = 10 # Em caso de lista totalmente vazia (0 infracoes)
        
    # Offset visual estipulado em 5% do valor maximo
    offset_label = (y_max * 1.25) * 0.05 

    # Adicionando os rótulos de dados (os números em cima das barras/pontos)
    for i, val in enumerate(resumo[COL_INFR_S_ATRASO]):
        ax.text(resumo[COL_SEMANA][i], val + offset_label, str(val), ha='center', fontweight='bold')

    for i, val in enumerate(resumo[COL_META_INFRA]):
        ax.text(resumo[COL_SEMANA][i], val, str(val), color='white', ha='center', va='center', 
                bbox=dict(facecolor='black', edgecolor='none', boxstyle='square,pad=0.3'))

    # Ajustes de layout
    ax.set_title('QTD TOTAL DE INFRAÇÕES POR SEMANA', fontweight='bold')
    ax.set_xticks(resumo[COL_SEMANA])
    
    ax.set_ylim(0, y_max * 1.25)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    
    #print(resumo)
    #return resumo


def gerar_imagem_tabela(df, nome_arquivo, estilo="detalhado", cor_cabecalho='#D9D9D9'):
    """
    df: DataFrame com os dados
    nome_arquivo: Nome do arquivo de saída (ex: 'resultado.png')
    estilo: "detalhado" (linhas normais) ou "resumo" (com última linha em negrito)
    """
    
    # Configurações de cores e fontes baseadas nos modelos
    font_family = "Arial"
    header_font_size = 12
    cell_font_size = 11
    
    # Preparar listas de valores para as células
    values = [df[col] for col in df.columns]
    
    # Se for o estilo "resumo", vamos colocar a última linha (Total Geral) em negrito
    if estilo == "resumo":
        formatted_values = []
        for col in df.columns:
            # Transforma a última célula de cada coluna em negrito usando HTML <b>
            col_data = df[col].astype(str).tolist()
            if col_data:
                col_data[-1] = f"<b>{col_data[-1]}</b>"
            formatted_values.append(col_data)
        values = formatted_values

    # Calcula a altura baseada no número de linhas
    altura_cabecalho = 30
    altura_linha = 25
    margem_vertical = 10 # 5 margin top + 5 margin bottom
    altura_total = altura_cabecalho + (len(df) * altura_linha) + margem_vertical

    # Calcula a largura aproximada baseada no conteúdo
    largura_total = 0
    larguras_colunas = []
    for col in df.columns:
        # Remover tags HTML para o calculo do tamanho do texto no rodape (se for o caso)
        dados_col = df[col].astype(str).str.replace('<b>', '', regex=False).str.replace('</b>', '', regex=False)
        len_dados = dados_col.str.len().max() if not dados_col.empty else 0
        max_len = max(len_dados, len(str(col)))
        
        # 8 pixels em média por caractere + padding das celulas
        largura_coluna = max(max_len * 8, 40) + 25 
        largura_total += largura_coluna
        larguras_colunas.append(largura_coluna)
        
    margem_horizontal = 10 # 5 margin left + 5 margin right
    largura_total += margem_horizontal

    fig = go.Figure(data=[go.Table(
        columnwidth=larguras_colunas,
        header=dict(
            values=[f"<b>{col}</b>" for col in df.columns],
            fill_color=cor_cabecalho,
            align='center',
            line_color='darkgrey',
            font=dict(color='black', size=header_font_size, family=font_family),
            #height=30
        ),
        cells=dict(
            values=values,
            fill_color='white',
            align='center',
            line_color='darkgrey',
            font=dict(color='black', size=cell_font_size, family=font_family),
            height=25
        )
    )])

    # Ajusta o layout para usar o tamanho exato da tabela, removendo sobras laterais e inferiores
    fig.update_layout(
        margin=dict(l=5, r=5, t=5, b=5),
        height=int(altura_total),
        width=int(largura_total),
        autosize=False
    )

    # Salva a imagem (scale=2 aumenta a qualidade/resolução)
    fig.write_image(nome_arquivo, scale=2)
    print(f"Sucesso: {nome_arquivo} gerado.")

import os
if __name__ == "__main__":
    print("Carregando base de dados principal (BD.csv)...")
    df_bd = pd.read_csv("BD.csv", sep=";", encoding="utf-8-sig", low_memory=False)

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
    
    operacoes_unicas = list(dict.fromkeys(operacao_regiao))
    
    for operacao in operacoes_unicas:
        print(f"\n--- Gerando imagens para a operação: {operacao} ---")
        
        operacao_limpa = str(operacao).strip()
        pasta_origem = f"docs/{operacao_limpa}"
        pasta_destino = f"imagem/imagens_{operacao_limpa}"
        os.makedirs(pasta_destino, exist_ok=True)
        
        try:
            df_grafico = gerar_grafico(df_bd, operacao)
            caminho_grafico = os.path.join(pasta_destino, 'grafico_geral.png')
            plt.savefig(caminho_grafico, dpi=300, bbox_inches='tight')
            plt.close() # Fechar para não sobrepor aos próximos
        except Exception as e:
            print(f"Erro ao gerar gráfico para {operacao}: {e}")



        try:
            arquivo = os.path.join(pasta_origem, 'pivot_infracoes.csv')
            if os.path.exists(arquivo):
                df = pd.read_csv(arquivo, sep=';', encoding='utf-8-sig')
                gerar_imagem_tabela(df, os.path.join(pasta_destino, "pivot_infracoes.png"), estilo="resumo")
        except Exception as e:
            print(f"Erro em pivot_infracoes.csv para {operacao}: {e}")

        try:
            arquivo = os.path.join(pasta_origem, 'ocorrencia_pontos.csv')
            if os.path.exists(arquivo):
                df = pd.read_csv(arquivo, sep=';', encoding='utf-8-sig')
                gerar_imagem_tabela(df, os.path.join(pasta_destino, "ocorrencia_pontos.png"), estilo="detalhado")
        except Exception as e:
            print(f"Erro em ocorrencia_pontos.csv para {operacao}: {e}")

        try:
            arquivo = os.path.join(pasta_origem, 'ocorrencia_pontos_mensal.csv')
            if os.path.exists(arquivo):
                df = pd.read_csv(arquivo, sep=';', encoding='utf-8-sig')
                gerar_imagem_tabela(df, os.path.join(pasta_destino, "ocorrencia_pontos_mensal.png"), estilo="resumo")
        except Exception as e:
            print(f"Erro em ocorrencia_pontos_mensal.csv para {operacao}: {e}")

        try:
            arquivo = os.path.join(pasta_origem, 'quadro_detalhado.csv')
            if os.path.exists(arquivo):
                df = pd.read_csv(arquivo, sep=';', encoding='utf-8-sig')
                gerar_imagem_tabela(df, os.path.join(pasta_destino, "quadro_detalhado.png"), estilo="resumo")
        except Exception as e:
            print(f"Erro em quadro_detalhado.csv para {operacao}: {e}")

        try:
            arquivo = os.path.join(pasta_origem, 'quadro_equipes.csv')
            if os.path.exists(arquivo):
                df = pd.read_csv(arquivo, sep=';', encoding='utf-8-sig')
                gerar_imagem_tabela(df, os.path.join(pasta_destino, "quadro_equipes.png"), estilo="detalhado")
        except Exception as e:
            print(f"Erro em quadro_equipes.csv para {operacao}: {e}")