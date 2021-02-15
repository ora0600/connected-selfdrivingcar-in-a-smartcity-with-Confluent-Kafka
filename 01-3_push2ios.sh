#!/bin/bash
# set titke
export PROMPT_COMMAND='echo -ne "\033]0;Push Notifications\007"'
echo -e "\033];Push Notifications\007"

# push Notifications
python3 push2ios.py

