from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
import translators as ts
import re
import logging

logger = logging.getLogger(__name__)


def remove_urls(text: str) -> str:
    return re.sub(r'http\S+|www\.\S+', '', text)


def remove_emails(text: str) -> str:
    return re.sub(r'\S+@\S+', '', text)


def remove_phone_numbers(text: str) -> str:
    return re.sub(r'\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{1,4}\)?[-.\s]?)?(?:\d{1,4}[-.\s]?){1,3}\d{1,4}\b', '', text)


def remove_html_tags(text: str) -> str:
    return re.sub(r'<.*?>', '', text)


def remove_special_characters(text: str) -> str:
    return re.sub(r'[^\w\s.,!?()\-#+:/]', '', text)


def normalize_whitespace(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def clean_text(text: str) -> str | None:
    text = remove_urls(text)
    text = remove_emails(text)
    text = remove_phone_numbers(text)
    text = remove_html_tags(text)
    text = remove_special_characters(text)
    text = normalize_whitespace(text)

    return text


def translate(text: str, max_len=4500) -> str:
    try:
        lang = detect(text)
    except LangDetectException:
        lang = ''
    if lang != 'en':
        try:
            if len(text) <= max_len:
                text = ts.translate_text(text, translator='google')
            else:
                chunks = [text[i:i + max_len] for i in range(0, len(text), max_len)]
                translated_chunks = [ts.translate_text(chunk, translator='google') for chunk in chunks]
                text = ''.join(translated_chunks)
        except Exception as e:
            logger.warning(f"Google translation failed: {e}, returning original text")

    return text
