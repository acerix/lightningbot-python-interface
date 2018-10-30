#!/usr/bin/env python3

# Choose a random direction and move in that direction forever,
# but move one tile over when crossing the board so we don't hit our trail

from LightningBot import LightningBot
from random import randint

# Initialize bot and connect to a game
bot = LightningBot(

  # Unique bot name for test server
  bot_name = 'Basic' + '%04d' % randint(0, 9999),

  # Or token for ranked server, supplied as first command line argument
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

  # Otherwise just go straight
  else:

    # But avoid losing
    move_direction = bot.avoidLosingMove(move_direction)

    bot.move(move_direction)
