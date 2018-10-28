#!/usr/bin/env bash

# Continuously reconnect after each game is over, or error

if [ -z "$1" ]
  then
    echo "Usage: ./auto_play.sh [bot script filename] [api token]"
    exit
fi

while [ 1 ]
do
  clear
  echo "Launching bot..."
  ./$1 $2
  sleep 0.1
done
