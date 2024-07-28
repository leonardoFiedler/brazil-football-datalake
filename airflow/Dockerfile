#Dockerfile
FROM apache/airflow:2.9.3-python3.12

# Install additional dependencies
USER root
COPY requirements.txt ./requirements.txt
USER airflow

# Set up additional Python dependencies
RUN pip install --no-cache-dir -r ./requirements.txt