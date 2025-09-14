"""
Constants for BL2 Archipelago implementation
"""

# Base ID for all BL2 locations in Archipelago
BASE_ID = 3333000

# Location categories (alphabetically sorted to match JSON structure)
CATEGORIES = [
    "bosses",
    "cult_symbols",
    "echos", 
    "fast_travel",
    "red_chests",
    "regions"
]

# Category display names
CATEGORY_NAMES = {
    "bosses": "Boss",
    "cult_symbols": "Cult Symbol",
    "echos": "ECHO Log",
    "fast_travel": "Fast Travel",
    "red_chests": "Red Chest",
    "regions": "Region Discovery"
}

# Category actions
CATEGORY_ACTIONS = {
    "bosses": "Kill",
    "cult_symbols": "Find",
    "echos": "Find",
    "fast_travel": "Unlock",
    "red_chests": "Open",
    "regions": "Discover"
}

# ID ranges per category (50 IDs each)
CATEGORY_ID_RANGES = {
    "bosses": (0, 49),
    "cult_symbols": (50, 99),
    "echos": (100, 149),
    "fast_travel": (150, 199),
    "red_chests": (200, 249),
    "regions": (250, 299)
}

# Region spacing (550 IDs between regions: 300 used + 250 buffer)
REGION_SPACING = 550
REGION_BUFFER = 250