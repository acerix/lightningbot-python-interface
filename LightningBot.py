import random
import requests
import json
import time
from datetime import datetime, timezone, timedelta
from os import system
from pprint import pprint

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

    # Only output log messages, no tiles, etc, useful to run in the background or multiple bots in the same terminal
    self.background_output = background_output

    # Unix timestamp for the end of the turn
    self.next_turn_start_time = datetime.fromtimestamp(0)

    # Persist connection
    self.session = requests.Session()

    # Minimum round trip time of server requests in seconds
    # Ping lightningbot.tk to measure your latency
    self.latency = timedelta(milliseconds=99)

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


  # Wait until we have direections for the next turn
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

      # Game is over
      if response_data['error'] == 2:
        print(response_data['description'])
        exit()

      # Bot won
      if response_data['error'] == 200:
        print(response_data['description'])
        exit()

      # Bot died
      if response_data['error'] == 201:
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

    print('Bots:')
    pprint(self.game_bots)

    if self.bot_name not in self.game_bots:
      raise Exception('Starting position not found')


    print('Starting Position:', self.position)

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
  def positionIsBlocked(self, tiles, position):

    if self.opponentsAreMovingToPosition(position):
      return True

    return tiles[ position[0] ][ position[1] ]


  # Rotate the move direction by an integer
  def rotateMoveDirection(self, move_direction, rotation):
    return (move_direction + rotation) % 4

