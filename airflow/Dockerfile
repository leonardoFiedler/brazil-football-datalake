#Dockerfile
FROM apache/airflow:2.9.3-python3.12

# Install additional dependencies
USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt ./requirements.txt
USER airflow

# installing specific DBT dependencies
RUN python -m pip install --upgrade "pip==24.0" "setuptools==69.2.0" "wheel==0.43.0" --no-cache-dir

# Set up additional Python dependencies
RUN pip install -r ./requirements.txt

# Configurar variáveis de ambiente para DBT
ENV DBT_PROFILES_DIR=/opt/airflow/dbt