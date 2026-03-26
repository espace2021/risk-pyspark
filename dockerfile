FROM python:3.10

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y default-jdk && apt-get clean

# Détecte automatiquement le bon chemin Java
RUN echo "export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))" >> /etc/environment
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH=$JAVA_HOME/bin:$PATH
ENV PYSPARK_PYTHON=python3

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "fastapiserver:app", "--host", "0.0.0.0", "--port", "10000"]