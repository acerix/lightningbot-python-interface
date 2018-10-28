#!/usr/bin/env bash

# Continuously reconnect after each game is over, or error

if [ -z "$1" ]
  then
    echo "Usage: ./auto_play.sh [bot script]"
    exit
fi

while [ 1 ]
do
  clear
  echo "Launching bot..."
  ./$1
  sleep 5
done
