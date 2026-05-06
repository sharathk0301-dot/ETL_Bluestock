from pathlib import Path
import os
import sys
import pandas as pd
from sqlalchemy import create_engine, text

# Base directory: F:\etl
BASE_DIR = Path(__file__).resolve().parent

# Input: output of 04_compute_health_scores.py
INPUT_FILE = BASE_DIR / "data" / "clean" / "processed" / "company_health_scores.csv"

DB_USER = "postgres"
DB_PASSWORD = "sharath"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "nifty100"

TABLE_NAME = "company_health_scores"


def get_engine():
    db_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(db_url)


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # Normalize column names
    df.columns = [col.strip().lower() for col in df.columns]

    # Expected columns based on 04 script
    expected_columns = [
        "company_name",
        "avg_opm_5y",
        "revenue_cagr_5y",
        "net_profit_cagr_5y",
        "de_ratio_latest",
        "cash_conversion_5y",
        "dividend_consistency",
        "growth_stability",
        "score_profitability",
        "score_growth",
        "score_leverage",
        "score_cashflow",
        "score_dividend",
        "score_growth_trend",
        "health_score",
        "health_label",
    ]

    available_columns = [c for c in expected_columns if c in df.columns]
    if not available_columns:
        raise ValueError("No expected columns found in CSV; check the input file.")

    df = df[available_columns].copy()

    numeric_cols = [
        "avg_opm_5y",
        "revenue_cagr_5y",
        "net_profit_cagr_5y",
        "de_ratio_latest",
        "cash_conversion_5y",
        "dividend_consistency",
        "growth_stability",
        "score_profitability",
        "score_growth",
        "score_leverage",
        "score_cashflow",
        "score_dividend",
        "score_growth_trend",
        "health_score",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "company_name" in df.columns:
        df["company_name"] = df["company_name"].astype(str).str.strip()

    if "health_label" in df.columns:
        df["health_label"] = df["health_label"].astype(str).str.strip()

    return df


def create_table(engine):
    # Simple schema matching the cleaned DataFrame
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        company_name TEXT PRIMARY KEY,
        avg_opm_5y FLOAT,
        revenue_cagr_5y FLOAT,
        net_profit_cagr_5y FLOAT,
        de_ratio_latest FLOAT,
        cash_conversion_5y FLOAT,
        dividend_consistency FLOAT,
        growth_stability FLOAT,
        score_profitability FLOAT,
        score_growth FLOAT,
        score_leverage FLOAT,
        score_cashflow FLOAT,
        score_dividend FLOAT,
        score_growth_trend FLOAT,
        health_score FLOAT,
        health_label TEXT
    );
    """
    with engine.begin() as conn:
        conn.execute(text(create_table_sql))


def load_data(engine, df: pd.DataFrame):
    with engine.begin() as conn:
        conn.execute(text(f"DELETE FROM {TABLE_NAME}"))
    df.to_sql(TABLE_NAME, engine, if_exists="append", index=False)


def main():
    print("Current working directory:", os.getcwd())
    print("Looking for file at:", INPUT_FILE)
    print("File exists:", INPUT_FILE.exists())

    if not INPUT_FILE.exists():
        print("\nERROR: Input file not found.")
        print("Expected location:", INPUT_FILE)
        print("\nPlease run 04_compute_health_scores.py first.")
        sys.exit(1)

    print("\nLoading health scores CSV...")
    df = pd.read_csv(INPUT_FILE)
    print("CSV loaded successfully.")
    print("Rows found:", len(df))
    print("Columns:", list(df.columns))

    df = clean_dataframe(df)
    print("Rows after cleaning:", len(df))

    if df.empty:
        print("ERROR: CSV is empty after cleaning. Nothing to load.")
        sys.exit(1)

    print("\nConnecting to PostgreSQL...")
    engine = get_engine()

    print("Creating table if not exists...")
    create_table(engine)

    print("Loading data into table...")
    load_data(engine, df)

    print(f"\nSuccess: Loaded {len(df)} rows into '{TABLE_NAME}'.")


if __name__ == "__main__":
    main()