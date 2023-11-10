#!/bin/bash

# Check if the email argument is provided
if [ -z "$1" ]; then
    echo "Error: Please provide your email."
    exit 1
fi

# Validate the email format (a very basic check)
if [[ ! "$1" =~ ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$ ]]; then
    echo "Error: Invalid email format."
    exit 1
fi

CONTAINER_NAME="kth-rdm-v12-worker-1"
# Find the container ID whose name starts with "CONTAINER_NAME"
container_id=$(docker ps --format "{{.ID}}\t{{.Names}}" | awk "/${CONTAINER_NAME}/ {print \$1}")


# Check if the container ID was found
if [ -z "$container_id" ]; then
  echo "Container not found."
  exit 1
fi

echo selected container id -> $container_id

# Execute a script inside the container
docker exec -it $container_id bash -c "invenio access allow administration-access user $1"