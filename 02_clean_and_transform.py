import pandas as pd
from pathlib import Path
import re


def load_raw_excels(raw_dir: Path):
    companies_df     = pd.read_excel(raw_dir / "companies.xlsx",     header=1)
    balancesheet_df  = pd.read_excel(raw_dir / "balancesheet.xlsx",  header=1)
    profitandloss_df = pd.read_excel(raw_dir / "profitandloss.xlsx", header=1)
    cashflow_df      = pd.read_excel(raw_dir / "cashflow.xlsx",      header=1)
    analysis_df      = pd.read_excel(raw_dir / "analysis.xlsx",      header=1)
    prosandcons_df   = pd.read_excel(raw_dir / "prosandcons.xlsx",   header=1)
    documents_df     = pd.read_excel(raw_dir / "documents.xlsx",     header=1)

    return {
        "companies": companies_df,
        "balancesheet": balancesheet_df,
        "profitandloss": profitandloss_df,
        "cashflow": cashflow_df,
        "analysis": analysis_df,
        "prosandcons": prosandcons_df,
        "documents": documents_df,
    }


def build_dim_company(companies_df: pd.DataFrame) -> pd.DataFrame:
    companies_clean = companies_df.copy()
    companies_clean.columns = (
        companies_clean.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    dim_company = companies_clean[[
        "id",
        "company_name",
        "about_company",
        "website",
        "nse_profile",
        "bse_profile",
        "face_value",
        "book_value",
        "roce_percentage",
        "roe_percentage",
    ]].copy()

    dim_company = dim_company.rename(columns={"id": "company_id"})
    dim_company["company_id"] = dim_company["company_id"].astype(str).str.strip()

    return dim_company


def build_fact_balance_sheet(balancesheet_df: pd.DataFrame) -> pd.DataFrame:
    df = balancesheet_df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    df["company_id"] = df["company_id"].astype(str).str.strip()
    df["year"] = df["year"].astype(str).str.strip()

    df["fiscal_year"] = (
        df["year"]
        .str.extract(r"(\d{4})", expand=False)
        .astype(int)
    )

    fact = df[[
        "company_id",
        "fiscal_year",
        "equity_capital",
        "reserves",
        "borrowings",
        "other_liabilities",
        "total_liabilities",
        "fixed_assets",
        "cwip",
        "investments",
        "other_asset",
        "total_assets",
    ]].copy()

    fact["debt_to_equity"] = fact["borrowings"] / fact["equity_capital"]
    fact["equity_ratio"] = (
        (fact["equity_capital"] + fact["reserves"]) / fact["total_assets"]
    )

    return fact


def build_fact_profit_loss(profitandloss_df: pd.DataFrame) -> pd.DataFrame:
    df = profitandloss_df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    df["company_id"] = df["company_id"].astype(str).str.strip()
    df["year"] = df["year"].astype(str).str.strip()

    df["fiscal_year"] = (
        df["year"]
        .str.extract(r"(\d{4})", expand=False)
    ).astype("float")

    fact = df[[
        "company_id",
        "fiscal_year",
        "sales",
        "expenses",
        "operating_profit",
        "opm_percentage",
        "other_income",
        "interest",
        "depreciation",
        "profit_before_tax",
        "tax_percentage",
        "net_profit",
        "eps",
        "dividend_payout",
    ]].copy()

    fact["net_margin"] = fact["net_profit"] / fact["sales"]
    fact["operating_margin"] = fact["operating_profit"] / fact["sales"]

    return fact


def build_fact_cash_flow(cashflow_df: pd.DataFrame) -> pd.DataFrame:
    df = cashflow_df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    df["company_id"] = df["company_id"].astype(str).str.strip()
    df["year"] = df["year"].astype(str).str.strip()

    df["fiscal_year"] = (
        df["year"]
        .str.extract(r"(\d{4})", expand=False)
    ).astype("float")

    fact = df[[
        "company_id",
        "fiscal_year",
        "operating_activity",
        "investing_activity",
        "financing_activity",
        "net_cash_flow",
    ]].copy()

    fact["free_cash_flow"] = (
        fact["operating_activity"] - fact["investing_activity"]
    )

    return fact


def build_fact_analysis(analysis_df: pd.DataFrame) -> pd.DataFrame:
    df = analysis_df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    df["company_id"] = df["company_id"].astype(str).str.strip()
    return df


def build_fact_pros_cons(prosandcons_df: pd.DataFrame) -> pd.DataFrame:
    df = prosandcons_df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    df["company_id"] = df["company_id"].astype(str).str.strip()
    return df


def build_documents(documents_df: pd.DataFrame) -> pd.DataFrame:
    df = documents_df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    df["company_id"] = df["company_id"].astype(str).str.strip()
    return df


def main():
    base_dir = Path(__file__).resolve().parent      # <-- now base_dir = F:\etl
    raw_dir = base_dir / "data" / "raw"
    clean_dir = base_dir / "data" / "clean"
    clean_dir.mkdir(parents=True, exist_ok=True)

    dfs = load_raw_excels(raw_dir)

    dim_company = build_dim_company(dfs["companies"])
    fact_balance_sheet = build_fact_balance_sheet(dfs["balancesheet"])
    fact_profit_loss = build_fact_profit_loss(dfs["profitandloss"])
    fact_cash_flow = build_fact_cash_flow(dfs["cashflow"])
    fact_analysis = build_fact_analysis(dfs["analysis"])
    fact_pros_cons = build_fact_pros_cons(dfs["prosandcons"])
    documents_clean = build_documents(dfs["documents"])

    dim_company.to_csv(clean_dir / "dim_company.csv", index=False)
    fact_balance_sheet.to_csv(clean_dir / "fact_balance_sheet.csv", index=False)
    fact_profit_loss.to_csv(clean_dir / "fact_profit_loss.csv", index=False)
    fact_cash_flow.to_csv(clean_dir / "fact_cash_flow.csv", index=False)
    fact_analysis.to_csv(clean_dir / "fact_analysis.csv", index=False)
    fact_pros_cons.to_csv(clean_dir / "fact_pros_cons.csv", index=False)
    documents_clean.to_csv(clean_dir / "documents.csv", index=False)

    print("Cleaned CSVs written to", clean_dir)


if __name__ == "__main__":
    main()