# This Dockerfile was created for local development and testing
FROM apache/airflow:2.9.3-python3.12

# Install additional dependencies
USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get -y install libpq-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r airflow

USER airflow

RUN echo "Airflow UID: $(id -u airflow) GID: $(id -g airflow)"

COPY requirements.txt ./requirements.txt

# Set up additional Python dependencies
RUN pip install -r ./requirements.txt
