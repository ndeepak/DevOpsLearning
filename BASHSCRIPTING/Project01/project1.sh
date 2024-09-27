#!/bin/bash

# Description: This script reads quotes from a file and displays a random quote in red.

# Check if quotes.txt exists in the same directory as the script
if [ ! -f "quotes.txt" ]; then
    echo "Error: quotes.txt file not found!"
    exit 1
fi

# Read the quotes from the file into an array
IFS=$'\n' read -d '' -r -a ARRAY < quotes.txt

# Check if the array is not empty
if [ ${#ARRAY[@]} -eq 0 ]; then
    echo "Error: No quotes found in quotes.txt!"
    exit 1
fi

# Select a random quote from the array
RANDOM_QUOTE=${ARRAY[$RANDOM % ${#ARRAY[@]}]}

# Display the random quote in red color
echo -e "\e[31m$RANDOM_QUOTE\e[0m"
