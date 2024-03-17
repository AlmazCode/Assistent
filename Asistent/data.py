import os
import json
import colorama
import tools

DATA_FILENAME = "DATA.json"
DATA_PATH = os.path.join(tools._get_work_path(), DATA_FILENAME)

class Data:

    @staticmethod
    def _read_file(path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(colorama.Fore.YELLOW + __class__.__name__ + "." + tools.get_current_method_name() + 
                  colorama.Fore.RESET + f" : Файл `{DATA_FILENAME}` не был найден")
            return {}
        except json.JSONDecodeError:
            return {}

    @staticmethod
    def _write_file(path, data):
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def get_data(key: str, not_found_value: any = 0) -> any:
        data = Data._read_file(DATA_PATH)
        return data.get(key, not_found_value)

    def save_data(key: str, value: any) -> None:
        data = Data._read_file(DATA_PATH)
        data[key] = value
        Data._write_file(DATA_PATH, data)