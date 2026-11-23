from pyspark.sql import SparkSession
import csv

# 1. Create Spark session
spark = SparkSession.builder \
    .appName("BrewBeats_Question_2") \
    .master("local[*]") \
    .getOrCreate()

# 2. Read Spotify CSV file
spotify_rdd = spark.sparkContext.textFile(
    "data/raw/Spotify_data.csv"
)

# 3. Remove header
header = spotify_rdd.first()

spotify_data = spotify_rdd.filter(
    lambda row: row != header
)

# 4. Parse CSV rows correctly
rows = spotify_data.map(
    lambda row: next(csv.reader([row]))
)

# 5. Extract danceability values
danceability = rows.map(
    lambda row: float(row[2])
)

# 6. Calculate sum and count
total = danceability.sum()
count = danceability.count()

# 7. Calculate average
average = total / count

# 8. Print result
print("\nDANCEABILITY ANALYSIS")
print("Total songs:", count)
print("Average danceability:", round(average, 4))

spark.stop()