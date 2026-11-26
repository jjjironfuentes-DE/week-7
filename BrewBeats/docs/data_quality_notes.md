
# BrewBeats - Data Quality Notes

## 1. Coffee Sales Dataset

- Total records: 3,636
- Total columns: 6
- Card transactions: 3,547
- Cash transactions: 89
- Missing values in card: 89

### Finding

All 89 missing values in the card column
belong to cash transactions.

### Decision

Keep the missing card values because they
are expected for cash payments.

## 2. Spotify Dataset

- Total records: 2,017
- Total columns: 17
- Missing values: 0
- Unnamed column: Unnamed: 0

### Finding

The Spotify dataset has no missing values.
The Unnamed: 0 column appears to be an
index column and should be reviewed.

#Pandas
--Leer, explorar y preparar los datos

#Matplotlib
--Visualizar y explorar resultados

#Jupyter
--Ejecutar y documentar nuestro análisis por celdas

#Python será nuestro lenguaje de programación.

#PySpark será la interfaz para trabajar con Spark desde Python.

#Java proporcionará el entorno de ejecución de Spark.