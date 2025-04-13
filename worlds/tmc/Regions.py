import typing

from BaseClasses import Region
from .constants import TMCRegion, TMCEvent, MinishCapLocation
from .Locations import all_locations

if typing.TYPE_CHECKING:
    from . import MinishCapWorld

def excluded_locations_by_region(region: str, disabled_locations: set[str]):
    return (loc for loc in all_locations if loc.region == region and loc.id not in disabled_locations)

def create_regions(world: "MinishCapWorld", disabled_locations: set[str]):
    menu_region = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)

    for region_key in list(TMCRegion):
        create_region(world, region_key, excluded_locations_by_region(region_key, disabled_locations))

def create_region(world: "MinishCapWorld", name, locations):
    ret = Region(name, world.player, world.multiworld)
    for location in locations:
        if location.name.value in world.disabled_locations:
            continue
        loc = MinishCapLocation(world.player, location.name.value, location.id, ret)
        ret.locations.append(loc)
    world.multiworld.regions.append(ret)
