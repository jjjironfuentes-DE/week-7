import json
import random
import time
import uuid
from datetime import datetime, timezone, timedelta

from faker import Faker
from confluent_kafka import Producer
from dotenv import load_dotenv
import os
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

# Create Kafka Producer
producer = Producer({
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS
})

# Initialize Faker
fake = Faker()

# Generate a random e-commerce order
def generate_order():

    order = {
        "order_id": str(uuid.uuid4()),
        "customer_name": fake.name(),
        "city": random.choice([
            "Hamburg",
            "Berlin",
            "Munich",
            "Frankfurt"
        ]),
        "product": random.choice([
            "Laptop",
            "Smartphone",
            "Tablet",
            "Headphones"
        ]),
        "amount": round(random.uniform(500, 80000), 2),
        "payment_mode": random.choice([
            "Card",
            "Cash",
            "PayPal",
            "Bank Transfer"
        ]),
        "order_time": datetime.now(timezone.utc).isoformat()
    }

    return order

# Confirm message delivery
def delivery_report(err, msg):

    if err is not None:
        print(f"Message delivery failed: {err}")

    else:
        print(
            f"Order delivered successfully | "
            f"Topic: {msg.topic()} | "
            f"Partition: {msg.partition()}"
        )

# Send order to Kafka
def send_order(order):

    producer.produce(
        topic=KAFKA_TOPIC,
        key=order["order_id"],
        value=json.dumps(order),
        callback=delivery_report
    )

    producer.poll(0)


# Main loop: generate and send orders every 2 seconds
def main():

    print("Starting E-Commerce Kafka Producer...")
    print(f"Sending orders to topic: {KAFKA_TOPIC}")

    try:
        while True:

            order = generate_order()

            send_order(order)

            print(f"New order generated: {order}")

            time.sleep(2)

    except KeyboardInterrupt:
        print("\nStopping Producer...")

    finally:
        producer.flush()
        print("Producer closed successfully.")


if __name__ == "__main__":
    main()