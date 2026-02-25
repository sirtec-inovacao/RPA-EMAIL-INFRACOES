import os
import shutil
from colorama import Fore

def delete_folders(folder_path):
    print(Fore.CYAN + "Removendo pasta: " + folder_path + ". Exclusão sendo iniciada para baixar novos dados/arquivos!")

    # Verifica se a pasta existe
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path, ignore_errors=True)
        print(Fore.GREEN + f'A pasta "{folder_path}" foi excluída com sucesso.\n')
    else:
        print(Fore.RED + f'A pasta "{folder_path}" não existe.\n')
