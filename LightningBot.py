import random
import requests
import json
import time
from datetime import datetime, timezone, timedelta
from os import system
from pprint import pprint
from sys import argv

class LightningBot:
  """Python interface for lightingbot.tk"""

  TEST_API_URL = 'https://lightningbot.tk/api/test'
  RANKED_API_URL = 'https://lightningbot.tk/api'

  DIRECTION_NAMES = {
    -2: 'Dead',
    -1: 'Start',
    0: 'Right',
    1: 'Down',
    2: 'Left',
    3: 'Up',
  }

  def __init__(self, bot_name=None, api_token=None, background_output=False):

    # "None" for random name
    self.bot_name = bot_name

    # "None" for test mode
    self.api_token = api_token

    # Get token from command line arg
    if self.api_token is None and len(argv) > 1:
      self.api_token = argv[1]

    # Only output log messages, no tiles, etc, useful to run in the background or multiple bots in the same terminal
    self.background_output = background_output

    # Unix timestamp for the end of the turn
    self.next_turn_start_time = datetime.fromtimestamp(0)

    # Persist connection
    self.session = requests.Session()

    # Minimum round trip time of server requests in seconds
    # Ping lightningbot.tk to measure your latency
    self.latency = timedelta(milliseconds=75)

    # Turn number, first actual turn is 1
    self.turn_number = -1

    # Games settings
    self.game_name = None
    self.game_size = None

    # List of bots in the game
    self.game_bots = {}

    # 2d array of game tiles, False when open, True when blocked
    tiles = None

    # Last position
    self.position = None

    # Last move direction
    self.move_direction = -1

    # Get token from server
    if self.api_token is None:
      self.api_url = self.TEST_API_URL
      self.api_token = self.getToken()
      #print('Token:', self.api_token)

    # Connect with existing token
    else:
      self.api_url = self.RANKED_API_URL
      self.bot_name = self.connect()

    print('Bot Name:', self.bot_name)

    print('Game starts in ' + str( (self.next_turn_start_time - datetime.now()).total_seconds() ) + ' seconds...')

    # Wait for game to start
    self.waitForNextTurn()

    # Get game info from server
    self.game_info = self.getGameInfo()


  # Sleep until the end of the turn
  def waitForNextTurn(self):

    if self.next_turn_start_time > datetime.now():
      seconds_to_sleep = (self.next_turn_start_time - datetime.now()).total_seconds()
      #print('Waiting ' + str(seconds_to_sleep) + ' seconds until the next phase...')
      time.sleep(seconds_to_sleep)

    self.turn_number += 1

    return True


  # Wait until we have directions for the next turn
  def waitForNextTurnDirections(self):
    self.waitForNextTurn()
    self.getDirections()
    self.displayDirectionUpdate()

    return True


  # Send request to the server, return parsed json
  def request(self, method_name, *args):

    request_url = '/'.join([self.api_url, method_name, *args])
    #print(request_url)

    # Send request
    response = self.session.request('GET', request_url)

    # Parse response
    response_data = json.loads(response.text)

    # "the response also contains a description string that holds more details about the error, and an error code"
    if response_data['success'] is not True:

      # The request path is invalid.
      if response_data['error'] == 0:
        print('The request path is invalid.')
        print(response_data['description'])

      # A parameter is invalid.
      if response_data['error'] == 1:
        if response_data['description'] == 'The token is invalid.':
          print(response_data['description'])
          print('This probably means that no competitor joined before the room timed-out. Consider running 2 bots in parallel so they compete against each other.')
          exit()
        if response_data['description'] == 'The direction is invalid.':
          print(response_data['description'])
          print('Your bot tried to move backwards or surrendered.')
          exit()
        print('A parameter is invalid.')
        print(response_data['description'])

      # The requested phase is over.
      if response_data['error'] == 2:
        if response_data['description'] == 'The Connect phase is over.':
          print(response_data['description'])
          print('There\'s already a game in progress, try again when it\'s over.')
          exit()
        print('Game Over!')
        print(response_data['description'])
        exit()

      # The requested phase is not yet in progress.
      if response_data['error'] == 3:
        print('The requested phase is not yet in progress, moron.')
        print(response_data['description'])

      # The game is full, the 20 bots limit is reached.
      if response_data['error'] == 100:
        print('The game is full')
        print(response_data['description'])
        exit()

      # The token is already used in the game.
      if response_data['error'] == 101:
        print('The token is already used in the game.')
        print(response_data['description'])
        exit()

      # Bot won
      if response_data['error'] == 200:
        print('Winner!')
        print(response_data['description'])
        exit()

      # Bot died
      if response_data['error'] == 201:
        print('Died!')
        print(response_data['description'])
        exit()

      pprint(response_data)
      raise Exception('Request failed')

    # "failed to make a valid request in time, used an invalid token or an invalid path"
    if response_data['wait'] < 0:
      pprint(response_data)
      raise Exception('Kicked from game')

    # "the amount of time in milliseconds before the next phase"
    if response_data['wait'] > 0:
      # calculate when the next request should be sent
      self.next_turn_start_time = datetime.now() + timedelta(milliseconds=response_data['wait']) - self.latency

    return response_data

  # Get a one time token from the server, ie. login to test server
  def getToken(self):

    # Use random bot name
    if self.bot_name is None:
      self.bot_name = 'PyLB' + str(random.randint(0, 9999))

    print('Connecting to test game...')
    response_data = self.request('connect', self.bot_name)

    return response_data['token']

  # Connect to a game with registered token, ie. login to ranked server
  def connect(self):

    print('Connecting to ranked game...')
    response_data = self.request('connect', self.api_token)

    return response_data['pseudo']

  # Get info about the connected game
  def getGameInfo(self):

    print('Requesting game info...')
    response_data = self.request('info', self.api_token)

    self.turn_number = 0
    self.game_name = response_data['name']
    self.game_size = response_data['dimensions']

    print('Game:', self.game_name)
    print('Size:', self.game_size)

    # Make a 2d array of False's, which is game_size x game_size
    self.tiles = [[False] * self.game_size for _ in range(self.game_size)]

    self.game_bots = {}

    for bot in response_data['positions']:
      self.game_bots[bot['pseudo']] = {
        'position': [bot['x'], bot['y']]
      }
      game_bot = self.game_bots[bot['pseudo']]
      self.tiles[ game_bot['position'][0] ][ game_bot['position'][1] ] = True

    pprint(self.game_bots)

    if self.bot_name not in self.game_bots:
      raise Exception('Starting position not found')

    return response_data

  # Get directions of bots
  def getDirections(self):

    response_data = self.request('directions', self.api_token, str(self.turn_number))

    for bot in response_data['directions']:
      game_bot = self.game_bots[bot['pseudo']]
      game_bot['direction'] = bot['direction']

      # Update positions, only works if run once per move
      if bot['direction'] == 0:
        game_bot['position'][0] = (game_bot['position'][0] + 1) % self.game_size
      elif bot['direction'] == 1:
        game_bot['position'][1] = (game_bot['position'][1] - 1) % self.game_size
      elif bot['direction'] == 2:
        game_bot['position'][0] = (game_bot['position'][0] - 1) % self.game_size
      elif bot['direction'] == 3:
        game_bot['position'][1] = (game_bot['position'][1] + 1) % self.game_size

    # Mark all the tiles with bots as blocked
    for bot_name, game_bot in self.game_bots.items():
      self.tiles[ game_bot['position'][0] ][ game_bot['position'][1] ] = True

    return response_data

  # Submit direction for the current turn
  # 0: right, 1: down, 2: left, 3: up
  def move(self, move_direction):
    self.move_direction = move_direction
    response_data = self.request('move', self.api_token, str(self.move_direction), str(self.turn_number))
    #pprint(response_data)

  # Display a 2d array of tiles in the console
  def printTiles(self):
    for y in reversed(list(zip(*self.tiles))):
      print( ''.join( ['●' if x else '○' for x in y] ) )


  # Output updated direction info
  def displayDirectionUpdate(self):

    if self.background_output:
      print(
        self.bot_name,
        self.turn_number,
        self.game_bots[self.bot_name]['position'],
        self.DIRECTION_NAMES[self.move_direction],
      )

    else:
      self.refreshConsoleOutput()


  # Refresh the displayed output
  def refreshConsoleOutput(self):

    # Clear screen so output positions are consistent
    system('clear')

    print('Game:', self.game_name)
    print('Size:', self.game_size)
    print('Turn:', self.turn_number)
    print('')
    print('Bot Name:', self.bot_name)
    print('Position:', self.game_bots[self.bot_name]['position'])
    print('Direction:', self.DIRECTION_NAMES[self.move_direction])
    print('')
    pprint(self.game_bots)

    print('')
    self.printTiles()

    print('')
    print('Next phase starts in ' + str( (self.next_turn_start_time - datetime.now()).total_seconds() ) + ' seconds')


  # Get the position after moving
  def getNextPosition(self, last_position, move_direction):

    position = last_position[:]

    # Find where we'd end up after moving
    if move_direction == 0:
      position[0] = (position[0] + 1) % self.game_size
    elif move_direction == 1:
      position[1] = (position[1] - 1) % self.game_size
    elif move_direction == 2:
      position[0] = (position[0] - 1) % self.game_size
    elif move_direction == 3:
      position[1] = (position[1] + 1) % self.game_size

    return position


  # Count how many opponents will move to this position if they don't turn
  def opponentsAreMovingToPosition(self, position):

    opponents = 0

    for bot_name, game_bot in self.game_bots.items():
      if bot_name != self.bot_name:
        if self.getNextPosition(game_bot['position'], game_bot['direction']) == position:
          opponents += 1

    return opponents


  # Returns True if the position is blocked, False if empty
  def positionIsBlocked(self, position):

    if self.opponentsAreMovingToPosition(position):
      return True

    return self.tiles[ position[0] ][ position[1] ]


  # Rotate the move direction by an integer
  def rotateMoveDirection(self, move_direction, rotation):
    return (move_direction + rotation) % 4

  # Return the direction that leads to the longest possible path
  def directionToLongestPath(self):

    position = self.game_bots[self.bot_name]['position']
    direction = self.game_bots[self.bot_name]['direction']

    if direction < 0:
      return random.randint(0, 3)

    max_depth = 0
    max_depth_direction = direction

    for turn_direction in [0, -1, 1]:

      try_direction = (direction + turn_direction) % 4

      depth = self.longestPathDepth(position, try_direction, [], )

      print('turn', turn_direction, 'depth', depth)

      if depth > max_depth:
        max_depth = depth
        max_depth_direction = try_direction

    return max_depth_direction

  # Starting at `position`, and coming from `direction` return the longest path possible
  # blocked_tiles is a list of tiles that are blocked by our trail so far
  # needs to be more efficient before it can look far enough ahead to be useful...
  def longestPathDepth(self, position, direction, blocked_tiles, limit = 8):

    max_depth = 0

    new_position = self.getNextPosition(position, direction)
    new_blocked_tiles = blocked_tiles[:]
    new_blocked_tiles.append(new_position)

    for turn_direction in [0, -1, 1]:

      try_direction = (direction + turn_direction) % 4

      if new_position in blocked_tiles or self.positionIsBlocked(new_position) or limit == 0:
        depth = 0
      else:
        depth = 1 + self.longestPathDepth(new_position, try_direction, new_blocked_tiles, limit - 1)

      if depth > max_depth:
        max_depth = depth

    return max_depth


  # Return a list of directions which are open
  def allowedDirections(self):
    position = self.game_bots[self.bot_name]['position']
    direction = self.game_bots[self.bot_name]['direction']
    allowed_directions = []
    for try_direction in [0, 1, 2, 3]:
      if not self.positionIsBlocked(self.getNextPosition(position, try_direction)) and try_direction != (direction + 2) % 4:
        allowed_directions.append(try_direction)

    return allowed_directions


  # If the proposed move would lose the game, try to return a move which doesn't
  def avoidLosingMove(self, move_direction):

    direction = self.game_bots[self.bot_name]['direction']

    # Not allowed to go backwards
    if move_direction == (direction + 2) % 4 and self.move_direction > -1:
      print('Trying to go backwards!', move_direction, direction)

      # Reverse to fix
      return direction


    # Return the move if ok
    allowed_directions = self.allowedDirections()
    if move_direction in allowed_directions:
      return move_direction

    # Return the next found move that is ok
    for try_direction in [0, 1, 2, 3]:
      if try_direction in allowed_directions and try_direction != (direction + 2) % 4:
        return try_direction

    # Surrender
    #self.move(-1)
    raise Exception('No moves left, surrendering.')


  # Starting at `position`, and coming from `direction` return the longest path possible
  # blocked_tiles is a list of tiles that are blocked by our trail so far
  # needs to be more efficient before it can look far ahead to be useful...
  def longestWallPathDepth(self, position, direction, blocked_tiles, limit = 8):

    max_depth = 0

    new_position = self.getNextPosition(position, direction)
    new_blocked_tiles = blocked_tiles[:]
    new_blocked_tiles.append(new_position)

    for turn_direction in [0, -1, 1]:

      try_direction = (direction + turn_direction) % 4

      if new_position in blocked_tiles or self.positionIsBlocked(new_position) or limit == 0:
        depth = 0
      else:
        depth = 1 + self.longestPalongestWallPathDepththDepth(new_position, try_direction, new_blocked_tiles, limit - 1)

      if depth > max_depth:
        max_depth = depth

    return max_depth

  # Return the direction that leads to the longest possible path along a wall
  def directionToLongestWallPath(self):

    position = self.game_bots[self.bot_name]['position']
    direction = self.game_bots[self.bot_name]['direction']

    if direction < 0:
      return random.randint(0, 3)

    max_depth = 0
    max_depth_direction = direction

    for turn_direction in [0, -1, 1]:

      try_direction = (direction + turn_direction) % 4

      depth = self.longestWallPathDepth(position, try_direction, [], )

      print('turn', turn_direction, 'depth', depth)

      if depth > max_depth:
        max_depth = depth
        max_depth_direction = try_direction

    return max_depth_direction
