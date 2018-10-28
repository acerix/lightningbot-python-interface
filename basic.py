#!/usr/bin/env python3

from LightningBot import LightningBot
from random import randint

# Initialize bot and connect to a game
bot = LightningBot(

  # Unique bot name for test server
  bot_name = 'Basic' + '%04d' % randint(0, 9999),

  # Or token for ranked server
  #api_token = '00000000000000000000',

)

# Choose a direction to start moving in
# 0: right, 1: down, 2: left, 3: up
move_direction = randint(0, 3)

# Wait until the "wait" time from the last response has passed
while bot.waitForNextTurn():

  # Get directions of players
  # bot_directions = bot.getDirections()

  # After crossing the board, avoid hitting self
  if bot.turn_number % bot.game_size == 0:
    bot.move((move_direction + 1) % 4)

  # Otherwise just move in this direction
  else:
    bot.move(move_direction)
