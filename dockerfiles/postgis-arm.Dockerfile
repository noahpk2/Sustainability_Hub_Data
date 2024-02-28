FROM --platform=linux/arm64 postgres:latest



#install postgis
    RUN apt-get update && apt-get install -y \
        postgis \
        postgresql-16-postgis-3 \
        postgresql-16-postgis-3-scripts \
        && rm -rf /var/lib/apt/lists/*

    RUN mkdir -p /docker-entrypoint-initdb.d
    COPY ./initdb-postgis.sh /docker-entrypoint-initdb.d/postgis.sh
    COPY ./update-postgis.sh /usr/local/bin

    
    

