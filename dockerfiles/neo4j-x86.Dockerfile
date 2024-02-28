FROM --platform=linux/amd64 bitnami/neo4j:latest




# Expose the Neo4j ports
EXPOSE 7474 7687
# Set the default command to run when starting the container
CMD ["neo4j"]
