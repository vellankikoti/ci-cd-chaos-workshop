FROM python:3.12-slim

WORKDIR /app

# Install curl
RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

ARG APP_VERSION

COPY Jenkins/jenkins_scenarios/scenario_01_docker_build/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY Jenkins/jenkins_scenarios/scenario_01_docker_build/app/main_v${APP_VERSION}.py /app/app.py

EXPOSE 3000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000"]
