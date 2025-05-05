import re
import tqdm
import pandas as pd


def remove_urls(text: str) -> str:
    return re.sub(r'http\S+|www\.\S+', '', text)


def remove_emails(text: str) -> str:
    return re.sub(r'\S+@\S+', '', text)


def remove_phone_numbers(text: str) -> str:
    return re.sub(r'\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{1,4}\)?[-.\s]?)?(?:\d{1,4}[-.\s]?){1,3}\d{1,4}\b', '', text)


def remove_html_tags(text: str) -> str:
    return re.sub(r'<.*?>', '', text)


def remove_special_characters(text: str) -> str:
    return re.sub(r'[^\w\s.,!?()\-]', '', text)


def normalize_whitespace(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def clean_text(text: str, min_length: int = 500) -> str | None:
    text = remove_urls(text)
    text = remove_emails(text)
    text = remove_phone_numbers(text)
    text = remove_html_tags(text)
    text = remove_special_characters(text)
    text = normalize_whitespace(text)

    if len(text) >= min_length:
        return text
    else:
        return None
