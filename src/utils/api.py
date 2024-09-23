import re
import logging
import requests

from src.config import Config

logger = logging.getLogger(__name__)


# разделения текста на фрагменты по ограничению в 10000 байт
def split_text(text: str, limit: int) -> list:
    try: 
        fragments = []
        words = text.split(' ')
        fragment = []
        fragment_len = 0

        for word in words:
            # русский символ = 6 байт
            if fragment_len + len(word) * 6 > limit:
                fragments.append(' '.join(fragment))
                fragment = []
                fragment_len = 0

            fragment.append(word)
            fragment_len += len(word) * 6 + 3  # + пробел: %20 = 3 символа

            # Добавляем последний фрагмент
            if word == words[-1]:
                fragments.append(' '.join(fragment))

        return fragments
    except Exception as e:
            logger.error(f'Error in /split_text: {e}')


# Функция для проверки текста через API и замены слов
def check_and_replace(text: str) -> str:
    try: 
        # запрос к API Яндекс.Спеллера
        response = requests.get(Config.YANDEX_SPELLER_API, params={"text": text, "options": 7})
        if response.status_code == 200:
            data = response.json()
            return replace_words(text, data)
        else:
            print(f"Ошибка: {response.status_code}")
            return text
    except Exception as e:
            logger.error(f'Error in /check_and_replace: {e}')


# замена слов в тексте
def replace_words(original_text: str, corrections: list) -> str:
    try:
        for correction in corrections:
            if correction['s'] and len(correction['word']) > 4:
                corrected_word = correction['s'][0]
                original_word = correction['word']
                original_text = re.sub(re.escape(original_word), corrected_word, original_text)

        return original_text
    except Exception as e:
        logger.error(f'Error in /replace_words: {e}')


# основная функция
def final_correcting(text: str) -> str:
    try:
        # разделяем текст на фрагменты по лимиту API
        fragments = split_text(text, Config.MAX_REQUEST_SIZE)

        for fragment in fragments:
            final_text = check_and_replace(fragment)

        return final_text
    except Exception as e:
        logger.error(f'Error in /final_correcting: {e}')
