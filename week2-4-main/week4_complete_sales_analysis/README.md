# Week 4 — Complete Sales Data Analysis

A beginner-friendly end-to-end data analysis project using **pandas** and **Matplotlib**. It loads the supplied CSV, validates and cleans the data, calculates metrics, generates charts, and writes a Markdown report.

## Project overview
The goal is to understand sales performance by product and region using numerical summaries and visualizations.

## Project structure
```text
week4_complete_sales_analysis/
├── README.md
├── main.py
├── requirements.txt
├── data/
│   └── sales_data.csv
├── visualizations/
│   ├── sales_by_product.png
│   ├── sales_by_region.png
│   └── monthly_sales_trend.png  # created if usable dates exist
└── report/
    └── analysis_report.md
```

## Requirements
- Python 3.9 or newer
- pandas
- Matplotlib

## Setup and run
1. Install Python from https://www.python.org/downloads/.
2. Open a terminal in this project folder.
3. Install packages: `python -m pip install -r requirements.txt`
4. Run: `python main.py`
5. Read `report/analysis_report.md` and open the charts in `visualizations/`.

## Analysis pipeline
1. **Load:** read `data/sales_data.csv` using `pandas.read_csv`.
2. **Validate:** confirm the required columns exist.
3. **Clean:** trim text, convert numeric columns, remove duplicates, recalculate missing sales from quantity × price when possible, and remove rows that cannot support reliable analysis.
4. **Analyze:** calculate total, average, maximum and minimum sales; aggregate revenue and quantity by product and revenue by region.
5. **Visualize:** generate a bar chart and a pie chart, plus a monthly line chart if valid dates are present.
6. **Report:** save key metrics, tables, insights, and chart references to `report/analysis_report.md`.

## Main functions
- `load_and_clean_data(file_path)`: validates and cleans source data.
- `analyze_data(df)`: calculates metrics and grouped summaries.
- `create_charts(df, metrics)`: creates and saves charts.
- `write_report(df, metrics, cleaning)`: generates the Markdown report.
- `main()`: runs the full workflow and handles common input errors.

## Findings from the supplied dataset
Run `python main.py` to generate the report and obtain current findings from the CSV included in this repository. The report includes total revenue, average sale, highest and lowest sale, best product, top region, and grouped tables.

## Testing evidence
- Run the script and confirm it exits successfully and creates the report and at least two chart images.
- Check that the product and region totals reconcile to the total revenue.
- Try a copy of the CSV with a missing required column or a missing file to verify error handling.
- Try a copy with duplicate rows or missing values to inspect cleaning behaviour.

## Notes
The supplied dataset is the source of truth. Conclusions are descriptive and should not be interpreted as proof of cause or as a forecast.
