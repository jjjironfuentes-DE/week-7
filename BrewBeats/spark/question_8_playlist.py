from pyspark.sql import SparkSession
import csv

# 1. Create Spark session
spark = SparkSession.builder \
    .appName("BrewBeats_Question_8") \
    .master("local[*]") \
    .getOrCreate()

# 2. Read Spotify CSV
spotify_rdd = spark.sparkContext.textFile(
    "data/raw/Spotify_data.csv"
)

# 3. Remove header
header = spotify_rdd.first()

spotify_data = spotify_rdd.filter(
    lambda row: row != header
)

# 4. Parse CSV correctly
rows = spotify_data.map(
    lambda row: next(csv.reader([row]))
)

# 5. Extract relevant information
songs = rows.map(
    lambda row: (
        row[15],          # Song title
        row[16],          # Artist
        float(row[2]),    # Danceability
        float(row[3]),    # Duration
        float(row[4])     # Energy
    )
)

# 6. Songs selected for the children's birthday playlist
approved_songs = [
    ("The Happy Song", "Jamie Grace"),
    ("My Favorite Snack", "Imagination Movers"),
    ("When Can I See You Again?", "Owl City"),
    ("Try Everything", "Shakira"),
    ("I2I", "Tevin Campbell"),
    ("Cha Cha Slide", "Mr. C"),
    ("Agadoo", "Black Lace"),
    ("Das Lied Der Schluempfe", "Vader Abraham")
]

# 7. Filter only approved songs
birthday_playlist = songs.filter(
    lambda song: (song[0], song[1]) in approved_songs
)

# 8. Display final playlist
print("\nCHILDREN'S BIRTHDAY PLAYLIST")

for song in birthday_playlist.collect():
    print(song[0], "-", song[1])

print("\nTotal songs:", birthday_playlist.count())