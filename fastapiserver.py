from fastapi import FastAPI
from pydantic import BaseModel
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel

# Init Spark
spark = SparkSession.builder.appName("RiskAPI").getOrCreate()

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
        # Créer DataFrame Spark
        df = spark.createDataFrame([{
            "Budget": data.Budget,
            "Montant_collecte": data.Montant_collecte
        }])

        # Prédiction
        result = model.transform(df)

        prediction = result.select("prediction").collect()[0][0]

        return {
            "risk_class": int(prediction)
        }

    except Exception as e:
        return {"error": str(e)}