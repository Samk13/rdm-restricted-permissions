#!/bin/bash

# Exit if the number of arguments is not exactly 2
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <email> <role>"
    exit 1
fi

email=$1
role=$2

# Function to execute the command and check for errors
function add_role {
    output=$(invenio roles add "$email" "$role" 2>&1)
    if [[ $? -ne 0 ]]; then
        echo "Error: $output"
        return 1
    fi
    echo "$output"
    return 0
}

# Try to add the role
add_role

# If the command failed, prompt the user to create the role
if [[ $? -ne 0 ]]; then
    echo -n "Do you want to create the role '$role' and try again? (y/n) "
    read answer
    if [[ $answer == [Yy] ]]; then
        invenio roles create "$role"
        # Try to add the role again
        add_role
    fi
fi


# Title: User Role Assignment Script

# Description:
# This script facilitates the addition of roles to users within the Invenio framework. 
# It requires two arguments: an email address and a role name. Initially, it attempts to add the specified role to the user. 
# If the role doesn't exist, it prompts the user to create the role, and upon affirmation, 
# creates the role and then attempts the role addition again.

# Usage:
# Execute the script from the terminal followed by the email and role as arguments.

#     bash script_name.sh <email> <role>

# Arguments:
# <email> - The email address of the user to which the role is to be added.
# <role> - The name of the role to be added to the user.

# Example:
#     bash script_name.sh user@example.com admin

# This will try to add the 'admin' role to the user with the email 'user@example.com'. If the 'admin' role does not exist, it will prompt the user to create the role. If the user agrees by entering 'y' or 'Y', it creates the role and attempts to add the role to the user again.

# Error Handling:
# 1. If the arguments are not exactly two, the script will output a usage error message and exit.
# 2. If the role addition fails initially, the script outputs the error message and prompts the user to create the role.
# 3. If the role addition fails after creating the role, the script outputs the error message.

# Dependencies:
# The script depends on the 'invenio' command-line interface and assumes it's installed and configured properly in the environment where the script is executed.
