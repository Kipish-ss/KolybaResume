from .text_cleaning import clean_text
from .translation import translate
from deepl import DeepLClient
from tqdm import tqdm
import pandas as pd


def preprocess_text(text: str, client: DeepLClient | None = None, min_length: int = 300) -> str | None:
    text = clean_text(text)
    text = translate(text, client)

    if text and len(text) >= min_length:
        return text.lower()
    else:
        return


def preprocess_dataframe(df: pd.DataFrame, client: DeepLClient | None = None, min_length: int = 300) -> pd.DataFrame:
    df = df.copy()
    tqdm.pandas(desc="Preprocessing resumes")
    df['Resume'] = df['Resume'].progress_apply(lambda x: preprocess_text(x, client, min_length))
    df = df.dropna(subset=['Resume'])
    df = df.drop_duplicates(subset=['Resume'])
    return df
