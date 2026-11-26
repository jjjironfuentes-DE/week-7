
import os
import yaml

from snowflake.snowpark import Session
from snowflake.snowpark.functions import (
    col,
    count,
    sum as sum_,
    avg,
)


def create_snowpark_session():
    profile_path = os.path.expanduser("~/.dbt/profiles.yml")

    with open(profile_path, "r") as file:
        profiles = yaml.safe_load(file)

    config = profiles["brewbeats_transformations"]["outputs"]["dev"]

    connection_parameters = {
        "account": config["account"],
        "user": config["user"],
        "authenticator": config["authenticator"],
        "token": config["token"],
        "role": config["role"],
        "warehouse": config["warehouse"],
        "database": config["database"],
        "schema": config["schema"],
    }

    return Session.builder.configs(connection_parameters).create()


def transform_daily_revenue(session):
    # Read raw coffee sales data
    coffee_sales = session.table("BREWBEATS_DB.RAW.COFFEE_SALES")

    # Aggregate sales by date
    daily_revenue = (
        coffee_sales
        .group_by(col("DATE"))
        .agg(
            count("*").alias("TOTAL_TRANSACTIONS"),
            sum_(col("MONEY")).alias("TOTAL_REVENUE"),
            avg(col("MONEY")).alias("AVERAGE_TRANSACTION_VALUE"),
        )
        .sort(col("DATE"))
    )

    # Display transformation results
    daily_revenue.show()

    # Save results in Snowflake
    daily_revenue.write.mode("overwrite").save_as_table(
        "BREWBEATS_DB.DBT_DEV.SNOWPARK_DAILY_REVENUE"
    )

    print("Snowpark transformation completed successfully!")


if __name__ == "__main__":
    session = create_snowpark_session()

    try:
        transform_daily_revenue(session)

    finally:
        session.close()
