# storage.py
import json
import os
import datetime

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

# storage.py - Add these functions to your existing file

def save_arcraiders_panel(guild_id, panel_channel_id, logs_channel_id):
    """Save Arc Raiders panel info"""
    try:
        config = load_config()
        guild_key = str(guild_id)
        
        if guild_key not in config:
            config[guild_key] = {}
        
        # Store arc panel info
        config[guild_key]["arcraiders_panel"] = {
            "panel_channel_id": panel_channel_id,
            "logs_channel_id": logs_channel_id,
        }
        
        save_config(config)
        return True
    except Exception as e:
        print(f"Error saving Arc Raiders panel: {e}")
        return False

def get_arcraiders_panel(guild_id):
    """Get Arc Raiders panel info for a guild"""
    try:
        config = load_config()
        return config.get(str(guild_id), {}).get("arcraiders_panel")
    except Exception as e:
        print(f"Error getting Arc Raiders panel: {e}")
        return None

def has_arcraiders_panel(guild_id):
    """Check if guild already has an Arc Raiders panel"""
    try:
        config = load_config()
        guild_config = config.get(str(guild_id), {})
        
        # Check if we have arc panel info
        if "arcraiders_panel" in guild_config:
            panel_info = guild_config["arcraiders_panel"]
            # Verify channels might still exist
            if panel_info.get("panel_channel_id") and panel_info.get("logs_channel_id"):
                return True
        return False
    except Exception as e:
        print(f"Error checking Arc Raiders panel: {e}")
        return False

def cleanup_arcraiders_panel(guild_id):
    """Remove Arc Raiders panel info"""
    try:
        config = load_config()
        guild_key = str(guild_id)
        
        if guild_key in config and "arcraiders_panel" in config[guild_key]:
            del config[guild_key]["arcraiders_panel"]
            save_config(config)
            return True
        return False
    except Exception as e:
        print(f"Error cleaning up Arc Raiders panel: {e}")
        return False