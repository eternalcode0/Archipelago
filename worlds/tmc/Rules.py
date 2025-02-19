from worlds.generic.Rules import add_rule

from . import StateLogic

def set_rules(world: "MinishCapWorld", excluded):
    add_rule(
        world.get_location("Castle Intro - Smith's Sword"), lambda state: StateLogic.canShield(state, world.player)
    )

    add_rule(
        world.get_location("Minish Village - Barrel"), lambda state: StateLogic.canAttack(state, world.player)
    )

    add_rule(
        world.get_location("DWS - Gust Jar"), lambda state: state.has("Jabber Nut", world.player)
    )

    add_rule(
        world.get_location("DWS - Heart Piece after Madderpillar"), lambda state: state.has("Gust Jar", world.player)
    )

    add_rule(
        world.get_location("DWS - Red Rupee Chest before Boss"), lambda state: state.has("Gust Jar", world.player)
    )

    add_rule(
        world.get_location("DWS - Boss Heart Container"), lambda state: state.has("Gust Jar", world.player)
    )

    add_rule(
        world.get_location("DWS - Green ChuChu"), lambda state: state.has("Gust Jar", world.player)
    )
