import pandas as pd
from pathlib import Path

RAW_DIR = Path(r"F:\etl\data\raw")
CLEAN_DIR = Path(r"F:\etl\data\clean")
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

files = [
    "companies.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "prosandcons.xlsx",
    "profitandloss.xlsx",
    "documents.xlsx"
]

for file in files:
    file_path = RAW_DIR / file
    df = pd.read_excel(file_path)
    print(f"{file} -> {df.shape[0]} rows, {df.shape[1]} columns")
    
    out_name = file.replace(".xlsx", ".csv")
    df.to_csv(CLEAN_DIR / out_name, index=False)