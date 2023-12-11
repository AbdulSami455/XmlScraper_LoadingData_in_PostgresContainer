# Use an official PostgreSQL image with Alpine Linux as the base
FROM postgres:alpine

# Set environment variables
ENV POSTGRES_PASSWORD=pass
ENV POSTGRES_HOST_AUTH_METHOD=trust

# Copy scripts into the container
COPY psql_search_masha.sh /psql_search_masha.sh
COPY parserMasha.py /parserMasha.py

# Set working directory
WORKDIR /

# Expose PostgreSQL default port
EXPOSE 5432
