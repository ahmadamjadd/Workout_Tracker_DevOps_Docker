# Using your pre-configured Ubuntu 24.04 image
FROM ubuntu:24.04

# Prevent interactive prompts during the install
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# 1. Install pip3 and the PostgreSQL headers
# Even if you think libpq-dev is there, it's safer to include it with pip
RUN apt-get update && apt-get install -y \
    python3-pip 

# 2. Layer Caching: Copy requirements first
COPY requirements.txt .

# 3. Install dependencies globally
# Required flag for Ubuntu 24.04 system-managed environments
RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

# 4. Copy your application code
COPY . .

EXPOSE 8000

# 5. Environment Variables for Postgres
ENV POSTGRES_USER=postgres \
    POSTGRES_PASSWORD=password \
    POSTGRES_HOST=db \
    POSTGRES_DB=workout_db

# 6. Start the API
CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]