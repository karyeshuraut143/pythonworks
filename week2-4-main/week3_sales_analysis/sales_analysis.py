"""
Sales Data Analysis — Week 3
Loads sales_data.csv, cleans the data, calculates metrics, and writes analysis_report.md.
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "sales_data.csv"
REPORT_FILE = BASE_DIR / "analysis_report.md"


def load_and_clean_data(file_path):
    """Load the CSV, standardise values, handle missing values, and remove duplicates."""
    df = pd.read_csv(file_path)

    # Remove duplicate records so they do not inflate sales metrics.
    duplicates_removed = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()

    # Clean text columns by trimming accidental spaces.
    for column in ["Product", "Customer_ID", "Region"]:
        if column in df.columns:
            df[column] = df[column].astype("string").str.strip()

    # Convert expected numeric columns safely; invalid values become missing.
    for column in ["Quantity", "Price", "Total_Sales"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    # Parse dates when the Date column exists.
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # If Total_Sales is missing but Quantity and Price exist, calculate it.
    if {"Total_Sales", "Quantity", "Price"}.issubset(df.columns):
        missing_sales = df["Total_Sales"].isna()
        df.loc[missing_sales, "Total_Sales"] = (
            df.loc[missing_sales, "Quantity"] * df.loc[missing_sales, "Price"]
        )

    # Fill remaining numeric gaps with the column median; text gaps with "Unknown".
    # Date gaps are left as NaT because guessing a date would be misleading.
    for column in ["Quantity", "Price", "Total_Sales"]:
        if column in df.columns and df[column].isna().any():
            median_value = df[column].median()
            df[column] = df[column].fillna(median_value)

    for column in ["Product", "Customer_ID", "Region"]:
        if column in df.columns:
            df[column] = df[column].fillna("Unknown")

    # Only keep rows that have the fields required to calculate sales.
    required = [c for c in ["Product", "Quantity", "Price", "Total_Sales"] if c in df.columns]
    rows_before_required_filter = len(df)
    df = df.dropna(subset=required).copy()
    rows_dropped = rows_before_required_filter - len(df)

    return df, duplicates_removed, rows_dropped


def build_report(df, duplicates_removed, rows_dropped):
    """Calculate key metrics and return a Markdown report."""
    total_revenue = float(df["Total_Sales"].sum())
    average_sale = float(df["Total_Sales"].mean())
    highest_sale = float(df["Total_Sales"].max())
    lowest_sale = float(df["Total_Sales"].min())

    product_revenue = df.groupby("Product", dropna=False)["Total_Sales"].sum().sort_values(ascending=False)
    product_quantity = df.groupby("Product", dropna=False)["Quantity"].sum().sort_values(ascending=False)
    region_revenue = df.groupby("Region", dropna=False)["Total_Sales"].sum().sort_values(ascending=False)

    best_product = str(product_revenue.index[0]) if not product_revenue.empty else "N/A"
    best_product_revenue = float(product_revenue.iloc[0]) if not product_revenue.empty else 0
    best_quantity_product = str(product_quantity.index[0]) if not product_quantity.empty else "N/A"
    best_region = str(region_revenue.index[0]) if not region_revenue.empty else "N/A"

    missing_after_cleaning = int(df.isna().sum().sum())
    lines = [
        "# Sales Data Analysis Report",
        "",
        "## Project overview",
        "This report analyses the supplied sales CSV with pandas to summarise revenue, product performance, and regional performance.",
        "",
        "## Data preparation",
        f"- Rows analysed after cleaning: **{len(df)}**",
        f"- Columns in source dataset: **{len(df.columns)}**",
        f"- Duplicate rows removed: **{duplicates_removed}**",
        f"- Rows dropped because required sales fields were unavailable: **{rows_dropped}**",
        f"- Missing cells remaining in cleaned data: **{missing_after_cleaning}**",
        "- Text values were trimmed. Numeric fields were converted safely. Missing `Total_Sales` values are calculated from `Quantity × Price` where possible; remaining numeric gaps use the median, and missing categorical values are labelled `Unknown`.",
        "",
        "## Key metrics",
        f"- **Total revenue:** ₹{total_revenue:,.2f}",
        f"- **Average sale per row:** ₹{average_sale:,.2f}",
        f"- **Highest single-row sale:** ₹{highest_sale:,.2f}",
        f"- **Lowest single-row sale:** ₹{lowest_sale:,.2f}",
        f"- **Best-selling product by revenue:** {best_product} (₹{best_product_revenue:,.2f})",
        f"- **Product with the highest total quantity:** {best_quantity_product}",
        f"- **Highest-revenue region:** {best_region}",
        "",
        "## Revenue by product",
        "| Product | Revenue | Units sold |",
        "|---|---:|---:|",
    ]
    for product in product_revenue.index:
        revenue = float(product_revenue.loc[product])
        qty = float(product_quantity.get(product, 0))
        lines.append(f"| {product} | ₹{revenue:,.2f} | {qty:,.0f} |")

    lines += [
        "",
        "## Revenue by region",
        "| Region | Revenue |",
        "|---|---:|",
    ]
    for region, revenue in region_revenue.items():
        lines.append(f"| {region} | ₹{float(revenue):,.2f} |")

    lines += [
        "",
        "## Insights",
        f"- {best_product} contributes the most revenue among the products in this dataset.",
        f"- {best_quantity_product} has the highest total units sold.",
        f"- {best_region} is the strongest region by total revenue.",
        "",
        "## How to run",
        "1. Install Python 3.9 or newer.",
        "2. Install dependencies with `python -m pip install -r requirements.txt`.",
        "3. Keep `sales_analysis.py` and `sales_data.csv` in the same folder.",
        "4. Run `python sales_analysis.py`.",
        "",
        "## Technical details",
        "- `pandas.read_csv()` loads the CSV into a DataFrame.",
        "- `drop_duplicates()` removes exact duplicate records.",
        "- `to_numeric()` and `to_datetime()` standardise data types.",
        "- `groupby()` and `sum()` aggregate revenue and quantity by product and region.",
        "- The script writes this report to `analysis_report.md` each time it runs.",
        "",
        "## Testing evidence",
        "- Confirm the report is created after running the script.",
        "- Check total revenue against the sum of the cleaned `Total_Sales` column.",
        "- Check that product and region revenue tables add up to total revenue (subject to any cleaned rows).",
        "- Test a copy of the CSV with a duplicate row, blank value, and non-numeric value to observe cleaning behaviour.",
        "",
        "## Limitations",
        "The report describes the supplied dataset only. It does not establish future sales trends or explain why products perform differently.",
        "",
    ]
    return "\n".join(lines)


def main():
    df, duplicates_removed, rows_dropped = load_and_clean_data(DATA_FILE)
    if df.empty:
        raise ValueError("No usable rows remain after cleaning. Check sales_data.csv.")
    report = build_report(df, duplicates_removed, rows_dropped)
    REPORT_FILE.write_text(report, encoding="utf-8")
    print("SALES DATA ANALYSIS")
    print("=" * 45)
    print(f"Rows analysed: {len(df)}")
    print(f"Total revenue: ₹{df['Total_Sales'].sum():,.2f}")
    print(f"Average sale: ₹{df['Total_Sales'].mean():,.2f}")
    print(f"Best-selling product by revenue: {df.groupby('Product')['Total_Sales'].sum().idxmax()}")
    print(f"Report saved to: {REPORT_FILE.name}")


if __name__ == "__main__":
    main()
