FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl iproute2 && rm -rf /var/lib/apt/lists/*
RUN pip install flask requests
COPY app.py .
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1
CMD ["python", "app.py"]
