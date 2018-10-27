#!/usr/bin/env python3

from LightningBot import LightningBot
from random import randint

bot = LightningBot('Spiral' + '%04d' % randint(0, 9999))

move_direction = randint(0, 3)

while bot.waitForNextTurn():

  bot.move(move_direction)
