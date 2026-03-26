FROM python:3.10

WORKDIR /app

COPY . .

# Installer OpenJDK 17 pour Spark
RUN apt-get update && apt-get install -y default-jdk && apt-get clean

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Important pour Spark
ENV PYSPARK_PYTHON=python3

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "fastapiserver:app", "--host", "0.0.0.0", "--port", "10000"]