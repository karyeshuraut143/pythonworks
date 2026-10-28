"""
Week 4 — Complete Sales Data Analysis Project
Pipeline: load -> clean -> analyze -> visualize -> report.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "sales_data.csv"
CHART_DIR = BASE_DIR / "visualizations"
REPORT_DIR = BASE_DIR / "report"
REPORT_FILE = REPORT_DIR / "analysis_report.md"

REQUIRED_COLUMNS = {"Product", "Quantity", "Price", "Total_Sales", "Region"}


def load_and_clean_data(file_path):
    """Load CSV, validate required columns, clean values, and remove duplicates."""
    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}. Put sales_data.csv inside the data folder."
        )

    df = pd.read_csv(file_path)
    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {', '.join(sorted(missing_columns))}")

    original_rows = len(df)
    duplicates_removed = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()

    for column in ["Product", "Region"]:
        df[column] = df[column].astype("string").str.strip()
        df[column] = df[column].replace("", pd.NA).fillna("Unknown")

    for column in ["Quantity", "Price", "Total_Sales"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Recalculate missing revenue when quantity and price are available.
    missing_sales = df["Total_Sales"].isna()
    can_recalculate = missing_sales & df["Quantity"].notna() & df["Price"].notna()
    df.loc[can_recalculate, "Total_Sales"] = (
        df.loc[can_recalculate, "Quantity"] * df.loc[can_recalculate, "Price"]
    )

    # Remove rows that cannot support reliable revenue analysis.
    before_drop = len(df)
    df = df.dropna(subset=["Product", "Quantity", "Price", "Total_Sales", "Region"]).copy()
    rows_dropped = before_drop - len(df)

    if df.empty:
        raise ValueError("No valid rows remain after cleaning. Please check the CSV data.")
    if (df[["Quantity", "Price", "Total_Sales"]] < 0).any().any():
        raise ValueError("Negative quantity, price, or sales values were found. Please verify the dataset.")

    cleaning_summary = {
        "original_rows": original_rows,
        "duplicates_removed": duplicates_removed,
        "rows_dropped": rows_dropped,
        "rows_analyzed": len(df),
        "missing_values_after_cleaning": int(df.isna().sum().sum()),
    }
    return df, cleaning_summary


def analyze_data(df):
    """Calculate summary metrics and aggregate sales by product, month, and region."""
    product_sales = df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)
    product_quantity = df.groupby("Product")["Quantity"].sum().sort_values(ascending=False)
    region_sales = df.groupby("Region")["Total_Sales"].sum().sort_values(ascending=False)
    total_revenue = float(df["Total_Sales"].sum())
    average_sale = float(df["Total_Sales"].mean())
    highest_sale = float(df["Total_Sales"].max())
    lowest_sale = float(df["Total_Sales"].min())

    monthly_sales = None
    if "Date" in df.columns:
        dates = pd.to_datetime(df["Date"], errors="coerce")
        if dates.notna().any():
            monthly_sales = df.assign(Month=dates.dt.to_period("M").astype(str))
            monthly_sales = monthly_sales[monthly_sales["Month"] != "NaT"]
            monthly_sales = monthly_sales.groupby("Month")["Total_Sales"].sum().sort_index()

    return {
        "total_revenue": total_revenue,
        "average_sale": average_sale,
        "highest_sale": highest_sale,
        "lowest_sale": lowest_sale,
        "product_sales": product_sales,
        "product_quantity": product_quantity,
        "region_sales": region_sales,
        "monthly_sales": monthly_sales,
    }


def create_charts(df, metrics):
    """Save a product bar chart and regional pie chart; add monthly line chart if dates exist."""
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    product_sales = metrics["product_sales"].sort_values(ascending=False)
    plt.figure(figsize=(9, 5.5))
    product_sales.plot(kind="bar")
    plt.title("Total Sales Revenue by Product")
    plt.xlabel("Product")
    plt.ylabel("Revenue (₹)")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "sales_by_product.png", dpi=160)
    plt.close()

    region_sales = metrics["region_sales"]
    plt.figure(figsize=(7, 7))
    region_sales.plot(kind="pie", autopct="%1.1f%%", startangle=90)
    plt.title("Revenue Share by Region")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "sales_by_region.png", dpi=160)
    plt.close()

    if metrics["monthly_sales"] is not None and not metrics["monthly_sales"].empty:
        plt.figure(figsize=(10, 5))
        metrics["monthly_sales"].plot(kind="line", marker="o")
        plt.title("Monthly Sales Revenue")
        plt.xlabel("Month")
        plt.ylabel("Revenue (₹)")
        plt.xticks(rotation=35, ha="right")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(CHART_DIR / "monthly_sales_trend.png", dpi=160)
        plt.close()


def write_report(df, metrics, cleaning):
    """Write a Markdown report with metrics, insights, and chart references."""
    best_product = str(metrics["product_sales"].idxmax())
    best_product_revenue = float(metrics["product_sales"].max())
    best_quantity_product = str(metrics["product_quantity"].idxmax())
    best_region = str(metrics["region_sales"].idxmax())

    lines = [
        "# Complete Sales Data Analysis",
        "",
        "## 1. Project overview",
        "This project uses pandas and Matplotlib to clean, analyze, and visualize the supplied sales dataset.",
        "",
        "## 2. Dataset and cleaning",
        f"- Original rows: **{cleaning['original_rows']}**",
        f"- Duplicate rows removed: **{cleaning['duplicates_removed']}**",
        f"- Rows removed due to unusable required values: **{cleaning['rows_dropped']}**",
        f"- Rows analyzed: **{cleaning['rows_analyzed']}**",
        f"- Missing cells after cleaning: **{cleaning['missing_values_after_cleaning']}**",
        "- Required columns are validated before analysis.",
        "- Text fields are trimmed; numeric fields are converted to numeric types.",
        "- Missing sales values are recalculated from quantity × price when possible.",
        "- Rows without the fields required for reliable sales analysis are removed.",
        "",
        "## 3. Key metrics",
        f"- **Total revenue:** ₹{metrics['total_revenue']:,.2f}",
        f"- **Average sale per row:** ₹{metrics['average_sale']:,.2f}",
        f"- **Highest sale:** ₹{metrics['highest_sale']:,.2f}",
        f"- **Lowest sale:** ₹{metrics['lowest_sale']:,.2f}",
        f"- **Top product by revenue:** {best_product} (₹{best_product_revenue:,.2f})",
        f"- **Top product by quantity:** {best_quantity_product}",
        f"- **Top region by revenue:** {best_region}",
        "",
        "## 4. Revenue by product",
        "| Product | Revenue | Units sold |",
        "|---|---:|---:|",
    ]
    for product, revenue in metrics["product_sales"].items():
        qty = metrics["product_quantity"].get(product, 0)
        lines.append(f"| {product} | ₹{float(revenue):,.2f} | {float(qty):,.0f} |")

    lines += ["", "## 5. Revenue by region", "", "| Region | Revenue |", "|---|---:|"]
    for region, revenue in metrics["region_sales"].items():
        lines.append(f"| {region} | ₹{float(revenue):,.2f} |")

    lines += [
        "",
        "## 6. Visualizations",
        "- ![Sales by product](../visualizations/sales_by_product.png)",
        "- ![Revenue share by region](../visualizations/sales_by_region.png)",
    ]
    if metrics["monthly_sales"] is not None and not metrics["monthly_sales"].empty:
        lines.append("- ![Monthly sales trend](../visualizations/monthly_sales_trend.png)")

    lines += [
        "",
        "## 7. Insights",
        f"1. **{best_product}** generated the highest revenue in the dataset.",
        f"2. **{best_quantity_product}** had the greatest total quantity sold.",
        f"3. **{best_region}** was the highest-revenue region.",
        "4. The product bar chart makes revenue differences easy to compare; the regional pie chart shows each region's share of total revenue.",
        "",
        "## 8. How to run",
        "1. Install Python 3.9 or newer.",
        "2. In the project directory, run `python -m pip install -r requirements.txt`.",
        "3. Run `python main.py`.",
        "4. Review `report/analysis_report.md` and the charts in `visualizations/`.",
        "",
        "## 9. Code structure",
        "- `main.py`: pipeline orchestration and error handling.",
        "- `data/sales_data.csv`: source dataset.",
        "- `visualizations/`: generated chart images.",
        "- `report/analysis_report.md`: generated written report.",
        "",
        "## 10. Testing evidence",
        "- Dataset shape and required columns are checked by the code.",
        "- Missing file and missing required columns produce clear errors.",
        "- The analysis was run on the supplied dataset; see the metrics and generated charts above.",
        "- For additional testing, try a CSV copy with duplicate rows, blank values, or an invalid numeric entry.",
        "",
        "## Limitations",
        "These findings describe only the supplied dataset and do not prove the causes of sales performance or predict future results.",
        "",
    ]
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")


def main():
    try:
        df, cleaning = load_and_clean_data(DATA_FILE)
        metrics = analyze_data(df)
        create_charts(df, metrics)
        write_report(df, metrics, cleaning)
        print("COMPLETE SALES DATA ANALYSIS")
        print("=" * 42)
        print(f"Rows analyzed: {len(df)}")
        print(f"Total revenue: ₹{metrics['total_revenue']:,.2f}")
        print(f"Best product by revenue: {metrics['product_sales'].idxmax()}")
        print(f"Charts saved in: {CHART_DIR.relative_to(BASE_DIR)}")
        print(f"Report saved to: {REPORT_FILE.relative_to(BASE_DIR)}")
    except (FileNotFoundError, ValueError, pd.errors.ParserError) as error:
        print(f"Analysis could not be completed: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
