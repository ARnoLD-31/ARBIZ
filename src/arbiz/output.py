from datetime import datetime

import colorama
from colorama import Fore, Style

colorama.init()


def info(chat_id: str, message: str) -> None:
    print(
        f"{Style.BRIGHT}{Fore.BLUE}[{datetime.now().strftime('%H:%M:%S')}] "
        f"[INFO] [{chat_id}]{Style.RESET_ALL} {message}"
    )


def warning(chat_id: str, message: str) -> None:
    print(
        f"{Style.BRIGHT}{Fore.YELLOW}[{datetime.now().strftime('%H:%M:%S')}] "
        f"[WARNING] [{chat_id}]{Style.RESET_ALL} {message}"
    )


def error(chat_id: str, message: str) -> None:
    print(
        f"{Style.BRIGHT}{Fore.RED}[{datetime.now().strftime('%H:%M:%S')}] "
        f"[ERROR] [{chat_id}]{Style.RESET_ALL} {message}"
    )


def fatal_error(chat_id: str, message: str) -> None:
    print(
        f"{Style.BRIGHT}{Fore.RED}[{datetime.now().strftime('%H:%M:%S')}] "
        f"[FATAL ERROR] [{chat_id}] {message}"
    )
