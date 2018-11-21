#!/usr/bin/env bash

# Run one of every bot in parallel

./basic.py &
./cross.py &
./depth.py &
./fibonacci.py &
./hilbert.py &

./rando.py &
./snowflake.py &
./spiral.py &
./stepdown.py &
./swerve.py &

./trapper.py &
./waller.py &

# Use snowflakes for the rest of the 20

# delay connection since these are lower priority
sleep 0.1

./snowflake.py &
./snowflake.py &
./snowflake.py &

./snowflake.py &
./snowflake.py &
./snowflake.py &
./snowflake.py &
./snowflake.py &
