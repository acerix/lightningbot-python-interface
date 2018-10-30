#!/usr/bin/env python3

# Continuously turn in one direction to make a spiral

from LightningBot import LightningBot
from random import randint
from sys import argv

bot = LightningBot(
  bot_name = 'Spiral' + '%04d' % randint(0, 9999),
  api_token = argv[1] if len(argv) > 1 else None
)

move_direction = randint(0, 3)
turn_direction = -1 if randint(0, 1) == 0 else 1

side_length = 0
turn_after = -1
turn_number = 0

while bot.waitForNextTurnDirections():

  # Go straight
  if side_length < turn_after:
    side_length += 1

  # Turn around the corner
  else:
    move_direction = (move_direction + turn_direction) % 4
    side_length = 0
    turn_number += 1
    if turn_number > 0 and turn_number % 2 == 1:
      turn_after += 1

  bot.move(move_direction)
