FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Important pour Spark
ENV PYSPARK_PYTHON=python3

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]