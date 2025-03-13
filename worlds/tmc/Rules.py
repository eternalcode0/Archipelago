from typing import Union, Callable, Iterable, Dict
from worlds.generic.Rules import add_rule, CollectionRule
from BaseClasses import CollectionState

from . import StateLogic, Items
from .Items import ItemData
from .Constants.LocationName import TMCLocation

item_to_name = lambda item: item.item_name

def player_state(player: int):
    def has(item: ItemData, count: int = 1) -> CollectionRule:
        return lambda state: state.has(item.item_name, player, count)

    def has_all(items: Iterable[ItemData]) -> CollectionRule:
        return lambda state: state.has_all(map(item_to_name, items), player)

    def has_any(items: Iterable[ItemData]) -> CollectionRule:
        return lambda state: state.has_any(map(item_to_name, items), player)

    return {"has": has, "has_all": has_all, "has_any": has_any}

class PlayerState():
    player: int

    def __init__(self, player: int):
        self.player = player

    def has(item: ItemData, count: int = 1) -> CollectionRule:
        return lambda state: state.has(item.item_name, player, count)

    def has_all(items: Iterable[ItemData]) -> CollectionRule:
        return lambda state: state.has_all(map(item_to_name, items), player)

    def has_any(items: Iterable[ItemData]) -> CollectionRule:
        return lambda state: state.has_any(map(item_to_name, items), player)


def base_rules(player) -> Dict[str, Iterable[CollectionRule]]:
    p_state = PlayerState(player)
    has = p_state.has
    has_all = p_state.has_all
    has_any = p_state.has_any

    return {
        TMCLocation.SOUTH_FIELD_MINISH_SIZE_WATER_HOLE_HP: [p_state.has_all([Items.PEGASUS_BOOTS, Items.FLIPPERS])],
        TMCLocation.TOWN_WELL_LEFT_CHEST: [has(Items.MOLE_MITTS)],
        TMCLocation.TOWN_WELL_TOP_CHEST: [has(Items.BOMB_BAG)],
        TMCLocation.TOWN_WELL_BOTTOM_CHEST: [has_any([Items.ROCS_CAPE, Items.FLIPPERS])]
    }

def set_rules(world: "MinishCapWorld", excluded):
    def tmc_rule(location: str, rule: CollectionRule, combine: str = "and"):
        add_rule(world.get_location(location), rule, combine)

    # rules = base_rules(world.player)

    # for loc_name, loc_rules in rules.items():
    #     for loc_rule in loc_rules:
    #         tmc_rule(loc_name, loc_rule)

    add_rule(
        world.get_location(TMCLocation.MINISH_VILLAGE_BARREL_HOUSE_ITEM),
        lambda state: StateLogic.canAttack(state, world.player)
    )

    add_rule(
        world.get_location(TMCLocation.DEEPWOOD_1F_MADDERPILLAR_BIG_CHEST),
        lambda state: state.has(Items.JABBER_NUT.item_name, world.player)
    )

    add_rule(
        world.get_location(TMCLocation.DEEPWOOD_1F_MADDERPILLAR_HP),
        lambda state: state.has(Items.GUST_JAR.item_name, world.player)
    )

    add_rule(
        world.get_location(TMCLocation.DEEPWOOD_2F_CHEST),
        lambda state: state.has(Items.GUST_JAR.item_name, world.player)
    )

    add_rule(
        world.get_location(TMCLocation.DEEPWOOD_BOSS_ITEM),
        lambda state: state.has(Items.GUST_JAR.item_name, world.player)
    )

    add_rule(
        world.get_location(TMCLocation.DEEPWOOD_PRIZE),
        lambda state: state.has(Items.GUST_JAR.item_name, world.player)
    )
