import pandas as pd
import numpy as np


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    for col in ["Sales", "Discount", "Profit"]:
        df[col] = df[col].astype(str).str.replace(",", ".").astype(float)

    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d/%m/%Y", errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%d/%m/%Y", errors="coerce")

    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Month Name"] = df["Order Date"].dt.strftime("%b")
    df["Year-Month"] = df["Order Date"].dt.to_period("M").astype(str)

    df = df.dropna(subset=["Order Date", "Sales"])
    df = df[df["Sales"] > 0]

    return df


def apply_filters(
    df: pd.DataFrame,
    year_range=None,
    regions=None,
    states=None,
    cities=None,
    segments=None,
    categories=None,
    subcategories=None,
) -> pd.DataFrame:
    if year_range and len(year_range) == 2:
        df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]
    if regions:
        df = df[df["Region"].isin(regions)]
    if states:
        df = df[df["State"].isin(states)]
    if cities:
        df = df[df["City"].isin(cities)]
    if segments:
        df = df[df["Segment"].isin(segments)]
    if categories:
        df = df[df["Category"].isin(categories)]
    if subcategories:
        df = df[df["Sub-Category"].isin(subcategories)]
    return df


def get_data_quality_report(df_raw: pd.DataFrame) -> dict:
    total = len(df_raw)
    nulls = df_raw.isnull().sum()
    nulls = nulls[nulls > 0].to_dict()
    return {"total_rows": total, "nulls_per_column": nulls}


# ── Q1 ──────────────────────────────────────────────────────────────────────
def q1_city_office_supplies(df: pd.DataFrame) -> pd.DataFrame:
    result = (
        df[df["Category"] == "Office Supplies"]
        .groupby("City", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .reset_index(drop=True)
    )
    result["Sales"] = result["Sales"].round(2)
    return result


# ── Q2 ──────────────────────────────────────────────────────────────────────
def q2_sales_by_date(df: pd.DataFrame) -> pd.DataFrame:
    result = (
        df.groupby("Year-Month", as_index=False)["Sales"]
        .sum()
        .sort_values("Year-Month")
    )
    result["Sales"] = result["Sales"].round(2)
    return result


# ── Q3 ──────────────────────────────────────────────────────────────────────
def q3_sales_by_state(df: pd.DataFrame) -> pd.DataFrame:
    result = (
        df.groupby("State", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .reset_index(drop=True)
    )
    result["Sales"] = result["Sales"].round(2)
    return result


# ── Q4 ──────────────────────────────────────────────────────────────────────
def q4_top_cities(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    result = (
        df.groupby("City", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
    result["Sales"] = result["Sales"].round(2)
    return result


# ── Q5 ──────────────────────────────────────────────────────────────────────
def q5_sales_by_segment(df: pd.DataFrame) -> pd.DataFrame:
    result = (
        df.groupby("Segment", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )
    result["Sales"] = result["Sales"].round(2)
    result["Percentual"] = (result["Sales"] / result["Sales"].sum() * 100).round(1)
    return result


# ── Q6 ──────────────────────────────────────────────────────────────────────
def q6_sales_by_segment_year(df: pd.DataFrame) -> pd.DataFrame:
    result = (
        df.groupby(["Segment", "Year"], as_index=False)["Sales"]
        .sum()
        .sort_values(["Year", "Segment"])
    )
    result["Sales"] = result["Sales"].round(2)
    return result


def q6_pivot(df: pd.DataFrame) -> pd.DataFrame:
    data = q6_sales_by_segment_year(df)
    pivot = data.pivot(index="Segment", columns="Year", values="Sales").fillna(0)
    pivot.columns = [str(c) for c in pivot.columns]
    return pivot.round(2)


# ── Q7 ──────────────────────────────────────────────────────────────────────
def q7_discount_simulation(df: pd.DataFrame, threshold: float = 1000.0) -> dict:
    total = len(df)
    count_high = int((df["Sales"] > threshold).sum())
    count_low = total - count_high
    pct = round(count_high / total * 100, 1) if total > 0 else 0
    return {
        "total_orders": total,
        "count_15pct": count_high,
        "count_10pct": count_low,
        "pct_15pct": pct,
        "threshold": threshold,
    }


# ── Q8 ──────────────────────────────────────────────────────────────────────
def q8_avg_before_after(
    df: pd.DataFrame,
    threshold: float = 1000.0,
    rate_high: float = 0.15,
    rate_low: float = 0.10,
) -> dict:
    avg_before = df["Sales"].mean()
    sales_after = np.where(
        df["Sales"] > threshold,
        df["Sales"] * (1 - rate_high),
        df["Sales"] * (1 - rate_low),
    )
    avg_after = sales_after.mean()
    delta = avg_after - avg_before
    delta_pct = (delta / avg_before * 100) if avg_before > 0 else 0
    return {
        "avg_before": round(avg_before, 2),
        "avg_after": round(avg_after, 2),
        "delta": round(delta, 2),
        "delta_pct": round(delta_pct, 2),
    }


# ── Q9 ──────────────────────────────────────────────────────────────────────
def q9_avg_by_segment_year_month(df: pd.DataFrame) -> pd.DataFrame:
    month_order = {1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai",
                   6: "Jun", 7: "Jul", 8: "Ago", 9: "Set", 10: "Out",
                   11: "Nov", 12: "Dez"}
    result = (
        df.groupby(["Segment", "Year", "Month"], as_index=False)["Sales"]
        .mean()
        .sort_values(["Year", "Month"])
    )
    result["Sales"] = result["Sales"].round(2)
    result["Month Name"] = result["Month"].map(month_order)
    result["Period"] = result["Year"].astype(str) + "-" + result["Month"].astype(str).str.zfill(2)
    return result


# ── Q10 ─────────────────────────────────────────────────────────────────────
def q10_sales_by_category_subcat(df: pd.DataFrame, top_n: int = 12) -> pd.DataFrame:
    top_subcats = (
        df.groupby("Sub-Category")["Sales"]
        .sum()
        .nlargest(top_n)
        .index.tolist()
    )
    result = (
        df[df["Sub-Category"].isin(top_subcats)]
        .groupby(["Category", "Sub-Category"], as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )
    result["Sales"] = result["Sales"].round(2)
    return result
