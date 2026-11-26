# Apache Kafka – Useful Commands

This document contains frequently used Apache Kafka commands for macOS.

## 1. Kafka Service Management

Check Kafka service status:

```bash
brew services list
```

Start Kafka:

```bash
brew services start kafka
```

Stop Kafka:

```bash
brew services stop kafka
```

Restart Kafka:

```bash
brew services restart kafka
```

## 2. Kafka Version and Broker Verification

Check Kafka version:

```bash
kafka-topics --version
```

Check running Java processes:

```bash
jps
```

Verify broker connectivity:

```bash
kafka-broker-api-versions --bootstrap-server localhost:9092
```

## 3. Topic Management

Create a topic:

```bash
kafka-topics --create --topic TOPIC_NAME --bootstrap-server localhost:9092
```

List topics:

```bash
kafka-topics --list --bootstrap-server localhost:9092
```

Describe a topic:

```bash
kafka-topics --describe --topic TOPIC_NAME --bootstrap-server localhost:9092
```

Delete a topic:

```bash
kafka-topics --delete --topic TOPIC_NAME --bootstrap-server localhost:9092
```

## 4. Console Producer

Start a producer:

```bash
kafka-console-producer --topic TOPIC_NAME --bootstrap-server localhost:9092
```

Send messages manually, pressing Enter after each message.

## 5. Console Consumer

Start a consumer:

```bash
kafka-console-consumer --topic TOPIC_NAME --bootstrap-server localhost:9092
```

Read messages from the beginning:

```bash
kafka-console-consumer --topic TOPIC_NAME --from-beginning --bootstrap-server localhost:9092
```

Read a limited number of messages:

```bash
kafka-console-consumer --topic TOPIC_NAME --from-beginning --max-messages 10 --bootstrap-server localhost:9092
```

## 6. File Transfer

Create a text file:

```bash
printf "first line\nsecond line\nthird line\n" > data.txt
```

Send a file through Kafka:

```bash
cat data.txt | kafka-console-producer --topic TOPIC_NAME --bootstrap-server localhost:9092
```

Receive messages into a file:

```bash
kafka-console-consumer --topic TOPIC_NAME --from-beginning --max-messages 3 --bootstrap-server localhost:9092 > received.txt
```

Compare files:

```bash
diff data.txt received.txt
```

## 7. Important Notes

- Replace `TOPIC_NAME` with the actual topic name.
- Kafka broker address: `localhost:9092`.
- Use `CTRL + C` to stop an interactive producer or consumer.
- An empty `diff` result indicates identical files.
- These commands are intended for the local macOS Homebrew Kafka environment.

---

**Documentation:** Kafka Data Engineering Labs