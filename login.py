from gsheets import Gsheets
import pandas as pd

gsheets = Gsheets()

acessos = gsheets.pegar_dados_aba_access()
df_acessos = pd.DataFrame(acessos)
df_acessos.columns = df_acessos.iloc[0]

for index, row in df_acessos.iterrows():
    local = str(row['local'])
    login = str(row['login'])
    senha = str(row['passw'])

    if local == 'pontomaisRS':
        login_pontomaisRS = login
        senha_pontomaisRS = senha

    if local == 'pontomaisCE':
        login_pontomaisCE = login
        senha_pontomaisCE = senha

    if local == 'pontomaisVTC':
        login_pontomaisVTC = login
        senha_pontomaisVTC = senha

    if local == 'pontomaisBAR':
        login_pontomaisBAR = login
        senha_pontomaisBAR = senha

    if local == 'pontomaisFRS':
        login_pontomaisFRS = login
        senha_pontomaisFRS = senha

    if local == 'pontomaisPEL':
        login_pontomaisPEL = login
        senha_pontomaisPEL = senha

    if local == 'pontomaisPOA':
        login_pontomaisPOA = login
        senha_pontomaisPOA = senha

    if local == 'pontomaisBJL':
        login_pontomaisBJL = login
        senha_pontomaisBJL = senha


print(f'pontomaisRS: Login:{login_pontomaisRS} // Senha:{senha_pontomaisRS}')
print(f'pontomaisCE: Login:{login_pontomaisCE} // Senha:{senha_pontomaisCE}')
print(f'pontomaisVTC: Login:{login_pontomaisVTC} // Senha:{senha_pontomaisVTC}')
print(f'pontomaisBAR: Login:{login_pontomaisBAR} // Senha:{senha_pontomaisBAR}')
print(f'pontomaisFRS: Login:{login_pontomaisFRS} // Senha:{senha_pontomaisFRS}')
print(f'pontomaisPEL: Login:{login_pontomaisPEL} // Senha:{senha_pontomaisPEL}')
print(f'pontomaisPOA: Login:{login_pontomaisPOA} // Senha:{senha_pontomaisPOA}')
print(f'pontomaisBJL: Login:{login_pontomaisBJL} // Senha:{senha_pontomaisBJL}')










