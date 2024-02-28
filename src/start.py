# Script to initialize PostGIS docker container and attach geodata volme

import os
import subprocess
import docker 


def app():
    '''Main application loop'''
    # Init
    print("Starting Docker")
    success = docker_start()
    import process_wiki
    if success:
        print("Containers started successfully")
    else:
        print("Docker failed to start, exiting")
        return False

    while success:
        print("Sustainability Hub - Database Management CLI\n")
        print("--------------------------------------------\n")
        print("1. Upload Data")
        print("2. Process Wiki Data")
        print("3. Construct Geo Knowledge Graph")
        print("4. Exit")
        print("--------------------------------------------\n")
        choice = input("Enter your choice: ")
        if choice == '1':
            upload_data()
        elif choice == '2':
            process_wiki.process_wiki()
        elif choice == '3':
            print("Not implemented yet")
        elif choice == '4':
            shutdown()
            break
        else:
            print("Invalid choice. Please try again.")
        print("\n\n\n\n\n --")


def shutdown():
    '''Shutdown the docker containers'''
    print("Shutting down Docker")
    os.system('docker-compose -f ../docker-compose-arm.yml down')
    print("Docker containers stopped")
    return True    


def docker_start():
    # if docker is not installed, return false, print error message
    if os.system("docker --version") != 0:
        print("Docker not installed")
        return False

    OS = os.uname().sysname
    print(f"OS is {OS}")
    # if the OS is arm (Darwin), use the arm version of the images
    if OS == "Darwin":
        process = subprocess.Popen(['docker-compose', '-f', '../docker-compose-arm.yml', 'up', '-d'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            print(line, end='')
    process.wait()

    # add container name to environment variables, so it can be accessed by other scripts, taken from docker container list
    container_name_output = (
        os.popen("docker ps -a | grep postgis | awk '{print $1}'").read().strip()
    )
    if container_name_output:
        os.environ["POSTGIS_CONTAINER_NAME"] = container_name_output
        print(f"Container name is {os.environ['POSTGIS_CONTAINER_NAME']}")
    else:
        print("No postgis container found. Please ensure the container is running.")
    # TODO: Add support for other OS
    # Print container status
    os.system("docker ps -a")
    # if the containers are running, return true
    if os.system("docker ps -a") == 0:
        return True


def upload_data():
    '''Walk through the geodata directory and upload the data to the PostGIS container as individual tables/layers'''
    for root, dirs, files in os.walk('../geodata'):
        for file in files:
            if file.endswith('.pbf'):
                full_path = os.path.join(root, file)
                osm2pgsql(full_path)
        for dir in dirs:
            if dir.endswith('.gdb'):
                ogr2ogr(dir)    
    return True


def ogr2ogr(gdb_name):
    '''Converts file geodatabase to PostGIS format using ogr2ogr'''
    os.system(f'ogr2ogr -f "PostgreSQL" PG:"dbname=gis user=docker password=docker host=localhost port=5432" {gdb_name} -lco SCHEMA=public -nln {gdb_name} -progress')


def osm2pgsql(osm_file):
    '''Converts OSM file to PostGIS format using osm2pgsql'''
    os.system(f'osm2pgsql -c -d gis -U docker -W -H localhost -P 5432 {osm_file}')


# main loop
if __name__ == '__main__':
    app()
