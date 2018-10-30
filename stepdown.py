#!/usr/bin/env python3

# Make like a root and step down

from LightningBot import LightningBot
from random import randint

bot = LightningBot(
  bot_name = 'StpDwn' + '%04d' % randint(0, 9999),
)

step_direction = 3 if randint(0, 1) == 0 else 1

while bot.waitForNextTurnDirections():

  # Move down on odd turns
  if bot.turn_number % 2 == 0:
    move_direction = step_direction

  # Left or right on even turns
  else:
    move_direction = randint(0, 1) * 2

  move_direction = bot.avoidLosingMove(move_direction)

  bot.move(move_direction)

