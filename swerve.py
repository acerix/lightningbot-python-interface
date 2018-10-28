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

  print('Tiles:')

  # Display the tiles
  for y in reversed(list(zip(*tiles))):
    print( ''.join( ['   ' if x==0 else ' ● ' for x in y] ) )

  print('Position:', bot.game_bots[bot.bot_name]['position'])
  print('Default Direction:', move_direction)

  # Check where we'd end up after moving
  next_position = bot.game_bots[bot.bot_name]['position'][:]

  if move_direction == 0:
    next_position[0] = (next_position[0] + 1) % bot.game_size
  elif move_direction == 1:
    next_position[1] = (next_position[1] - 1) % bot.game_size
  elif move_direction == 2:
    next_position[0] = (next_position[0] - 1) % bot.game_size
  elif move_direction == 3:
    next_position[1] = (next_position[1] + 1) % bot.game_size

  # If next position is blocked
  if tiles[ next_position[0] ][ next_position[1] ]:
    # Swerve!
    print('Swerve!')
    move_direction = (move_direction + turn_preference) % 4

  # Check where we'd end up after moving @todo dedupe!
  next_position = bot.game_bots[bot.bot_name]['position'][:]

  if move_direction == 0:
    next_position[0] = (next_position[0] + 1) % bot.game_size
  elif move_direction == 1:
    next_position[1] = (next_position[1] - 1) % bot.game_size
  elif move_direction == 2:
    next_position[0] = (next_position[0] - 1) % bot.game_size
  elif move_direction == 3:
    next_position[1] = (next_position[1] + 1) % bot.game_size

  # If next position is blocked
  if tiles[ next_position[0] ][ next_position[1] ]:
    # Swerve the other way!
    print('Swerve!!!')
    move_direction = (move_direction - turn_preference - turn_preference) % 4

  print('Final Direction:', move_direction)

  bot.move(move_direction)
