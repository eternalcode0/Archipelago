import typing

from BaseClasses import Region, Entrance
from .Constants.RegionName import TMCRegion, all_regions
from .Locations import MinishCapLocation, LocationData, all_locations

if typing.TYPE_CHECKING:
    from . import MinishCapWorld

def excluded_locations_by_region(region: str, disabled_locations: set[int]):
    return (loc for loc in all_locations if loc.region == region and loc.id not in disabled_locations)

def create_regions(world: "MinishCapWorld", disabled_locations: set[int]):
    menu_region = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)

    for region_key in all_regions:
        create_region(world, region_key, excluded_locations_by_region(region_key, disabled_locations))

    create_region(world, "Vaati Fight", [LocationData(None, "Defeat Vaati", "Vaati Fight", None, None, (0x2CA6, 0x02), 0x008B)])

def create_region(world: "MinishCapWorld", name, locations):
    ret = Region(name, world.player, world.multiworld)
    for location in locations:
        loc = MinishCapLocation(world.player, location.name, location.id, ret)
        if location.name in world.disabled_locations:
            continue
        ret.locations.append(loc)
    world.multiworld.regions.append(ret)

def connect(
    world: "MinishCapWorld",
    used_names: typing.Dict[str, int],
    source: str,
    target: str,
    rule: typing.Optional[typing.Callable] = None,
    reach: typing.Optional[bool] = False,
) -> typing.Optional[Entrance]:
    source_region = world.multiworld.get_region(source, world.player)
    target_region = world.multiworld.get_region(target, world.player)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (" " * used_names[target])

    connection = Entrance(world.player, name, source_region)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)
    return connection if reach else None

def connect_regions(world: "MinishCapWorld"):
    names: typing.Dict[str, int] = {}

    connect(world, names, "Menu", TMCRegion.SOUTH_FIELD)
    connect(world, names, TMCRegion.SOUTH_FIELD, TMCRegion.HYRULE_TOWN)
    connect(world, names, TMCRegion.SOUTH_FIELD, TMCRegion.EASTERN_HILLS) # lambda state: StateLogic.canPassTrees(state, world.player))
    connect(world, names, TMCRegion.SOUTH_FIELD, TMCRegion.WESTERN_WOODS)

    connect(world, names, TMCRegion.HYRULE_TOWN, TMCRegion.EASTERN_HILLS, lambda state: state.has("Bomb", world.player))
    connect(world, names, TMCRegion.HYRULE_TOWN, TMCRegion.NORTH_FIELD)
    connect(world, names, TMCRegion.HYRULE_TOWN, TMCRegion.TRILBY_HIGHLANDS)

    connect(world, names, TMCRegion.TRILBY_HIGHLANDS, TMCRegion.CRENEL)
    connect(world, names, TMCRegion.CRENEL, TMCRegion.DUNGEON_COF)

    connect(world, names, TMCRegion.EASTERN_HILLS, TMCRegion.MINISH_WOODS, lambda state: state.has("Bomb", world.player))
    connect(world, names, TMCRegion.EASTERN_HILLS, TMCRegion.LONLON)

    connect(world, names, TMCRegion.WESTERN_WOODS, TMCRegion.CASTOR_WILDS)
    connect(world, names, TMCRegion.WESTERN_WOODS, TMCRegion.TRILBY_HIGHLANDS)

    connect(world, names, TMCRegion.NORTH_FIELD, TMCRegion.LONLON) #, lambda state: StateLogic.canPassTrees(state, world.player))
    connect(world, names, TMCRegion.NORTH_FIELD, TMCRegion.CASTLE_EXTERIOR)
    connect(world, names, TMCRegion.NORTH_FIELD, TMCRegion.TRILBY_HIGHLANDS)
    connect(world, names, TMCRegion.NORTH_FIELD, TMCRegion.LOWER_FALLS)
    connect(world, names, TMCRegion.NORTH_FIELD, TMCRegion.VALLEY)

    connect(world, names, TMCRegion.CASTLE_EXTERIOR, TMCRegion.SANCTUARY)
    connect(world, names, TMCRegion.SANCTUARY, TMCRegion.DUNGEON_DHC, lambda state: state.has_all(["Earth Element", "Fire Element", "Water Element", "Wind Element"], world.player))
    connect(world, names, TMCRegion.DUNGEON_DHC, "Vaati Fight")

    connect(world, names, TMCRegion.LOWER_FALLS, TMCRegion.UPPER_FALLS)
    connect(world, names, TMCRegion.UPPER_FALLS, TMCRegion.CLOUDS)

    connect(world, names, TMCRegion.CLOUDS, TMCRegion.WIND_TRIBE)
    connect(world, names, TMCRegion.CLOUDS, TMCRegion.DUNGEON_POW)

    connect(world, names, TMCRegion.VALLEY, TMCRegion.DUNGEON_RC)

    connect(world, names, TMCRegion.CASTOR_WILDS, TMCRegion.RUINS)
    connect(world, names, TMCRegion.RUINS, TMCRegion.DUNGEON_FOW)

    connect(world, names, TMCRegion.LONLON, TMCRegion.MINISH_WOODS) # There isn't a direct connection but there's no checks going through Eastern Hills
    connect(world, names, TMCRegion.LONLON, TMCRegion.LAKE_HYLIA)
    connect(world, names, TMCRegion.LONLON, TMCRegion.LOWER_FALLS)

    connect(world, names, TMCRegion.LAKE_HYLIA, TMCRegion.DUNGEON_TOD)
    connect(world, names, TMCRegion.LAKE_HYLIA, TMCRegion.MINISH_WOODS)

    connect(world, names, TMCRegion.MINISH_WOODS, TMCRegion.DUNGEON_DWS, lambda state: state.has("Jabber Nut", world.player))
