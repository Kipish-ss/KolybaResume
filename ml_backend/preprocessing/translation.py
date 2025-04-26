import time
from langdetect import detect
from deepl import DeepLClient
from deepl.exceptions import DeepLException
from langdetect.lang_detect_exception import LangDetectException


def translate(text: str, client: DeepLClient | None = None) -> str | None:
    try:
        lang = detect(text)
    except LangDetectException:
        lang = 'unknown'
    if lang != "en":
        if client:
            retries = 0
            while retries < 3:
                try:
                    result = client.translate_text(text, target_lang="EN-US")
                    return result.text
                except DeepLException:
                    retries += 1
                    time.sleep(5)
            return
        else:
            return

    return text
