#!/usr/bin/env python3

from LightningBot import LightningBot
from random import randint
from sys import argv

bot = LightningBot(
  bot_name = 'Loser' + '%05d' % randint(0, 99999),
  api_token = argv[1] if len(argv) > 1 else None
)

bot.move(-1)
