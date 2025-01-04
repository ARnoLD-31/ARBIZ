import os

_PATH: str = os.path.dirname(os.path.abspath(__file__))
with open(f"{_PATH}/chat.txt", encoding="utf-8") as file:
    CHAT: str = file.read()
with open(f"{_PATH}/email.txt", encoding="utf-8") as file:
    EMAIL: str = file.read()
