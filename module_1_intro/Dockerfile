# Use the python:3.9 docker image as a base image
FROM python:3.9

# Run this command after the establishment
RUN pip install pandas 

# Specifiy the working directory
WORKDIR /app

# Copy src destination
COPY pipeline.py pipeline.py

# Use bash as the entrypoint
# ENTRYPOINT ["bash"]
ENTRYPOINT ["python", "pipeline.py"]
