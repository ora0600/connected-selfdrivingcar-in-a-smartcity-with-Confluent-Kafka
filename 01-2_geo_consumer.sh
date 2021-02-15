#!/bin/bash

# set titke
export PROMPT_COMMAND='echo -ne "\033]0;Geo-Consumer\007"'
echo -e "\033];Geo-Consumer\007"

#start geo-consumer
python3 geo_consumer.py
