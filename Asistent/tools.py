import platform
import subprocess
import webbrowser
import pygame
import os
import hashlib
import unidecode
import random
import time
import wikipedia
import threading
import inspect

from gtts import gTTS

pygame.mixer.init()
tts_language = "ru"
wikipedia.set_lang(tts_language)
#os.system("cls")

def init():
    global dataset
    global Data

    from dataset import dataset
    from data import Data


def _get_browser_path() -> str | None:
    osPlatform = platform.system()

    if osPlatform == 'Windows':
        try:
            from winreg import HKEY_CLASSES_ROOT, HKEY_CURRENT_USER, OpenKey, QueryValueEx

            with OpenKey(HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice') as regkey:
                browser_choice = QueryValueEx(regkey, 'ProgId')[0]

            with OpenKey(HKEY_CLASSES_ROOT, r'{}\shell\open\command'.format(browser_choice)) as regkey:
                browser_path_tuple = QueryValueEx(regkey, None)
                browser_path = browser_path_tuple[0].split('"')[1]
                return browser_path

        except Exception:
            print('Failed to look up default browser in system registry. Using fallback value.')
            return None

def launch_app(path: str) -> None:
    try:
        subprocess.Popen([path])
    except:
        print(f"couldn't open the {path}")
        tts("К сожалению, у меня не получилось открыть данное приложение.")

def open_url(url: str) -> None:
    webbrowser.open_new(url)

def tts(text: str) -> None:
    save_path = _get_work_path()
    file_name = os.path.join(save_path, hashlib.sha256(text.encode()).hexdigest() + ".mp3")
    speech = gTTS(text = text, lang = tts_language, slow = False)
    speech.save(file_name)
    _player = pygame.mixer.Sound(file_name)
    _player.play()
    os.remove(file_name)
    time.sleep(_player.get_length())

def close_assistent() -> None:
    tts("До свидания Сэр!")
    exit()

def utf8_to_ascii(utf8_string: str, to_upper: bool = False):
    ascii_string = unidecode.unidecode(utf8_string)
    if to_upper: ascii_string = ascii_string.upper()
    return ascii_string

def random_tts(options: list | tuple) -> None:
    elem = random.choice(options)
    tts(elem)

def reboot_system():
    Data.save_data("from_reboot", True)
    try:
        os.system("shutdown /r /t 1")
    except Exception as e:
        print(e)
        tts("Упс, у меня не получилось перезагрузить систему")

def shutdown_system():
    try:
        os.system("shutdown /s /t 1")
    except Exception as e:
        print(e)
        tts("Упс, у меня не получилось выключить систему")

def print_random(num1, num2):
    tts(str(random.randint(num1, num2)))

def _remove_brackets_content(text: str) -> str:
    result = ''
    open_brackets = 0
    for char in text:
        if char == '(':
            open_brackets += 1
        elif char == ')':
            if open_brackets > 0:
                open_brackets -= 1
        elif open_brackets == 0:
            result += char
    return result

def save_note(text: str) -> None:
    path = os.path.join(_get_work_path(), "notes.txt")
    with open(path, "a", encoding = "utf-8") as file:
        file.write(f"{text};\n")
    tts("Записала")

def _timer(seconds: int, multiplier_text: str) -> None:
    multiplier = 1

    if seconds in dataset["ONE"]:
        seconds = 1

    if multiplier_text in dataset["MINUTE"]:
        multiplier = 60
    elif multiplier_text in dataset["HOUR"]:
        multiplier = 600
    
    time.sleep(seconds * multiplier)
    _player = pygame.mixer.Sound(os.path.join(_get_work_path(),"Sounds", "timer_sound.mp3"))
    _player.play()

def start_timer_stream(seconds: int, multiplier_text: str) -> None:
    stream = threading.Thread(target = _timer, args = (seconds, multiplier_text))
    stream.start()

def search_wikipedia(text: str) -> None:

    try: page = wikipedia.summary(text)
    except: page = "Мне не удалось найти что-то по вашему запросу."

    page = _remove_brackets_content(page)

    idx = 0
    if len(page) > 128:
        while 1:
            if len(".".join(page.split(".")[0:idx])) < 128:
                idx += 1
            else:
                break

    if idx == 0:
        idx += 1

    result = ". ".join(page.split(".")[0:idx]) + "."
    tts(result)

def get_current_method_name():
    # Получаем стек вызовов
    stack = inspect.stack()
    # Извлекаем имя текущей функции (метода)
    current_function_name = stack[1][3]
    return current_function_name

def _get_work_path() -> str:
    return os.path.dirname(__file__)


BROWSER_PATH = _get_browser_path()