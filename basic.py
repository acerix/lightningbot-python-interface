#!/usr/bin/env python3

from LightningBot import LightningBot
from random import randint
from sys import argv

# Initialize bot and connect to a game
bot = LightningBot(

  # Unique bot name for test server
  bot_name = 'Basic' + '%04d' % randint(0, 9999),

  # Or token for ranked server, supplied as first command line argument
  api_token = argv[1] if len(argv) > 1 else None
  #api_token = '00000000000000000000',

  # Disable the interactive output to run in the background or multiple bots in parallel in the same terminal
  #background_output = True,

)

# Choose a direction to start moving in
# 0: right, 1: down, 2: left, 3: up
move_direction = randint(0, 3)

# Wait until we have the directions for the next turn
while bot.waitForNextTurnDirections():

  # After crossing the board, avoid hitting self
  if bot.turn_number % bot.game_size == 0:
    bot.move((move_direction + 1) % 4)

  # Otherwise just move in this direction
  else:
    bot.move(move_direction)
