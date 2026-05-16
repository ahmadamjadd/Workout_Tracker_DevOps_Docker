FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-pip 

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

COPY . .

EXPOSE 8000

ENV POSTGRES_USER=postgres \
    POSTGRES_PASSWORD=password \
    POSTGRES_HOST=db \
    POSTGRES_DB=workout_db

CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]