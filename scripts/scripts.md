# Scripts docs

## acr_pull_latest_tag

This script authenticates with Azure Container Registry (ACR), retrieves the latest image tag, and updates the IMAGE_TAG variable in the .env file.

Note: To use a different image tag, disable this functionality in run_full_container.sh.

## ignite_app.sh

Executes the following operations:
CONTAINER_NAME: change the value to identifies the container worker name.
Verifies the existence of the container ID.
Runs a specified script within the identified container.

## services_setup.sh

Cache Clearing
Drops all tables from the database
Creates all tables for the database
Destroys existing Opensearch indices
Initializes new Opensearch indices
Creates a default file location for the Invenio instance
Creates an 'admin' role
Grants superuser access to the 'admin' role
Installs fixtures data
Adds demo data
Activation of the admin user

## run_full_container

Pulls latest image tag from ACR
Starts containers
Initiates app commands
Restarts containers
