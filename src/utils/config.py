import sys
import json
from typing import List
from src.utils.logger import Logger
from src.constants.main import CONFIG_FILEPATH
from src.interfaces.main import CEO

def load_config():
    logger = Logger("Config loader")
    try:
        logger.info(f"Loading configuration from {CONFIG_FILEPATH}")
        with open(CONFIG_FILEPATH, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError as e:
        logger.error(f"Error: The configuration file was not found - {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Error: Failed to parse the configuration file - {e}")
        sys.exit(1)

def get_ceo_by_config_name(ceos: List[CEO], selected_ceo_name: str) -> CEO:
    ceo = next((ceo for ceo in ceos if ceo["name"] == selected_ceo_name), None)
    
    if ceo is None:
        print("Error: CEO not found")
        sys.exit(1)
    
    return ceo