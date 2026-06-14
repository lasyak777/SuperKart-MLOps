
FROM python:3.9-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy dependency file separately to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy application files
COPY . .

# Expose application port
EXPOSE 7860

# Start the Flask API with Gunicorn
CMD ["gunicorn", "--workers=2", "--timeout=120", "--bind=0.0.0.0:7860", "superkart_sales_app:superkart_api"]
