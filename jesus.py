#!/usr/bin/env python3

# Follow a cycle of turns

from LightningBot import LightningBot
from random import randint, shuffle

bot = LightningBot(
  bot_name = 'Christ' + '%04d' % randint(0, 9999),
)


move_direction = randint(0, 3)

# Cycle of turns to make
turn_path = [0, -1, 1, 1, -1, 1, 1, -1, 1, 1, -1, 0, -1]

# Randomize where in the cycle to start
cycle_offset = randint(0, len(turn_path))

# Reverse the direction
if randint(0, 1) == 0:
  turn_path = [i * -1 for i in reversed(turn_path)]

# First move
bot.waitForNextTurn()
bot.move(move_direction)

while bot.waitForNextTurnDirections():

  # Turn direction is based on position in cycle
  turn_direction = turn_path[(bot.turn_number + cycle_offset) % len(turn_path)]

  # Turn
  if turn_direction != 0:
    move_direction = (move_direction + turn_direction) % 4

  move_direction = bot.avoidLosingMove(move_direction)

  # Move
  bot.move(move_direction)
