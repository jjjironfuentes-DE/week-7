# Section E – BrewBeats Case Study

## Business Objective

The objective of this project is to build a data engineering pipeline for a coffee shop business. The pipeline processes coffee sales data to analyse revenue, transactions, product performance and purchasing patterns.

## Proposed Architecture

- **Source data:** Coffee Sales CSV.
- **Extraction and ingestion:** Python and Pandas.
- **Data storage:** Snowflake.
- **Data transformation:** SQL, dbt and Snowpark.
- **Workflow orchestration:** Apache Airflow.
- **Business intelligence:** Tableau.

## Data Pipeline Implementation

Coffee sales data is loaded into Snowflake using SQL staging and ingestion operations. dbt transforms the raw data into analytical models, including staging and daily revenue models.

Snowpark provides an additional Python-based transformation that aggregates sales by date, calculating total transactions, total revenue and average transaction value.

Apache Airflow orchestrates the workflow through two tasks: executing dbt transformations and validating the resulting daily revenue data.

## Data Validation

The Airflow DAG was successfully tested. The dbt build completed with all selected tests passing. The daily revenue model contains 381 records.

The Snowpark transformation also completed successfully and created the `SNOWPARK_DAILY_REVENUE` table with 381 daily records.

## Business Intelligence

The Tableau dashboard is intended to monitor the following business metrics:

1. Total sales revenue.
2. Total number of transactions.
3. Average transaction value.
4. Best-selling coffee.
5. Revenue by coffee type.
6. Revenue by month.
7. Sales by weekday.
8. Sales by hour.
9. Cash versus card transactions.
10. Monthly sales trends.

## Conclusion

The project demonstrates an integrated data engineering workflow using Python, Snowflake, SQL, dbt, Snowpark and Apache Airflow. The resulting analytical data supports business monitoring and coffee sales analysis through Tableau.