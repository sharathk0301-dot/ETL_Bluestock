from pathlib import Path
print("DEBUG: 03_load_to_warehouse.py from VS Code")

import pandas as pd
from sqlalchemy import create_engine, text


def get_engine():
    user = "postgres"
    password = "sharath"
    host = "localhost"
    port = 5432
    dbname = "nifty_warehouse"

    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    print("Connecting to:", url)
    return create_engine(url, echo=False)


def load_dim_company(engine, clean_dir: Path):
    print("=== Loading dim_company from CSV ===")
    df = pd.read_csv(clean_dir / "dim_company.csv")
    print("Rows in CSV:", len(df))

    insert_sql = text(
        """
        INSERT INTO dim_company (
            company_id,
            company_name,
            about_company,
            website,
            nse_profile,
            bse_profile,
            face_value,
            book_value,
            roce_percentage,
            roe_percentage
        )
        VALUES (
            :company_id,
            :company_name,
            :about_company,
            :website,
            :nse_profile,
            :bse_profile,
            :face_value,
            :book_value,
            :roce_percentage,
            :roe_percentage
        )
        ON CONFLICT (company_id) DO UPDATE
        SET
            company_name    = EXCLUDED.company_name,
            about_company   = EXCLUDED.about_company,
            website         = EXCLUDED.website,
            nse_profile     = EXCLUDED.nse_profile,
            bse_profile     = EXCLUDED.bse_profile,
            face_value      = EXCLUDED.face_value,
            book_value      = EXCLUDED.book_value,
            roce_percentage = EXCLUDED.roce_percentage,
            roe_percentage  = EXCLUDED.roe_percentage;
        """
    )

    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(insert_sql, {
                "company_id": row["company_id"],
                "company_name": row["company_name"],
                "about_company": row["about_company"],
                "website": row["website"],
                "nse_profile": row["nse_profile"],
                "bse_profile": row["bse_profile"],
                "face_value": row["face_value"],
                "book_value": row["book_value"],
                "roce_percentage": row["roce_percentage"],
                "roe_percentage": row["roe_percentage"],
            })

    print("dim_company upsert complete.")


def load_fact_balance_sheet(engine, clean_dir: Path):
    print("=== Loading fact_balance_sheet from CSV ===")
    df = pd.read_csv(clean_dir / "fact_balance_sheet.csv")
    print("Rows in CSV before cleaning:", len(df))

    bad_rows = df[df["fiscal_year"].isna()]
    if not bad_rows.empty:
        print("Dropping rows with NaN fiscal_year in balance_sheet:")
        print(bad_rows[["company_id", "fiscal_year"]])

    df = df.dropna(subset=["fiscal_year"])
    df["fiscal_year"] = df["fiscal_year"].astype(int)
    print("Rows in CSV after cleaning:", len(df))

    insert_sql = text(
        """
        INSERT INTO fact_balance_sheet (
            company_id,
            fiscal_year,
            equity_capital,
            reserves,
            borrowings,
            other_liabilities,
            total_liabilities,
            fixed_assets,
            cwip,
            investments,
            other_asset,
            total_assets,
            debt_to_equity
        )
        VALUES (
            :company_id,
            :fiscal_year,
            :equity_capital,
            :reserves,
            :borrowings,
            :other_liabilities,
            :total_liabilities,
            :fixed_assets,
            :cwip,
            :investments,
            :other_asset,
            :total_assets,
            :debt_to_equity
        )
        ON CONFLICT (company_id, fiscal_year) DO UPDATE
        SET
            equity_capital    = EXCLUDED.equity_capital,
            reserves          = EXCLUDED.reserves,
            borrowings        = EXCLUDED.borrowings,
            other_liabilities = EXCLUDED.other_liabilities,
            total_liabilities = EXCLUDED.total_liabilities,
            fixed_assets      = EXCLUDED.fixed_assets,
            cwip              = EXCLUDED.cwip,
            investments       = EXCLUDED.investments,
            other_asset       = EXCLUDED.other_asset,
            total_assets      = EXCLUDED.total_assets,
            debt_to_equity    = EXCLUDED.debt_to_equity;
        """
    )

    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(insert_sql, {
                "company_id": row["company_id"],
                "fiscal_year": row["fiscal_year"],
                "equity_capital": row["equity_capital"],
                "reserves": row["reserves"],
                "borrowings": row["borrowings"],
                "other_liabilities": row["other_liabilities"],
                "total_liabilities": row["total_liabilities"],
                "fixed_assets": row["fixed_assets"],
                "cwip": row["cwip"],
                "investments": row["investments"],
                "other_asset": row["other_asset"],
                "total_assets": row["total_assets"],
                "debt_to_equity": row["debt_to_equity"],
            })

    print("fact_balance_sheet upsert complete.")


