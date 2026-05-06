import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CLEAN_DIR = BASE_DIR / "data" / "clean"
PROCESSED_DIR = CLEAN_DIR / "processed"
OUTPUT_FILE = PROCESSED_DIR / "company_health_scores.csv"


def min_max_0_100(series: pd.Series) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")
    min_val = s.min()
    max_val = s.max()

    if pd.isna(min_val) or pd.isna(max_val) or max_val == min_val:
        return pd.Series([50.0] * len(series), index=series.index)

    return ((s - min_val) / (max_val - min_val) * 100).round(2)


def assign_health_label(score: float) -> str:
    if pd.isna(score):
        return "UNKNOWN"
    if score >= 85:
        return "EXCELLENT"
    elif score >= 70:
        return "GOOD"
    elif score >= 50:
        return "AVERAGE"
    elif score >= 35:
        return "WEAK"
    else:
        return "POOR"


def load_csv(name: str) -> pd.DataFrame:
    path = CLEAN_DIR / name
    print(f"Loading {name} from: {path}")
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    return df


def main():
    print("Base dir:", BASE_DIR)

    # 1) dim_company (id + name)
    dim_company = load_csv("dim_company.csv")

    if "company_id" not in dim_company.columns:
        raise ValueError("dim_company.csv must have 'company_id' column")

    dim_company["company_id"] = pd.to_numeric(
        dim_company["company_id"], errors="coerce"
    )

    name_col = "company_name" if "company_name" in dim_company.columns else "name"

    base = dim_company[["company_id", name_col]].copy()

    # 2) fact_analysis: revenue and net profit CAGR, growth stability etc.
    fact_analysis = load_csv("fact_analysis.csv")

    for col in ["company_id"]:
        if col not in fact_analysis.columns:
            raise ValueError(f"fact_analysis.csv must have '{col}' column")

    fact_analysis["company_id"] = pd.to_numeric(
        fact_analysis["company_id"], errors="coerce"
    )

    # TODO: adjust these column names to match your file header
    col_revenue_cagr = "revenue_cagr_5y"
    col_net_profit_cagr = "net_profit_cagr_5y"
    col_growth_stability = "growth_stability"

    analysis_cols = ["company_id"]
    for col in [col_revenue_cagr, col_net_profit_cagr, col_growth_stability]:
        if col in fact_analysis.columns:
            analysis_cols.append(col)
        else:
            print(f"WARNING: column '{col}' not found in fact_analysis.csv")

    fact_analysis = fact_analysis[analysis_cols]

    base = base.merge(fact_analysis, on="company_id", how="left")

    # 3) fact_profit_loss: avg operating margin (avg_opm_5y?)
    fact_profit = load_csv("fact_profit_loss.csv")
    fact_profit["company_id"] = pd.to_numeric(
        fact_profit["company_id"], errors="coerce"
    )

    # TODO: adjust this column name
    col_avg_opm = "avg_opm_5y"

    profit_cols = ["company_id"]
    if col_avg_opm in fact_profit.columns:
        profit_cols.append(col_avg_opm)
    else:
        print(f"WARNING: column '{col_avg_opm}' not found in fact_profit_loss.csv")

    fact_profit = fact_profit[profit_cols]

    base = base.merge(fact_profit, on="company_id", how="left")

    # 4) fact_balance_sheet: leverage (de_ratio_latest)
    fact_balance = load_csv("fact_balance_sheet.csv")
    fact_balance["company_id"] = pd.to_numeric(
        fact_balance["company_id"], errors="coerce"
    )

    # TODO: adjust this column name
    col_de_ratio = "de_ratio_latest"

    balance_cols = ["company_id"]
    if col_de_ratio in fact_balance.columns:
        balance_cols.append(col_de_ratio)
    else:
        print(f"WARNING: column '{col_de_ratio}' not found in fact_balance_sheet.csv")

    fact_balance = fact_balance[balance_cols]

    base = base.merge(fact_balance, on="company_id", how="left")

    # 5) fact_cash_flow: cash_conversion_5y
    fact_cash = load_csv("fact_cash_flow.csv")
    fact_cash["company_id"] = pd.to_numeric(
        fact_cash["company_id"], errors="coerce"
    )

    # TODO: adjust this column name
    col_cash_conv = "cash_conversion_5y"

    cash_cols = ["company_id"]
    if col_cash_conv in fact_cash.columns:
        cash_cols.append(col_cash_conv)
    else:
        print(f"WARNING: column '{col_cash_conv}' not found in fact_cash_flow.csv")

    fact_cash = fact_cash[cash_cols]

    base = base.merge(fact_cash, on="company_id", how="left")

    # 6) fact_pros_cons or documents: dividend_consistency
    # (guessing from your file list: fact_pros_cons.csv)
    fact_pros = load_csv("fact_pros_cons.csv")
    fact_pros["company_id"] = pd.to_numeric(
        fact_pros["company_id"], errors="coerce"
    )

    # TODO: adjust this column name
    col_div_cons = "dividend_consistency"

    pros_cols = ["company_id"]
    if col_div_cons in fact_pros.columns:
        pros_cols.append(col_div_cons)
    else:
        print(f"WARNING: column '{col_div_cons}' not found in fact_pros_cons.csv")

    fact_pros = fact_pros[pros_cols]

    base = base.merge(fact_pros, on="company_id", how="left")

    # Now base has: company_id, name_col, and the 7 feature columns (with whatever names exist).

    # Standardize column names we expect for scoring
    base = base.rename(
        columns={
            col_avg_opm: "avg_opm_5y",
            col_revenue_cagr: "revenue_cagr_5y",
            col_net_profit_cagr: "net_profit_cagr_5y",
            col_de_ratio: "de_ratio_latest",
            col_cash_conv: "cash_conversion_5y",
            col_div_cons: "dividend_consistency",
            col_growth_stability: "growth_stability",
        }
    )

    # Convert to numeric
    for col in [
        "avg_opm_5y",
        "revenue_cagr_5y",
        "net_profit_cagr_5y",
        "de_ratio_latest",
        "cash_conversion_5y",
        "dividend_consistency",
        "growth_stability",
    ]:
        if col in base.columns:
            base[col] = pd.to_numeric(base[col], errors="coerce")

    # Scores
    base["score_profitability"] = min_max_0_100(base.get("avg_opm_5y"))

    base["score_growth"] = min_max_0_100(
        0.5 * base.get("revenue_cagr_5y")
        + 0.5 * base.get("net_profit_cagr_5y")
    )

    base["score_leverage"] = 100 - min_max_0_100(base.get("de_ratio_latest"))

    base["score_cashflow"] = min_max_0_100(base.get("cash_conversion_5y"))

    base["score_dividend"] = min_max_0_100(base.get("dividend_consistency"))

    base["score_growth_trend"] = min_max_0_100(base.get("growth_stability"))

    base["health_score"] = (
        0.25 * base["score_profitability"]
        + 0.20 * base["score_growth"]
        + 0.20 * base["score_leverage"]
        + 0.15 * base["score_cashflow"]
        + 0.10 * base["score_dividend"]
        + 0.10 * base["score_growth_trend"]
    ).round(2)

    base["health_label"] = base["health_score"].apply(assign_health_label)

    output_cols = [
        "company_id",
        name_col,
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

    df_output = base[output_cols].rename(columns={name_col: "company_name"})
    df_output = df_output.sort_values("health_score", ascending=False)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df_output.to_csv(OUTPUT_FILE, index=False)

    print("\nHealth score calculation complete.")
    print("Output saved to:", OUTPUT_FILE)
    print(df_output.head(10))


if __name__ == "__main__":
    main()