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

## Postgres Container
- docker run: This command is used to run a Docker container.
- -it: These options are used to allocate a pseudo-TTY and keep the container running in interactive mode, allowing you to interact with the container's shell.
- -e POSTGRES_USER="root": This option sets the environment variable POSTGRES_USER to "root". It specifies the username for the PostgreSQL database.
- -e POSTGRES_PASSWORD="root": This option sets the environment variable POSTGRES_PASSWORD to "root". It specifies the password for the PostgreSQL database.
- -e POSTGRES_DB="ny_taxi": This option sets the environment variable POSTGRES_DB to "ny_taxi". It specifies the name of the PostgreSQL database.
- -v `$(pwd)`:/var/lib/postgresql/data: This option mounts the current directory ($(pwd)) to the /var/lib/postgresql/data directory inside the container. It allows the container to persist data in the current directory.
- -p 5432:5432: This option maps the host port 5432 to the container port 5432. It enables communication with the PostgreSQL server running inside the container.

```shell
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd):/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres
```
If there is an error because the port 5432 is not free, we can check this out by running:
```shell
sudo lsof -i -P -n | grep LISTEN
```

And check if there is something running on that port:
```
postgres    366           postgres    8u  IPv6 0x146b34934d8ceed      0t0    TCP *:5432 (LISTEN)
postgres    366           postgres    9u  IPv4 0x146b3493424437d      0t0    TCP *:5432 (LISTEN)
````

Then we can run:
```shell
kill 366
```

### pgcli
A CLI client to connect to postgres server. 

```shell
$ pgcli -h localhost -p 5432 -u root -d ny_taxi
```

On mac with silicon chip, it was necessary to:  
1. ```pip install psycopg2-binary ```
2. ```brew install libpq```
3. ```echo 'export PATH="/opt/homebrew/opt/libpq/bin:$PATH"' >> ~/.zshrc```


Data can be quickly explored on linux using the command:
```shell
head -n 100 yellow_tripdata_2021-01.csv
```

To save only the first 100 into a new csv file:
```shell
head -n 100 yellow_tripdata_2021-01.csv > yellow_head.csv
```

Dictionary for the dataset:
https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
#### postgres commands
``` \dt ``` ---> list of tables
``` \d 'table_name' ``` ---> describe the table

## pgadmin container
To pull the docker image:
```shell
docker pull dpage/pgadmin4
```

To run the pgAdmin container:
```shell
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4
```

In order to be able to link the postgres container with the pgAdmin container, we have to create a network in docker:
```shell
docker network create  pg-network
```

Run the postgres container again with the network parameter added:

```shell
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v /Users/mahmoudabdelrahman/Desktop/de_zoomcamp_2024/module_1_intro/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
postgres
```

Run the pgadmin container again with the network parameter added:
```shell
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pg-admin \
dpage/pgadmin4
```

### nbconvert problem
```shell
ln -s /opt/homebrew/share/jupyter/nbconvert ~/Library/Jupyter
```

python3 ingest_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz