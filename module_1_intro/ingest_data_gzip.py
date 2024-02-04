import argparse
import gzip
import os
import shutil
import pandas as pd
from sqlalchemy import create_engine
from time import time
import requests


def download_file(url, local_filename):
    # Stream download to handle large files without consuming too much memory
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return local_filename


def decompress_gzip(gzip_path, output_path):
    with gzip.open(gzip_path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def get_db_engine(user, password, host, port, db):
    return create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")


def ingest_csv_to_db(csv_name, table_name, engine):
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    df = next(df_iter)

    # Assume that we're working with a fixed schema (add any additional preprocessing here)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    while True:
        try:
            t_start = time()

            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            df.to_sql(name=table_name, con=engine, if_exists='append')
            
            t_end = time()
            print(f"Inserted another chunk... took {t_end - t_start:.3f} second")
            
            df = next(df_iter)
        except StopIteration:
            break
        except Exception as e:
            print("An error occurred:", e)
            break


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    compressed_file_path = "output.csv.gz"
    csv_name = "output.csv"

    # Step 1: Download and save .csv.gz file
    download_file(url, compressed_file_path)

    # Step 2: Decompress .csv.gz file
    decompress_gzip(compressed_file_path, csv_name)

    # Step 3: Ingest CSV data to PostgreSQL database
    engine = get_db_engine(user, password, host, port, db)
    ingest_csv_to_db(csv_name, table_name, engine)

    # Remove temporary files
    os.remove(compressed_file_path)
    os.remove(csv_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV data into Postgres")

    # Define command line arguments
    parser.add_argument("--user", required=True, help="Username for Postgres database")
    parser.add_argument("--password", required=True, help="Password for Postgres database")
    parser.add_argument("--host", required=True, help="Host for Postgres database")
    parser.add_argument("--port", required=True, help="Port for Postgres database")
    parser.add_argument("--db", required=True, help="Database name")
    parser.add_argument("--table_name", required=True, help="Name of the table to write to")
    parser.add_argument("--url", required=True, help="URL of the CSV file to download")

    # Parse command line arguments
    params = parser.parse_args()

    # Run main program
    main(params=params)
