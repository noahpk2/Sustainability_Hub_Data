## Process Wiki

# imports
import os
import re
import psycopg2

postgis_container_name = os.environ['POSTGIS_CONTAINER_NAME']

# This script will process the wiki data and upload it to the database.
# We will read each file in the wiki directory and infer location data from the file name. We will then create an entry in the database for each file, with the location data and the file name/index

def process_wiki():
    '''Process the wiki data and index it in the database.'''
    if os.system("docker ps -a") != 0:
        print("Database not running")
        return False

    dbname = "gis"
    user = "docker"
    password = "docker"
    host = "localhost"
    port = "5432"

    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    cur = conn.cursor()
    #create wiki table if it does not exist
    cur.execute(
        "CREATE TABLE IF NOT EXISTS wiki (id SERIAL PRIMARY KEY, name TEXT, url TEXT, coordinates GEOMETRY)"
    )
    progress = 0
    for root, dirs, files in os.walk('../wikidata'):
        total = len(files)
        for file in files:
            file_path = os.path.join(root, file)
            progress += 1
            name = file.title()
            with open(file_path, "r") as f:  # Use 'with' to open the file
                file_content = f.read()
            # search file for url and coordinates
            urls = re.findall("https://[^\s]+", file_content)
            if urls:
                url = urls[0]  # This gets the first URL found
            else:
                url = None  # No URL found

            # search file for coordinates
            # txt format: Coordinates: 38.33556°N 103.34250°W or Coordinates: Coordinates not found

            coordinates_pattern = r"Coordinates: (\d{1,3}\.\d+)[°]?([N|S]) (\d{1,3}\.\d+)[°]?([W|E])"
            coordinates = re.findall(coordinates_pattern, file_content)
            if coordinates:
                lat, lat_dir, long, long_dir = coordinates[0]  # Unpack the first tuple of coordinates along with directions

                # Convert latitude and longitude to float
                lat = float(lat)
                long = float(long)

                # Convert S to negative latitude and W to negative longitude
                if lat_dir == 'S':
                    lat = -lat
                if long_dir == 'W':
                    long = -long

                # Convert to PostGIS friendly format (POINT)
                coordinates_postgis = f"POINT({long} {lat})"
                print(f"Coordinates: {coordinates_postgis}")
            else:
                coordinates_postgis = None

            # create entry in database with name, url and coordinates
            # check database exists and is running

            # create entry in database
            try:
                cur.execute(
                    "INSERT INTO wiki (name, url, coordinates) VALUES (%s, %s, %s)",
                    (name, url, coordinates_postgis),
                )
                conn.commit()
                print(f"Uploaded {name} to database {progress}/{total}")
            except Exception as e:
                print(f"Error uploading to database: {e}")
                conn.rollback()  # Rollback the transaction on error
                break

                
    #
