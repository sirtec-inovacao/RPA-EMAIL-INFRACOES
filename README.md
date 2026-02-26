# Robô - E-mail de Infrações

Este projeto consiste em uma automação (RPA) desenvolvida em Python para o setor de Recursos Humanos/PCP. O objetivo principal é extrair relatórios de atrasos do sistema de ponto (Pontomais), cruzar com a base de dados interna da equipe (armazenada no Google Drive), gerar indicadores visuais (tabelas e gráficos em imagem) e realizar o disparo automatizado de e-mails para os gestores e responsáveis de cada unidade/operação.

## 🚀 Visão Geral do Fluxo

A automação segue um pipeline rígido, executando as seguintes etapas em sequência:

1. **RPA de Extração (Playwright):** Acessa o painel do Pontomais de diversas regionais (RS, CE, SP, etc.), insere as credenciais via leitura do Google Sheets, aplica os filtros de data e faz o download dos relatórios de atrasos em `.csv`.
2. **Download das Bases no Drive:** Obtém as bases gerais mais recentes direto do Google Drive.
3. **Cruzamento de Dados:** Cruza os atrasos do Pontomais com a base geral, gerando um consolidado (`final.csv` / `final.xlsx`).
4. **Tratamento Analítico:** Script de formatação de tabelas e sumarização dos dados por equipe/unidade.
5. **Geração de Imagens:** Converte os dados sumarizados em painéis visuais (`.png`) para facilitar a digestibilidade no corpo do e-mail.
6. **Disparo de E-mails:** Envia os avisos de infrações (com anexos e imagens no corpo do e-mail) utilizando as listas de distribuição configuradas.

## 🛠️ Tecnologias e Bibliotecas

- **Linguagem Principal:** Python 3.10+
- **Web Scraping / RPA:** `playwright` (Chromium em modo headless)
- **Manipulação de Dados:** `pandas`, `numpy`
- **Integração Google (Drive e Sheets):** `google-api-python-client`, `gspread`, `google-auth`
- **Orquestração e Integração Contínua (CI/CD):** GitHub Actions
- **Outras Bibliotecas Auxiliares:** `colorama` (cores no terminal), `logging` (monitoramento local)

---

## 📂 Estrutura de Arquivos Principais

```text
dev_robo-email-infracoes/
├── .github/workflows/
│   └── robo_ponto.yml        # Pipeline do GitHub Actions que orquestra toda a execução
├── functions/                # Funções utilitárias refatoradas (limpeza, logs, requests ao drive)
│   └── drive_utils.py        # Módulos de download e upload focado na API do GDrive
├── src/                      # Scripts secundários de processamento (etapas ou testes)
├── main.py                   # ETAPA 1: RPA Pontomais + Join de bases principais (Gera final.csv)
├── gerar_BD.py               # ETAPA 2: Processamento e tratamento do BD completo
├── gerar_BD_RES.py           # ETAPA 3: Processamento dos tempos e intervalos (BD Resumo)
├── transform.py              # ETAPA 4: Conversão de dados e agrupamento para visão da liderança
├── gerar_imagem.py           # ETAPA 5: Renderização de gráficos/tabelas PNG salvos na pasta 'imagem/'
├── enviar_emails.py          # ETAPA 6: Disparo via SMTP/Email usando as imagens geradas
├── gsheets.py                # Wrapper para fácil integração com planilhas Google Sheets
├── requirements.txt          # Dependências do projeto (focado para rodar em Linux/Ubuntu)
└── chaveGoogle.json / service_account.json # Credentials do Google Cloud (Não versionadas por segurança)
```

## ▶️ Fluxo de Execução Local

Idealmente, os scripts são executados na ordem mostrada. Pode rodar tudo em sequência para testar a pipeline completa:

```bash
python main.py
python gerar_BD.py
python gerar_BD_RES.py
python transform.py
python gerar_imagem.py
python enviar_emails.py
```
