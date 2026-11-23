# Lab 1: Kafka Console Producer and Consumer

## 1. Overview

This lab introduces the fundamental concepts of Apache Kafka using its built-in command-line tools.

The exercises were performed on macOS using Apache Kafka 4.4.0 installed through Homebrew.

**Environment:**
- Operating System: macOS
- Apache Kafka: 4.4.0
- Java: OpenJDK 27
- Installation method: Homebrew
- Kafka broker: localhost:9092

## 2. Learning Objectives

- Create and inspect Kafka topics.
- Produce messages using the Kafka Console Producer.
- Consume messages using the Kafka Console Consumer.
- Replay messages from the beginning of a topic.
- Transfer a text file through Kafka.
- Compare the original and received files.

## 3. Part 1: Create and Inspect a Topic

### 3.1 Verify Kafka Service

```bash
brew services list
```

Kafka service status: `started`.

### 3.2 Create a Topic

```bash
kafka-topics --create --topic lab1-topic --bootstrap-server localhost:9092
```

Result:

```text
Created topic lab1-topic.
```

### 3.3 List Topics

```bash
kafka-topics --list --bootstrap-server localhost:9092
```

Result:

```text
lab1-topic
```

### 3.4 Describe the Topic

```bash
kafka-topics --describe --topic lab1-topic --bootstrap-server localhost:9092
```

Observed configuration:

| Property | Value |
|---|---|
| Topic | lab1-topic |
| PartitionCount | 1 |
| ReplicationFactor | 1 |
| Partition | 0 |
| Leader | 1 |
| Replicas | 1 |
| ISR | 1 |

**Conclusion:** The topic was successfully created and inspected.

## 4. Part 2: Console Producer and Consumer

### 4.1 Start the Consumer

Open Terminal Window A:

```bash
kafka-console-consumer --topic lab1-topic --bootstrap-server localhost:9092
```

The consumer waits for incoming messages.

### 4.2 Start the Producer

Open Terminal Window B:

```bash
kafka-console-producer --topic lab1-topic --bootstrap-server localhost:9092
```

### 4.3 Produce Messages

The following messages were sent:

```text
My name is
i am a DE
learning kafka
```

**Result:** All three messages were received successfully in the consumer terminal in real time.

## 5. Replay Messages from the Beginning

Stop the previous producer and consumer processes using `CTRL + C`.

Start a new consumer:

```bash
kafka-console-consumer --topic lab1-topic --from-beginning --bootstrap-server localhost:9092
```

**Result:** All three previously published messages were retrieved in their original order.

This demonstrates that Kafka retains messages and allows consumers to read them again from the beginning.

## 6. Part 3: Send a Text File Through Kafka

### 6.1 Create a New Topic

```bash
kafka-topics --create --topic files-console --bootstrap-server localhost:9092
```

### 6.2 List Available Topics

```bash
kafka-topics --list --bootstrap-server localhost:9092
```

Topics observed:

- `lab1-topic`
- `files-console`
- `__consumer_offsets` (internal Kafka topic)

### 6.3 Create a Text File

```bash
printf "first line\nsecond line\nthird line\nfourth line\n" > data.txt
```

Verify the file:

```bash
cat data.txt
```

Expected content:

```text
first line
second line
third line
fourth line
```

### 6.4 Send the File Through Kafka

```bash
cat data.txt | kafka-console-producer --topic files-console --bootstrap-server localhost:9092
```

Each line of the file was published as an individual Kafka message.

### 6.5 Retrieve Messages into a New File

```bash
kafka-console-consumer --topic files-console --from-beginning --max-messages 4 --bootstrap-server localhost:9092 > received.txt
```

Result:

```text
Processed a total of 4 messages
```

### 6.6 Verify the Received File

```bash
cat received.txt
```

The received file contained:

```text
first line
second line
third line
fourth line
```

### 6.7 Compare Both Files

```bash
diff data.txt received.txt
```

**Result:** No output was returned, confirming that both files contain identical content.

## 7. Key Concepts

| Concept | Description |
|---|---|
| Topic | A named stream of messages |
| Producer | Publishes messages to Kafka |
| Consumer | Reads messages from Kafka |
| Partition | A topic's unit of parallelism and storage |
| Broker | Kafka server that handles messages |
| Replay | Reading previously stored messages again |

## 8. Troubleshooting Notes

- If Kafka is stopped, start it with `brew services start kafka`.
- Ensure the producer and consumer use the same topic name.
- Use `--from-beginning` to replay previously stored messages.
- The KIP-848 message displayed by the consumer is informational.
- An empty `diff` result means both files are identical.

## 9. Lab Conclusion

Lab 1 was successfully completed using Apache Kafka 4.4.0 on macOS.

The exercises demonstrated topic management, message production, message consumption, replay functionality, and text file transfer through Kafka.

**Status: COMPLETED**
