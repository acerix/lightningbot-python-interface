#!/usr/bin/env python3

# Move in a random direction

from LightningBot import LightningBot
from random import randint
from sys import argv

bot = LightningBot(
  bot_name = 'Rando' + '%04d' % randint(0, 9999),
)

move_direction = randint(0, 3)

while bot.waitForNextTurnDirections():

  turn_direction = randint(-1, 1)

  move_direction = (move_direction + turn_direction) % 4

  bot.move(move_direction)
