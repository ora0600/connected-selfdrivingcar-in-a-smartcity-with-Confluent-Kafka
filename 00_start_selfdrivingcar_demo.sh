#!/bin/bash

# create self-driving car demo

wait-for-url() {
    echo "Testing $1"
    timeout -s TERM 500 bash -c \
    'while [[ "$(curl -s -o /dev/null -L -w ''%{http_code}'' ${0})" != "200" ]];\
    do echo "Waiting for ksql ${0}" && sleep 2;\
    done' ${1}
    echo "OK!"
    curl -I $1
}

pwd > basedir
export BASEDIR=$(cat basedir)
echo $BASEDIR

# Start Local CP 6.0
echo "Start Confluent Platform 6.0..."
confluent local services start


# Run KSQL Script
wait-for-url http://localhost:8088/info

echo "Run KSQL Scripts..."

echo "Run KSQL Scripts..."
echo "---Start Running KSQL scripts..."
echo "------KSQL statements 1..."
ksql http://ksql-server:8088 <<< "RUN SCRIPT 'scripts/ksql_statements1.sql';"
sleep 10
echo "------KSQL statements 2..."
ksql http://ksql-server:8088 <<< "RUN SCRIPT 'scripts/ksql_statements2.sql';"
sleep 10
echo "------KSQL statements 3..."
ksql http://ksql-server:8088 <<< "RUN SCRIPT 'scripts/ksql_statements3.sql';"

# open all terminals and Applications:
echo "open Simulator..."
open -a SelfDrivingCar-Simulator
echo "open all terminals..."
#Producer and Consumer Terminals
echo "Open all Terminals with iterm...."
open -a iterm
sleep 10
osascript 01_terminals.scpt $BASEDIR
echo "wait 2 minutes"
sleep 120
echo "open chrome as consumer..."
open -a "/Applications/Google Chrome.app" 'http://localhost:5001/topic/CONNECTEDCAR_S'
echo "open chrome as map..."
open -a "/Applications/Google Chrome.app" 'http://localhost:5001/'
echo "open chrome with Confluent Control Center..."
open -a "/Applications/Google Chrome.app" 'http://localhost:9021/'

echo "execute insert into ksqlDB cli"
cat scripts/ksql_inserts.sql
echo "####################################"
echo "####   ALL services started     ####"
echo "####################################"
