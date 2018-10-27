#!/usr/bin/env python3

from LightningBot import LightningBot
from random import randint

bot = LightningBot('Spiral' + '%04d' % randint(0, 9999))

move_direction = randint(0, 3)
turn_direction = -1 if randint(0, 1) == 0 else 1

side_length = 0
turn_after = -1
turn_number = 0

while bot.waitForNextTurn():

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
