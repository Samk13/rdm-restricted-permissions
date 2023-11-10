#!/bin/bash

# Load variables from .env file
source .env

# Authenticate with Azure (assuming you're already logged in and have access to the registry)
az acr login --name $CONTAINER_REGISTRY

# Fetch the list of tags from Azure ACR and sort them
newest_tag=$(az acr repository show-tags --name $CONTAINER_REGISTRY --repository $REPOSITORY_NAME --orderby time_desc --output tsv | head -n 1)

echo "Selected base image tag: $newest_tag"
# Export the tag as an environment variable
#export IMAGE_TAG=$newest_tag

# Update the .env file with the newest tag
sed -i "s/IMAGE_TAG=.*/IMAGE_TAG=\"$newest_tag\"/" .env
