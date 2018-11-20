#!/usr/bin/env python3

# Follow the wall which way leads to the longest possible path

from LightningBot import LightningBot
from random import randint

bot = LightningBot(
  bot_name = 'Waller' + '%04d' % randint(0, 9999),
)

while bot.waitForNextTurnDirections():

  bot.move(bot.directionToLongestWallPath())
