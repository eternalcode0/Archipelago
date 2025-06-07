from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from Fill import fill_restrictive
from .constants import DUNGEON_ABBR, TMCItem, TMCLocation
from .Locations import location_groups
from .Options import ShuffleElements

if TYPE_CHECKING:
    from . import MinishCapWorld


ELEMENT_LOCATIONS = frozenset({TMCLocation.DEEPWOOD_PRIZE, TMCLocation.COF_PRIZE, TMCLocation.DROPLETS_PRIZE,
                               TMCLocation.PALACE_PRIZE, TMCLocation.FORTRESS_PRIZE, TMCLocation.CRYPT_PRIZE})

BANNED_KEY_LOCATIONS = frozenset({TMCLocation.CRENEL_MELARI_NPC})
"""
A set of locations that dungeon filling should never place dungeon items at.
"""

ELEMENTS = frozenset({TMCItem.EARTH_ELEMENT, TMCItem.FIRE_ELEMENT, TMCItem.WATER_ELEMENT, TMCItem.WIND_ELEMENT})
"""
The list of elements that need placing when shuffle_elements is either
own_dungeon or vanilla. Order must be preserved to ensure they place onto the
same location for vanilla placement
"""

KEYS = frozenset({TMCItem.BIG_KEY_DWS, TMCItem.SMALL_KEY_DWS,
                  TMCItem.BIG_KEY_COF, TMCItem.SMALL_KEY_COF,
                  TMCItem.BIG_KEY_FOW, TMCItem.SMALL_KEY_FOW,
                  TMCItem.SMALL_KEY_TOD,
                  TMCItem.SMALL_KEY_RC,
                  TMCItem.BIG_KEY_POW, TMCItem.SMALL_KEY_POW,
                  TMCItem.BIG_KEY_DHC, TMCItem.SMALL_KEY_DHC})
"""
A list of keys to place, excluding ToD Big Key since that needs manual placement
to change the access rules.
"""

MAPS_COMPASSES = frozenset({TMCItem.DUNGEON_MAP_DWS, TMCItem.DUNGEON_COMPASS_DWS,
                            TMCItem.DUNGEON_MAP_COF, TMCItem.DUNGEON_COMPASS_COF,
                            TMCItem.DUNGEON_MAP_FOW, TMCItem.DUNGEON_COMPASS_FOW,
                            TMCItem.DUNGEON_MAP_TOD, TMCItem.DUNGEON_COMPASS_TOD,
                            TMCItem.DUNGEON_MAP_POW, TMCItem.DUNGEON_COMPASS_POW,
                            TMCItem.DUNGEON_MAP_DHC, TMCItem.DUNGEON_COMPASS_DHC})

def fill_dungeons(world: "MinishCapWorld"):
    multiworld = world.multiworld

    # Initialize collection state to assume player has all items except pre_filled items
    base_state = CollectionState(multiworld)
    for item in world.item_pool:
        base_state.collect(item)

    # Element Shuffle
    elements = list(map(world.create_item, [TMCItem.EARTH_ELEMENT, TMCItem.FIRE_ELEMENT, TMCItem.WATER_ELEMENT,
                                            TMCItem.WIND_ELEMENT]))
    # Create an element state that will have all the items from future pre_fill stages
    element_state = base_state.copy()
    for pre_fill_item in world.get_pre_fill_items():
        if pre_fill_item.name not in ELEMENTS:
            element_state.collect(pre_fill_item, prevent_sweep=True)
    element_state.sweep_for_advancements(multiworld.get_locations(world.player))

    if world.options.shuffle_elements.value is ShuffleElements.option_dungeon_prize:
        # Place elements into any "prize" location, shuffle locations
        locations = [world.get_location(element_loc) for element_loc in ELEMENT_LOCATIONS]
        world.random.shuffle(locations)
        # Don't allow excluded locations so that players can ban specific dungeons
        fill_restrictive(multiworld, element_state, locations, elements, single_player_placement=True, lock=True,
                         allow_excluded=False, name="TMC Element Fill")
    elif world.options.shuffle_elements.value is ShuffleElements.option_vanilla:
        # Place elements into ordered locations, don't shuffle
        locations = [world.get_location(TMCLocation.PALACE_PRIZE), world.get_location(TMCLocation.DROPLETS_PRIZE),
                     world.get_location(TMCLocation.COF_PRIZE), world.get_location(TMCLocation.DEEPWOOD_PRIZE)]
        fill_restrictive(multiworld, element_state, locations, elements, single_player_placement=True, lock=True,
                         allow_excluded=True, name="TMC Element Fill")

    # Big Key, Small Key, Maps & Compass Fill
    for stage in [KEYS, MAPS_COMPASSES]:
        # Randomized dungeon order (sets aren't ordered) but keep DHC last to ensure access conditions are met
        dungeon_fill_order = list(DUNGEON_ABBR)
        dungeon_fill_order.sort(key=lambda dungeon: 0 if dungeon != "DHC" else 1)
        for dungeon in dungeon_fill_order:
            fill_dungeon(world, dungeon, stage, base_state)


def fill_dungeon(world: "MinishCapWorld", dungeon: str, stage_items: set[str], base_state: CollectionState):
    multiworld = world.multiworld
    world_locations = multiworld.get_unfilled_locations(world.player)
    pre_fill_items = world.get_pre_fill_items()

    # Grab items from pre_fill list and filter to what's part of this dungeon & stage
    fill_stage_items = [item for item in pre_fill_items if item.name in stage_items and dungeon in item.name]
    if not fill_stage_items:
        return

    # Get list of locations that we can place items, filtered for current dungeon group
    fill_locations = [loc for loc in world_locations \
                      if loc.name in location_groups[dungeon] and loc.name not in BANNED_KEY_LOCATIONS]
    world.random.shuffle(fill_locations)
    world.random.shuffle(fill_stage_items)

    # Create a new collection state that collects all the already placed items
    dungeon_state = base_state.copy()
    dungeon_state.sweep_for_advancements(multiworld.get_locations(world.player))

    fill_restrictive(multiworld, dungeon_state, fill_locations, fill_stage_items, single_player_placement=True,
                     lock=True, allow_excluded=True, name=f"TMC Dungeon Fill: {dungeon}")
