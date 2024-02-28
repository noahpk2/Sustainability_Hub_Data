FROM --platform=linux/amd64 postgres:latest



#install postgis
RUN apt-get update && apt-get install -y \
    postgis \
    postgresql-13-postgis-3 \
    postgresql-13-postgis-3-scripts \
    && rm -rf /var/lib/apt/lists/*

    # Set environment variables
    ENV POSTGRES_USER=docker
    ENV POSTGRES_PASSWORD=docker
    ENV POSTGRES_DB=gis

    # Expose the PostgreSQL port
    EXPOSE 5432

    # Volume configuration
    VOLUME ["/var/lib/postgresql/data", "/geodata"]

    # Set the default command to run when starting the container
    CMD ["postgres"]

