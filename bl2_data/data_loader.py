"""
Data loader for BL2 Archipelago shared data

Provides both functional and namespace-based access to game data loaded from JSON.
"""

import json
from types import SimpleNamespace
from typing import Dict, List, Any, Optional
from functools import lru_cache
from pathlib import Path

from .constants import BASE_ID, CATEGORIES, DEFAULT_DATA_PATH

# Get the package directory for relative path resolution
PACKAGE_DIR = Path(__file__).parent

def _get_data_path(json_path: Optional[str] = None) -> Path:
    """Get the path to the JSON data file"""
    if json_path is None:
        return PACKAGE_DIR / DEFAULT_DATA_PATH
    return Path(json_path)

# Functional approach for data loading and processing
@lru_cache(maxsize=1)
def load_bl2_data(json_path: Optional[str] = None) -> Dict[str, Any]:
    """Load raw JSON data (cached)"""
    data_path = _get_data_path(json_path)
    
    with open(data_path, 'r') as f:
        return json.load(f)

@lru_cache(maxsize=1)
def load_as_namespace(json_path: Optional[str] = None) -> SimpleNamespace:
    """Load data as namespace for dot notation access"""
    data = load_bl2_data(json_path)
    
    def dict_to_namespace(d):
        if isinstance(d, dict):
            # Handle region names with spaces/special chars for dot notation
            clean_dict = {}
            for k, v in d.items():
                # Convert "Southern Shelf - Bay" -> "Southern_Shelf___Bay"
                clean_key = (k.replace(" ", "_")
                           .replace("-", "_")
                           .replace("'", "")
                           .replace("&", "and"))
                clean_dict[clean_key] = dict_to_namespace(v)
            return SimpleNamespace(**clean_dict)
        elif isinstance(d, list):
            return [dict_to_namespace(item) for item in d]
        return d
    
    return dict_to_namespace(data)

# Functional utilities for common operations
def get_all_locations(data: Optional[Dict] = None) -> Dict[str, Dict]:
    """Get flat dictionary of all locations across all regions"""
    if data is None:
        data = load_bl2_data()
    
    locations = {}
    for region_name, region_data in data["regions"].items():
        for category in CATEGORIES:
            for item in region_data[category]:
                locations[item["name"]] = {
                    **item,
                    "region": region_name,
                    "category": category,
                    "full_id": data["base_id"] + item["id"]
                }
    return locations

def get_region_connections(data: Optional[Dict] = None) -> Dict[str, List[str]]:
    """Get Archipelago-style region connections"""
    if data is None:
        data = load_bl2_data()
    return {name: region["connections"] for name, region in data["regions"].items()}

def get_locations_by_region(region_name: str, data: Optional[Dict] = None) -> List[Dict]:
    """Get all locations in a specific region"""
    if data is None:
        data = load_bl2_data()
    
    if region_name not in data["regions"]:
        return []
    
    region_data = data["regions"][region_name]
    locations = []
    
    for category in CATEGORIES:
        for item in region_data[category]:
            locations.append({
                **item,
                "region": region_name,
                "category": category,
                "full_id": data["base_id"] + item["id"]
            })
    
    return locations

def get_locations_by_category(category: str, data: Optional[Dict] = None) -> Dict[str, Dict]:
    """Get all locations of a specific category (bosses, collectibles, discoveries)"""
    all_locations = get_all_locations(data)
    return {name: loc for name, loc in all_locations.items() if loc["category"] == category}

def find_location_by_name(name: str, data: Optional[Dict] = None) -> Optional[Dict]:
    """Find a location by name across all regions"""
    all_locations = get_all_locations(data)
    return all_locations.get(name)

def find_location_by_id(location_id: int, data: Optional[Dict] = None) -> Optional[Dict]:
    """Find a location by its ID"""
    all_locations = get_all_locations(data)
    for location in all_locations.values():
        if location["id"] == location_id:
            return location
    return None

def get_bosses_only(data: Optional[Dict] = None) -> Dict[str, Dict]:
    """Get only boss locations"""
    return get_locations_by_category("bosses", data)

def get_discoveries_only(data: Optional[Dict] = None) -> Dict[str, Dict]:
    """Get only discovery locations"""
    return get_locations_by_category("discoveries", data)

def get_collectibles_only(data: Optional[Dict] = None) -> Dict[str, Dict]:
    """Get only collectible locations"""
    return get_locations_by_category("collectibles", data)

def get_region_names(data: Optional[Dict] = None) -> List[str]:
    """Get list of all region names"""
    if data is None:
        data = load_bl2_data()
    return list(data["regions"].keys())

def get_base_id(data: Optional[Dict] = None) -> int:
    """Get the base ID for location calculations"""
    if data is None:
        data = load_bl2_data()
    return data["base_id"]

def validate_region_connections(data: Optional[Dict] = None) -> List[str]:
    """Validate that all region connections reference existing regions"""
    if data is None:
        data = load_bl2_data()
    
    errors = []
    region_names = set(data["regions"].keys())
    
    for region_name, region_data in data["regions"].items():
        for connection in region_data["connections"]:
            if connection not in region_names:
                errors.append(f"Region '{region_name}' connects to non-existent region '{connection}'")
    
    return errors

# Convenience functions for Archipelago integration
def create_location_table_for_archipelago(data: Optional[Dict] = None) -> Dict[str, Dict]:
    """Create location table in the format expected by Archipelago"""
    all_locations = get_all_locations(data)
    
    # Convert to the format your current APWorld expects
    location_table = {}
    for name, location_data in all_locations.items():
        location_table[name] = {
            "region": location_data["region"],
            "code": location_data["id"],
            "category": location_data["category"]
        }
    
    return location_table

def create_lookup_tables(data: Optional[Dict] = None) -> tuple[Dict[int, str], Dict[str, int]]:
    """Create ID to name and name to ID lookup tables"""
    if data is None:
        data = load_bl2_data()
    
    all_locations = get_all_locations(data)
    base_id = data["base_id"]
    
    id_to_name = {base_id + loc["id"]: name for name, loc in all_locations.items()}
    name_to_id = {name: base_id + loc["id"] for name, loc in all_locations.items()}
    
    return id_to_name, name_to_id

# Statistics and debugging functions
def get_stats(data: Optional[Dict] = None) -> Dict[str, Any]:
    """Get statistics about the loaded data"""
    if data is None:
        data = load_bl2_data()
    
    all_locations = get_all_locations(data)
    bosses = get_bosses_only(data)
    discoveries = get_discoveries_only(data)
    collectibles = get_collectibles_only(data)
    
    return {
        "total_regions": len(data["regions"]),
        "total_locations": len(all_locations),
        "boss_locations": len(bosses),
        "discovery_locations": len(discoveries),
        "collectible_locations": len(collectibles),
        "base_id": data["base_id"]
    }

def print_stats(data: Optional[Dict] = None) -> None:
    """Print statistics about the loaded data"""
    stats = get_stats(data)
    print("BL2 Data Statistics:")
    print(f"  Total Regions: {stats['total_regions']}")
    print(f"  Total Locations: {stats['total_locations']}")
    print(f"  Boss Locations: {stats['boss_locations']}")
    print(f"  Discovery Locations: {stats['discovery_locations']}")
    print(f"  Collectible Locations: {stats['collectible_locations']}")
    print(f"  Base ID: {stats['base_id']}")

# Clear cache functions for testing/development
def clear_cache():
    """Clear the LRU cache for data loading functions"""
    load_bl2_data.cache_clear()
    load_as_namespace.cache_clear()