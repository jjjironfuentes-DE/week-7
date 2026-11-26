from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, date_format

# 1. Create Spark session
spark = SparkSession.builder \
    .appName("BrewBeats_Question_5") \
    .master("local[*]") \
    .getOrCreate()

# 2. Read coffee sales CSV
coffee_df = spark.read.csv(
    "data/raw/coffee_sales.csv",
    header=True,
    inferSchema=True
)

# 3. Extract month from date
coffee_df = coffee_df.withColumn(
    "month",
    date_format("date", "yyyy-MM")
)

# 4. Calculate monthly revenue
monthly_revenue = coffee_df.groupBy(
    "month"
).agg(
    sum("money").alias("monthly_revenue")
)

# 5. Sort by month
monthly_revenue = monthly_revenue.orderBy("month")

# 6. Show results
print("\nMONTHLY REVENUE")

monthly_revenue.show()

spark.stop()

##### RDD vs DataFrame

#RDD (Resilient Distributed Dataset) is a low-level Spark structure that allows developers to process distributed data using transformations and actions.

#DataFrame is a higher-level structure that organizes data into named columns, similar to a database table.
#RDD provides more control over data processing, while DataFrames offer better optimization and easier data manipulation.
#DataFrames are generally preferred for structured data analysis.