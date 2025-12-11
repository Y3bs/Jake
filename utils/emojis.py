import discord

EMOJIS = {}

async def load_emojis(bot: discord.Client) -> int:
    """Populate the global emoji cache and return how many entries were loaded."""
    global EMOJIS
    EMOJIS.clear()

    try:
        emoji_list = await bot.fetch_application_emojis()
    except discord.HTTPException:
        emoji_list = []

    for emoji in emoji_list:
        EMOJIS[emoji.name] = emoji

    for guild in bot.guilds:
        for emoji in getattr(guild, "emojis", []):
            EMOJIS.setdefault(emoji.name, emoji)

    return len(EMOJIS)
