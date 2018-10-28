#!/usr/bin/env python3

from LightningBot import LightningBot
from random import randint
from sys import argv

bot = LightningBot(
  bot_name = 'Rando' + '%04d' % randint(0, 9999),
  api_token = argv[1] if len(argv) > 1 else None
)


move_direction = randint(0, 3)

while bot.waitForNextTurn():

  turn_direction = -1 if randint(0, 1) == 0 else 1

  move_direction = (move_direction + turn_direction) % 4

  bot.move(move_direction)
