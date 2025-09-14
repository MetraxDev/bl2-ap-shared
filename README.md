# BL2 Archipelago Shared Data

Shared data and utilities for Borderlands 2 Archipelago implementation.

This repository contains:
- Game data (regions, bosses, locations, collectibles)
- Data loading utilities
- Common constants and enums

## Usage

This repository is designed to be used as a git submodule in both:
- `bl2-apworld` - Archipelago APWorld implementation
- `bl2-ap-mod` - Borderlands 2 SDK mod

## Structure

```
bl2_data/
  __init__.py          # Package initialization
  data_loader.py       # Data loading functions
  constants.py         # Game constants
data/
  bl2_data.json        # Game data (regions, bosses, locations)
```

## Installation as Submodule

```bash
# In your project directory
git submodule add <repository-url> shared
git submodule update --init --recursive
```

## Usage in Code

```python
from shared.bl2_data.data_loader import get_all_locations, get_region_connections

# Load all game locations
locations = get_all_locations()

# Get region connection data
connections = get_region_connections()
```

## Updating Data

1. Edit `data/bl2_data.json`
2. Test changes with both APWorld and mod
3. Commit and tag new version
4. Update submodule in dependent projects