#!/bin/bash

# Run the mashaDockerTask container
sudo docker run --name mashaDockerTask --rm \
  -e POSTGRES_PASSWORD=pass \
  -e POSTGRES_HOST_AUTH_METHOD=trust \
  -p 5440:5432 -d postgres

# Sleep for a while to allow the PostgreSQL server to start
sleep 10

# Connect to the mashaDockerTask container and execute SQL commands
sudo docker exec -i mashaDockerTask psql -U postgres << EOF
CREATE ROLE wiki WITH LOGIN SUPERUSER PASSWORD 'wiki';
CREATE DATABASE wiki OWNER wiki;
\c wiki;
CREATE TABLE IF NOT EXISTS public.articles(id SERIAL PRIMARY KEY, title VARCHAR(128), content TEXT);
EOF

# Exit the script with success status
exit 0


