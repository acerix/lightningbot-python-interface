#!/usr/bin/env python3

# Move along a hilbert curve which fills the board

from LightningBot import LightningBot
from random import randint

bot = LightningBot(
  bot_name = 'Hilbert' + '%03d' % randint(0, 999),
)


# Return the direction to the next point in the hilbert curve
def directionToNextHilbertCurvePoint(game_size, position, direction):

  number_of_tiles = game_size * game_size

  # Find current position in hilbert curve
  for i in range(0, number_of_tiles):
    test_position = hilbertIndexToXY(i, game_size)
    if test_position[0] == position[0] and test_position[1] == position[1]:
      break

  next_point = hilbertIndexToXY( (i + direction) % number_of_tiles, game_size)

  # right
  if next_point[0] > position[0]:
    return 0
  # down
  if next_point[1] < position[1]:
    return 1
  # left
  if next_point[0] < position[0]:
    return 2
  # up
  if next_point[1] > position[1]:
    return 3

  raise Exception('Failed to determine direction')


# Return the last 2 bits of x
def lastTwoBits(x):
  return x & 3

# logical shift right (>>>)
def rshift(v, n):
  return (v % 0x100000000) >> n

# Return the coordinates from the hilbert curve index
# from https://marcin-chwedczuk.github.io/iterative-algorithm-for-drawing-hilbert-curve
def hilbertIndexToXY(index, N):

  positions = [
    [0, 0],
    [0, 1],
    [1, 1],
    [1, 0],
  ]

  tmp = positions[lastTwoBits(index)]

  index = rshift(index, 2)

  x = tmp[0]
  y = tmp[1]

  n = 4

  while n <= N:
    n2 = n / 2
    l2b = lastTwoBits(index)

    # case A: left-bottom
    if l2b == 0:
      tmp = x
      x = y
      y = tmp

    # case B: left-upper
    elif l2b == 1:
      x = x
      y = y + n2

    # case C: right-upper
    elif l2b == 2:
      x = x + n2
      y = y + n2

    # case D: right-bottom
    elif l2b == 3:
      tmp = y
      y = n2 - 1 - x
      x = n2 - 1 - tmp
      x = x + n2

    index = rshift(index, 2)
    n *= 2

  return [x, y]


#curve_direction = -1 if randint(0, 1) == 0 else 1
curve_direction = -1

while bot.waitForNextTurnDirections():

  move_direction = directionToNextHilbertCurvePoint(bot.game_size, bot.game_bots[bot.bot_name]['position'], curve_direction)

  # turn this off to get many hilbert bots to join eachothers ends
  move_direction = bot.avoidLosingMove(move_direction)

  bot.move(move_direction)
