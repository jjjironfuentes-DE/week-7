from pyspark.sql import SparkSession

# 1. Create Spark session
spark = SparkSession.builder \
    .appName("BrewBeats_Question_3") \
    .master("local[*]") \
    .getOrCreate()

# 2. Read coffee sales CSV
coffee_df = spark.read.csv(
    "data/raw/coffee_sales.csv",
    header=True,
    inferSchema=True
)

# 3. Show the first five rows
coffee_df.show(5)

# 4. Show the DataFrame structure
coffee_df.printSchema()

# 5. Calculate total revenue
from pyspark.sql.functions import sum

total_revenue = coffee_df.agg(
    sum("money").alias("total_revenue")
)

# 6. Show the result
print("\nTOTAL COFFEE REVENUE")

total_revenue.show()