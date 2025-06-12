# Use a slim, minimal image
FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .

RUN apk add gcc musl-dev linux-headers python3-dev

RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Run the collector script
CMD ["python", "collector.py"]