FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make puzzle scripts executable
RUN chmod +x ../puzzles/*.sh
RUN chmod +x ../puzzles/puzzle5_multistage/setup.sh

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"] 