from pyspark.sql import SparkSession
from pyspark.sql.functions import count

# 1. Create Spark session
spark = SparkSession.builder \
    .appName("BrewBeats_Question_4") \
    .master("local[*]") \
    .getOrCreate()

# 2. Read coffee sales CSV
coffee_df = spark.read.csv(
    "data/raw/coffee_sales.csv",
    header=True,
    inferSchema=True
)

# 3. Count transactions by coffee name
coffee_counts = coffee_df.groupBy(
    "coffee_name"
).agg(
    count("*").alias("total_transactions")
)

# 4. Sort results
coffee_counts = coffee_counts.orderBy(
    "total_transactions",
    ascending=False
)

# 5. Show results
print("\nTRANSACTIONS BY COFFEE")

coffee_counts.show()

spark.stop()