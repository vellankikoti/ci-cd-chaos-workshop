FROM python:3.9-slim

WORKDIR /app

# Install system dependencies and Docker CLI
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    gnupg \
    lsb-release \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y docker-ce-cli

# Copy requirements and install Python dependencies
COPY webui/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY webui/ .

# Copy puzzle scripts from parent directory
COPY puzzles ./puzzles/

# Make puzzle scripts executable
RUN chmod +x puzzles/*.sh
RUN chmod +x puzzles/puzzle5_multistage/setup.sh

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"] 