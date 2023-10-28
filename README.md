# discord-bot-py
Discord Bot using discord.py library.

## Discord Battlepass
I wanted to create some sort of leveling system for users in my Discord server. The user can request 'points' and use them to either level up or purchase items 
from an inventory shop. The items and points have no real application, but I just wanted to make some sort of level system.

### Shop Inventory
I started the shop by creating a csv with item names, value, and 'rarity'. This worked fine until I wanted to refresh the shop items and only display set amounts of different rarities. 
`generate_shop_data.py` reads the `shop.csv` file and categorizes the items in a json file. Items can be added and removed at any time as long as `generate_shop_data.py` is run before 
starting the bot up again.

### Setting Up Simple Database for Users in Server
`database_setup.py` is ran to create db tables for user battlepass stats and item inventories. The commands can be edited to add or remove fields in the tables.

## YouTube Audio in Discord Voice Chat
`download_yt.py` uses the PyTube library to download the audio file of a YouTube video. I tried to stream the audio directly to the Discord voice connection, but only thirty seconds of the video would play. 
Since I use this for one server, I decided to download the audio file and play it from there instead of streaming. 
With only a handful of users submitting videos to play, it hasn't run into any major issues.

## Future Plans for Bot
- Stream audio instead of downloading
- Minimize code resuse (database interface)
- Host bot on a server instead of local machine
- Add more audio playback features (stop, skip, seek...)
