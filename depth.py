#!/usr/bin/env python3

from LightningBot import LightningBot
from random import randint

bot = LightningBot('Depth' + '%04d' % randint(0, 9999))

while bot.waitForNextTurnDirections():

  bot.move(bot.directionToLongestPath())
