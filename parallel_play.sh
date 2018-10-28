#!/usr/bin/env bash

# Runs multiple instances of the same bot times in parallel

if [ -z "$2" ]
  then
    echo "Usage: ./parallel_play.sh [bot script] [number of copies]"
    exit
fi

echo "Launching $2 bots..."

for i in $(seq $2)
do
  eval "./$1" &
  pids[${i}]=$! # store process ids
done

for pid in ${pids[*]}; do
  wait $pid
done

echo "Game over"
