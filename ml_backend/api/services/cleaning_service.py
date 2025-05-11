from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
import translators as ts
import re
import logging
import time
import random

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


def translate(text: str, max_len=4500, max_retries=3) -> str:
    try:
        lang = detect(text)
    except LangDetectException:
        lang = ''

    if lang != 'en':
        for attempt in range(max_retries):
            try:
                if len(text) <= max_len:
                    text = ts.translate_text(text, translator='google')
                else:
                    chunks = [text[i:i + max_len] for i in range(0, len(text), max_len)]
                    translated_chunks = []

                    for chunk in chunks:
                        for chunk_attempt in range(max_retries):
                            try:
                                translated_chunk = ts.translate_text(chunk, translator='google')
                                translated_chunks.append(translated_chunk)
                                break
                            except Exception as chunk_exception:
                                if chunk_attempt == max_retries - 1:
                                    logger.warning(
                                        f"Failed to translate chunk after {max_retries} attempts: {chunk_exception}")
                                    translated_chunks.append(chunk)
                                else:
                                    wait_time = 2 ** chunk_attempt + random.random()
                                    logger.info(
                                        f"Chunk translation attempt {chunk_attempt + 1} failed, retrying in {wait_time:.1f}s")
                                    time.sleep(wait_time)

                    text = ''.join(translated_chunks)
                break

            except Exception as e:
                if attempt == max_retries - 1:
                    logger.warning(f"Translation failed after {max_retries} attempts: {e}, returning best result")
                else:
                    wait_time = 2 ** attempt + random.random()
                    logger.info(f"Translation attempt {attempt + 1} failed, retrying in {wait_time:.1f}s")
                    time.sleep(wait_time)

    return text
