from worlds.generic.Rules import add_rule

from . import StateLogic
from .Constants.LocationName import TMCLocation


def set_rules(world: "MinishCapWorld", excluded):
    add_rule(
        world.get_location(TMCLocation.MINISH_VILLAGE_BARREL_HOUSE_ITEM), lambda state: StateLogic.canAttack(state, world.player)
    )

    add_rule(
        world.get_location(TMCLocation.DEEPWOOD_1F_MADDERPILLAR_BIG_CHEST), lambda state: state.has("Jabber Nut", world.player)
    )

    add_rule(
        world.get_location(TMCLocation.DEEPWOOD_1F_MADDERPILLAR_HP), lambda state: state.has("Gust Jar", world.player)
    )

    add_rule(
        world.get_location(TMCLocation.DEEPWOOD_2F_CHEST), lambda state: state.has("Gust Jar", world.player)
    )

    add_rule(
        world.get_location(TMCLocation.DEEPWOOD_BOSS_ITEM), lambda state: state.has("Gust Jar", world.player)
    )

    add_rule(
        world.get_location(TMCLocation.DEEPWOOD_PRIZE), lambda state: state.has("Gust Jar", world.player)
    )