def load_fact_profit_loss(engine, clean_dir: Path):
    print("=== Loading fact_profit_loss from CSV ===")
    df = pd.read_csv(clean_dir / "fact_profit_loss.csv")
    print("Rows in CSV before cleaning:", len(df))

    bad_rows = df[df["fiscal_year"].isna()]
    if not bad_rows.empty:
        print("Dropping rows with NaN fiscal_year in profit_loss:")
        print(bad_rows[["company_id", "fiscal_year"]])

    df = df.dropna(subset=["fiscal_year"])
    df["fiscal_year"] = df["fiscal_year"].astype(int)
    print("Rows in CSV after cleaning:", len(df))

    insert_sql = text(
        """
        INSERT INTO fact_profit_loss (
            company_id,
            fiscal_year,
            sales,
            expenses,
            operating_profit,
            opm_percentage,
            other_income,
            interest,
            depreciation,
            profit_before_tax,
            tax_percentage,
            net_profit,
            eps,
            dividend_payout,
            net_margin,
            operating_margin
        )
        VALUES (
            :company_id,
            :fiscal_year,
            :sales,
            :expenses,
            :operating_profit,
            :opm_percentage,
            :other_income,
            :interest,
            :depreciation,
            :profit_before_tax,
            :tax_percentage,
            :net_profit,
            :eps,
            :dividend_payout,
            :net_margin,
            :operating_margin
        )
        ON CONFLICT (company_id, fiscal_year) DO UPDATE
        SET
            sales             = EXCLUDED.sales,
            expenses          = EXCLUDED.expenses,
            operating_profit  = EXCLUDED.operating_profit,
            opm_percentage    = EXCLUDED.opm_percentage,
            other_income      = EXCLUDED.other_income,
            interest          = EXCLUDED.interest,
            depreciation      = EXCLUDED.depreciation,
            profit_before_tax = EXCLUDED.profit_before_tax,
            tax_percentage    = EXCLUDED.tax_percentage,
            net_profit        = EXCLUDED.net_profit,
            eps               = EXCLUDED.eps,
            dividend_payout   = EXCLUDED.dividend_payout,
            net_margin        = EXCLUDED.net_margin,
            operating_margin  = EXCLUDED.operating_margin;
        """
    )

    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(insert_sql, {
                "company_id": row["company_id"],
                "fiscal_year": row["fiscal_year"],
                "sales": row["sales"],
                "expenses": row["expenses"],
                "operating_profit": row["operating_profit"],
                "opm_percentage": row["opm_percentage"],
                "other_income": row["other_income"],
                "interest": row["interest"],
                "depreciation": row["depreciation"],
                "profit_before_tax": row["profit_before_tax"],
                "tax_percentage": row["tax_percentage"],
                "net_profit": row["net_profit"],
                "eps": row["eps"],
                "dividend_payout": row["dividend_payout"],
                "net_margin": row["net_margin"],
                "operating_margin": row["operating_margin"],
            })

    print("fact_profit_loss upsert complete.")


def load_fact_cash_flow(engine, clean_dir: Path):
    print("=== Loading fact_cash_flow from CSV ===")
    df = pd.read_csv(clean_dir / "fact_cash_flow.csv")
    print("Rows in CSV before cleaning:", len(df))

    bad_rows = df[df["fiscal_year"].isna()]
    if not bad_rows.empty:
        print("Dropping rows with NaN fiscal_year in cash_flow:")
        print(bad_rows[["company_id", "fiscal_year"]])

    df = df.dropna(subset=["fiscal_year"])
    df["fiscal_year"] = df["fiscal_year"].astype(int)
    print("Rows in CSV after cleaning:", len(df))

    insert_sql = text(
        """
        INSERT INTO fact_cash_flow (
            company_id,
            fiscal_year,
            operating_activity,
            investing_activity,
            financing_activity,
            net_cash_flow,
            free_cash_flow
        )
        VALUES (
            :company_id,
            :fiscal_year,
            :operating_activity,
            :investing_activity,
            :financing_activity,
            :net_cash_flow,
            :free_cash_flow
        )
        ON CONFLICT (company_id, fiscal_year) DO UPDATE
        SET
            operating_activity = EXCLUDED.operating_activity,
            investing_activity = EXCLUDED.investing_activity,
            financing_activity = EXCLUDED.financing_activity,
            net_cash_flow      = EXCLUDED.net_cash_flow,
            free_cash_flow     = EXCLUDED.free_cash_flow;
        """
    )

    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(insert_sql, {
                "company_id": row["company_id"],
                "fiscal_year": row["fiscal_year"],
                "operating_activity": row["operating_activity"],
                "investing_activity": row["investing_activity"],
                "financing_activity": row["financing_activity"],
                "net_cash_flow": row["net_cash_flow"],
                "free_cash_flow": row["free_cash_flow"],
            })

    print("fact_cash_flow upsert complete.")


