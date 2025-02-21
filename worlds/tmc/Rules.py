from worlds.generic.Rules import add_rule

from . import StateLogic
from .Constants import LocationName


def set_rules(world: "MinishCapWorld", excluded):
    add_rule(
        world.get_location(LocationName.MINISH_VILLAGE_BARREL_HOUSE), lambda state: StateLogic.canAttack(state, world.player)
    )

    add_rule(
        world.get_location(LocationName.DWS_GUST_JAR), lambda state: state.has("Jabber Nut", world.player)
    )

    add_rule(
        world.get_location(LocationName.DWS_MADDERPILLAR_HEART_PIECE), lambda state: state.has("Gust Jar", world.player)
    )

    add_rule(
        world.get_location(LocationName.DWS_2F_RED_RUPEE), lambda state: state.has("Gust Jar", world.player)
    )

    add_rule(
        world.get_location(LocationName.DWS_BOSS_HEART_CONTAINER), lambda state: state.has("Gust Jar", world.player)
    )

    add_rule(
        world.get_location("DWS - Green ChuChu"), lambda state: state.has("Gust Jar", world.player)
    )
