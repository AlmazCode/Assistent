import speech_recognition
import tools
import dataset
import startup
import datetime
import colorama

from text_parser import Parser
from config import EMPTY, ASSISTENT_NAME, ASSISTENT_NAME_IN_ASCII
from data import Data

_current_day = datetime.datetime.now().day
STARTED_TODAY = Data.get_data("last_opened_day", -1) == _current_day
Data.save_data("last_opened_day", _current_day)

del _current_day

class Assistent:
    def __init__(self):
        self.sr = speech_recognition.Recognizer()
        self.sr.pause_threshold = 0.5
        self.sr.energy_threshold = 400
        self.sr.dynamic_energy_threshold = False

        self.ASSISTENT_CALLED = False

    def _listen(self):
        with speech_recognition.Microphone() as mic:
            self.sr.adjust_for_ambient_noise(mic, duration = 0.5)
            audio = self.sr.listen(mic)
        try:
            query = self.sr.recognize_google(audio_data = audio, language = tools.tts_language)
            return query
        except:
            return EMPTY
    
    def _split_str(self, text: str) -> list:
        return list(set(text.split()))

    def start(self):

        choice = tools.random.randint(0, 1)
        from_reboot = Data.get_data("from_reboot", False)
        fisrt_start = Data.get_data("first_start", True)

        # после перезагрузки ассистентом
        if from_reboot:
            tools.tts("С удачной перезагрузкой!")
            Data.save_data("from_reboot", False)

        elif not fisrt_start:
            # Приветствует с новым днем
            if choice == 0:
                if STARTED_TODAY:
                    tools.random_tts(dataset.welcome_messages_for_restart)
                else:
                    tools.random_tts(dataset.welcome_messages)

            # Иначе, просто здаровывается в зависимости от времени
            else:
                hour = datetime.datetime.now().hour
                time_periods = ["night", "morning", "dinner", "evening"]
                time_ranges = [(22, 4), (5, 10), (11, 16), (17, 21)]

                for period, (start, end) in zip(time_periods, time_ranges):
                    if start <= hour <= end:
                        tools.random_tts(dataset.welcome_messages_by_time[period])
                        break

        # Первый запуск ассистента
        elif fisrt_start:
            tools.tts(dataset.ASSISTENT_FIRST_START_TEXT)
            text = self._listen()
            text = dataset.get_key_from_word(self._split_str(text)[0])

            if text == "YES":
                tools.tts("отлично")
                successfully = startup.add_to_startup()
                if not successfully:
                    tools.tts("К сожалению, у меня почему-то не получилось добавить себя в автозагрузку.")
            else:
                tools.tts("как скажите")
            
            Data.save_data("first_start", False)

        while 1:
            text = self._listen()
            setted_text = self._split_str(text)

            if ASSISTENT_NAME in text or self.ASSISTENT_CALLED:
                if text != EMPTY:
                    self.ASSISTENT_CALLED = False
                if len(setted_text) == 1 and setted_text[0] == ASSISTENT_NAME:
                    tools.tts("Да сэр")
                    self.ASSISTENT_CALLED = True
                    continue

                parser = Parser(text)
                parsed_command = parser.parse_text()
                setted_command = self._split_str(parsed_command)

                if len(setted_command) == 1 and setted_command[0] == ASSISTENT_NAME_IN_ASCII:
                    tools.tts("Да сэр")
                    self.ASSISTENT_CALLED = True
                    continue

                print(colorama.Fore.GREEN + f"Input text: {text}" + colorama.Fore.RESET)
                print(colorama.Fore.YELLOW + f"Parsed command: {parsed_command}" + colorama.Fore.RESET)
                
                parser.execute_command()

                print("-" * 20)