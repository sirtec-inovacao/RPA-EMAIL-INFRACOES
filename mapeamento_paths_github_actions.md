# Mapeamento de Paths para GitHub Actions (Google Drive API)

Este documento lista todos os caminhos (paths) locais e de rede identificados no projeto atuais que precisarão ser mapeados e adaptados para o uso da **Google Drive API** ao migrar para o **GitHub Actions**.

---

## 1. Credenciamento / Autenticação

**Arquivo:** `chaveGoogle.json`
**Onde é usado:** `gsheets.py` e `extracao_dados.py` (Localizado na raiz do projeto, concatenado com `path_script`).

> **Ação necessária para GitHub Actions:**
> O Github Actions não deve armazenar arquivos de chaves no repositório por questões de segurança. Você deve salvar o conteúdo deste JSON nos **GitHub Secrets** (ex: `GCP_CREDENTIALS`). No workflow (`.yml`), você recria este arquivo dinamicamente antes de rodar seu script Python, ou passa as credenciais diretamente via variável de ambiente.

---

## 2. Arquivos de Documento do Word (.docx)

**Arquivos:**

- `RS.docx`
- `CEARÁ.docx`
- `SUDOESTE VDC.docx`
- `EXTREMO OESTE BAR.docx` / `OESTE BAR-IBO.docx`
- `CENTRO FRS.docx`
- `PELOTAS.docx`
- `OESTE GUA-BJL.docx`
- `POA.docx`
- `SP.docx`

**Caminho Atual:** `G:/Drives compartilhados/Inovação - RH/{NomeDaOperacao}.docx`
**Onde é usado:** Variáveis de operação instanciadas em `extracao_dados.py`, `main_etp2.py`, e `teste.py`.

> **Ação necessária para GitHub Actions:**
> O mapeamento fixo para a unidade `G:` não funcionará no Actions. O robô precisará usar a **API do Google Drive (`google-api-python-client`)** para buscar listar arquivos na pasta de ID correspondente ao `Inovação - RH`, buscar o `fileId` do `.docx` em questão e realizar o **download** para o disco virtual do container do Actions antes que a ferramenta de manipulação de Word (ou conversão) consuma este arquivo.

---

## 3. Diretórios de Base de Dados e Resultados (Origem e Destino)

### 3.1. Origem (Leitura)

**Caminho Atual:** `G:\Drives compartilhados\PCP\Time Inovação\Soluções\BI - Painel RH\Bases\Geral`
**Onde é usado:** Função `combine_latest_csvs` no `extracao_dados.py` para descobrir os CSVs mais recentes.

### 3.2. Destino (Escrita)

**Caminho Atual:** `G:\Drives compartilhados\PCP\Time Inovação\Soluções\BI - Painel RH\Bases\E-mail\`
**Onde é usado:** Salvar arquivos processados como `final.xlsx`, `BD.csv` e `BD_RES.csv` em `gerar_BD.py` e `extracao_dados.py`.

> **Ação necessária para GitHub Actions:**
> Em vez de listar arquivos no disco local com `os.listdir()` ou `glob.glob()`, você terá que chamar o endpoint `files.list` da API do Drive com a query `parents in '{folderId}'`. Após os processamentos e junções de bases, você fará um script final que chama o endpoint `files.create` / `files.update` (`MediaFileUpload`) enviando o arquivo processado do contêiner para o Drive.

---

## 4. Arquivos PDF de Gráficos e Ocorrências

**Arquivos (por Operação):**

- `grafico_geral.pdf`
- `ocorrencia_pontos.pdf`
- `ocorrencia_pontos_mensal.pdf`
- `quadro_detalhado.pdf`
- `quadro_equipes.pdf`

**Caminho Atual:** `G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/{OPERAÇÃO}/{arquivo}.pdf`
**Onde é usado:** Função `pdf_to_images` nas chamadas iterativas de `main_etp2.py` e `teste_sirtec.py`.

> **Ação necessária para GitHub Actions:**
> A mesma lógica para os arquivos `.docx` se aplica aqui. Estes PDFs precisarão ser baixados via Google Drive API para um diretório local temporário, como por exemplo `./temp_pdfs/{OPERAÇÃO}/`, e então passados para a biblioteca que de fato vai transformá-los em imagem (`pdf_to_images`).

---

## 5. Caminhos Locais Fixos "Chumbados" (Absolute Paths)

**Caminhos Atuais:**

- `C:\Users\Sirtec\arquivos_teste\E-mail\BD.csv`
- `C:\Users\Sirtec\arquivos_teste\E-mail\BD_RES.csv`
- `C:\Users\Sirtec\arquivos_teste\E-mail\final.xlsx`

**Onde são usados:** `gerar_BD.py` (linhas 197 e 205) e `extracao_dados.py` (linha 389).

> **Ação necessária para GitHub Actions:**
> Como o Linux Ubuntu (usado nas runners padrão do Actions) não mapeia diretórios estilo Windows, códigos que tentam salvar em `C:\Users\Sirtec\...` falharão imediatamente lançando a exceção `FileNotFoundError` ou `os error 2`.
>
> **Solução:** Substitua para caminhos relativos ao projeto, como:
>
> - `./data/output/E-mail/BD.csv`
> - `./data/output/E-mail/final.xlsx`
>   E após estarem presentes nestas pastas, realizar o upload novamente.

---

## 📝 Resumo de Transição

1. **Substituir bibliotecas de manipulação de OS/File System:** Trocar usos de diretórios compartilhados de disco (ex: `os.listdir('G:\\...')`) para chamadas usando a `google-api-python-client` (`driveService.files().list(...)` e `.get_media()`).
2. **Utilizar Storage Temporal:** Tudo que o seu script hoje lê magicamente pela rede G: deverá transitar por uma etapa anterior de **Download**.
3. **Paths Relativos:** Eliminar qualquer existência de `C:\` e padronizar toda saída para pastas dentro de `/workspace/` do GitHub (que na sua máquina será referenciada apenas como relativa `./pasta`).
