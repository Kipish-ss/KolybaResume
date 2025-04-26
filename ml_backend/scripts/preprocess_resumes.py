from ml_backend.preprocessing.preprocessing_pipeline import preprocess_dataframe
import pandas as pd
from pathlib import Path
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def main():
    script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    ml_backend_dir = script_dir.parent

    input_path = ml_backend_dir / "data" / "raw" / "resumes.parquet"
    output_path = ml_backend_dir / "data" / "processed" / "preprocessed_resumes.parquet"

    df = pd.read_parquet(input_path)
    preprocessed_df = preprocess_dataframe(df)
    preprocessed_df.to_parquet(output_path, index=False)

    logger.info(f"Preprocessed {len(preprocessed_df)} resumes and saved to {output_path}")


if __name__ == "__main__":
    main()
