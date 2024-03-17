from config import ASSISTENT_NAME, ASSISTENT_NAME_IN_ASCII

all_synonyms = []
dataset = {
    "HI": [
        "Привет",
        "Чотам",
        "Хай",
    ],
    "OPEN": [
        "Открой",
        "открой-ка",
        "включи"
    ],
    "BROWSER": [
        "Браузер"
    ],
    "YOUTUBE": [
        "youtube"
    ],
    "HOW_ARE_YOU": [
        "Как дела"
    ],
    "WHO_ARE_YOU": [
        "Ты кто"
    ],
    ASSISTENT_NAME_IN_ASCII: [
        ASSISTENT_NAME
    ],
    "QUIT": [
        "Вырубайся",
        "Отключайся",
        "Иди спать",
        "Иди поспи"
    ],
    "STEAM": [
        "steam",
        "стим"
    ],
    "REBOOT": [
        "перезагрузи"
    ],
    "SYSTEM": [
        "пк",
        "ноут",
        "ноутбук",
        "компьютер",
        "систему"
    ],
    "SHUTDOWN": [
        "выключи",
        "отключи",
        "выруби"
    ],
    "YES": [
        "да",
        "конечно"
    ],
    "RANDOM": [
        "случайное"
    ],
    "NUM": [
        "число"
    ],
    "FROM": [
        "от"
    ],
    "BEFORE": [
        "до"
    ],
    "WHAT_IS": [
        "что такое",
        "кто такой"
    ],
    "WRITE": [
        "запиши туда",
        "запиши"
    ],
    "SERIFS": [
        "засеки"
    ],
    "SET": [
        "поставь"
    ],
    "TIMER": [
        "таймер",
        "будильник"
    ],
    "FOR": [
        "на"
    ],
    "MINUTE": [
        "минут",
        "минуты",
        "минуту",
        "минута"
    ],
    "SECOND": [
        "секунд",
        "секунды",
        "секунда",
        "секунду"
    ],
    "HOUR": [
        "час",
        "часа",
    ],
    "ONE": [
        "одна",
        "одну"
    ]
}

welcome_messages = [
    "Здравствуйте сэр",
    "С новым рабочим днем сэр",
    "Хай сэр, хорошего вам настроения"
]

welcome_messages_by_time = {
    "day": ["Добрый день сэр"],
    "morning": ["Доброе утро сэр"],
    "dinner": ["Доброго обеда сэр"],
    "evening": [
        "Добрый вечер сэр",
    ],
    "night": ["Доброй ночи сэр, чего не спим?"]
}

welcome_messages_for_restart = [
    "Еще раз здравствуйте",
    "Как ваши дела? отдохнули?",
    "Я рада видеть вас снова"
]

ASSISTENT_FIRST_START_TEXT = f"""Здравствуйте, я {ASSISTENT_NAME}, ваш голосовой помощник. вы впервые меня запустили,
                                хотите чтобы я автоматически запускалась при старте системы?"""

def get_key_from_word(word: str) -> str | None:
    if word in all_synonyms:
        for key, synonyms in dataset.items():
            if word.lower().strip() in synonyms:
                return key
    return None

for key in dataset:
    for idx, string in enumerate(dataset[key]):
        dataset[key][idx] = dataset[key][idx].lower().strip()
        all_synonyms.append(dataset[key][idx])

all_synonyms = set(all_synonyms)