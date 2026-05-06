import re
import csv
import pandas as pd
from io import StringIO
from pathlib import Path

SQL_FILE = r"F:\etl\data\raw\scriptticker.sql"
OUT_DIR = Path("data/raw")
TABLES = [
    "companies",
    "balancesheet",
    "profitandloss",
    "cashflow",
    "analysis",
    "prosandcons",
    "documents"
]

OUT_DIR.mkdir(parents=True, exist_ok=True)

with open(SQL_FILE, "r", encoding="utf-8", errors="ignore") as f:
    sql_text = f.read()

print("SQL file loaded")
print("Total characters:", len(sql_text))

for table in TABLES:
    pattern = rf"INSERT INTO\s+`?{table}`?.*?VALUES\s*(.*?);"
    matches = re.findall(pattern, sql_text, re.S)

    print(f"\nTable: {table}")
    print("Matches found:", len(matches))

    rows = []

    for match in matches:
        chunks = re.findall(r"\((.*?)\)", match, re.S)
        print("Chunks found:", len(chunks))

        for chunk in chunks:
            try:
                reader = csv.reader(StringIO(chunk), delimiter=',', quotechar="'", escapechar='\\')
                row = next(reader)
                row = [None if str(x).upper() == "NULL" else x for x in row]
                rows.append(row)
            except Exception as e:
                print(f"Error parsing row in {table}: {e}")

    df = pd.DataFrame(rows)
    df.to_csv(OUT_DIR / f"{table}.csv", index=False)
    print(f"{table}: {df.shape[0]} rows, {df.shape[1]} columns")