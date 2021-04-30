#!/bin/bash
# set titke
export PROMPT_COMMAND='echo -ne "\033]0;Smart CIty Control Center - Admin ksqlDB cli - enter data here\007"'
echo -e "\033];Admin ksqlDB cli - enter data here\007"

# run ksqldb cli
$CONFLUENT_HOME/bin/ksql
