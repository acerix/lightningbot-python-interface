#!/usr/bin/env python3

from LightningBot import LightningBot
from random import randint
from pprint import pprint
from sys import argv

bot = LightningBot(
  bot_name = 'Swerve' + '%04d' % randint(0, 9999),
  api_token = argv[1] if len(argv) > 1 else None,
)

move_direction = randint(0, 3)
#turn_preference = -1 if randint(0, 1) == 0 else 1
turn_preference = -1

while bot.waitForNextTurnDirections():

  last_position = bot.game_bots[bot.bot_name]['position'][:]
  original_move_direction = move_direction

  # If next position is blocked
  if bot.positionIsBlocked(bot.tiles, bot.getNextPosition(last_position, move_direction)) or randint(0, 420) == 0:
    # Swerve
    move_direction = bot.rotateMoveDirection(original_move_direction, turn_preference)

  # If swerved position is blocked
  if bot.positionIsBlocked(bot.tiles, bot.getNextPosition(last_position, move_direction)):
    # Swerve the other way!
    move_direction = bot.rotateMoveDirection(original_move_direction, -1 * turn_preference)

  # If all options position are blocked
  if bot.positionIsBlocked(bot.tiles, bot.getNextPosition(last_position, move_direction)):
    print('No moves left')
    # Go straight
    move_direction = original_move_direction
    turn_preference = -1 if randint(0, 1) == 0 else 1
    # Surrender
    exit()

  bot.move(move_direction)
