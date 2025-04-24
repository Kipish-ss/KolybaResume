from pathlib import Path
import pandas as pd
import os


def map_position(row: pd.Series) -> str:
    pos = row['Position']
    keyword = row['Primary Keyword'] if pd.notna(row['Primary Keyword']) else ''

    if (any(front in pos for front in ['angular', 'frontend', 'react', 'vue']) and
            'developer' in pos and 'backend' not in pos and
            'fullstack' not in pos and keyword == 'javascript'):
        return 'frontend'
    elif (('backend' in pos or 'back-end' in pos) and 'developer' in pos and
          'frontend' not in pos and 'front-end' not in pos and
          'fullstack' not in pos):
        return 'backend'
    elif 'fullstack' in pos or 'full-stack' in pos:
        return 'full stack'
    elif ('devops' in pos or 'sysadmin' in pos) and keyword == 'devops':
        return 'devops'
    elif 'qa engineer' in pos and 'qa' in keyword:
        return 'qa engineer'
    elif ('designer' in pos and
          any(u in pos for u in ['ui', 'ux', 'ui/ux']) and
          keyword == 'designer'):
        return 'ux'
    elif 'data engineer' in pos:
        return 'data engineer'
    elif ('data scientist' in pos or 'ml engineer' in pos or 'ai engineer' in pos) and keyword == 'data science':
        return 'data scientist'
    elif 'data' in pos and 'analyst' in pos and keyword == 'data analyst':
        return 'data analyst'
    elif 'business analyst' in pos:
        return 'business analyst'
    elif (any(mobile in pos for mobile in ['ios', 'android', 'flutter']) and
          keyword in ['ios', 'android', 'flutter']):
        return 'mobile'
    elif 'product manager' in pos and keyword == 'product manager':
        return 'product manager'
    elif 'project manager' in pos and keyword == 'project manager':
        return 'project manager'
    elif 'marketing' in pos and keyword == 'marketing':
        return 'marketing'
    elif (any(hr in pos for hr in ['recruiter', 'hiring', 'talent', 'hr']) and
          keyword in ['recruiter', 'hr']):
        return 'hr'
    elif 'seo' in pos:
        return 'seo'
    elif ('customer support' in pos or 'customer success' in pos) and keyword == 'support':
        return 'customer support'
    elif 'c++' in pos and keyword == 'c++':
        return 'c++'
    elif 'rust' in pos:
        return 'rust'
    elif 'sales manager' in pos and keyword == 'sales':
        return 'sales manager'
    elif 'ui/ux designer' in pos and keyword == 'design':
        return 'ux'
    else:
        return 'other'


def process_and_save_data(input_path: str, output_path: str) -> None:
    input_path = Path(input_path)
    output_path = Path(output_path)

    df = pd.read_parquet(input_path, columns=['Position', 'CV', 'Primary Keyword'])

    for col in ['Position', 'Primary Keyword']:
        df[col] = df[col].str.lower().str.strip()

    df['Category'] = df.apply(map_position, axis=1)
    df = df[['Category', 'CV']][df['Category'] != 'other']
    df.rename(columns={'CV': 'Resume'}, inplace=True)
    output_path.mkdir(parents=True, exist_ok=True)
    for category in df['Category'].unique():
        output_file = output_path / f"{category}.csv"
        df[df['Category'] == category].to_csv(output_file, index=False)


def main():
    script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    ml_backend_dir = script_dir.parent
    input_path = ml_backend_dir / "data" / "train-00000-of-00001.parquet"
    output_path = ml_backend_dir / "data" / "raw" / "huggingface"
    process_and_save_data(input_path, output_path)


if __name__ == "__main__":
    main()
