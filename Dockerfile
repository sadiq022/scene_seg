FROM python:3.13.0

# Set working directory
WORKDIR /app

# Copy requirements first (for better Docker cache)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code and .env file
COPY scenesage.py .
COPY .env .

# Default command — user can override in docker run
CMD ["python", "scenesage.py", "--help"]
