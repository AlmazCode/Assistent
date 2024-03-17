import tools

ASSISTENT_NAME = "Джарвис"
ASSISTENT_NAME_IN_ASCII = tools.utf8_to_ascii(ASSISTENT_NAME, True)

CONTENT = "<CONTENT>"
CONTENT_TO_END = "<CONTENT_TO_END>"
FUNC = "<FUNC>"
ELSE = "<ELSE>"
EMPTY = "<EMPTY>"

config = {
    "HI": {
        ELSE: [tools.tts, "Добрый день, Сэр"],
        "HOW_ARE_YOU": {
            ELSE: [tools.tts, "Жить можно, у вас?"],
            "WHO_ARE_YOU": [tools.tts, f"Здравствуйте, меня зовут {ASSISTENT_NAME}"]
        },
        "WHO_ARE_YOU": [tools.tts, f"Здравствуйте, меня зовут {ASSISTENT_NAME}"]
    },
    "OPEN": {
        "BROWSER": [tools.launch_app, tools.BROWSER_PATH],
        "YOUTUBE": [tools.open_url, r"https://youtube.com"],
        "STEAM": [tools.launch_app, r"C:\Program Files (x86)\Steam\Steam.exe"]
    },
    "WHO_ARE_YOU": {
        ELSE: [tools.tts, f"Меня зовут {ASSISTENT_NAME}"]
    },
    "HOW_ARE_YOU": {
        ELSE: [tools.tts, "Жить можно, у вас?"],
    },
    ASSISTENT_NAME_IN_ASCII: {
        ELSE: [tools.tts, "Я слушаю вас"]
    },
    "QUIT": {
        ELSE: [tools.close_assistent]
    },
    "REBOOT": {
        "SYSTEM": [tools.reboot_system]
    },
    "SHUTDOWN": {
        "SYSTEM": [tools.shutdown_system]
    },
    "RANDOM": {
        "NUM": {
            "FROM": {
                CONTENT: {
                    "BEFORE": CONTENT
                }
            }
        },
        FUNC: tools.print_random
    },

    "WHAT_IS": {
        CONTENT: None,
        FUNC: tools.search_wikipedia
    },
    "WRITE": {
        CONTENT_TO_END: None,
        FUNC: tools.save_note
    },
    "SERIFS": {
        CONTENT: CONTENT,
        FUNC: tools.start_timer_stream
    },
    "SET": {
        "TIMER": {
            "FOR": {
                CONTENT: CONTENT,
                FUNC: tools.start_timer_stream
            },
            CONTENT: CONTENT,
            FUNC: tools.start_timer_stream
        }
    }
}