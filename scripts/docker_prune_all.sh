#!/bin/bash
# Prune all except images
# DO NOT USE IN PROD!

invenio-cli services destroy  
docker system prune --volumes --force && docker container prune --force && docker network prune --force

