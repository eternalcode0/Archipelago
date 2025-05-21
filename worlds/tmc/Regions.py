import typing

from BaseClasses import Region
from .constants import ALL_REGIONS, MinishCapLocation, TMCRegion, TMCEvent
from .Locations import all_locations

if typing.TYPE_CHECKING:
    from . import MinishCapWorld


def excluded_locations_by_region(region: str, disabled_locations: set[str]):
    return (loc for loc in all_locations if loc.region == region and loc.id not in disabled_locations)


def create_regions(world: "MinishCapWorld", disabled_locations: set[str], disabled_dungeons: set[str]):
    menu_region = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)

    for region_key in ALL_REGIONS:
        create_region(world, region_key, excluded_locations_by_region(region_key, disabled_locations))

    dungeon_clears = {
        TMCRegion.DUNGEON_DWS_CLEAR: ("DWS", TMCEvent.CLEAR_DWS),
        TMCRegion.DUNGEON_COF_CLEAR: ("CoF", TMCEvent.CLEAR_COF),
        TMCRegion.DUNGEON_FOW_CLEAR: ("FoW", TMCEvent.CLEAR_FOW),
        TMCRegion.DUNGEON_TOD_CLEAR: ("ToD", TMCEvent.CLEAR_TOD),
        TMCRegion.DUNGEON_RC_CLEAR: ("RC", TMCEvent.CLEAR_RC),
        TMCRegion.DUNGEON_POW_CLEAR: ("PoW", TMCEvent.CLEAR_POW),
    }

    for clear, (dungeon, event) in dungeon_clears.items():
        # If the entire dungeon has been excluded, don't add the dungeon clear so players aren't expected to beat it
        if dungeon in disabled_dungeons:
            continue
        reg = world.get_region(clear)
        loc = MinishCapLocation(world.player, event, None, reg)
        loc.place_locked_item(world.create_event(event))
        reg.locations.append(loc)


def create_region(world: "MinishCapWorld", name, locations):
    ret = Region(name, world.player, world.multiworld)
    for location in locations:
        if location.name in world.disabled_locations:
            continue
        loc = MinishCapLocation(world.player, location.name, location.id, ret)
        ret.locations.append(loc)
    world.multiworld.regions.append(ret)
