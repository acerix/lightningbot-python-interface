#!/usr/bin/env python3

# Make like a root and step down

from LightningBot import LightningBot
from random import randint
from sys import argv

bot = LightningBot(
  bot_name = 'StpDwn' + '%04d' % randint(0, 9999),
  api_token = argv[1] if len(argv) > 1 else None
)

while bot.waitForNextTurnDirections():

  # Move down on odd turns
  if bot.turn_number % 2 == 0:
    bot.move(1)

  # Left or right on even turns
  else:
    bot.move(randint(0, 1) * 2)
