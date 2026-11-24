# Lab 03: Kafka Partitions, Keys and Consumer Groups

## 1. Overview

This lab explores three important Kafka concepts: partitions, message keys, and consumer groups.

The objective is to understand how Kafka distributes messages across partitions, maintains message ordering, and allows multiple consumers to process messages in parallel.

The lab was completed using Apache Kafka installed locally on macOS through Homebrew.

## 2. Learning Objectives

- Create and inspect a Kafka topic with multiple partitions.
- Understand how message keys determine partition assignment.
- Verify message ordering within a partition.
- Run multiple consumers within the same consumer group.
- Observe partition assignment and consumer load distribution.
- Understand consumer failover and partition reassignment.
- Demonstrate how different consumer groups independently read the same topic.

## 3. Environment

| Component | Version / Configuration |
|---|---|
| Operating System | macOS |
| Apache Kafka | 4.4.0 |
| Java | OpenJDK 27 |
| Installation | Homebrew |
| Broker | localhost:9092 |
| Code Editor | Visual Studio Code |

## 4. Part 1 – Creating a Topic with Three Partitions

First, a topic named `orders` was created with three partitions.

Command:

```bash
kafka-topics --create --topic orders --partitions 3 --bootstrap-server localhost:9092
```

The topic was created successfully.

To inspect its configuration:

```bash
kafka-topics --describe --topic orders --bootstrap-server localhost:9092
```

### Results

The topic description confirmed:

- Topic name: orders
- Partition count: 3
- Replication factor: 1
- Broker ID: 1

The three partitions were:

| Partition | Leader | Replicas | ISR |
|---|---:|---:|---:|
| 0 | 1 | 1 | 1 |
| 1 | 1 | 1 | 1 |
| 2 | 1 | 1 | 1 |

Since the environment uses a single Kafka broker, all three partitions have the same leader.

### Key Concepts

- **Partition:** An ordered log of messages within a topic.
- **Leader:** The broker responsible for handling requests for a partition.
- **Replicas:** Copies of a partition stored on brokers.
- **ISR (In-Sync Replicas):** Replicas that are synchronized with the leader.

## 5. Part 2 – Message Keys and Ordering

The next step demonstrated how Kafka uses message keys to assign messages to partitions.

A console consumer was started with key and partition information enabled:

```bash
kafka-console-consumer \
  --topic orders \
  --from-beginning \
  --bootstrap-server localhost:9092 \
  --property print.key=true \
  --property print.partition=true
```

A console producer was started with key parsing enabled:

```bash
kafka-console-producer \
  --topic orders \
  --bootstrap-server localhost:9092 \
  --property parse.key=true \
  --property key.separator=:
```

The following messages were sent:

```text
user1:login
user2:login
user3:login
user1:add-to-cart
user2:add-to-cart
user1:logout
user3:logout
user2:logout
```

### Results

The observed partition assignment was:

| User | Messages | Partition |
|---|---|---:|
| user1 | login, add-to-cart, logout | 0 |
| user2 | login, add-to-cart, logout | 2 |
| user3 | login, logout | 2 |

The experiment confirmed that messages with the same key were assigned to the same partition.

The messages belonging to each user also maintained their original order.

### Key Concepts

Kafka uses the message key to determine the partition assignment.

Messages with the same key are routed to the same partition, allowing Kafka to preserve their order within that partition.

Kafka guarantees ordering within a partition, not across the entire topic.

## 6. Part 3 – Consumer Groups

This section demonstrated how multiple consumers can share the partitions of a topic.

Two console consumers were started using the same group ID:

```bash
kafka-console-consumer \
  --topic orders \
  --group ironhack-group \
  --bootstrap-server localhost:9092 \
  --property print.key=true \
  --property print.partition=true
```

Both consumers belonged to the group:

`ironhack-group`

After the consumers joined the group, Kafka distributed the three partitions between them.

### 6.1 Producing Messages

The following messages were sent:

```text
user1:one
user2:two
user3:three
user4:four
user5:five
user6:six
```

### Results

The messages were distributed between the two consumers:

**Consumer A:**
- Partition 0
- Partition 1

**Consumer B:**
- Partition 2

The observed messages were:

| Consumer | Key | Message | Partition |
|---|---|---|---:|
| A | user1 | one | 0 |
| A | user4 | four | 1 |
| A | user5 | five | 1 |
| A | user6 | six | 0 |
| B | user2 | two | 2 |
| B | user3 | three | 2 |

Each message was delivered to only one consumer within the group.

