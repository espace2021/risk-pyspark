from fastapi import FastAPI
from pydantic import BaseModel
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel

# Init Spark en mode local avec config optimisée pour Render
spark = SparkSession.builder \
    .appName("RiskAPI") \
    .master("local[1]") \
    .config("spark.driver.host", "127.0.0.1") \
    .config("spark.driver.bindAddress", "0.0.0.0") \
    .config("spark.network.timeout", "800s") \
    .config("spark.executor.heartbeatInterval", "60s") \
    .config("spark.sql.shuffle.partitions", "2") \
    .config("spark.default.parallelism", "2") \
    .config("spark.ui.enabled", "false") \
    .config("spark.authenticate", "false") \
    .config("spark.driver.extraJavaOptions", "-Djava.net.preferIPv4Stack=true") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")  # Réduit le bruit dans les logs

# Charger modèle Spark
model = PipelineModel.load("spark_model")

app = FastAPI(title="API Spark Risk")

class Project(BaseModel):
    Budget: float
    Montant_collecte: float

@app.get("/")
def home():
    return {"message": "API Spark OK"}

@app.post("/predict")
def predict(data: Project):
    try:
        # Créer DataFrame Spark avec schema explicite (évite les erreurs de type)
        df = spark.createDataFrame([{
            "Budget": float(data.Budget),
            "Montant_collecte": float(data.Montant_collecte)
        }])

        # Prédiction
        result = model.transform(df)
        prediction = result.select("prediction").collect()[0][0]

        return {
            "risk_class": int(prediction)
        }

    except Exception as e:
        return {"error": str(e)}