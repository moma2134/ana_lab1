#!/bin/bash

# Variables
source_folder="/home/ana-moeez-2/lab4/updated_startup_configs/*"  # Specify the path to the source folder with wildcard
destination_machine="ana-moeez-1@192.168.1.81"  # Replace with the appropriate user and IP of the destination machine
destination_folder="/home/ana-moeez-1/lab1/"  # Specify the path to the destination folder

# Copy the files to the destination machine
scp $source_folder $destination_machine:$destination_folder

# Check if the copy was successful
if [ $? -eq 0 ]; then
    echo "Files copied successfully to the remote machine."
else
    echo "Error in copying the files to the remote machine."
fi
