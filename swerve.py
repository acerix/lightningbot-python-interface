#!/usr/bin/env python3

# Go straight but turn before crashing or if an opponent is moving in front of you

from LightningBot import LightningBot
from random import randint
from pprint import pprint

bot = LightningBot(
  bot_name = 'Swerve' + '%04d' % randint(0, 9999),
)

move_direction = randint(0, 3)
#turn_preference = -1 if randint(0, 1) == 0 else 1
turn_preference = -1

while bot.waitForNextTurnDirections():

  last_position = bot.game_bots[bot.bot_name]['position'][:]
  original_move_direction = move_direction

  # If next position is blocked or randomly
  if bot.positionIsBlocked(bot.getNextPosition(last_position, move_direction)) or randint(0, 420) == 0:
    # Swerve
    move_direction = bot.rotateMoveDirection(original_move_direction, turn_preference)

  # If swerved position is blocked
  if bot.positionIsBlocked(bot.getNextPosition(last_position, move_direction)):
    # Swerve the other way!
    move_direction = bot.rotateMoveDirection(original_move_direction, -1 * turn_preference)

  move_direction = bot.avoidLosingMove(move_direction)

  bot.move(move_direction)
