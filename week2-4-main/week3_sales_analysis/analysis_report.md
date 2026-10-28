# Sales Data Analysis Report

## Project overview
This report analyses the supplied sales CSV with pandas to summarise revenue, product performance, and regional performance.

## Data preparation
- Rows analysed after cleaning: **100**
- Columns in source dataset: **7**
- Duplicate rows removed: **0**
- Rows dropped because required sales fields were unavailable: **0**
- Missing cells remaining in cleaned data: **0**
- Text values were trimmed. Numeric fields were converted safely. Missing `Total_Sales` values are calculated from `Quantity × Price` where possible; remaining numeric gaps use the median, and missing categorical values are labelled `Unknown`.

## Key metrics
- **Total revenue:** ₹12,365,048.00
- **Average sale per row:** ₹123,650.48
- **Highest single-row sale:** ₹373,932.00
- **Lowest single-row sale:** ₹6,540.00
- **Best-selling product by revenue:** Laptop (₹3,889,210.00)
- **Product with the highest total quantity:** Laptop
- **Highest-revenue region:** North

## Revenue by product
| Product | Revenue | Units sold |
|---|---:|---:|
| Laptop | ₹3,889,210.00 | 136 |
| Tablet | ₹2,884,340.00 | 127 |
| Phone | ₹2,859,394.00 | 101 |
| Headphones | ₹1,384,033.00 | 48 |
| Monitor | ₹1,348,071.00 | 66 |

## Revenue by region
| Region | Revenue |
|---|---:|
| North | ₹3,983,635.00 |
| South | ₹3,737,852.00 |
| East | ₹2,519,639.00 |
| West | ₹2,123,922.00 |

## Insights
- Laptop contributes the most revenue among the products in this dataset.
- Laptop has the highest total units sold.
- North is the strongest region by total revenue.

## How to run
1. Install Python 3.9 or newer.
2. Install dependencies with `python -m pip install -r requirements.txt`.
3. Keep `sales_analysis.py` and `sales_data.csv` in the same folder.
4. Run `python sales_analysis.py`.

## Technical details
- `pandas.read_csv()` loads the CSV into a DataFrame.
- `drop_duplicates()` removes exact duplicate records.
- `to_numeric()` and `to_datetime()` standardise data types.
- `groupby()` and `sum()` aggregate revenue and quantity by product and region.
- The script writes this report to `analysis_report.md` each time it runs.

## Testing evidence
- Confirm the report is created after running the script.
- Check total revenue against the sum of the cleaned `Total_Sales` column.
- Check that product and region revenue tables add up to total revenue (subject to any cleaned rows).
- Test a copy of the CSV with a duplicate row, blank value, and non-numeric value to observe cleaning behaviour.

## Limitations
The report describes the supplied dataset only. It does not establish future sales trends or explain why products perform differently.
