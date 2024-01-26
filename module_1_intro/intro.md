# Docker
To run the application, use the following command in your terminal:

```shell
docker run <image_name>
```

To run an image in an interactive mode:

```shell
docker run -it ubuntu bash
```

Pull Python docker image and run in interactive mode:

```shell
docker run -it python:3.9 
```

To tell what exactly to be executed, we use the entrypoint parameter, that will let us have a bash prompt instead of Python prompt:

```shell
docker run -it --entrypoint=bash python:3.9
```

## Dockerfile
Instead of installing dependencies inside the container after creating it, we can have a Dockefile that contains everything to be installed:

```dockerfile
# Use the python:3.9 docker image as a base image
FROM python:3.9

# Run this command after the establishment
RUN pip install pandas 

# Specifiy the working directory
WORKDIR /app

# Copy src destination
COPY pipeline.py pipeline.py

# Use bash as the entrypoint
ENTRYPOINT ["bash"]
````

Using the already written Dockerfile, we can create a Docker container:
```bash
#                TAG         . --> look for the Dockerfile in the current directory
docker build -t test:pandas .
```

To run a container out of this image:
```bash
docker run -it test:pandas
```

We can overwrite the entry point to run a Python file inside the container
```dockerfile
# Use bash as the entrypoint
ENTRYPOINT ["python", "pipeline.py"]
````

To pass an argument while running a docker container:
```bash
docker run -it test:pandas 2021-01-15
```

