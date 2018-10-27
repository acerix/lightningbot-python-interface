#!/usr/bin/env python3

from LightningBot import LightningBot
from random import randint

bot = LightningBot('StpDwn' + '%04d' % randint(0, 9999))

while bot.waitForNextTurn():

  # Move down on odd turns
  if bot.turn_number % 2 == 0:
    bot.move(1)

  # Left or right on even turns
  else:
    bot.move(randint(0, 1) * 2)
