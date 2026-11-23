
from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder \
    .appName("BrewBeats") \
    .master("local[*]") \
    .getOrCreate()

print("Spark version:", spark.version)

# Create a small test DataFrame
data = [("Latte", 38.7), ("Americano", 28.9)]

df = spark.createDataFrame(data, ["coffee_name", "price"])

df.show()

# Stop Spark
spark.stop()
