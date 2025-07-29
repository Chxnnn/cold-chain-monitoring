# Cold Chain Monitoring System – Snowflake + Tableau

## 🔍 Problem
Pharma cold chain containers must be kept between 2°C–8°C. Any excursion = risk.

## 💡 Solution
Simulated cold chain data → Stored in Snowflake → Analyzed with SQL → Visualized in Tableau

## 📦 Tech Stack
- Python, Pandas
- Snowflake Cloud Warehouse
- Tableau Public
- VS Code Snowflake Extension

## 🛠 How to Run
1. Run `data/cold_chain_data_generator.py` to generate data
2. Use `snowflake/01_create_table.sql` in VS Code (Snowflake extension)
3. Load data using `snowflake/03_load_data_snowflake.py`
4. Explore using `snowflake/02_analysis_queries.sql`
5. Build dashboard in Tableau
