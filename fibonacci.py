#!/usr/bin/env python3

# Move straight by turn randomly when lengths in the fibonacci sequence
# are reached

from LightningBot import LightningBot
from random import randint
from sys import argv

bot = LightningBot(
  bot_name = 'Fibnci' + '%04d' % randint(0, 9999),
  api_token = argv[1] if len(argv) > 1 else None
)

move_direction = randint(0, 3)

fibonacci_numbers = [0, 1]
for i in range(2, 24):
  fibonacci_numbers.append(fibonacci_numbers[i-1]+fibonacci_numbers[i-2])

side_length = 0
turn_number = 0

while bot.waitForNextTurnDirections():

  # Go straight
  if side_length < fibonacci_numbers[turn_number]:
    side_length += 1

  # Turn
  else:
    turn_direction = -1 if randint(0, 1) == 0 else 1
    move_direction = (move_direction + turn_direction) % 4
    side_length = 0
    turn_number += 1

  bot.move(move_direction)
