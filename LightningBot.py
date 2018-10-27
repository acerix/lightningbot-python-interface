import random
import requests
import json
import time
from datetime import datetime, timezone, timedelta
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

  def __init__(self, bot_name=None, api_token=None):

    # "None" for random name
    self.bot_name = bot_name

    # "None" for test mode
    self.api_token = api_token

    # Unix timestamp for the end of the turn
    self.next_turn_start_time = datetime.fromtimestamp(0)

    # Persist connection
    self.session = requests.Session()

    # Minimum round trip time of server requests in seconds
    self.latency = timedelta(milliseconds=50)

    # Turn number, first actual turn is 1
    self.turn_number = -1

    # Games settings
    self.game_name = None
    self.game_size = None

    # List of bots in the game
    self.game_bots = {}

    # Last position
    self.position = None

    # Last move direction
    self.move_direction = -1

    # Get token from server
    if self.api_token is None:
      self.api_url = self.TEST_API_URL
      self.api_token = self.getToken()
      print('Token:', self.api_token)

    # Connect with existing token
    else:
      self.api_url = self.RANKED_API_URL
      self.bot_name = self.connect()

    print('Pseudo:', self.bot_name)

    # Wait for game to start
    self.waitForNextTurn()

    # Get game info from server
    self.game_info = self.getGameInfo()


  # Sleep until the end of the turn
  def waitForNextTurn(self):

    if self.next_turn_start_time > datetime.now():
      seconds_to_sleep = (self.next_turn_start_time - datetime.now()).total_seconds()
      print('Waiting ' + str(seconds_to_sleep) + ' seconds until the next phase...')
      time.sleep(seconds_to_sleep)

    self.turn_number += 1

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

    print('Requesting token...')
    response_data = self.request('connect', self.bot_name)

    return response_data['token']

  # Connect to a game with registered token, ie. login to ranked server
  def connect(self):

    print('Connecting to game...')
    response_data = self.request('connect', self.api_token)
    #pprint(response_data)

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

    self.game_bots = {}

    for bot in response_data['positions']:
      self.game_bots[bot['pseudo']] = {
        'position': [bot['x'], bot['y']]
      }

    print('Bots')
    pprint(self.game_bots)

    if self.bot_name not in self.game_bots:
      raise Exception('Starting position not found')


    print('Starting Position:', self.position)

    return response_data

  # Get directions of bots
  def getDirections(self):

    print('Requesting directions...')
    response_data = self.request('directions', self.api_token, str(self.turn_number))

    for bot in response_data['directions']:
      self.game_bots[bot['pseudo']]['direction'] = bot['direction']

    print('Bots')
    pprint(self.game_bots)

    return response_data

  # Submit direction for the current turn
  # 0: right, 1: down, 2: left, 3: up
  def move(self, move_direction):
    self.move_direction = move_direction
    print('Turn', self.turn_number, self.DIRECTION_NAMES[self.move_direction])
    response_data = self.request('move', self.api_token, str(self.move_direction), str(self.turn_number))
    #pprint(response_data)

