from pyspark.sql import SparkSession
import csv

# 1. Create Spark session
spark = SparkSession.builder \
    .appName("BrewBeats_Question_7") \
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

# 5. Extract song titles
song_titles = rows.map(
    lambda row: row[15]
)

# 6. Filter titles containing "love"
love_songs = song_titles.filter(
    lambda title: "love" in title.lower()
)

# 7. Count matching songs
total_love_songs = love_songs.count()

# 8. Print result
print("\nSONG TITLES CONTAINING LOVE")
print("Total songs containing 'love':", total_love_songs)

spark.stop()