#!/usr/bin/env python3

# Turn whichever way leads to the longest possible path, or go straight if there's a tie

from LightningBot import LightningBot
from random import randint

bot = LightningBot(
  bot_name = 'Depth' + '%04d' % randint(0, 9999),
)

while bot.waitForNextTurnDirections():

  bot.move(bot.directionToLongestPath())
