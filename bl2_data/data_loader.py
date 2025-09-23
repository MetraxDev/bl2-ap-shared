"""
Data loader for BL2 Archipelago shared data

Provides both functional and namespace-based access to game data loaded from JSON.
"""

import json
from types import SimpleNamespace
from typing import Dict, List, Any, Optional
from functools import lru_cache
from pathlib import Path
import pkgutil
import os

from .constants import (
    BASE_ID, REGION_CATEGORIES, REGION_CATEGORY_NAMES, REGION_CATEGORY_ACTIONS, 
    REGION_CATEGORY_ID_RANGES, REGION_SPACING
)

# Functional approach for data loading and processing
# @lru_cache(maxsize=1)
def load_bl2_data(json_path: Optional[str] = None) -> Dict[str, Any]:
    """Load raw JSON data (cached)"""

    bl2_data = pkgutil.get_data(__name__, "bl2_data.json")
    
    return json.loads(bl2_data)

# @lru_cache(maxsize=1)
def load_as_namespace(json_path: Optional[str] = None) -> SimpleNamespace:
    """Load data as namespace for dot notation access"""
    data = load_bl2_data(json_path)
    # print(data)
    
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
        
    locations = []
    for region_name, region_data in data["regions"].items():
        # Access locations through the new structure: region["locations"][category]
        for category in REGION_CATEGORIES:
            if category in region_data["locations"]:
                for item in region_data["locations"][category]:
                    locations.append({
                        **item,
                        "region": region_name,
                        "category": category,
                        "full_id": data["base_id"] + item["id"]
                    })
    return locations

def get_unlock_names(data: Optional[Dict] = None) -> List[str]:
    """Get list of all region names"""
    if data is None:
        data = load_bl2_data()
    return list(data["unlocks"].keys())

def get_unlocks(data: Optional[Dict] = None) -> List[Dict]:
    """Get list of all unlocks"""
    if data is None:
        data = load_bl2_data()

    unlocks = []
    for unlock_name, unlock_data in data["unlocks"].items():
        unlocks.append({
            **unlock_data,
            "name": unlock_name,
            "full_id": data["base_id"] + unlock_data["unlock_id"]
        })
        
    return unlocks

def get_unlocks_by_type(type: str, data: Optional[Dict] = None) -> List[Dict]:
    if data is None:
        data = load_bl2_data()

    unlocks = []
    for unlock_name, unlock_data in data["unlocks"].items():
        if unlock_data["type"] == type:
            unlocks.append({
                **unlock_data,
                "name": unlock_name,
                "full_id": data["base_id"] + unlock_data["unlock_id"]
            })
    
    return unlocks

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
    
    # Access locations through the new structure
    for category in REGION_CATEGORIES:
        if category in region_data["locations"]:
            for item in region_data["locations"][category]:
                locations.append({
                    **item,
                    "region": region_name,
                    "category": category,
                    "full_id": data["base_id"] + item["id"]
                })
    
    return locations

def get_locations_by_category(category: str, data: Optional[Dict] = None) -> Dict[str, Dict]:
    """Get all locations of a specific category"""
    all_locations = get_all_locations(data)
    return {loc["name"]: loc for loc in all_locations if loc["category"] == category}

def find_location_by_name(name: str, data: Optional[Dict] = None) -> Optional[Dict]:
    """Find a location by name across all regions"""
    all_locations = get_all_locations(data)
    for location in all_locations:
        if location["name"] == name:
            return location
    return None

def find_location_by_id(location_id: int, data: Optional[Dict] = None) -> Optional[Dict]:
    """Find a location by its ID"""
    all_locations = get_all_locations(data)
    for location in all_locations:
        if location["full_id"] == location_id:
            return location
    return None

def find_unlock_by_id(unlock_id: int, data: Optional[Dict] = None) -> Optional[Dict]:
    """Find a location by its ID"""
    all_unlocks = get_unlocks(data)
    for unlock in all_unlocks:
        if unlock["full_id"] == unlock_id:
            return unlock
    return None

# Category-specific functions for all 6 categories
def get_bosses_only(data: Optional[Dict] = None) -> Dict[str, Dict]:
    """Get only boss locations"""
    return get_locations_by_category("bosses", data)

def get_cult_symbols_only(data: Optional[Dict] = None) -> Dict[str, Dict]:
    """Get only cult symbol locations"""
    return get_locations_by_category("cult_symbols", data)

def get_echos_only(data: Optional[Dict] = None) -> Dict[str, Dict]:
    """Get only ECHO log locations"""
    return get_locations_by_category("echos", data)

def get_fast_travel_only(data: Optional[Dict] = None) -> Dict[str, Dict]:
    """Get only fast travel locations"""
    return get_locations_by_category("fast_travel", data)

def get_red_chests_only(data: Optional[Dict] = None) -> Dict[str, Dict]:
    """Get only red chest locations"""
    return get_locations_by_category("red_chests", data)

def get_regions_only(data: Optional[Dict] = None) -> Dict[str, Dict]:
    """Get only region discovery locations"""
    return get_locations_by_category("regions", data)

# Legacy function aliases for backward compatibility
def get_discoveries_only(data: Optional[Dict] = None) -> Dict[str, Dict]:
    """Get region discovery locations (legacy alias)"""
    return get_regions_only(data)

