#!/bin/bash
# DO NOT USE IT IN PROD!

CONTAINER_NAME="kth-rdm-prod-worker-1"
# Find the container ID whose name starts with "CONTAINER_NAME"
container_id=$(docker ps --format "{{.ID}}\t{{.Names}}" | awk "/${CONTAINER_NAME}/ {print \$1}")    

# Check if the container ID was found
if [ -z "$container_id" ]; then
  echo "Container name provided '${CONTAINER_NAME}' not found, please check the name and try again."
  exit 1
fi

# Execute a script inside the container
docker exec -it $container_id bash -c './scripts/services_setup.sh'
echo "Import vocabularies ..."
docker exec -it $container_id bash -c './scripts/vocabularies_import.sh'