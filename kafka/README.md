# Apache Kafka – Data Engineering Labs

## Overview

This directory contains practical Apache Kafka exercises completed as part of my Data Engineering learning journey.

The labs cover Kafka fundamentals, messaging, data streaming, producers, consumers, Python integration, and related technologies.

## Environment

| Component | Version / Configuration |
|---|---|
| Operating System | macOS |
| Apache Kafka | 4.4.0 |
| Java | OpenJDK 27 |
| Installation | Homebrew |
| Broker | localhost:9092 |
| Python | 3.14.7 |
| Kafka Python Client | confluent-kafka 2.16.2 |
| Code Editor | Visual Studio Code |

## Labs

| Lab | Topic | Status |
|---|---|---|
| Lab 01 | Kafka Console Producer and Consumer | Completed |
| Lab 02 | Custom Kafka Producer and Consumer (Python) | Completed |

### Lab 01 – Kafka Console Producer and Consumer

Topics covered:

- Creating and inspecting Kafka topics.
- Producing messages using the console producer.
- Consuming messages using the console consumer.
- Replaying messages from the beginning.
- Transferring text files through Kafka.
- Comparing original and received files.

[View Lab 01 Documentation](labs/Lab_01_Console_Producer_Consumer.md)

### Lab 02 – Custom Kafka Producer and Consumer (Python)

Topics covered:

- Installing and configuring the Confluent Kafka Python client.
- Creating a custom Python Producer.
- Streaming text files line by line into a Kafka topic.
- Creating a custom Python Consumer.
- Reconstructing text files from Kafka messages.
- Managing consumer groups and offsets.
- Verifying file integrity using `diff`.

[View Lab 02 Documentation](labs/Lab_02_Custom_Kafka_Producer_Consumer.md)

## Repository Structure

kafka/
├── README.md
├── labs/
│   ├── Lab_01_Console_Producer_Consumer.md
│   ├── Lab_02_Custom_Kafka_Producer_Consumer.md
│   └── lab_02/
│       ├── producer.py
│       ├── consumer.py
│       ├── sample.txt
│       └── received.txt
├── resources/
│   └── useful_commands.md
└── screenshots/
    ├── lab_01/
    └── lab_02/

## Learning Goals

- Understand distributed messaging systems.
- Work with Kafka topics, partitions, and brokers.
- Build practical producer and consumer workflows.
- Integrate Kafka with Python applications.
- Develop real-time data streaming skills.
- Document and version-control practical exercises using Git and GitHub.

---

**Project:** Data Engineering – Week 7
**Technology:** Apache Kafka, Python, confluent-kafka