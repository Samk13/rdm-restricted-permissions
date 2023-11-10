#!/bin/bash

# invenio roles create community-manager
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

# Run the desired command with the email
invenio roles add "$1" community-manager