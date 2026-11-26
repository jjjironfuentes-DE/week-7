import json
import os

from confluent_kafka import Consumer, KafkaException
from dotenv import load_dotenv
import snowflake.connector

# Load environment variables
load_dotenv()

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:9092"
)

KAFKA_TOPIC = os.getenv(
    "KAFKA_TOPIC",
    "ecommerce_orders"
)

KAFKA_GROUP_ID = "ecommerce_snowflake_consumer"

# Create Kafka Consumer
consumer = Consumer({
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    "group.id": KAFKA_GROUP_ID,
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False
})

# Subscribe to Kafka topic
consumer.subscribe([KAFKA_TOPIC])

# Create Snowflake connection
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

# Insert order into Snowflake
def insert_order(connection, order):

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO ORDERS (
                ORDER_ID,
                CUSTOMER_NAME,
                CITY,
                PRODUCT,
                AMOUNT,
                PAYMENT_MODE,
                ORDER_TIME,
                INGESTED_AT
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s,
                CURRENT_TIMESTAMP()
            )
            """,
            (
                order["order_id"],
                order["customer_name"],
                order["city"],
                order["product"],
                order["amount"],
                order["payment_mode"],
                order["order_time"]
            )
        )

        connection.commit()

        print(f"Order inserted into Snowflake: {order['order_id']}")

    finally:
        cursor.close()

        # Main consumer function
def main():

    connection = None

    try:
        print("Connecting to Snowflake...")

        connection = create_snowflake_connection()

        print("Successfully connected to Snowflake!")
        print(f"Listening to Kafka topic: {KAFKA_TOPIC}")

        while True:

            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                raise KafkaException(msg.error())

            order = json.loads(msg.value().decode("utf-8"))

            print(f"Received order: {order['order_id']}")

            insert_order(connection, order)

            consumer.commit(message=msg, asynchronous=False)

            print("Kafka message committed successfully.")

    except KeyboardInterrupt:
        print("\nStopping Consumer...")

    finally:
        consumer.close()

        if connection is not None:
            connection.close()

        print("Consumer closed successfully.")

        # Run the consumer
if __name__ == "__main__":
    main()