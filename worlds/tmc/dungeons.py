from typing import TYPE_CHECKING
from Fill import fill_restrictive
from BaseClasses import CollectionState

from .constants import DUNGEON_ABBR, TMCItem, MinishCapItem, DUNGEON_REGIONS, TMCLocation
from .Options import DungeonItem, ShuffleElements

if TYPE_CHECKING:
    from . import MinishCapWorld

DUNGEON_ITEMS = {
    "DWS": {
        "dungeon_big_keys": [TMCItem.BIG_KEY_DWS],
        "dungeon_small_keys": [TMCItem.SMALL_KEY_DWS] * 4,
        "dungeon_compasses": [TMCItem.DUNGEON_COMPASS_DWS],
        "dungeon_maps": [TMCItem.DUNGEON_MAP_DWS],
    },
    "CoF": {
        "dungeon_big_keys": [TMCItem.BIG_KEY_COF],
        "dungeon_small_keys": [TMCItem.SMALL_KEY_COF] * 2,
        "dungeon_compasses": [TMCItem.DUNGEON_COMPASS_COF],
        "dungeon_maps": [TMCItem.DUNGEON_MAP_COF],
    },
    "FoW": {
        "dungeon_big_keys": [TMCItem.BIG_KEY_FOW],
        "dungeon_small_keys": [TMCItem.SMALL_KEY_FOW] * 4,
        "dungeon_compasses": [TMCItem.DUNGEON_COMPASS_FOW],
        "dungeon_maps": [TMCItem.DUNGEON_MAP_FOW],
    },
    "ToD": {
        "dungeon_big_keys": [TMCItem.BIG_KEY_TOD],
        "dungeon_small_keys": [TMCItem.SMALL_KEY_TOD] * 4,
        "dungeon_compasses": [TMCItem.DUNGEON_COMPASS_TOD],
        "dungeon_maps": [TMCItem.DUNGEON_MAP_TOD],
    },
    "RC": {
        "dungeon_big_keys": [],
        "dungeon_small_keys": [TMCItem.SMALL_KEY_RC] * 3,
        "dungeon_compasses": [],
        "dungeon_maps": [],
    },
    "PoW": {
        "dungeon_big_keys": [TMCItem.BIG_KEY_POW],
        "dungeon_small_keys": [TMCItem.SMALL_KEY_POW] * 6,
        "dungeon_compasses": [TMCItem.DUNGEON_COMPASS_POW],
        "dungeon_maps": [TMCItem.DUNGEON_MAP_POW],
    },
    "DHC": {
        "dungeon_big_keys": [TMCItem.BIG_KEY_DHC],
        "dungeon_small_keys": [TMCItem.SMALL_KEY_DHC] * 5,
        "dungeon_compasses": [TMCItem.DUNGEON_COMPASS_DHC],
        "dungeon_maps": [TMCItem.DUNGEON_MAP_DHC],
    },
}

ELEMENT_LOCATIONS = frozenset({
    TMCLocation.DEEPWOOD_PRIZE,
    TMCLocation.COF_PRIZE,
    TMCLocation.DROPLETS_PRIZE,
    TMCLocation.PALACE_PRIZE,
    TMCLocation.FORTRESS_PRIZE,
    TMCLocation.CRYPT_PRIZE
})

BANNED_KEY_LOCATIONS = frozenset({
    TMCLocation.DEEPWOOD_PRIZE, TMCLocation.DEEPWOOD_BOSS_ITEM,
    TMCLocation.COF_PRIZE, TMCLocation.COF_BOSS_ITEM,
    TMCLocation.FORTRESS_PRIZE, TMCLocation.FORTRESS_BOSS_ITEM,
    TMCLocation.DROPLETS_PRIZE, TMCLocation.DROPLETS_BOSS_ITEM,
    TMCLocation.CRYPT_PRIZE,
    TMCLocation.PALACE_PRIZE, TMCLocation.PALACE_BOSS_ITEM,
})
"""
A set of locations that dungeon filling should never place dungeon items at.
Nobody wants to receive their Dungeon Map/Compass as the boss item.
"""

def fill_dungeons(world: "MinishCapWorld"):
    multiworld = world.multiworld
    # settings are in this order because `fill_restrictive` `pop`s them for the placement order.
    # Big Keys go first because ToD & PoW are a pain.
    settings = ["dungeon_compasses", "dungeon_maps", "dungeon_small_keys", "dungeon_big_keys"]
    items = {dungeon_key: [] for dungeon_key in DUNGEON_ABBR}

    for setting in settings:
        # If the setting is disabled, skip filling that item group
        if getattr(world.options, setting) == DungeonItem.option_anywhere:
            continue
        # Else add it all the items in that setting pool to the fill stage
        for dungeon in DUNGEON_ABBR:
            items[dungeon].extend(map(world.create_item, DUNGEON_ITEMS[dungeon][setting]))

    # Initialize collection state to assume player has all items except dungeon keys
    all_state = CollectionState(multiworld)
    collection = [all_state.collect(item) for item in multiworld.itempool if item.player == world.player]

    # Dungeon Keys/Maps/Compasses
    # Exclude DHC until Elements are placed
    for dungeon in ["DWS", "CoF", "FoW", "ToD", "RC", "PoW"]:
        fill_dungeon(world, dungeon, items[dungeon], all_state)

    # Element Shuffle
    # Place after the first 6 dungeons so that the prize locations are guaranteed reachable from the dungeon fill
    elements = list(map(world.create_item,
        [TMCItem.EARTH_ELEMENT, TMCItem.FIRE_ELEMENT, TMCItem.WATER_ELEMENT, TMCItem.WIND_ELEMENT])) # Order matters
    if world.options.shuffle_elements.value is ShuffleElements.option_own_dungeon:
        # Place elements into any "prize" location, shuffle locations
        locations = [loc for loc in world.get_locations() if loc.name in ELEMENT_LOCATIONS]
        world.random.shuffle(locations)
        # Don't allow excluded locations so that players can ban specific dungeons
        fill_restrictive(multiworld, all_state, locations, elements,
            single_player_placement=True, lock=True, allow_excluded=False, name="TMC Element Fill")
    elif world.options.shuffle_elements.value is ShuffleElements.option_original_dungeon:
        # Place elements into ordered locations, don't shuffle
        locations = []
        locations.append(world.get_location(TMCLocation.DEEPWOOD_PRIZE))
        locations.append(world.get_location(TMCLocation.COF_PRIZE))
        locations.append(world.get_location(TMCLocation.DROPLETS_PRIZE))
        locations.append(world.get_location(TMCLocation.PALACE_PRIZE))
        fill_restrictive(multiworld, all_state, locations, elements,
            single_player_placement=True, lock=True, allow_excluded=True, name="TMC Element Fill")

    # Fill DHC last since it needs the elements to be reachable
    fill_dungeon(world, "DHC", items["DHC"], all_state)

def fill_dungeon(world: "MinishCapWorld", dungeon: str, items: list[MinishCapItem], all_state: CollectionState):
    multiworld = world.multiworld
    locations = []
    for region in world.get_regions():
        if region.name not in DUNGEON_REGIONS[dungeon]:
            continue
        for loc in region.get_locations():
            if loc.item is not None or loc.name in BANNED_KEY_LOCATIONS:
                continue
            locations.append(loc)
    world.random.shuffle(locations)
    # locations = [loc for region in world.get_regions() for loc in region.get_locations() if region in DUNGEON_REGIONS[dungeon]]
    fill_restrictive(multiworld, all_state, locations, items,
        single_player_placement=True, lock=True, allow_excluded=True, name=f"TMC Dungeon Fill: {dungeon}")
