from typing import Union, Callable, Iterable, Dict
from worlds.generic.Rules import add_rule, CollectionRule
from BaseClasses import CollectionState

from . import Items
from .Items import ItemData
from .Constants.LocationName import TMCLocation

item_to_name = lambda item: item.item_name

class MinishCapRules():
    player: int
    world: "MinishCapWorld"
    connection_rules: dict[str, CollectionRule]
    region_rules: dict[str, CollectionRule]
    location_rules: dict[str, CollectionRule]

    def __init__(self, world: "MinishCapWorld") -> None:
        self.player = world.player
        self.world = world

        self.location_rules = {
            #region South Field
            # TMCLocation.SMITH_HOUSE_RUPEE: None,
            # TMCLocation.SMITH_HOUSE_SWORD: None,
            # TMCLocation.SMITH_HOUSE_SHIELD: None,
            TMCLocation.SOUTH_FIELD_MINISH_SIZE_WATER_HOLE_HP:
                [self.can_pass_trees, self.has_all([Items.PEGASUS_BOOTS, Items.FLIPPERS])],
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM1:
                self.can_pass_trees,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM2:
                self.can_pass_trees,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM3:
                self.can_pass_trees,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM4:
                self.can_pass_trees,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM5:
                self.can_pass_trees,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM6:
                self.can_pass_trees,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM7:
                self.can_pass_trees,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM8:
                self.can_pass_trees,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM9:
                self.can_pass_trees,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM10:
                self.can_pass_trees,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM11:
                self.can_pass_trees,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM12:
                self.can_pass_trees,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM13:
                self.can_pass_trees,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM14:
                self.can_pass_trees,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM15:
                self.can_pass_trees,
            TMCLocation.SOUTH_FIELD_FUSION_CHEST:
                self.can_pass_trees,
            TMCLocation.SOUTH_FIELD_TREE_FUSION_HP:
                self.can_pass_trees,
            TMCLocation.SOUTH_FIELD_MINISH_SIZE_WATER_HOLE_HP:
                [self.can_pass_trees, self.has_all([Items.FLIPPERS, Items.PEGASUS_BOOTS])],
            TMCLocation.SOUTH_FIELD_TINGLE_NPC:
                [self.can_pass_trees, self.has(Items.CANE_OF_PACCI)],
            #endregion

            #region Castle Gardens
            TMCLocation.CASTLE_MOAT_LEFT_CHEST:
                self.has(Items.FLIPPERS),
            TMCLocation.CASTLE_MOAT_RIGHT_CHEST:
                self.has(Items.FLIPPERS),
            TMCLocation.CASTLE_GOLDEN_ROPE: # Fusions 3C
                self.can_attack,
            # TMCLocation.CASTLE_RIGHT_FOUNTAIN_FUSION_HP: # Fusions 18
            # TMCLocation.CASTLE_DOJO_HP: None,
            TMCLocation.CASTLE_DOJO_NPC:
                [self.has(Items.LANTERN),
                lambda state: self.swords(state) > 0],
            TMCLocation.CASTLE_RIGHT_FOUNTAIN_FUSION_MINISH_HOLE_CHEST: # Fusions 18
                self.has(Items.PEGASUS_BOOTS),
            TMCLocation.CASTLE_LEFT_FOUNTAIN_FUSION_MINISH_HOLE_CHEST: # Fusions 35
                self.has(Items.PEGASUS_BOOTS),
            #endregion

            #region Eastern Hills
            TMCLocation.HILLS_FUSION_CHEST:
                self.can_pass_trees,
            TMCLocation.HILLS_BEANSTALK_FUSION_LEFT_CHEST:
                None,
            TMCLocation.HILLS_BEANSTALK_FUSION_HP:
                None,
            TMCLocation.HILLS_BEANSTALK_FUSION_RIGHT_CHEST:
                None,
            TMCLocation.HILLS_BOMB_CAVE_CHEST:
                None,
            TMCLocation.MINISH_GREAT_FAIRY_NPC:
                None,
            TMCLocation.HILLS_FARM_DIG_CAVE_ITEM:
                None,
            #endregion

            #region Cloud Tops
            # TMCLocation.CLOUDS_FREE_CHEST: None,
            TMCLocation.CLOUDS_NORTH_EAST_DIG_SPOT:
                self.has(Items.MOLE_MITTS),
            TMCLocation.CLOUDS_NORTH_KILL:
                self.has_any([Items.ROCS_CAPE, Items.MOLE_MITTS]),
            TMCLocation.CLOUDS_SOUTH_KILL:
                self.has_any([Items.ROCS_CAPE, Items.MOLE_MITTS]),
            #endregion

            #region Wind Tribe
            # TMCLocation.WIND_TRIBE_1F_LEFT_CHEST: None,
            # TMCLocation.WIND_TRIBE_1F_RIGHT_CHEST: None,
            #endregion

            #region Hyrule Town
            # TMCLocation.TOWN_CAFE_LADY_NPC: None,
            # TMCLocation.TOWN_SHOP_80_ITEM: None,
            TMCLocation.TOWN_SHOP_300_ITEM:
                self.has(Items.BIG_WALLET),
            TMCLocation.TOWN_SHOP_600_ITEM:
                self.has(Items.BIG_WALLET, 3),
            TMCLocation.TOWN_SHOP_BEHIND_COUNTER_ITEM:
                self.access_town_left(),
            TMCLocation.TOWN_SHOP_ATTIC_CHEST:
                self.access_town_left(),
            TMCLocation.TOWN_BAKERY_ATTIC_CHEST:
                self.access_town_left(),
            TMCLocation.TOWN_INN_BACKDOOR_HP:
                self.has_any([Items.ROCS_CAPE, Items.FLIPPERS, Items.CANE_OF_PACCI]),
            TMCLocation.TOWN_INN_LEDGE_CHEST:
                self.has(Items.LANTERN),
            # TMCLocation.TOWN_INN_POT: None,
            # TMCLocation.TOWN_WELL_RIGHT_CHEST: None,

            TMCLocation.TOWN_GORON_MERCHANT_1_LEFT:
                self.has(Items.BIG_WALLET),
            TMCLocation.TOWN_GORON_MERCHANT_1_MIDDLE: None,
            TMCLocation.TOWN_GORON_MERCHANT_1_RIGHT: None,
            TMCLocation.TOWN_DOJO_NPC_1:
                lambda state: self.swords(state) > 0,
            TMCLocation.TOWN_DOJO_NPC_2:
                lambda state: self.swords(state) > 1,
            TMCLocation.TOWN_DOJO_NPC_3:
                [lambda state: self.swords(state) > 0,
                self.has(Items.PEGASUS_BOOTS)],
            TMCLocation.TOWN_DOJO_NPC_4:
                [lambda state: self.swords(state) > 0,
                self.has(Items.ROCS_CAPE)],
            TMCLocation.TOWN_WELL_TOP_CHEST:
                lambda state: self.bombs(state) > 0,
            TMCLocation.TOWN_SCHOOL_ROOF_CHEST:
                self.has(Items.CANE_OF_PACCI),
            TMCLocation.TOWN_SCHOOL_PATH_FUSION_CHEST:
                self.has(Items.CANE_OF_PACCI),
            TMCLocation.TOWN_SCHOOL_PATH_LEFT_CHEST:
                [self.has(Items.CANE_OF_PACCI),
                self.split_rule(4)],
            TMCLocation.TOWN_SCHOOL_PATH_MIDDLE_CHEST:
                [self.has(Items.CANE_OF_PACCI),
                self.split_rule(4)],
            TMCLocation.TOWN_SCHOOL_PATH_RIGHT_CHEST:
                [self.has(Items.CANE_OF_PACCI),
                self.split_rule(4)],
            TMCLocation.TOWN_SCHOOL_PATH_HP:
                [self.has(Items.CANE_OF_PACCI),
                self.split_rule(4)],
            TMCLocation.TOWN_DIGGING_LEFT_CHEST:
                self.has(Items.MOLE_MITTS),
            TMCLocation.TOWN_DIGGING_TOP_CHEST:
                self.has(Items.MOLE_MITTS),
            TMCLocation.TOWN_DIGGING_RIGHT_CHEST:
                self.has(Items.MOLE_MITTS),
            TMCLocation.TOWN_WELL_LEFT_CHEST:
                self.has(Items.MOLE_MITTS),
            TMCLocation.TOWN_BELL_HP:
                self.has(Items.ROCS_CAPE),
            TMCLocation.TOWN_WATERFALL_FUSION_CHEST: # fusions 42
                self.has(Items.FLIPPERS),
            TMCLocation.TOWN_CARLOV_NPC:
                self.access_town_left(),
            TMCLocation.TOWN_WELL_BOTTOM_CHEST:
                self.has_any([Items.ROCS_CAPE, Items.FLIPPERS]),
            TMCLocation.TOWN_CUCCOS_LV_1_NPC:
                self.has_any([Items.ROCS_CAPE, Items.FLIPPERS]),
            TMCLocation.TOWN_JULLIETA_ITEM:
                [self.access_town_left(),
                self.has(Items.EMPTY_BOTTLE)],
            TMCLocation.TOWN_SIMULATION_CHEST:
                lambda state: self.swords(state) > 0,
            TMCLocation.TOWN_SHOE_SHOP_NPC:
                self.has(Items.WAKEUP_MUSHROOM),
            TMCLocation.TOWN_MUSIC_HOUSE_LEFT_CHEST:
                self.has(Items.CARLOV_MEDAL),
            TMCLocation.TOWN_MUSIC_HOUSE_MIDDLE_CHEST:
                self.has(Items.CARLOV_MEDAL),
            TMCLocation.TOWN_MUSIC_HOUSE_RIGHT_CHEST:
                self.has(Items.CARLOV_MEDAL),
            TMCLocation.TOWN_MUSIC_HOUSE_HP:
                self.has(Items.CARLOV_MEDAL),
            TMCLocation.TOWN_WELL_PILLAR_CHEST:
                self.can_reach([
                    TMCLocation.TOWN_WELL_TOP_CHEST,
                    TMCLocation.TOWN_WELL_LEFT_CHEST,
                    TMCLocation.TOWN_WELL_RIGHT_CHEST,
                    TMCLocation.TOWN_WELL_BOTTOM_CHEST,
                ]),
            TMCLocation.TOWN_DR_LEFT_ATTIC_ITEM:
                [self.access_town_left(),
                self.has(Items.POWER_BRACELETS),
                self.has_any([Items.GUST_JAR, Items.BOMB]),
                self.split_rule(2)],
            TMCLocation.TOWN_FOUNTAIN_BIG_CHEST:
                [self.can_attack, self.access_town_fountain(), self.has(Items.CANE_OF_PACCI)],
            TMCLocation.TOWN_FOUNTAIN_SMALL_CHEST:
                [self.access_town_fountain(), self.has_any([Items.FLIPPERS, Items.ROCS_CAPE])],
            TMCLocation.TOWN_FOUNTAIN_HP:
                [self.access_town_fountain(), self.has(Items.ROCS_CAPE)],
            TMCLocation.TOWN_LIBRARY_YELLOW_MINISH_NPC:
                self.complete_book_quest(),
            TMCLocation.TOWN_UNDER_LIBRARY_FROZEN_CHEST:
                [self.complete_book_quest(), self.has_all([Items.FLIPPERS, Items.LANTERN])],
            TMCLocation.TOWN_UNDER_LIBRARY_BIG_CHEST:
                [self.complete_book_quest(), self.can_attack, self.has(Items.FLIPPERS)],
            TMCLocation.TOWN_UNDER_LIBRARY_UNDERWATER:
                [self.complete_book_quest(), self.has(Items.FLIPPERS)],
            TMCLocation.TOWN_CUCCOS_LV_10_NPC:
                self.has_any([Items.ROCS_CAPE, Items.FLIPPERS]),
            #endregion

            #region North Field
            # TMCLocation.NORTH_FIELD_TREE_FUSION_BOTTOM_RIGHT_CHEST: None,
            # TMCLocation.NORTH_FIELD_TREE_FUSION_BOTTOM_LEFT_CHEST: None,
            # TMCLocation.NORTH_FIELD_TREE_FUSION_TOP_RIGHT_CHEST: None,
            # TMCLocation.NORTH_FIELD_TREE_FUSION_TOP_LEFT_CHEST: None,
            # TMCLocation.NORTH_FIELD_TREE_FUSION_CENTER_BIG_CHEST: None,
            TMCLocation.NORTH_FIELD_DIG_SPOT:
                self.has(Items.MOLE_MITTS),
            TMCLocation.NORTH_FIELD_HP:
                self.has_any([Items.BOMB, Items.FLIPPERS, Items.ROCS_CAPE]),
            TMCLocation.NORTH_FIELD_WATERFALL_FUSION_DOJO_NPC:
                [self.has(Items.FLIPPERS),
                lambda state: self.swords(state) > 0],
            #endregion
        }

    def elements(self, state: CollectionState) -> int:
        return state.count_from_list_unique(map(item_to_name, [
            Items.EARTH_ELEMENT,
            Items.FIRE_ELEMENT,
            Items.WATER_ELEMENT,
            Items.WIND_ELEMENT,
        ]), self.player)

    def swords(self, state: CollectionState) -> int:
        return state.count_from_list_unique(map(item_to_name, [
            Items.SMITHS_SWORD,
            Items.WHITE_SWORD_GREEN,
            Items.WHITE_SWORD_RED,
            Items.WHITE_SWORD_BLUE,
            Items.FOUR_SWORD,
        ]), self.player)

    def bombs(self, state: CollectionState) -> int:
        return state.count_from_list((item.item_name for item in [
            Items.BOMB,
            Items.REMOTE_BOMB,
        ]), self.player)

    def split_rule(self, link_count: int = 2) -> CollectionRule:
        return lambda state: self.swords(state) >= link_count + 1

    def can_shield(self, state: CollectionState):
        return state.has("Small Shield", self.player) or self.has(Items.MIRROR_SHIELD.item_name, self.player)

    def can_attack(self, state: CollectionState):
        return state.has("Smith's Sword", self.player)

    def can_pass_trees(self, state: CollectionState):
        return self.swords(state) > 0 or state.has_any(map(item_to_name, [
            Items.LIGHT_ARROW,
            Items.BOMB,
            Items.LANTERN
        ]), self.player)

    def has_weapon(self, state: CollectionState) -> bool:
        return self.swords(state) > 0

    def access_town_left(self) -> CollectionRule:
        return self.has_any([Items.ROCS_CAPE, Items.FLIPPERS, Items.CANE_OF_PACCI])

    def access_town_fountain(self) -> CollectionRule:
        return lambda state: self.access_town_left()(state) and self.has(Items.EMPTY_BOTTLE)(state)

    def complete_book_quest(self) -> CollectionRule:
        return self.has_all([
            Items.OCARINA,
            Items.CANE_OF_PACCI,
            Items.RED_BOOK,
            Items.BLUE_BOOK,
            Items.GREEN_BOOK,
        ])

    def has(self, item: ItemData, count: int = 1) -> CollectionRule:
        return lambda state: state.has(item.item_name, self.player, count)

    def has_all(self, items: [ItemData]) -> CollectionRule:
        return lambda state: state.has_all(map(item_to_name, items), self.player)

    def has_any(self, items: [ItemData]) -> CollectionRule:
        return lambda state: state.has_any(map(item_to_name, items), self.player)

    def can_reach(self, locations: [str]) -> CollectionRule:
        return lambda state: not any(state.can_reach(loc, "Location", self.player) for loc in locations)

    def set_rules(self, disabled_locations: set[int], location_name_to_id: dict[str, id]) -> None:
        multiworld = self.world.multiworld

        for loc in multiworld.get_locations(self.player):
            if loc.name not in location_name_to_id or location_name_to_id[loc.name] in disabled_locations:
                continue

            if loc.name in self.location_rules and self.location_rules[loc.name] is not None:
                if hasattr(self.location_rules[loc.name], '__iter__'):
                    for rule in self.location_rules[loc.name]:
                        add_rule(loc, rule)
                else:
                    add_rule(loc, self.location_rules[loc.name])

        multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