Kafka assigns partitions to consumers, rather than distributing individual messages in a round-robin pattern.

### 6.2 Inspecting the Consumer Group

The consumer group was inspected using:

```bash
kafka-consumer-groups \
  --describe \
  --group ironhack-group \
  --bootstrap-server localhost:9092
```

The observed results were:

| Partition | Current Offset | Log End Offset | Lag |
|---|---:|---:|---:|
| 0 | 5 | 5 | 0 |
| 1 | 2 | 2 | 0 |
| 2 | 7 | 7 | 0 |

The output confirmed that:

- Consumer A owned partitions 0 and 1.
- Consumer B owned partition 2.
- All three partitions had a lag of zero.

A lag of zero means that the consumer has processed all available messages up to the current log end offset.

## 7. Consumer Failover

The next experiment demonstrated what happens when a consumer leaves a group.

Consumer B was stopped using `Ctrl + C`.

After Kafka detected that the consumer had left, the remaining consumer took over the partitions.

Three additional messages were produced:

```text
user1:after-failover-1
user2:after-failover-2
user3:after-failover-3
```

### Results

The remaining consumer received all three messages:

| Key | Message | Partition |
|---|---|---:|
| user1 | after-failover-1 | 0 |
| user2 | after-failover-2 | 2 |
| user3 | after-failover-3 | 2 |

This demonstrated consumer failover and partition reassignment.

When a consumer leaves a group, Kafka can reassign its partitions to the remaining active consumers.

## 8. Reading Messages with a Different Consumer Group

A new consumer was started using a different group ID:

`other-group`

Command:

```bash
kafka-console-consumer \
  --topic orders \
  --group other-group \
  --from-beginning \
  --bootstrap-server localhost:9092 \
  --property print.key=true \
  --property print.partition=true
```

### Results

The new group successfully read all 17 messages stored in the topic.

It received messages from all previous experiments, including:

- The original user login, add-to-cart, and logout messages.
- The six messages from the consumer group experiment.
- The three messages sent during failover.

This demonstrated that different consumer groups maintain independent offsets.

A new consumer group can read the complete topic history using `--from-beginning`, independently of the progress of another group.

## 9. Part 4 – Chat Application

This exercise was completed previously.

A Kafka topic named `class-chat` was used to demonstrate communication between two writers and one reader.

The exercise demonstrated:

- Sending messages from two different producers.
- Using message keys to identify senders.
- Reading messages through one consumer.
- Replaying the conversation history using a new consumer.

The topic used a single partition to maintain the order of chat messages.

## 10. Cleanup

After completing the experiments, the temporary topics were removed.

To delete the `orders` topic:

```bash
kafka-topics --delete --topic orders --bootstrap-server localhost:9092
```

The `class-chat` topic was also checked for deletion. It was already absent, so Kafka returned a message indicating that the topic did not exist.

The final topic list was inspected using:

```bash
kafka-topics --bootstrap-server localhost:9092 --list
```

The remaining topics were:

```text
__consumer_offsets
file-topic
files-console
lab1-topic
```

This confirmed that the temporary topics had been removed while the topics from previous labs remained available.

## 11. Review Questions and Answers

**1. What is a partition, and why does a topic have more than one?**

A partition is an ordered log of messages within a topic. Multiple partitions allow Kafka to distribute data and processing across consumers.

**2. Why is it useful that messages with the same key go to the same partition?**

It allows Kafka to preserve the order of messages belonging to the same entity, such as a user or an order.

**3. A topic has 3 partitions and a group has 4 consumers. How many consumers sit idle?**

One consumer remains idle because a partition can be assigned to only one consumer within a group at a time.

**4. Two consumers with different group names read the same topic. What does each receive?**

Each group can receive every message independently because each group maintains its own offsets.

**5. Does Kafka guarantee the order of messages across the whole topic?**

No. Kafka guarantees message ordering only within an individual partition.

## 12. Conclusion

This lab demonstrated how Kafka partitions, message keys, and consumer groups work together to support scalable message processing.

The experiments confirmed that:

- Topics can contain multiple partitions.
- Messages with the same key are assigned to the same partition.
- Message ordering is maintained within each partition.
- Multiple consumers in the same group share partition assignments.
- Kafka can reassign partitions when a consumer leaves the group.
- Different consumer groups can independently read the same topic history.

These concepts are essential for designing scalable and reliable event-driven data pipelines.

---

**Project:** Data Engineering – Week 7
**Technology:** Apache Kafka, macOS, Homebrew