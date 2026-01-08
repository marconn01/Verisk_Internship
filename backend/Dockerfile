FROM python:3.11-slim

WORKDIR /app

# Accept build arguments for secrets/config
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# directly exposing port 80 instead of 5000
# EXPOSE 80

CMD ["python", "./app.py"]