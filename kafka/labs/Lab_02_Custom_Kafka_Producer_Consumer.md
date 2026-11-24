# Lab 2: Custom Kafka Producer and Consumer to Transfer Text Files (Python)

## 1. Overview

This lab demonstrates how to use Python to transfer text files through Apache Kafka.

A custom Python Producer reads a text file line by line and sends each line as an individual Kafka message. A Python Consumer reads those messages and reconstructs the original file.

## 2. Learning Objectives

- Install and use the Confluent Kafka Python client.
- Create a custom Kafka Producer.
- Stream a text file into a Kafka topic line by line.
- Create a custom Kafka Consumer.
- Reconstruct a text file from Kafka messages.
- Verify file integrity by comparing the original and received files.

## 3. Environment and Prerequisites

| Component | Configuration |
|---|---|
| Operating System | macOS |
| Kafka Installation | Homebrew |
| Kafka Version | 4.4.0 |
| Broker Address | localhost:9092 |
| Python Version | 3.14.7 |
| Python Kafka Client | confluent-kafka 2.16.2 |
| Development Environment | Visual Studio Code |
| Virtual Environment | .venv |

**Note:** Kafka was installed and configured locally using Homebrew. Docker was not required.

## 4. Project Structure

```text
lab_02/
├── .venv/
├── .vscode/
│   └── settings.json
├── producer.py
├── consumer.py
├── sample.txt
└── received.txt
```

## 5. Environment Setup

### 5.1 Create and activate the virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 5.2 Install the Kafka Python client

```bash
python -m pip install confluent-kafka
```

Verify the installation:

```bash
python -c "import confluent_kafka; print(confluent_kafka.__version__)"
```

Expected output:

```text
2.16.2
```

## 6. Kafka Topic Creation

Create the topic used for file transfer:

```bash
kafka-topics --create \
  --topic file-topic \
  --bootstrap-server localhost:9092
```

Verify available topics:

```bash
kafka-topics --list --bootstrap-server localhost:9092
```

Describe the topic:

```bash
kafka-topics --describe \
  --topic file-topic \
  --bootstrap-server localhost:9092
```

The topic was created successfully with the following configuration:

| Property | Value |
|---|---|
| Topic | file-topic |
| Partitions | 1 |
| Replication Factor | 1 |
| Leader | Broker 1 |
| ISR | 1 |

## 7. Create the Sample File

The original file, `sample.txt`, contains five lines:

```text
Kafka moves messages between programs.
Each line of this file is one message.
Producers write to topics.
Consumers read from topics.
This is the last line.
```

Each line represents one Kafka message.

## 8. Python Producer Implementation

The Producer reads the input file line by line and publishes each line to the Kafka topic.

The message key is set to the source filename.

The Producer uses delivery callbacks, polling, and flushing to manage message delivery.

The implementation is available in `producer.py`.

### Execute the Producer

```bash
python producer.py sample.txt --topic file-topic
```

Expected output:

```text
Sent 5 of 5 lines from sample.txt to topic file-topic
```

**Result:** All five lines were successfully sent to Kafka.

## 9. Python Consumer Implementation

The Consumer subscribes to `file-topic`, reads incoming messages, decodes them as UTF-8, and writes them to `received.txt`.

The configuration uses:

- A unique consumer group ID for each default execution.
- `auto.offset.reset = earliest` to read from the beginning for a new group.
- A 10-second idle timeout to stop when no new messages arrive.
- A clean consumer shutdown using `consumer.close()`.

The implementation is available in `consumer.py`.

### Execute the Consumer

```bash
python consumer.py --topic file-topic --out received.txt
```

Expected output:

```text
Wrote 5 lines to received.txt
```

**Result:** The Consumer successfully received and wrote all five messages.

## 10. File Integrity Verification

The original and received files were compared using:

```bash
diff sample.txt received.txt
```

Initially, the comparison identified a final newline difference. The original file did not contain a newline after its last line, while the Consumer added one when writing the received file.

This formatting difference was corrected with:

```bash
printf '\n' >> sample.txt
```

The comparison was executed again:

```bash
diff sample.txt received.txt
```

The command returned no output, confirming that both files were identical.

The received file was also inspected using:

```bash
cat received.txt
```

## 11. Final Results

| Test | Result |
|---|---|
| Python virtual environment | Successful |
| Kafka Python client installation | Successful |
| Kafka topic creation | Successful |
| Producer execution | 5/5 messages sent |
| Consumer execution | 5/5 messages received |
| Output file creation | Successful |
| File comparison | Identical files |

## 12. Key Concepts Learned

- A Kafka Producer publishes messages to a topic.
- A Kafka Consumer subscribes to a topic and reads messages.
- A Kafka topic stores messages in partitions.
- Message keys can help route related messages to the same partition.
- `poll()` handles delivery events and retrieves messages.
- `flush()` waits for pending Producer messages to be delivered.
- Consumer groups manage message consumption and offsets.
- `auto.offset.reset` controls the initial offset behavior for a new consumer group.
- File comparison tools such as `diff` help verify data integrity.

## 13. Conclusion

This lab successfully demonstrated how to transfer a text file through Apache Kafka using custom Python Producer and Consumer applications.

The Producer sent five individual messages to `file-topic`. The Consumer retrieved all five messages and reconstructed the original text file.

The final comparison confirmed that the original and received files were identical.

**Lab 2 completed successfully.**