def load_fact_analysis(engine, clean_dir: Path):
    print("=== Loading fact_analysis from CSV ===")
    df = pd.read_csv(clean_dir / "fact_analysis.csv")
    print("Rows in CSV before cleaning:", len(df))

    # Helper to convert strings like "10 Years: 21%" -> 21.0
    def parse_percent(value):
        if pd.isna(value):
            return None
        # Convert to string, remove text, keep digits, dot, minus sign
        s = str(value)
        # Common patterns in your CSV: "10 Years: 21%", "10 Years:     15%"
        # Remove 'Years', ':', '%', spaces; keep only the number part
        s = s.replace("Years", "").replace("Year", "")
        s = s.replace(":", " ").replace("%", " ")
        s = s.strip()
        # Now s might be "10 21" or just "21". We want the last number (the percentage).
        parts = [p for p in s.split() if p.replace(".", "", 1).replace("-", "", 1).isdigit()]
        if not parts:
            return None
        return float(parts[-1])

    # Apply cleaning to each numeric column
    df["compounded_sales_growth"] = df["compounded_sales_growth"].apply(parse_percent)
    df["compounded_profit_growth"] = df["compounded_profit_growth"].apply(parse_percent)
    df["stock_price_cagr"] = df["stock_price_cagr"].apply(parse_percent)
    df["roe"] = df["roe"].apply(parse_percent)

    print("Cleaned fact_analysis preview:")
    print(df.head())

    insert_sql = text(
        """
        INSERT INTO fact_analysis (
            company_id,
            compounded_sales_growth,
            compounded_profit_growth,
            stock_price_cagr,
            roe
        )
        VALUES (
            :company_id,
            :compounded_sales_growth,
            :compounded_profit_growth,
            :stock_price_cagr,
            :roe
        )
        """
    )

    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(insert_sql, {
                "company_id": row["company_id"],
                "compounded_sales_growth": row["compounded_sales_growth"],
                "compounded_profit_growth": row["compounded_profit_growth"],
                "stock_price_cagr": row["stock_price_cagr"],
                "roe": row["roe"],
            })

    print("fact_analysis insert complete.")


def load_fact_pros_cons(engine, clean_dir: Path):
    print("=== Loading fact_pros_cons from CSV ===")
    df = pd.read_csv(clean_dir / "fact_pros_cons.csv")
    print("Rows in CSV:", len(df))

    insert_sql = text(
        """
        INSERT INTO fact_pros_cons (
            company_id,
            pros,
            cons
        )
        VALUES (
            :company_id,
            :pros,
            :cons
        )
        """
    )

    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(insert_sql, {
                "company_id": row["company_id"],
                "pros": row["pros"],
                "cons": row["cons"],
            })

    print("fact_pros_cons insert complete.")

def load_fact_documents(engine, clean_dir: Path):
    print("=== Loading fact_documents from CSV ===")

    possible_files = [
        clean_dir / "fact_documents.csv",
        clean_dir / "fact_document.csv",
        clean_dir / "documents.csv",
        clean_dir / "document.csv",
    ]

    file_path = None
    for f in possible_files:
        if f.exists():
            file_path = f
            break

    if file_path is None:
        print("Available CSV files in clean dir:")
        for f in clean_dir.iterdir():
            if f.is_file() and f.suffix.lower() == ".csv":
                print(" -", f.name)
        raise FileNotFoundError("Could not find the documents CSV file in clean_dir")

    print("Reading file:", file_path.name)
    df = pd.read_csv(file_path)
    print("Rows in CSV:", len(df))

    if "year" in df.columns:
        bad_years = df[df["year"].isna()]
        if not bad_years.empty:
            print("Rows with NaN year in documents (will keep as null in DB):")
            print(bad_years[["company_id", "year"]])

    insert_sql = text(
        """
        INSERT INTO fact_documents (
            company_id,
            year,
            annual_report
        )
        VALUES (
            :company_id,
            :year,
            :annual_report
        )
        """
    )

    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(insert_sql, {
                "company_id": row["company_id"],
                "year": None if pd.isna(row["year"]) else int(row["year"]),
                "annual_report": row["annual_report"],
            })

    print("fact_documents insert complete.")


def main():
    print("Starting 03_load_to_warehouse.py")
    base_dir = Path(__file__).resolve().parent
    clean_dir = base_dir / "data" / "clean"
    print("Clean dir:", clean_dir)

    engine = get_engine()

    load_dim_company(engine, clean_dir)
    load_fact_balance_sheet(engine, clean_dir)
    load_fact_profit_loss(engine, clean_dir)
    load_fact_cash_flow(engine, clean_dir)
    load_fact_analysis(engine, clean_dir)
    load_fact_pros_cons(engine, clean_dir)
    load_fact_documents(engine, clean_dir)

    print("All done.")


if __name__ == "__main__":
    main()