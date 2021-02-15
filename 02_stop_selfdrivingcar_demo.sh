#!/bin/bash

# stop self-driving-car deme
echo "Stop iterm"
osascript -e 'quit app "iTerm"'

echo "Stop Simulator"
osascript -e 'quit app "Default Mac desktop Universal"'



# Stop local confluent platform
echo "Stop Confluent Platform 6.0..."
confluent local services stop
echo "Destroy Confluent Platform 6.0..."
confluent local destroy

echo "#########################################"
echo "####   Self-driving car demo stopped ####"
echo "#########################################"
