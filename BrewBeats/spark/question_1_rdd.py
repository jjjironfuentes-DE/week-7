import csv
from pyspark.sql import SparkSession

# 1. Create Spark session
spark = SparkSession.builder \
    .appName("BrewBeats_Question_1") \
    .master("local[*]") \
    .getOrCreate()

# 2. Read Spotify CSV file as an RDD
spotify_rdd = spark.sparkContext.textFile(
    "data/raw/Spotify_data.csv"
)

# 3. Remove the header
header = spotify_rdd.first()

spotify_data = spotify_rdd.filter(
    lambda row: row != header
)

# 4. Read CSV rows correctly
rows = spotify_data.map(
    lambda row: next(csv.reader([row]))
)

# 5. Extract artist and count songs
artist_counts = rows.map(
    lambda row: (row[16].strip(), 1)
).reduceByKey(
    lambda a, b: a + b
)

# 6. Sort artists by number of songs
top_artists = artist_counts.sortBy(
    lambda item: item[1],
    ascending=False
).take(20)

# 7. Show top 20 artists
print("\nTOP 20 ARTISTS BY NUMBER OF SONGS")

for artist, count in top_artists:
    print(artist, count)

spark.stop()