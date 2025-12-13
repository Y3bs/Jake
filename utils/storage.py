# storage.py
import json
import os

CONFIG_FILE = "bot_config.json"

def save_panel_channel_id(guild_id, channel_id):
    """Save the panel channel ID for a guild"""
    try:
        config = load_config()
        if str(guild_id) not in config:
            config[str(guild_id)] = {}
        config[str(guild_id)]["panel_channel_id"] = channel_id
        save_config(config)
    except Exception as e:
        print(f"Error saving panel channel: {e}")

def get_panel_channel_id(guild_id):
    """Get the panel channel ID for a guild"""
    try:
        config = load_config()
        return config.get(str(guild_id), {}).get("panel_channel_id")
    except Exception as e:
        print(f"Error getting panel channel: {e}")
        return None

def load_config():
    """Load the config file"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except Exception:
        return {}

def save_config(config):
    """Save the config file"""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving config: {e}")