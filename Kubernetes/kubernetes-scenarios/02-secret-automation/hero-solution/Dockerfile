FROM python:3.11-slim

WORKDIR /app

# Install Flask
RUN pip install --no-cache-dir flask==3.0.0

# Build argument for app file (defaults to standard version)
ARG APP_FILE=app.py

# Copy the specified app file
COPY ${APP_FILE} .

# Create non-root user
RUN useradd -m -u 1000 todouser && chown -R todouser:todouser /app

USER todouser

# Expose port
EXPOSE 8080

# Run the app
CMD python ${APP_FILE}
