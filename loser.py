#!/usr/bin/env python3

# Lose on the first turn by breaking the rules

from LightningBot import LightningBot
from random import randint

bot = LightningBot(
  bot_name = 'Loser' + '%05d' % randint(0, 99999),
)

bot.move(-1)
