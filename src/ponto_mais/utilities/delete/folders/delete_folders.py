import shutil
import os

def delete_folders(folder_path):
    print("Removendo pasta: " + folder_path + ". Exclusão sendo iniciada para baixar novos dados/arquivos!")

    # Verifica se a pasta existe
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f'A pasta "{folder_path}" foi excluída com sucesso.')
    else:
        print(f'A pasta "{folder_path}" não existe.')