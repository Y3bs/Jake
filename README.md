# Jake Development

Make sure to install `discord.py` using this command so you can run the bot on your local machine.

## Installation
```bash
pip install -U "git+https://github.com/Rapptz/discord.py"
```

## Change Log

### v4.1
1. **Stats Integration**: Added current month stats on the main panel.
2. **Mobile Experience**: Added a copy button for in-channel for ez copy for mobile version of discord.
3. **Payment Tracking**: Added an option to the money modal which asks for the method the money got into.
4. **Visual Improvements**: Changed the coloring of the text of the payment methods and the after receving money message.

### v4.5


1. **New Game Support**: Added full support for **Arc Raiders**, including custom emojis and dedicated panel logging.
2. **Database Overhaul**: Migrated logging to a new `records` collection for unified transaction tracking.
3. **Smart Channel Routing**: Paid & Banned account notifications now automatically create and route to game-specific channels (e.g., `#bo7-banned`).
4. **Enhanced Detection**: Improved game detection logic for titles like Black Ops 7 and Marvel Rivals.
5. **System Polish**: Added persisted view handling and auto-updates for Arc Raiders panels.
