import os
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()


def create_snowflake_connection():

    connection = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        token=os.getenv("SNOWFLAKE_PAT"),
        authenticator="PROGRAMMATIC_ACCESS_TOKEN",
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE")
    )

    return connection


if __name__ == "__main__":

    connection = None

    try:
        connection = create_snowflake_connection()

        print("Successfully connected to Snowflake!")

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                CURRENT_USER(),
                CURRENT_ROLE(),
                CURRENT_DATABASE(),
                CURRENT_SCHEMA(),
                CURRENT_WAREHOUSE()
        """)

        print("Connection details:")
        print(cursor.fetchone())

        cursor.close()

    except Exception as error:
        print(f"Snowflake connection failed: {error}")

    finally:
        if connection is not None:
            connection.close()
            print("Snowflake connection closed.")