import typing

from . import StateLogic
from BaseClasses import Region, Entrance
from .Locations import (MinishCapLocation, LocationData, intro_town, intro_castle, smith_house, dungeon_dws, minish_village, goal)

if typing.TYPE_CHECKING:
    from . import MinishCapWorld

def create_regions(world: "MinishCapWorld"):
    menu_region = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)

    create_region(world, "Smith House", smith_house)
    create_region(world, "Intro Town", intro_town)
    create_region(world, "Intro Castle", intro_castle)
    create_region(world, "Minish Village", minish_village)
    create_region(world, "Deepwood Shrine", dungeon_dws)
    create_region(world, "DWS - Boss", goal)

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

    connect(world, names, "Menu", "Smith House")
    connect(world, names, "Menu", "Intro Town")
    connect(world, names, "Intro Town", "Intro Castle", lambda state: StateLogic.canShield(state, world.player))
    connect(world, names, "Intro Castle", "Minish Village", lambda state: StateLogic.canAttack(state, world.player))
    connect(world, names, "Minish Village", "Deepwood Shrine", lambda state: state.has("Jabber Nut", world.player))
    connect(world, names, "Deepwood Shrine", "DWS - Boss", lambda state: state.has("Gust Jar", world.player))
