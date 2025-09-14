"""
Constants for BL2 Archipelago implementation
"""

# Base ID for all BL2 locations in Archipelago
BASE_ID = 3333000

# Location categories
CATEGORIES = [
    "bosses",
    "collectibles", 
    "discoveries"
]

# Category display names
CATEGORY_NAMES = {
    "bosses": "Boss",
    "collectibles": "Collectible",
    "discoveries": "Location"
}

# Default JSON data file path (relative to this package)
DEFAULT_DATA_PATH = "../data/bl2_data.json"