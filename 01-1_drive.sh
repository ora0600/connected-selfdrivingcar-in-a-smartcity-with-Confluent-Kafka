#!/bin/bash

# Set title
export PROMPT_COMMAND='echo -ne "\033]0;Self-Drive Service\007"'
echo -e "\033];Self-Drive Service\007"

# run pyhton drive.py
python3 drive.py
