
# BrewBeats – Data Architecture

## 1. Project Overview

BrewBeats is a data engineering project focused on analyzing coffee shop sales data and generating business insights.

## 2. Data Sources

The project uses CSV files containing coffee sales and Spotify data.

## 3. Data Storage

Snowflake is used as the cloud data warehouse.

- Database: BREWBEATS_DB
- Raw schema: RAW
- Transformation schema: DBT_DEV

## 4. Data Transformation

dbt transforms the raw coffee sales data.

- STG_COFFEE_SALES: staging view
- DAILY_REVENUE: daily revenue mart

Data quality is checked through dbt tests.

## 5. Workflow Orchestration

Apache Airflow orchestrates the pipeline.

1. run_dbt: executes dbt transformations and tests.
2. check_mart_data: validates the DAILY_REVENUE mart.

## 6. Data Visualization

Tableau is used to connect to the transformed Snowflake data and build a sales analytics dashboard.

## 7. Final Output

The project provides structured sales data and business insights through a Tableau dashboard.
