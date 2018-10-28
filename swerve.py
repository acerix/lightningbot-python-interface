#!/usr/bin/env python3

from LightningBot import LightningBot
from random import randint
from pprint import pprint
from os import system
from sys import argv

bot = LightningBot(
  bot_name = 'Swerve' + '%04d' % randint(0, 9999),
  api_token = argv[1] if len(argv) > 1 else None
)

move_direction = randint(0, 3)
turn_preference = -1 if randint(0, 1) == 0 else 1

# array of tiles to keep track of which one are blocked
# 0 = unblocked, 1 = blocked
tiles = [ [0] * bot.game_size for _ in range(bot.game_size)]



while bot.waitForNextTurn():

  # Get directions/positions of players
  bot.getDirections()

  # Clear screen so output positions are consistent
  system('clear')

  print('Bots:')
  pprint(bot.game_bots)

  # Mark all the tiles with bots are blocked
  for bot_name, game_bot in bot.game_bots.items():
    tiles[ game_bot['position'][0] ][ game_bot['position'][1] ] = 1

  print('Position:', bot.game_bots[bot.bot_name]['position'])

  bot.printTiles(tiles)

  last_position = bot.game_bots[bot.bot_name]['position']

  # If next position is blocked
  if bot.positionIsBlocked(tiles, bot.getNextPosition(last_position, move_direction)):
    # Swerve
    print('Swerve!')
    move_direction = (move_direction + turn_preference) % 4

  # If swerved position is blocked
  if bot.positionIsBlocked(tiles, bot.getNextPosition(last_position, move_direction)):
    # Swerve the other way!
    print('Swerve back!!!')
    move_direction = (move_direction - turn_preference - turn_preference) % 4

  # If all options position are blocked
  if bot.positionIsBlocked(tiles, bot.getNextPosition(last_position, move_direction)):
    print('No moves left')
    move_direction = (move_direction + turn_preference) % 4
    #exit()

  bot.move(move_direction)
