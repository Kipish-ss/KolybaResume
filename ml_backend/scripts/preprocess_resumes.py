from ml_backend.utils.text_cleaning import clean_text
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
import pandas as pd
from pathlib import Path
import os
import logging
from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def clean_and_filter(text: str, min_length: int = 300) -> str | None:
    try:
        lang = detect(text)
    except LangDetectException:
        return None

    if lang != "en":
        return None

    return clean_text(text, min_length=min_length)


def preprocess_dataframe(df: pd.DataFrame, min_length: int = 300) -> pd.DataFrame:
    df = df.copy()
    tqdm.pandas(desc="Preprocessing resumes")
    df['Resume'] = df['Resume'].progress_apply(lambda x: clean_and_filter(x, min_length))
    df = df.dropna(subset=['Resume'])
    df = df.drop_duplicates(subset=['Resume'])
    return df


def main():
    script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    ml_backend_dir = script_dir.parent

    input_path = ml_backend_dir / "data" / "raw" / "resumes.parquet"
    output_path = ml_backend_dir / "data" / "processed" / "preprocessed_resumes.parquet"

    df = pd.read_parquet(input_path)
    df = preprocess_dataframe(df)
    df.to_parquet(output_path, index=False)

    logger.info(f"Preprocessed {len(df)} resumes and saved to {output_path}")


if __name__ == "__main__":
    main()