def get_collectibles_only(data: Optional[Dict] = None) -> Dict[str, Dict]:
    """Get collectible locations (legacy alias - returns cult symbols + echos + red chests)"""
    if data is None:
        data = load_bl2_data()
    
    collectibles = {}
    collectibles.update(get_cult_symbols_only(data))
    collectibles.update(get_echos_only(data))
    collectibles.update(get_red_chests_only(data))
    return collectibles

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

def get_region_data(region_name: str, data: Optional[Dict] = None) -> Optional[Dict]:
    """Get complete data for a specific region"""
    if data is None:
        data = load_bl2_data()
    return data["regions"].get(region_name)

def get_region_id(region_name: str, data: Optional[Dict] = None) -> Optional[int]:
    """Get the region_id for a specific region"""
    region_data = get_region_data(region_name, data)
    return region_data.get("region_id") if region_data else None

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

def validate_location_ids(data: Optional[Dict] = None) -> List[str]:
    """Validate that location IDs are within expected ranges for their categories"""
    if data is None:
        data = load_bl2_data()
    
    errors = []
    
    for region_name, region_data in data["regions"].items():
        region_id = region_data["region_id"]
        
        for category in REGION_CATEGORIES:
            if category in region_data["locations"]:
                min_id, max_id = REGION_CATEGORY_ID_RANGES[category]
                expected_min = region_id + min_id
                expected_max = region_id + max_id
                
                for item in region_data["locations"][category]:
                    item_id = item["id"]
                    if not (expected_min <= item_id <= expected_max):
                        errors.append(
                            f"Region '{region_name}' {category} '{item['name']}' "
                            f"has ID {item_id}, expected range {expected_min}-{expected_max}"
                        )
    
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
            "category": location_data["category"],
            "action": location_data.get("action", REGION_CATEGORY_ACTIONS.get(location_data["category"], "Unknown"))
        }
    
    return location_table

def create_lookup_tables(data: Optional[Dict] = None) -> tuple[Dict[int, str], Dict[str, int]]:
    """Create ID to name and name to ID lookup tables"""
    if data is None:
        data = load_bl2_data()
    
    all_locations = get_all_locations(data)
    base_id = data["base_id"]
    
    id_to_name = {base_id + loc["id"]: f'{loc["action"]} {loc["name"]}' for loc in all_locations}
    name_to_id = {f'{loc["action"]} {loc["name"]}': base_id + loc["id"] for loc in all_locations}
    
    return id_to_name, name_to_id

def create_id_to_name_lookup_table(data: Optional[Dict] = None) -> Dict[int, str]:
    """Create ID to name and name to ID lookup tables"""
    
    id_to_name, _ = create_lookup_tables()
    
    return id_to_name

def create_name_to_id_lookup_table(data: Optional[Dict] = None) -> Dict[str, int]:
    """Create ID to name and name to ID lookup tables"""
    
    _, name_to_id = create_lookup_tables()
    
    return name_to_id

def create_region_lookup_tables(data: Optional[Dict] = None) -> tuple[Dict[int, str], Dict[str, int]]:
    """Create region ID to name and name to region ID lookup tables"""
    if data is None:
        data = load_bl2_data()
    
    region_id_to_name = {}
    region_name_to_id = {}
    
    for region_name, region_data in data["regions"].items():
        region_id = region_data["region_id"]
        region_id_to_name[region_id] = region_name
        region_name_to_id[region_name] = region_id
    
    return region_id_to_name, region_name_to_id

# Statistics and debugging functions
def get_stats(data: Optional[Dict] = None) -> Dict[str, Any]:
    """Get statistics about the loaded data"""
    if data is None:
        data = load_bl2_data()
    
    all_locations = get_all_locations(data)
    
    # Get counts for each category
    category_counts = {}
    for category in REGION_CATEGORIES:
        category_locations = get_locations_by_category(category, data)
        category_counts[f"{category}_locations"] = len(category_locations)
    
    return {
        "total_regions": len(data["regions"]),
        "total_locations": len(all_locations),
        **category_counts,
        "base_id": data["base_id"]
    }

def print_stats(data: Optional[Dict] = None) -> None:
    """Print statistics about the loaded data"""
    stats = get_stats(data)
    print("BL2 Data Statistics:")
    print(f"  Total Regions: {stats['total_regions']}")
    print(f"  Total Locations: {stats['total_locations']}")
    
    for category in REGION_CATEGORIES:
        count_key = f"{category}_locations"
        if count_key in stats:
            category_name = REGION_CATEGORY_NAMES.get(category, category.title())
            print(f"  {category_name} Locations: {stats[count_key]}")
    
    print(f"  Base ID: {stats['base_id']}")

def print_region_summary(data: Optional[Dict] = None) -> None:
    """Print summary of all regions and their location counts"""
    if data is None:
        data = load_bl2_data()
    
    print("Region Summary:")
    for region_name, region_data in data["regions"].items():
        region_id = region_data["region_id"]
        total_locations = sum(len(region_data["locations"][cat]) for cat in REGION_CATEGORIES if cat in region_data["locations"])
        print(f"  {region_name} (ID: {region_id}): {total_locations} locations")
        
        for category in REGION_CATEGORIES:
            if category in region_data["locations"] and region_data["locations"][category]:
                count = len(region_data["locations"][category])
                category_name = REGION_CATEGORY_NAMES.get(category, category.title())
                print(f"    - {category_name}: {count}")

# Clear cache functions for testing/development
def clear_cache():
    """Clear the LRU cache for data loading functions"""
    load_bl2_data.cache_clear()
    load_as_namespace.cache_clear()