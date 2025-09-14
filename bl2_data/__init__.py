"""
BL2 Archipelago Shared Data Package

This package provides shared data and utilities for Borderlands 2 Archipelago implementation.
Used by both the APWorld and the BL2 SDK mod.
"""

from .data_loader import (
    # Core loading functions
    load_bl2_data,
    load_as_namespace,
    
    # Data access functions
    get_all_locations,
    get_region_connections,
    get_locations_by_region,
    get_locations_by_category,
    
    # Search functions
    find_location_by_name,
    find_location_by_id,
    
    # Category-specific functions
    get_bosses_only,
    get_discoveries_only,
    get_collectibles_only,
    
    # Utility functions
    get_region_names,
    get_base_id,
    validate_region_connections,
    
    # Archipelago integration
    create_location_table_for_archipelago,
    create_lookup_tables,
    
    # Statistics
    get_stats,
    print_stats
)

from .constants import (
    BASE_ID,
    CATEGORIES
)

__version__ = "1.0.0"
__all__ = [
    # Core functions
    "load_bl2_data",
    "load_as_namespace",
    
    # Data access
    "get_all_locations",
    "get_region_connections",
    "get_locations_by_region",
    "get_locations_by_category",
    
    # Search
    "find_location_by_name",
    "find_location_by_id",
    
    # Categories
    "get_bosses_only",
    "get_discoveries_only", 
    "get_collectibles_only",
    
    # Utilities
    "get_region_names",
    "get_base_id",
    "validate_region_connections",
    
    # Archipelago
    "create_location_table_for_archipelago",
    "create_lookup_tables",
    
    # Stats
    "get_stats",
    "print_stats",
    
    # Constants
    "BASE_ID",
    "CATEGORIES"
]