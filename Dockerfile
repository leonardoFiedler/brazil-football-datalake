#Dockerfile
FROM apache/airflow:2.9.3-python3.12

# Install additional dependencies
USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get -y install libpq-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r airflow

COPY --chown=50000:0 /dbt/brazil_football /sources/brazil_football_dbt
RUN mkdir -p /sources/brazil_football_dbt/logs && chown -R airflow:airflow /sources/brazil_football_dbt

USER airflow

RUN echo "Airflow UID: $(id -u airflow) GID: $(id -g airflow)"

COPY requirements.txt ./requirements.txt

# installing specific DBT dependencies
RUN python -m pip install --upgrade "pip==24.2" "setuptools==66.1.1" "wheel==0.43.0" --no-cache-dir

# Set up additional Python dependencies
RUN pip install -r ./requirements.txt

# Configurar variáveis de ambiente para DBT
ENV DBT_PROFILES_DIR=/sources/brazil_football_dbt

RUN dbt deps --project-dir /sources/brazil_football_dbt
