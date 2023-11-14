#!/bin/bash

# Run the first command and wait for it to finish
coverage run --omit="/usr/lib/*" unit_testing.py

# Once the first command has finished, run the second command
coverage report -m
