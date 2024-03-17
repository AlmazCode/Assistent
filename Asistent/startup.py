import getpass
import os
import colorama

USER_NAME = getpass.getuser()
BAT_PATH = f'C:\\Users\\{USER_NAME}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'

def add_to_startup(file_path="") -> bool:
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    
    try:
        with open(os.path.join(BAT_PATH, "assistent.bat"), "w+", encoding="utf-8") as bat_file:
            bat_file.write(f'chcp 65001\npython "{file_path}\\main.py"\npause')
        
        print(colorama.Fore.GREEN + f"Ассистент успешно был добавлен в автозагрузку, путь:\n  {BAT_PATH}"
              + colorama.Fore.RESET)
        return True
    except:
        return False


if __name__ == "__main__":
    user = input("Включать автоматически ассистента при старте Windows? (y, n): >>> ")
    if user.lower().strip() == "y":
        add_to_startup()