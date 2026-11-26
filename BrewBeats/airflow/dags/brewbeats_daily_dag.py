from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator


with DAG(
    dag_id="brewbeats_daily_pipeline",
    description="Daily BrewBeats coffee sales transformation pipeline",
    start_date=datetime(2026, 11, 20),
    schedule="@daily",
    catchup=False,
    tags=["brewbeats", "dbt", "snowflake"],
) as dag:

    run_dbt = BashOperator(
        task_id="run_dbt",
        bash_command=(
            'cd "$AIRFLOW_HOME/../dbt/brewbeats_transformations" && '
            '../../.venv/bin/dbt build --select stg_coffee_sales daily_revenue '
            '--profile brewbeats_transformations'
        ),
    )

    check_mart_data = BashOperator(
        task_id="check_mart_data",
        bash_command=(
            'cd "$AIRFLOW_HOME/../dbt/brewbeats_transformations" && '
            '../../.venv/bin/dbt run-operation check_daily_revenue '
            '--profile brewbeats_transformations'
        ),
    )

    run_dbt >> check_mart_data
