import os
import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def get_subdirectories(base_path: str) -> list[str]:
    return [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]


def merge_category_files(folder_path: str, category: str,
                         special_cases: dict[str, list[str]] | None = None) -> pd.DataFrame:
    subdirs = get_subdirectories(folder_path)
    dfs = []

    if special_cases and category in special_cases:
        filenames = special_cases[category]
        for subdir in subdirs:
            for filename in filenames:
                file_path = os.path.join(folder_path, subdir, filename)
                if os.path.exists(file_path):
                    df = pd.read_csv(file_path)
                    dfs.append(df)
    else:
        filename = f"{category}.csv"
        for subdir in subdirs:
            file_path = os.path.join(folder_path, subdir, filename)
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                dfs.append(df)

    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.drop_duplicates(subset='Resume', inplace=True)
    combined_df.dropna(inplace=True)
    combined_df['Category'] = category

    return combined_df


def filter_backend_resumes(df: pd.DataFrame, backend_keywords: list[str],
                           frontend_fullstack_keywords: list[str]) -> pd.DataFrame:
    df_copy = df.copy()
    df_copy.dropna(inplace=True, subset=['Resume'])
    backend_only = df_copy[
        df_copy['Resume'].str.lower().apply(lambda text:
                                            any(k in text for k in backend_keywords) and
                                            not any(k in text for k in frontend_fullstack_keywords)
                                            )
    ]
    return backend_only


def augment_backend(base_path: str, categories_to_check: list[str],
                    backend_keywords: list[str],
                    frontend_fullstack_keywords: list[str]) -> pd.DataFrame:
    subdirs = get_subdirectories(base_path)
    all_augmented = []

    for subdir in subdirs:
        subdir_path = os.path.join(base_path, subdir)
        for category in categories_to_check:
            file_path = os.path.join(subdir_path, f"{category}.csv")
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                backend_resumes = filter_backend_resumes(df, backend_keywords, frontend_fullstack_keywords)
                if not backend_resumes.empty:
                    backend_resumes['Category'] = 'backend'
                    all_augmented.append(backend_resumes)

    if all_augmented:
        combined = pd.concat(all_augmented, ignore_index=True)
        combined.drop_duplicates(subset='Resume', inplace=True)
        logger.info(f"Augmented backend resumes collected: {len(combined)}")
        return combined

    logger.info("No augmented backend resumes found.")
    return pd.DataFrame(columns=['Resume', 'Category'])


def merge_all_categories(base_path: str, output_file: str, categories: list[str],
                         special_cases: dict[str, list[str]],
                         backend_keywords: list[str],
                         frontend_fullstack_keywords: list[str],
                         categories_to_check: list[str]) -> None:
    all_dfs = []

    for category in categories:
        merged_df = merge_category_files(base_path, category, special_cases)
        if not merged_df.empty:
            all_dfs.append(merged_df)
            logger.info(f"Merged {len(merged_df)} rows for category: {category}")

    backend_augmented_df = augment_backend(base_path, categories_to_check, backend_keywords,
                                           frontend_fullstack_keywords)
    if not backend_augmented_df.empty:
        all_dfs.append(backend_augmented_df)

    final_df = pd.concat(all_dfs, ignore_index=True)
    final_df.drop_duplicates(subset='Resume', inplace=True)
    output_path = os.path.join(base_path, output_file)
    final_df.to_parquet(output_path, index=False)
    logger.info(f"Saved total {len(final_df)} rows to {output_file}")


def main():
    script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    ml_backend_dir = script_dir.parent
    base_path = str(ml_backend_dir / "data" / "raw")
    output_file = 'resumes.parquet'

    CATEGORIES = [
        "frontend", "backend", "full stack", "devops", "qa engineer",
        "ux", "data engineer", "data analyst", "business analyst",
        "data scientist", "product manager", "project manager",
        "marketing", "hr", "customer support",
        "c++", "sales manager", "mobile"
    ]

    SPECIAL_CASES = {
        "hr": ["hr.csv", "recruiter.csv"],
        "mobile": ["mobile.csv", "android.csv", "flutter.csv", "ios.csv"],
        "marketing": ["marketing.csv", "seo.csv"],
        "c++": ["c++.csv", "rust.csv"]
    }

    backend_keywords = ['backend', 'back-end', 'back end']
    frontend_fullstack_keywords = [
        "frontend", "front-end", "react", "vue", "angular",
        "fullstack", "full-stack", "full stack"
    ]

    CATEGORIES_TO_CHECK = ['java', '_net', 'python']

    merge_all_categories(base_path, output_file, CATEGORIES, SPECIAL_CASES, backend_keywords,
                         frontend_fullstack_keywords,
                         CATEGORIES_TO_CHECK)


if __name__ == "__main__":
    main()
