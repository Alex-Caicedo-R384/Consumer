# Dockerfile para consumer.py (consumidor)
FROM python:3.11.0

# Instalar dependencias del sistema necesarias
RUN apt-get update && \
    apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY consumer.py .

RUN pip install pika

CMD ["python", "consumer.py"]
