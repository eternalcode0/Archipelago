from typing import Union, Callable, Iterable, Dict
from worlds.generic.Rules import add_rule, CollectionRule
from BaseClasses import CollectionState

from . import Items
from .Items import ItemData
from .Constants.LocationName import TMCLocation
from .Constants.RegionName import TMCRegion

item_to_name = lambda item: item.item_name

class MinishCapRules():
    player: int
    world: "MinishCapWorld"
    connection_rules: dict[(str, str), CollectionRule]
    region_rules: dict[str, CollectionRule]
    location_rules: dict[str, CollectionRule]

    def __init__(self, world: "MinishCapWorld") -> None:
        self.player = world.player
        self.world = world

        self.connection_rules = {
            ("Menu", TMCRegion.SOUTH_FIELD): None,
            (TMCRegion.SOUTH_FIELD, TMCRegion.HYRULE_TOWN): None,
            (TMCRegion.SOUTH_FIELD, TMCRegion.EASTERN_HILLS):
                self.can_pass_trees(),

            (TMCRegion.HYRULE_TOWN, TMCRegion.NORTH_FIELD): None,
            # (TMCRegion.HYRULE_TOWN, TMCRegion.SOUTH_FIELD): Already connected
            (TMCRegion.HYRULE_TOWN, TMCRegion.LONLON):
                self.has(Items.PROGRESSIVE_BOMB),
            (TMCRegion.HYRULE_TOWN, TMCRegion.TRILBY_HIGHLANDS):
                lambda state: self.has_any([Items.ROCS_CAPE, Items.FLIPPERS])(state) or self.can_spin()(state),

            (TMCRegion.NORTH_FIELD, TMCRegion.CASTLE_EXTERIOR): None,
            # (TMCRegion.NORTH_FIELD, TMCRegion.HYRULE_TOWN): Already connected
            (TMCRegion.NORTH_FIELD, TMCRegion.LONLON):
                self.can_pass_trees(),
            (TMCRegion.NORTH_FIELD, TMCRegion.TRILBY_HIGHLANDS):
                self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
            (TMCRegion.NORTH_FIELD, TMCRegion.UPPER_FALLS): # TODO double-check
                self.has_all([Items.PROGRESSIVE_BOMB, Items.KINSTONE_GOLD_FALLS, Items.LANTERN]),
            (TMCRegion.NORTH_FIELD, TMCRegion.VALLEY):
                lambda state: self.split_rule(3)(state) and \
                    self.has_any([Items.FLIPPERS, Items.PROGRESSIVE_BOMB])(state),

            # (TMCRegion.CASTLE_EXTERIOR, TMCRegion.NORTH_FIELD): Already connected
            (TMCRegion.CASTLE_EXTERIOR, TMCRegion.SANCTUARY): None,

            # (TMCRegion.SANCTUARY, TMCRegion.CASTLE_EXTERIOR): Already connected
            (TMCRegion.SANCTUARY, TMCRegion.DUNGEON_DHC):
                lambda state: self.elements(state) >= 4,

            (TMCRegion.DUNGEON_DHC, "Vaati Fight"): # TODO placeholder
                lambda state: self.has_all([Items.BIG_KEY_DHC, Items.SMALL_KEY_DHC, Items.GUST_JAR, Items.PROGRESSIVE_BOW, Items.CANE_OF_PACCI])(state) \
                    and self.has(Items.PROGRESSIVE_SWORD, 5)(state),

            # (TMCRegion.LONLON, TMCRegion.HYRULE_TOWN): Already connected
            #     self.has(Items.PROGRESSIVE_BOMB),
            # (TMCRegion.LONLON, TMCRegion.NORTH_FIELD): Already connected
            #     self.can_pass_trees(),
            (TMCRegion.LONLON, TMCRegion.EASTERN_HILLS): None,
            (TMCRegion.LONLON, TMCRegion.MINISH_WOODS): None, # Doesn't directly connect but it does through eastern hills with no logic in between
            (TMCRegion.LONLON, TMCRegion.LOWER_FALLS):
                self.has(Items.CANE_OF_PACCI),
            (TMCRegion.LONLON, TMCRegion.LAKE_HYLIA): # TODO double-check
                self.has(Items.LONLON_KEY),

            # (TMCRegion.EASTERN_HILLS, TMCRegion.LONLON): Already connected
            (TMCRegion.EASTERN_HILLS, TMCRegion.MINISH_WOODS): None,
            # (TMCRegion.EASTERN_HILLS, TMCRegion.SOUTH_FIELD): Already connected

            # (TMCRegion.MINISH_WOODS, TMCRegion.EASTERN_HILLS): Already connected
            (TMCRegion.MINISH_WOODS, TMCRegion.DUNGEON_DWS):
                self.has_any([Items.FLIPPERS, Items.JABBER_NUT]),

            (TMCRegion.WESTERN_WOODS, TMCRegion.SOUTH_FIELD): None,
            (TMCRegion.WESTERN_WOODS, TMCRegion.CASTOR_WILDS): # TODO double-check
                self.has_any([Items.PEGASUS_BOOTS, Items.ROCS_CAPE]),
            (TMCRegion.WESTERN_WOODS, TMCRegion.TRILBY_HIGHLANDS): None, # TODO

            # (TMCRegion.TRILBY_HIGHLANDS, TMCRegion.HYRULE_TOWN): Already connected
            (TMCRegion.TRILBY_HIGHLANDS, TMCRegion.WESTERN_WOODS): # TODO double-check
                self.split_rule(2),
            (TMCRegion.TRILBY_HIGHLANDS, TMCRegion.CRENEL): # TODO double-check
                self.has_bottle(),
            (TMCRegion.CRENEL, TMCRegion.DUNGEON_COF): # TODO double-check
                self.logic_or([
                    self.has_all([Items.PROGRESSIVE_BOMB, Items.CANE_OF_PACCI, Items.GUST_JAR]),
                    self.logic_and([
                        self.has_all([Items.GRIP_RING, Items.PROGRESSIVE_BOMB]),
                        self.has_any([Items.GUST_JAR, Items.CANE_OF_PACCI, Items.ROCS_CAPE])
                    ])
                ]),

            (TMCRegion.UPPER_FALLS, TMCRegion.CLOUDS):
                self.has(Items.GRIP_RING),
            (TMCRegion.CLOUDS, TMCRegion.WIND_TRIBE): # TODO double-check
                self.logic_and([
                    self.has(Items.KINSTONE_GOLD_CLOUD, 5),
                    self.has_any([Items.MOLE_MITTS, Items.ROCS_CAPE])
                ]),
            (TMCRegion.CLOUDS, TMCRegion.DUNGEON_POW): # TODO double-check
                self.logic_and([
                    self.has_any([Items.ROCS_CAPE, Items.PROGRESSIVE_BOOMERANG, Items.PROGRESSIVE_BOW]),
                    self.split_rule(3)
                ]),

            # (TMCRegion.VALLEY, TMCRegion.NORTH_FIELD): # Already connected
            (TMCRegion.VALLEY, TMCRegion.DUNGEON_RC): # TODO double-check
                self.has_all([Items.GRAVEYARD_KEY, Items.LANTERN]),

            (TMCRegion.CASTOR_WILDS, TMCRegion.RUINS): # TODO double-check
                self.has(Items.KINSTONE_GOLD_SWAMP, 3),
            (TMCRegion.RUINS, TMCRegion.DUNGEON_FOW): None, # TODO double-check

            (TMCRegion.LAKE_HYLIA, TMCRegion.DUNGEON_TOD): # TODO double-check
                self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
            (TMCRegion.LAKE_HYLIA, TMCRegion.MINISH_WOODS): # TODO double-check
                self.has(Items.FLIPPERS),
        }

        self.location_rules = {
            #region South Field
            # TMCLocation.SMITH_HOUSE_RUPEE: None,
            # TMCLocation.SMITH_HOUSE_SWORD: None,
            # TMCLocation.SMITH_HOUSE_SHIELD: None,
            TMCLocation.SOUTH_FIELD_MINISH_SIZE_WATER_HOLE_HP:
                [self.can_pass_trees(), self.has_all([Items.PEGASUS_BOOTS, Items.FLIPPERS])],
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM1:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE])
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM2:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE])
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM3:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE])
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM4:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE])
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM5:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE])
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM6:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE])
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM7:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE])
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM8:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE])
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM9:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE])
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM10:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE])
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM11:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE])
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM12:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE])
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM13:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE])
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM14:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE])
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM15:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE])
                ]),
            TMCLocation.SOUTH_FIELD_FUSION_CHEST:
                self.can_pass_trees(),
            TMCLocation.SOUTH_FIELD_TREE_FUSION_HP:
                self.can_pass_trees(),
            TMCLocation.SOUTH_FIELD_MINISH_SIZE_WATER_HOLE_HP:
                [self.can_pass_trees(), self.has_all([Items.FLIPPERS, Items.PEGASUS_BOOTS])],
            TMCLocation.SOUTH_FIELD_TINGLE_NPC:
                [self.can_pass_trees(), self.has(Items.CANE_OF_PACCI)],
            #endregion

            #region Castle Gardens
            TMCLocation.CASTLE_MOAT_LEFT_CHEST:
                self.has(Items.FLIPPERS),
            TMCLocation.CASTLE_MOAT_RIGHT_CHEST:
                self.has(Items.FLIPPERS),
            TMCLocation.CASTLE_GOLDEN_ROPE: # Fusions 3C
                self.can_attack(),
            # TMCLocation.CASTLE_RIGHT_FOUNTAIN_FUSION_HP: # Fusions 18
            # TMCLocation.CASTLE_DOJO_HP: None,
            TMCLocation.CASTLE_DOJO_NPC:
                self.has_all([Items.LANTERN, Items.PROGRESSIVE_SWORD]),
            TMCLocation.CASTLE_RIGHT_FOUNTAIN_FUSION_MINISH_HOLE_CHEST: # Fusions 18
                self.has(Items.PEGASUS_BOOTS),
            TMCLocation.CASTLE_LEFT_FOUNTAIN_FUSION_MINISH_HOLE_CHEST: # Fusions 35
                self.has(Items.PEGASUS_BOOTS),
            #endregion

            #region Eastern Hills TODO
            # Can Pass Trees
            TMCLocation.HILLS_FUSION_CHEST: None,
            TMCLocation.HILLS_BEANSTALK_FUSION_LEFT_CHEST: None,
            TMCLocation.HILLS_BEANSTALK_FUSION_HP: None,
            TMCLocation.HILLS_BEANSTALK_FUSION_RIGHT_CHEST: None,
            TMCLocation.HILLS_BOMB_CAVE_CHEST:
                self.has(Items.PROGRESSIVE_BOMB),
            TMCLocation.MINISH_GREAT_FAIRY_NPC:
                self.has(Items.CANE_OF_PACCI),
            TMCLocation.HILLS_FARM_DIG_CAVE_ITEM:
                self.has(Items.MOLE_MITTS),
            #endregion

            #region Cloud Tops TODO
            # TMCLocation.CLOUDS_FREE_CHEST: None,
            TMCLocation.CLOUDS_NORTH_EAST_DIG_SPOT:
                self.has(Items.MOLE_MITTS),
            TMCLocation.CLOUDS_NORTH_KILL:
                self.has_any([Items.ROCS_CAPE, Items.MOLE_MITTS]),
            TMCLocation.CLOUDS_SOUTH_KILL:
                self.has_any([Items.ROCS_CAPE, Items.MOLE_MITTS]),
            #endregion

            #region Wind Tribe TODO
            # TMCLocation.WIND_TRIBE_1F_LEFT_CHEST: None,
            # TMCLocation.WIND_TRIBE_1F_RIGHT_CHEST: None,
            #endregion

            #region Minish Woods TODO
            # Can Pass Trees
            TMCLocation.MINISH_WOODS_TOP_HP:
                self.has_any([Items.ROCS_CAPE, Items.FLIPPERS]),
            TMCLocation.MINISH_WOODS_NORTH_FUSION_CHEST:
                self.has_any([Items.ROCS_CAPE, Items.FLIPPERS]),
            TMCLocation.MINISH_WOODS_WITCH_HUT_ITEM:
                self.has_any([Items.ROCS_CAPE, Items.FLIPPERS]),
            TMCLocation.WITCH_DIGGING_CAVE_CHEST:
                self.has_any([Items.ROCS_CAPE, Items.FLIPPERS]),
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
                self.has(Items.PROGRESSIVE_SWORD),
            TMCLocation.TOWN_DOJO_NPC_2:
                self.has(Items.PROGRESSIVE_SWORD, 2),
            TMCLocation.TOWN_DOJO_NPC_3:
                self.has_all([Items.PROGRESSIVE_SWORD, Items.PEGASUS_BOOTS]),
            TMCLocation.TOWN_DOJO_NPC_4:
                self.has_all([Items.PROGRESSIVE_SWORD, Items.ROCS_CAPE]),
            TMCLocation.TOWN_WELL_TOP_CHEST:
                self.has(Items.PROGRESSIVE_BOMB),
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
                self.has_bottle()],
            TMCLocation.TOWN_SIMULATION_CHEST:
                self.has(Items.PROGRESSIVE_SWORD),
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
                self.has_any([Items.GUST_JAR, Items.PROGRESSIVE_BOMB]),
                self.split_rule(2)],
            TMCLocation.TOWN_FOUNTAIN_BIG_CHEST:
                [self.can_attack(), self.access_town_fountain(), self.has(Items.CANE_OF_PACCI)],
            TMCLocation.TOWN_FOUNTAIN_SMALL_CHEST:
                [self.access_town_fountain(), self.has_any([Items.FLIPPERS, Items.ROCS_CAPE])],
            TMCLocation.TOWN_FOUNTAIN_HP:
                [self.access_town_fountain(), self.has(Items.ROCS_CAPE)],
            TMCLocation.TOWN_LIBRARY_YELLOW_MINISH_NPC:
                self.complete_book_quest(),
            TMCLocation.TOWN_UNDER_LIBRARY_FROZEN_CHEST:
                [self.complete_book_quest(), self.has_all([Items.FLIPPERS, Items.LANTERN])],
            TMCLocation.TOWN_UNDER_LIBRARY_BIG_CHEST:
                [self.complete_book_quest(), self.can_attack(), self.has(Items.FLIPPERS)],
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
                self.has_any([Items.PROGRESSIVE_BOMB, Items.FLIPPERS, Items.ROCS_CAPE]),
            TMCLocation.NORTH_FIELD_WATERFALL_FUSION_DOJO_NPC:
                self.has_all([Items.FLIPPERS, Items.PROGRESSIVE_SWORD]),
            #endregion
        }

    def logic_or(self, rules: [CollectionRule]) -> CollectionRule:
        return lambda state: any(rule(state) for rule in rules)

    def logic_and(self, rules: [CollectionRule]) -> CollectionRule:
        return lambda state: all(rule(state) for rule in rules)

    def elements(self, state: CollectionState) -> int:
        return state.count_from_list_unique(map(item_to_name, [
            Items.EARTH_ELEMENT,
            Items.FIRE_ELEMENT,
            Items.WATER_ELEMENT,
            Items.WIND_ELEMENT,
        ]), self.player)

    def can_spin(self) -> CollectionRule:
        return lambda state: self.has(Items.PROGRESSIVE_SWORD)(state) and self.has_any([Items.SPIN_ATTACK, Items.FAST_SPIN_SCROLL])(state)

    def split_rule(self, link_count: int = 2) -> CollectionRule:
        return lambda state: self.has(Items.PROGRESSIVE_SWORD, link_count + 1)(state) and self.can_spin()(state)

    def can_shield(self) -> CollectionRule:
        return self.has_any([Items.SHIELD, Items.MIRROR_SHIELD])

    def can_attack(self) -> CollectionRule:
        return self.has(Items.PROGRESSIVE_SWORD)

    def can_pass_trees(self) -> CollectionRule:
        return lambda state: self.has_any([
            Items.PROGRESSIVE_SWORD,
            Items.PROGRESSIVE_BOMB,
            Items.LANTERN,
        ])(state) or self.has(Items.PROGRESSIVE_BOW, 2)(state)

    def access_town_left(self) -> CollectionRule:
        return self.has_any([Items.ROCS_CAPE, Items.FLIPPERS, Items.CANE_OF_PACCI])

    def has_bottle(self) -> CollectionRule:
        return self.has_any([Items.BOTTLE_1, Items.BOTTLE_2, Items.BOTTLE_3, Items.BOTTLE_4])

    def access_town_fountain(self) -> CollectionRule:
        return lambda state: self.access_town_left()(state) and self.has_bottle()(state)

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

        # menu_region = multiworld.get_region("Menu", self.player)
        for region_pair, rule in self.connection_rules.items():
            region_one = multiworld.get_region(region_pair[0], self.player)
            region_two = multiworld.get_region(region_pair[1], self.player)
            region_one.connect(region_two, rule=rule)
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
