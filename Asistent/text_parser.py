import tools
import colorama

from config import config, CONTENT, FUNC, ELSE, CONTENT_TO_END
from dataset import dataset, all_synonyms, get_key_from_word

# punctuation = r"""!"#$%&'()*+,./:;<=>?@[\]^`{|}~"""
# _translator = str.maketrans('', '', punctuation)

class Parser:
    def __init__(self, text: str) -> None:
        self.text = text
        self.dataset = dataset
        self.config = config
        self.command: str = None
    
    def _pre_parse(self, s):
        words = s.lower().split()
        result = []
        temp = ''
        i = 0
        while i < len(words):
            for j in range(len(words), i, -1):
                phrase = ' '.join(words[i:j])
                if phrase in all_synonyms:
                    if temp:
                        result.append(temp)
                        temp = ''
                    result.append(phrase)
                    i = j-1
                    break
            else:
                if temp:
                    temp += ' ' + words[i]
                else:
                    temp = words[i]
            i += 1
        if temp:
            result.append(temp)
        return result
    
    def parse_text(self) -> str:
        text = self._pre_parse(self.text)
        parsed_keys = []
        current_config = self.config

        for index, word in enumerate(text):
            found = False
            key = get_key_from_word(word)
            if type(current_config) != str and current_config not in [None, ""] and key in current_config:
                parsed_keys.append(key)
                current_config = current_config[key]
                if index != len(text) - 1 and text[index+1] in all_synonyms and get_key_from_word(text[index+1]) not in current_config and CONTENT not in current_config:
                    current_config = self.config
                found = True
            if not found and current_config not in ["", None]:
                if CONTENT in current_config:
                    parsed_keys.append(f'{CONTENT}="{word.replace(" ", "_")}"')
                    if type(current_config) != str:
                        current_config = current_config.get(CONTENT, {})
                    else:
                        current_config = self.config
                elif CONTENT_TO_END in current_config:
                    parsed_keys.append(f'{CONTENT}="{" ".join(text[index:]).replace(" ", "_")}"')
                    break

        self.command = " ".join(parsed_keys)
        return self.command

    def _parse_func_block(self, block: list[str]):
        args = []
        for key in block:
            if key.startswith(CONTENT):
                value: str = key.split("=", 1)[1].replace("_", " ")
                if value[1:-1].isdigit(): value = eval(value[1:-1])
                else: value = value[1:-1]
                args.append(value)
        
        return args

    def execute_command(self):
        command_chain = self.command.split()
        current_config = config
        functions = []

        for index, key in enumerate(command_chain):
            current_config = current_config.get(key, config)
            
            if FUNC in current_config:
                args = self._parse_func_block(command_chain[index+1:])
                functions.append([current_config[FUNC], args])
                current_config = config
                continue

            if isinstance(current_config, list) and callable(current_config[0]):
                function, *args = current_config
                functions.append([function, args])
                current_config = config
            elif isinstance(current_config, dict) and ELSE in current_config:
                function, *args = current_config[ELSE]
                functions.append([function, args])
                current_config = config

        tts_funcs = [func for func in functions if func[0] == tools.tts]
        other_funcs = [func for func in functions if func[0] != tools.tts]

        if len(tts_funcs) > 1 and not tts_funcs:
            functions = tts_funcs[-1]
        elif len(other_funcs) > 0:
            functions = other_funcs
        for func in functions:
            try:
                func[0](*func[1])
            except Exception as e:
                print(colorama.Fore.RED + f"Error executing function {func[0].__name__}: {e}" + colorama.Fore.RESET)