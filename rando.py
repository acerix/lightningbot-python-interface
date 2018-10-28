#!/usr/bin/env python3

from LightningBot import LightningBot
from random import randint

bot = LightningBot('Random' + '%04d' % randint(0, 9999))

move_direction = randint(0, 3)

while bot.waitForNextTurn():

  turn_direction = -1 if randint(0, 1) == 0 else 1

  move_direction = (move_direction + turn_direction) % 4

  bot.move(move_direction)
