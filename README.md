# lightningbot-python-interface

A helper object to make Python 3 bots for lightningbot.tk.

## Getting Started

Clone this repo.

### Prerequisites

Python 3

### Running

Run a bot script to connect to the test server with that bot.

```
python3 basic.py
```

The game won't start unless there are at least 2 bots.

There's a script to run the same bot multiple times:

```
./parallel_play.sh hilbert.py 2
```

And this script makes the bot reconnect when the game is over to keep playing forever.

```
./auto_play.sh snowflake.py
```

## License

This project is licensed under the GNU General Public License - see the [LICENSE](LICENSE) file for details
