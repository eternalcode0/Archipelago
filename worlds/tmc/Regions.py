import typing

from BaseClasses import Region, Entrance
from .Constants.RegionName import TMCRegion
from .Locations import (
    MinishCapLocation,
    LocationData,
    south_field,
    castle_exterior,
    eastern_hills,
    lonlon,
    lower_falls,
    lake_hylia,
    minish_woods,
    trilby_highlands,
    western_woods,
    crenel,
    swamp,
    ruins,
    valley,
    dungeon_crypt,
    upper_falls,
    clouds,
    wind_tribe,
    dungeon_dws,
    dungeon_cof,
    dungeon_fow,
    dungeon_tod,
    dungeon_pow,
    sanctuary,
    dungeon_dhc,
    hyrule_town,
    north_field,
    vaati
)

if typing.TYPE_CHECKING:
    from . import MinishCapWorld

def create_regions(world: "MinishCapWorld"):
    menu_region = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)
    regions = {}

    create_region(world, TMCRegion.SOUTH_FIELD, south_field)
    create_region(world, TMCRegion.CASTLE_EXTERIOR, castle_exterior)
    create_region(world, TMCRegion.EASTERN_HILLS, eastern_hills)
    create_region(world, TMCRegion.LONLON, lonlon)
    create_region(world, TMCRegion.LOWER_FALLS, lower_falls)
    create_region(world, TMCRegion.LAKE_HYLIA, lake_hylia)
    create_region(world, TMCRegion.MINISH_WOODS, minish_woods)
    create_region(world, TMCRegion.TRILBY_HIGHLANDS, trilby_highlands)
    create_region(world, TMCRegion.WESTERN_WOODS, western_woods)
    create_region(world, TMCRegion.CRENEL, crenel)
    create_region(world, TMCRegion.SWAMP, swamp)
    create_region(world, TMCRegion.RUINS, ruins)
    create_region(world, TMCRegion.VALLEY, valley)
    create_region(world, TMCRegion.DUNGEON_CRYPT, dungeon_crypt)
    create_region(world, TMCRegion.UPPER_FALLS, upper_falls)
    create_region(world, TMCRegion.CLOUDS, clouds)
    create_region(world, TMCRegion.WIND_TRIBE, wind_tribe)
    create_region(world, TMCRegion.DUNGEON_DWS, dungeon_dws)
    create_region(world, TMCRegion.DUNGEON_COF, dungeon_cof)
    create_region(world, TMCRegion.DUNGEON_FOW, dungeon_fow)
    create_region(world, TMCRegion.DUNGEON_TOD, dungeon_tod)
    create_region(world, TMCRegion.DUNGEON_POW, dungeon_pow)
    create_region(world, TMCRegion.SANCTUARY, sanctuary)
    create_region(world, TMCRegion.DUNGEON_DHC, dungeon_dhc)
    create_region(world, TMCRegion.HYRULE_TOWN, hyrule_town)
    create_region(world, TMCRegion.NORTH_FIELD, north_field)
    create_region(world, "Vaati Fight", vaati)

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

    connect(world, names, TMCRegion.WESTERN_WOODS, TMCRegion.SWAMP)
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

    connect(world, names, TMCRegion.VALLEY, TMCRegion.DUNGEON_CRYPT)

    connect(world, names, TMCRegion.SWAMP, TMCRegion.RUINS)
    connect(world, names, TMCRegion.RUINS, TMCRegion.DUNGEON_FOW)

    connect(world, names, TMCRegion.LONLON, TMCRegion.MINISH_WOODS) # There isn't a direct connection but there's no checks going through Eastern Hills
    connect(world, names, TMCRegion.LONLON, TMCRegion.LAKE_HYLIA)
    connect(world, names, TMCRegion.LONLON, TMCRegion.LOWER_FALLS)

    connect(world, names, TMCRegion.LAKE_HYLIA, TMCRegion.DUNGEON_TOD)
    connect(world, names, TMCRegion.LAKE_HYLIA, TMCRegion.MINISH_WOODS)

    connect(world, names, TMCRegion.MINISH_WOODS, TMCRegion.DUNGEON_DWS, lambda state: state.has("Jabber Nut", world.player))
