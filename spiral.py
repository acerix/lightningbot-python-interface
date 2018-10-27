#!/usr/bin/env python3

from LightningBot import LightningBot
from random import randint

bot = LightningBot('Spiral' + '%04d' % randint(0, 9999))

move_direction = randint(0, 3)
turn_direction = -1 if randint(0, 1) == 0 else 1

side_length = 0
turn_after = 1

while bot.waitForNextTurn():

  # Go straight
  if side_length < turn_after:
    bot.move(move_direction)
    side_length += 1

  # Turn right around the corner


  bot.move(move_direction)
