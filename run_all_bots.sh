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

# Use losers for the rest of the 20
./loser.py &
./loser.py &
./loser.py &

./loser.py &
./loser.py &
./loser.py &
./loser.py &
./loser.py &
