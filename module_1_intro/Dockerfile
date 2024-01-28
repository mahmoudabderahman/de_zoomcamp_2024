# Use the python:3.9 docker image as a base image
FROM python:3.9

# Run this command after the establishment
RUN apt-get update && apt-get install -y \
    wget
RUN pip install pandas sqlalchemy psycopg2 requests

# Specifiy the working directory
WORKDIR /app

# Copy src destination
COPY ingest_data.py ingest_data.py

# Use bash as the entrypoint
# ENTRYPOINT ["bash"]
ENTRYPOINT ["python", "ingest_data.py"]
