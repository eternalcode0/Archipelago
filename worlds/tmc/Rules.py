from typing import Union, Callable, Iterable, Dict
from worlds.generic.Rules import add_rule, forbid_item, CollectionRule
from BaseClasses import CollectionState

from . import Items
from .Items import ItemData
from .Constants.LocationName import TMCLocation
from .Constants.RegionName import TMCRegion
from .Options import MinishCapOptions

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
                self.has(Items.BOMB_BAG),
            (TMCRegion.HYRULE_TOWN, TMCRegion.TRILBY_HIGHLANDS):
                self.logic_or([
                    self.has_any([Items.ROCS_CAPE, Items.FLIPPERS]),
                    self.can_spin(),
                ]),

            (TMCRegion.NORTH_FIELD, TMCRegion.CASTLE_EXTERIOR): None,
            # (TMCRegion.NORTH_FIELD, TMCRegion.HYRULE_TOWN): Already connected
            (TMCRegion.NORTH_FIELD, TMCRegion.LONLON):
                self.can_pass_trees(),
            (TMCRegion.NORTH_FIELD, TMCRegion.TRILBY_HIGHLANDS):
                self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
            (TMCRegion.NORTH_FIELD, TMCRegion.UPPER_FALLS): # TODO double-check
                self.has_all([Items.BOMB_BAG, Items.KINSTONE_GOLD_FALLS, Items.LANTERN]),
            (TMCRegion.NORTH_FIELD, TMCRegion.ROYAL_VALLEY):
                self.logic_and([
                    self.split_rule(3),
                    self.has_any([Items.FLIPPERS, Items.BOMB_BAG]),
                ]),

            # (TMCRegion.CASTLE_EXTERIOR, TMCRegion.NORTH_FIELD): Already connected
            (TMCRegion.CASTLE_EXTERIOR, TMCRegion.SANCTUARY): None,

            # (TMCRegion.SANCTUARY, TMCRegion.CASTLE_EXTERIOR): Already connected
            (TMCRegion.SANCTUARY, TMCRegion.DUNGEON_DHC):
                self.has_4_elements(),

            (TMCRegion.DUNGEON_DHC, "Vaati Fight"): # TODO placeholder
                self.logic_and([
                    self.has_all([Items.BIG_KEY_DHC, Items.SMALL_KEY_DHC, Items.GUST_JAR, Items.PROGRESSIVE_BOW, Items.CANE_OF_PACCI]),
                    self.has(Items.PROGRESSIVE_SWORD, 5),
                ]),

            # (TMCRegion.LONLON, TMCRegion.HYRULE_TOWN): Already connected
            #     self.has(Items.BOMB_BAG),
            # (TMCRegion.LONLON, TMCRegion.NORTH_FIELD): Already connected
            #     self.can_pass_trees(),
            (TMCRegion.LONLON, TMCRegion.EASTERN_HILLS): None,
            (TMCRegion.LONLON, TMCRegion.MINISH_WOODS): None, # Doesn't directly connect but it does through eastern hills with no logic in between
            (TMCRegion.LONLON, TMCRegion.LOWER_FALLS):
                self.has(Items.CANE_OF_PACCI),
            (TMCRegion.LONLON, TMCRegion.LAKE_HYLIA_NORTH): # TODO double-check
                self.has(Items.LONLON_KEY),

            # (TMCRegion.EASTERN_HILLS, TMCRegion.LONLON): Already connected
            (TMCRegion.EASTERN_HILLS, TMCRegion.MINISH_WOODS): None,
            # (TMCRegion.EASTERN_HILLS, TMCRegion.SOUTH_FIELD): Already connected

            # (TMCRegion.MINISH_WOODS, TMCRegion.EASTERN_HILLS): Already connected
            (TMCRegion.MINISH_WOODS, TMCRegion.DUNGEON_DWS):
                self.has_any([Items.FLIPPERS, Items.JABBER_NUT]),
            (TMCRegion.MINISH_WOODS, TMCRegion.LAKE_HYLIA_SOUTH):
                self.logic_and([
                    self.access_minish_woods_top_left(),
                    self.has(Items.MOLE_MITTS),
                ]),

            (TMCRegion.WESTERN_WOODS, TMCRegion.SOUTH_FIELD): None,
            (TMCRegion.WESTERN_WOODS, TMCRegion.CASTOR_WILDS):
                self.has_any([Items.PEGASUS_BOOTS, Items.ROCS_CAPE]),
            # (TMCRegion.WESTERN_WOODS, TMCRegion.TRILBY_HIGHLANDS): Already connected

            # (TMCRegion.TRILBY_HIGHLANDS, TMCRegion.HYRULE_TOWN): Already connected
            (TMCRegion.TRILBY_HIGHLANDS, TMCRegion.WESTERN_WOODS):
                self.split_rule(2),
            (TMCRegion.TRILBY_HIGHLANDS, TMCRegion.CRENEL_BASE):
                self.has_bottle(),
            (TMCRegion.CRENEL_BASE, TMCRegion.CRENEL):
                self.logic_or([
                    self.has_any([Items.GRIP_RING, Items.BOMB_BAG]),
                ]),
            (TMCRegion.CRENEL, TMCRegion.MELARI):
                self.logic_or([
                    self.has_all([
                        Items.CANE_OF_PACCI,
                        Items.GRIP_RING,
                    ]),
                    self.has_all([
                        Items.CANE_OF_PACCI,
                        Items.BOMB_BAG,
                    ]),
                    self.logic_and([
                        self.has(Items.GRIP_RING),
                        self.logic_or([
                            self.has_any([
                                Items.GUST_JAR,
                                Items.ROCS_CAPE,
                            ]),
                            self.has(Items.PROGRESSIVE_BOW,2),
                        ]),
                        self.has_any([
                            Items.BOMB_BAG,
                            Items.PROGRESSIVE_BOW,
                            Items.PROGRESSIVE_BOOMERANG,
                            Items.ROCS_CAPE,
                        ]),
                    ]),
                ]),
            (TMCRegion.MELARI, TMCRegion.DUNGEON_COF):
                self.logic_and([
                    self.can_attack(),
                    self.logic_or([
                        self.has_all([
                            Items.DOWNTHRUST,
                            Items.ROCS_CAPE,
                        ]),
                        self.has_any([
                            Items.CANE_OF_PACCI,
                            Items.PROGRESSIVE_SHIELD,
                            Items.BOMB_BAG
                        ])
                    ])
                ]),
            (TMCRegion.UPPER_FALLS, TMCRegion.CLOUDS):
                self.has(Items.GRIP_RING),
            (TMCRegion.CLOUDS, TMCRegion.WIND_TRIBE): # TODO double-check
                self.logic_and([
                    self.has(Items.KINSTONE_GOLD_CLOUD, 5),
                    self.has_any([Items.MOLE_MITTS, Items.ROCS_CAPE]),
                ]),
            (TMCRegion.WIND_TRIBE, TMCRegion.DUNGEON_POW): # TODO double-check
                self.logic_and([
                    self.has_any([Items.ROCS_CAPE, Items.PROGRESSIVE_BOOMERANG, Items.PROGRESSIVE_BOW]),
                    self.split_rule(3),
                ]),

            # (TMCRegion.ROYAL_VALLEY, TMCRegion.NORTH_FIELD): # Already connected
            (TMCRegion.ROYAL_VALLEY, TMCRegion.GRAVEYARD):
                self.has_all([Items.GRAVEYARD_KEY, Items.PEGASUS_BOOTS, Items.LANTERN]),
            (TMCRegion.GRAVEYARD, TMCRegion.DUNGEON_RC): # TODO double-check
                self.logic_and([
                    self.has(Items.LANTERN),
                    self.split_rule(3)
                ]),

            (TMCRegion.CASTOR_WILDS, TMCRegion.WIND_RUINS): # TODO double-check
                self.has(Items.KINSTONE_GOLD_SWAMP, 3),
            (TMCRegion.WIND_RUINS, TMCRegion.DUNGEON_FOW): None, # TODO double-check

            (TMCRegion.LAKE_HYLIA_NORTH, TMCRegion.LAKE_HYLIA_SOUTH):
                self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
            (TMCRegion.LAKE_HYLIA_NORTH, TMCRegion.DUNGEON_TOD): # TODO double-check
                self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
            # (TMCRegion.LAKE_HYLIA_SOUTH, TMCRegion.MINISH_WOODS): # Already connected
            (TMCRegion.DUNGEON_TOD, TMCRegion.DUNGEON_TOD_MAIN): # TODO double-check
                self.has(Items.BIG_KEY_TOD),
        }

        self.location_rules = {
            #region South Field
            # TMCLocation.SMITH_HOUSE_RUPEE: None,
            # TMCLocation.SMITH_HOUSE_SWORD: None,
            # TMCLocation.SMITH_HOUSE_SHIELD: None,
            TMCLocation.SOUTH_FIELD_MINISH_SIZE_WATER_HOLE_HP:
                self.logic_and([
                    self.can_pass_trees(),
                    self.has_all([Items.PEGASUS_BOOTS, Items.FLIPPERS]),
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM1:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM2:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM3:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM4:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM5:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM6:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM7:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM8:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM9:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM10:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM11:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM12:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM13:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM14:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
                ]),
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM15:
                self.logic_or([
                    self.can_pass_trees(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
                ]),
            TMCLocation.SOUTH_FIELD_FUSION_CHEST:
                self.can_pass_trees(),
            TMCLocation.SOUTH_FIELD_TREE_FUSION_HP:
                self.can_pass_trees(),
            TMCLocation.SOUTH_FIELD_MINISH_SIZE_WATER_HOLE_HP:
                self.logic_and([
                    self.can_pass_trees(),
                    self.has_all([Items.FLIPPERS, Items.PEGASUS_BOOTS]),
                ]),
            TMCLocation.SOUTH_FIELD_TINGLE_NPC:
                self.logic_and([
                    self.can_pass_trees(),
                    self.has_all([Items.CANE_OF_PACCI, Items.TINGLE_TROPHY]),
                ]),
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
                self.has(Items.BOMB_BAG),
            TMCLocation.MINISH_GREAT_FAIRY_NPC:
                self.has(Items.CANE_OF_PACCI),
            TMCLocation.HILLS_FARM_DIG_CAVE_ITEM:
                self.has(Items.MOLE_MITTS),
            #endregion

            #region LonLon
            # Can Pass Trees
            # TMCLocation.LON_LON_RANCH_POT: None,
            TMCLocation.LON_LON_PUDDLE_FUSION_BIG_CHEST:
                self.access_lonlon_right(),
            TMCLocation.LON_LON_CAVE_CHEST:
                self.logic_and([
                    # Fusion 1E
                    self.access_lonlon_right(),
                    self.split_rule(2),
                ]),
            TMCLocation.LON_LON_CAVE_SECRET_CHEST:
                self.logic_and([
                    self.can_reach([TMCLocation.LON_LON_CAVE_CHEST]),
                    self.has_all([Items.BOMB_BAG, Items.LANTERN]),
                ]),
            TMCLocation.LON_LON_PATH_FUSION_CHEST:
                self.logic_and([
                    # Fusion 50
                    self.access_lonlon_right(),
                    self.has(Items.PEGASUS_BOOTS),
                ]),
            TMCLocation.LON_LON_PATH_HP:
                self.logic_and([
                    self.access_lonlon_right(),
                    self.has(Items.PEGASUS_BOOTS),
                ]),
            TMCLocation.LON_LON_DIG_SPOT:
                self.logic_and([
                    self.access_lonlon_right(),
                    self.has_any([Items.CANE_OF_PACCI, Items.ROCS_CAPE]),
                    self.has(Items.MOLE_MITTS),
                ]),
            TMCLocation.LON_LON_NORTH_MINISH_CRACK_CHEST:
                self.logic_and([
                    self.access_lonlon_right(),
                    self.has_any([Items.CANE_OF_PACCI, Items.ROCS_CAPE]),
                ]),
            TMCLocation.LON_LON_GORON_CAVE_FUSION_SMALL_CHEST:
                # 4 of Fusions 25, 26, 29, 2A, 2B, 2F
                self.logic_or([
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
                    self.logic_and([
                        self.has(Items.CANE_OF_PACCI),
                        self.access_lonlon_right(),
                    ]),
                ]),
            TMCLocation.LON_LON_GORON_CAVE_FUSION_BIG_CHEST:
                # 6 of Fusions 25, 26, 29, 2A, 2B, 2F
                self.logic_or([
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
                    self.logic_and([
                        self.has(Items.CANE_OF_PACCI),
                        self.access_lonlon_right(),
                    ]),
                ]),
            #endreigon

            #region Lower Falls
            # TMCLocation.FALLS_LOWER_LON_LON_FUSION_CHEST: None, # Fusion 60
            # TMCLocation.FALLS_LOWER_HP: None,
            TMCLocation.FALLS_LOWER_WATERFALL_FUSION_DOJO_NPC: # Fusion 1D
                self.has_all([Items.FLIPPERS, Items.PROGRESSIVE_SWORD]),
            TMCLocation.FALLS_LOWER_ROCK_ITEM1:
                self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
            TMCLocation.FALLS_LOWER_ROCK_ITEM2:
                self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
            TMCLocation.FALLS_LOWER_ROCK_ITEM3:
                self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
            TMCLocation.FALLS_LOWER_DIG_CAVE_LEFT_CHEST:
                self.logic_and([
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
                    self.has(Items.MOLE_MITTS),
                ]),
            TMCLocation.FALLS_LOWER_DIG_CAVE_RIGHT_CHEST:
                self.logic_and([
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
                    self.has(Items.MOLE_MITTS),
                ]),
            #endregion

            #region Upper Falls
            TMCLocation.FALLS_ENTRANCE_HP: # The first 3 are part of North Field logic, doesn't require falls fusion stone or lantern
                self.has_all([Items.FLIPPERS, Items.BOMB_BAG]),
            TMCLocation.FALLS_WATER_DIG_CAVE_FUSION_HP: # Fusion 1F
                self.has_all([Items.FLIPPERS, Items.BOMB_BAG, Items.MOLE_MITTS]),
            TMCLocation.FALLS_WATER_DIG_CAVE_FUSION_CHEST: # Fusion 1F
                self.has_all([Items.FLIPPERS, Items.BOMB_BAG, Items.MOLE_MITTS]),
            # TMCLocation.FALLS_1ST_CAVE_CHEST: None,
            TMCLocation.FALLS_CLIFF_CHEST:
                self.split_rule(3),
            TMCLocation.FALLS_SOUTH_DIG_SPOT:
                self.has(Items.MOLE_MITTS),
            TMCLocation.FALLS_GOLDEN_TEKTITE: # Fusion 4A
                self.logic_and([
                    self.can_attack(),
                    self.has(Items.GRIP_RING),
                ]),
            TMCLocation.FALLS_NORTH_DIG_SPOT:
                self.has_all([Items.GRIP_RING, Items.MOLE_MITTS]),
            TMCLocation.FALLS_ROCK_FUSION_CHEST: # Fusion 61
                self.has(Items.GRIP_RING),
            TMCLocation.FALLS_WATERFALL_FUSION_HP:
                self.has_all([Items.GRIP_RING, Items.FLIPPERS]),
            TMCLocation.FALLS_RUPEE_CAVE_TOP_TOP:
                self.has(Items.GRIP_RING),
            TMCLocation.FALLS_RUPEE_CAVE_TOP_LEFT:
                self.has(Items.GRIP_RING),
            TMCLocation.FALLS_RUPEE_CAVE_TOP_MIDDLE:
                self.has(Items.GRIP_RING),
            TMCLocation.FALLS_RUPEE_CAVE_TOP_RIGHT:
                self.has(Items.GRIP_RING),
            TMCLocation.FALLS_RUPEE_CAVE_TOP_BOTTOM:
                self.has(Items.GRIP_RING),
            TMCLocation.FALLS_RUPEE_CAVE_SIDE_TOP:
                self.has(Items.GRIP_RING),
            TMCLocation.FALLS_RUPEE_CAVE_SIDE_LEFT:
                self.has(Items.GRIP_RING),
            TMCLocation.FALLS_RUPEE_CAVE_SIDE_RIGHT:
                self.has(Items.GRIP_RING),
            TMCLocation.FALLS_RUPEE_CAVE_SIDE_BOTTOM:
                self.has(Items.GRIP_RING),
            TMCLocation.FALLS_RUPEE_CAVE_UNDERWATER_TOP_LEFT:
                self.has_all([Items.GRIP_RING, Items.FLIPPERS]),
            TMCLocation.FALLS_RUPEE_CAVE_UNDERWATER_TOP_RIGHT:
                self.has_all([Items.GRIP_RING, Items.FLIPPERS]),
            TMCLocation.FALLS_RUPEE_CAVE_UNDERWATER_MIDDLE_LEFT:
                self.has_all([Items.GRIP_RING, Items.FLIPPERS]),
            TMCLocation.FALLS_RUPEE_CAVE_UNDERWATER_MIDDLE_RIGHT:
                self.has_all([Items.GRIP_RING, Items.FLIPPERS]),
            TMCLocation.FALLS_RUPEE_CAVE_UNDERWATER_BOTTOM_LEFT:
                self.has_all([Items.GRIP_RING, Items.FLIPPERS]),
            TMCLocation.FALLS_RUPEE_CAVE_UNDERWATER_BOTTOM_RIGHT:
                self.has_all([Items.GRIP_RING, Items.FLIPPERS]),
            TMCLocation.FALLS_TOP_CAVE_BOMB_WALL_CHEST:
                self.has_all([Items.GRIP_RING, Items.BOMB_BAG]),
            TMCLocation.FALLS_TOP_CAVE_CHEST:
                self.has(Items.GRIP_RING),
            #endregion

            #region Cloud Tops
            # TMCLocation.CLOUDS_FREE_CHEST: None,
            TMCLocation.CLOUDS_NORTH_EAST_DIG_SPOT:
                self.has(Items.MOLE_MITTS),
            TMCLocation.CLOUDS_NORTH_KILL:
                self.logic_and([
                    self.has_any([Items.ROCS_CAPE, Items.MOLE_MITTS]),
                    self.can_attack(),
                ]),
            TMCLocation.CLOUDS_NORTH_WEST_LEFT_CHEST:
                self.has(Items.MOLE_MITTS),
            TMCLocation.CLOUDS_NORTH_WEST_RIGHT_CHEST:
                self.has(Items.MOLE_MITTS),
            TMCLocation.CLOUDS_NORTH_WEST_DIG_SPOT:
                self.has(Items.MOLE_MITTS),
            TMCLocation.CLOUDS_NORTH_WEST_BOTTOM_CHEST:
                self.has_any([Items.MOLE_MITTS, Items.ROCS_CAPE]),
            TMCLocation.CLOUDS_SOUTH_LEFT_CHEST:
                self.has(Items.MOLE_MITTS),
            TMCLocation.CLOUDS_SOUTH_DIG_SPOT:
                self.has(Items.MOLE_MITTS),
            TMCLocation.CLOUDS_SOUTH_MIDDLE_CHEST:
                self.has_any([Items.MOLE_MITTS, Items.ROCS_CAPE]),
            TMCLocation.CLOUDS_SOUTH_MIDDLE_DIG_SPOT:
                self.has(Items.MOLE_MITTS),
            TMCLocation.CLOUDS_SOUTH_KILL:
                self.logic_and([
                    self.has_any([Items.ROCS_CAPE, Items.MOLE_MITTS]),
                    self.can_attack(),
                ]),
            TMCLocation.CLOUDS_SOUTH_RIGHT_CHEST:
                self.has_any([Items.MOLE_MITTS, Items.ROCS_CAPE]),
            TMCLocation.CLOUDS_SOUTH_RIGHT_DIG_SPOT:
                self.has(Items.MOLE_MITTS),
            TMCLocation.CLOUDS_SOUTH_EAST_BOTTOM_DIG_SPOT:
                self.has(Items.MOLE_MITTS),
            TMCLocation.CLOUDS_SOUTH_EAST_TOP_DIG_SPOT:
                self.has(Items.MOLE_MITTS),
            #endregion

            #region Wind Tribe
            # Doesn't require many special access rules *yet*
            # 1F-2F is accessible due to open fusions
            # TMCLocation.WIND_TRIBE_1F_LEFT_CHEST: None,
            # TMCLocation.WIND_TRIBE_1F_RIGHT_CHEST: None,
            # TMCLocation.WIND_TRIBE_2F_CHEST: None,
            TMCLocation.WIND_TRIBE_2F_GREGAL_NPC_1:
                self.has(Items.GUST_JAR),
            # Here starts the rules that require access to Cloudtops/Wind Tribe
            TMCLocation.WIND_TRIBE_2F_GREGAL_NPC_2:
                self.has(Items.GUST_JAR),
            # TMCLocation.WIND_TRIBE_3F_LEFT_CHEST: None,
            # TMCLocation.WIND_TRIBE_3F_CENTER_CHEST: None,
            # TMCLocation.WIND_TRIBE_3F_RIGHT_CHEST: None,
            # TMCLocation.WIND_TRIBE_4F_LEFT_CHEST: None,
            # TMCLocation.WIND_TRIBE_4F_RIGHT_CHEST: None,
            #endregion

            #region Minish Woods TODO
            # Can Pass Trees
            TMCLocation.MINISH_WOODS_GOLDEN_OCTO:
                # fusion 56
                self.logic_and([
                    self.access_minish_woods_top_left(),
                    self.can_attack()
                ]),
            TMCLocation.MINISH_WOODS_WITCH_HUT_ITEM:
                self.access_minish_woods_top_left(),
            TMCLocation.WITCH_DIGGING_CAVE_CHEST:
                self.logic_and([
                    self.access_minish_woods_top_left(),
                    self.has(Items.MOLE_MITTS),
                ]),
            TMCLocation.MINISH_WOODS_NORTH_FUSION_CHEST:
                # fusion 44
                self.access_minish_woods_top_left(),
            TMCLocation.MINISH_WOODS_TOP_HP:
                self.access_minish_woods_top_left(),
            # TMCLocation.MINISH_WOODS_WEST_FUSION_CHEST: None, # fusion 47
            TMCLocation.MINISH_WOODS_LIKE_LIKE_DIGGING_CAVE_LEFT_CHEST:
                self.logic_and([
                    self.has(Items.MOLE_MITTS),
                    self.can_attack(),
                ]),
            TMCLocation.MINISH_WOODS_LIKE_LIKE_DIGGING_CAVE_RIGHT_CHEST:
                self.logic_and([
                    self.has(Items.MOLE_MITTS),
                    self.can_attack(),
                ]),
            # TMCLocation.MINISH_WOODS_EAST_FUSION_CHEST: None, # fusion 46
            # TMCLocation.MINISH_WOODS_SOUTH_FUSION_CHEST: None, # fusion 39
            # TMCLocation.MINISH_WOODS_BOTTOM_HP: None,
            # TMCLocation.MINISH_WOODS_CRACK_FUSION_CHEST: None, # fusion 4E
            # TMCLocation.MINISH_WOODS_MINISH_PATH_FUSION_CHEST: None, # fusion 37
            # TMCLocation.MINISH_VILLAGE_BARREL_HOUSE_ITEM: None,
            # TMCLocation.MINISH_VILLAGE_HP: None,
            TMCLocation.MINISH_WOODS_BOMB_MINISH_NPC_1:
                self.has(Items.BOMB_BAG),
            TMCLocation.MINISH_WOODS_BOMB_MINISH_NPC_2: # fusion 1C
                self.has(Items.BOMB_BAG),
            TMCLocation.MINISH_WOODS_POST_VILLAGE_FUSION_CHEST:
                self.has(Items.BOMB_BAG),
            TMCLocation.MINISH_WOODS_FLIPPER_HOLE_MIDDLE_CHEST:
                self.has_all([Items.BOMB_BAG, Items.FLIPPERS]),
            TMCLocation.MINISH_WOODS_FLIPPER_HOLE_RIGHT_CHEST:
                self.has_all([Items.BOMB_BAG, Items.FLIPPERS]),
            TMCLocation.MINISH_WOODS_FLIPPER_HOLE_LEFT_CHEST:
                self.has_all([Items.BOMB_BAG, Items.FLIPPERS]),
            TMCLocation.MINISH_WOODS_FLIPPER_HOLE_HP:
                self.has_all([Items.BOMB_BAG, Items.FLIPPERS]),
            #endregion

            #region Trilby Highlands
            # Can Spin / Flippers / Roc's Cape
            # TMCLocation.TRILBY_MIDDLE_FUSION_CHEST: None, # fusion 5E
            # TMCLocation.TRILBY_TOP_FUSION_CHEST: None, # fusion 52
            TMCLocation.TRILBY_DIG_CAVE_LEFT_CHEST:
                self.has(Items.MOLE_MITTS),
            TMCLocation.TRILBY_DIG_CAVE_RIGHT_CHEST:
                self.has(Items.MOLE_MITTS),
            TMCLocation.TRILBY_DIG_CAVE_WATER_FUSION_CHEST: # fusion 22
                self.logic_and([
                    self.has(Items.MOLE_MITTS),
                    self.has_any([Items.ROCS_CAPE, Items.FLIPPERS]),
                ]),
            TMCLocation.TRILBY_SCRUB_NPC:
                self.has_all([Items.BOMB_BAG, Items.PROGRESSIVE_SHIELD]),
            TMCLocation.TRILBY_BOMB_CAVE_CHEST:
                self.has(Items.BOMB_BAG),
            #endregion

            #region Crenel
            # Crenel Base = bottle
            # TMCLocation.CRENEL_BASE_ENTRANCE_VINE: None, # Assigned to Trilby so it doesn't require bottle
            TMCLocation.CRENEL_BASE_FAIRY_CAVE_ITEM1:
                self.has(Items.BOMB_BAG),
            TMCLocation.CRENEL_BASE_FAIRY_CAVE_ITEM2:
                self.has(Items.BOMB_BAG),
            TMCLocation.CRENEL_BASE_FAIRY_CAVE_ITEM3:
                self.has(Items.BOMB_BAG),
            TMCLocation.CRENEL_BASE_GREEN_WATER_FUSION_CHEST: # Fusion 4F
                self.has(Items.BOMB_BAG),
            TMCLocation.CRENEL_BASE_WEST_FUSION_CHEST: # Fusion 63
                self.has_any([Items.BOMB_BAG, Items.ROCS_CAPE]),
            TMCLocation.CRENEL_BASE_WATER_CAVE_LEFT_CHEST:
                self.has(Items.BOMB_BAG), # can alternatively require cape if the bomb wall is broken
            TMCLocation.CRENEL_BASE_WATER_CAVE_RIGHT_CHEST:
                self.has(Items.BOMB_BAG), # can alternatively require cape if the bomb wall is broken
            TMCLocation.CRENEL_BASE_WATER_CAVE_HP:
                self.has(Items.BOMB_BAG), # can alternatively require cape/flippers if the bomb wall is broken
            TMCLocation.CRENEL_BASE_MINISH_VINE_HOLE_CHEST:
                self.logic_and([
                    self.has_any([Items.BOMB_BAG, Items.ROCS_CAPE]),
                    self.has_any([Items.BOMB_BAG, Items.GUST_JAR]),
                ]),
            TMCLocation.CRENEL_BASE_MINISH_CRACK_CHEST:
                self.logic_and([
                    self.has_any([Items.BOMB_BAG, Items.ROCS_CAPE]),
                    self.has_any([Items.BOMB_BAG, Items.GUST_JAR]),
                ]),
            TMCLocation.CRENEL_VINE_TOP_GOLDEN_TEKTITE: # Fusion 3B
                self.can_attack(),
            TMCLocation.CRENEL_BRIDGE_CAVE_CHEST:
                self.has(Items.BOMB_BAG),
            TMCLocation.CRENEL_FAIRY_CAVE_HP:
                self.has(Items.BOMB_BAG),
            TMCLocation.CRENEL_BELOW_COF_GOLDEN_TEKTITE: # Fusion 0D
                self.logic_and([
                    self.has(Items.PROGRESSIVE_SWORD),
                    self.logic_or([
                        self.has_any([Items.GRIP_RING, Items.BOMB_BAG]),
                        self.has_any([Items.GUST_JAR, Items.ROCS_CAPE]),
                    ])
                ]),
            TMCLocation.CRENEL_SCRUB_NPC:
                self.logic_and([
                    self.has_all([Items.BOMB_BAG, Items.PROGRESSIVE_SHIELD]),
                    self.logic_or([
                        self.has(Items.GRIP_RING),
                        self.has_any([Items.GUST_JAR, Items.ROCS_CAPE]),
                    ])
                ]),
            TMCLocation.CRENEL_DOJO_LEFT_CHEST:
                self.logic_and([
                    self.has(Items.GRIP_RING),
                    self.split_rule(2),
                ]),
            TMCLocation.CRENEL_DOJO_RIGHT_CHEST:
                self.logic_and([
                    self.has(Items.GRIP_RING),
                    self.split_rule(2),
                ]),
            TMCLocation.CRENEL_DOJO_HP:
                self.logic_and([
                    self.has(Items.GRIP_RING),
                    self.split_rule(2),
                ]),
            TMCLocation.CRENEL_DOJO_NPC:
                self.logic_and([
                    self.has(Items.GRIP_RING),
                    self.split_rule(2),
                ]),
            TMCLocation.CRENEL_GREAT_FAIRY_NPC:
                self.has_all([Items.GRIP_RING, Items.BOMB_BAG]),
            TMCLocation.CRENEL_CLIMB_FUSION_CHEST: # Fustion 62
                self.has_all([Items.GRIP_RING, Items.BOMB_BAG]),
            TMCLocation.CRENEL_DIG_CAVE_HP:
                self.has_all([Items.GRIP_RING, Items.MOLE_MITTS]),
            TMCLocation.CRENEL_BEANSTALK_FUSION_HP: # Fusion 1A
                self.has(Items.GRIP_RING),
            TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM1: # Fusion 1A
                self.has(Items.GRIP_RING),
            TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM2: # Fusion 1A
                self.has(Items.GRIP_RING),
            TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM3: # Fusion 1A
                self.has(Items.GRIP_RING),
            TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM4: # Fusion 1A
                self.has(Items.GRIP_RING),
            TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM5: # Fusion 1A
                self.has(Items.GRIP_RING),
            TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM6: # Fusion 1A
                self.has(Items.GRIP_RING),
            TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM7: # Fusion 1A
                self.has(Items.GRIP_RING),
            TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM8: # Fusion 1A
                self.has(Items.GRIP_RING),
            TMCLocation.CRENEL_RAIN_PATH_FUSION_CHEST: # Fusion 43
                self.has(Items.GRIP_RING),
            #endregion

            #region Melari
            # TMCLocation.CRENEL_UPPER_BLOCK_CHEST: None
            # TMCLocation.CRENEL_MINES_PATH_FUSION_CHEST: None, # Fusion 45
            TMCLocation.CRENEL_MELARI_MIDDLE_LEFT_DIG:
                self.has(Items.MOLE_MITTS),
            TMCLocation.CRENEL_MELARI_TOP_MIDDLE_DIG:
                self.has(Items.MOLE_MITTS),
            TMCLocation.CRENEL_MELARI_TOP_LEFT_DIG:
                self.has(Items.MOLE_MITTS),
            TMCLocation.CRENEL_MELARI_TOP_RIGHT_DIG:
                self.has(Items.MOLE_MITTS),
            TMCLocation.CRENEL_MELARI_BOTTOM_RIGHT_DIG:
                self.has(Items.MOLE_MITTS),
            TMCLocation.CRENEL_MELARI_BOTTOM_MIDDLE_DIG:
                self.has(Items.MOLE_MITTS),
            TMCLocation.CRENEL_MELARI_BOTTOM_LEFT_DIG:
                self.has(Items.MOLE_MITTS),
            TMCLocation.CRENEL_MELARI_CENTER_DIG:
                self.has(Items.MOLE_MITTS),
            TMCLocation.CRENEL_MELARI_NPC_COF:
                self.can_reach([TMCLocation.COF_PRIZE]),
            #endregion

            #region Western Woods
            # All of the below require Fusion 3F
            # They also are part of the western wood region
            # TMCLocation.TRILBY_PUDDLE_FUSION_ITEM1: None,
            # TMCLocation.TRILBY_PUDDLE_FUSION_ITEM2: None,
            # TMCLocation.TRILBY_PUDDLE_FUSION_ITEM3: None,
            # TMCLocation.TRILBY_PUDDLE_FUSION_ITEM4: None,
            # TMCLocation.TRILBY_PUDDLE_FUSION_ITEM5: None,
            # TMCLocation.TRILBY_PUDDLE_FUSION_ITEM6: None,
            # TMCLocation.TRILBY_PUDDLE_FUSION_ITEM7: None,
            # TMCLocation.TRILBY_PUDDLE_FUSION_ITEM8: None,
            # TMCLocation.TRILBY_PUDDLE_FUSION_ITEM9: None,
            # TMCLocation.TRILBY_PUDDLE_FUSION_ITEM10: None,
            # TMCLocation.TRILBY_PUDDLE_FUSION_ITEM11: None,
            # TMCLocation.TRILBY_PUDDLE_FUSION_ITEM12: None,
            # TMCLocation.TRILBY_PUDDLE_FUSION_ITEM13: None,
            # TMCLocation.TRILBY_PUDDLE_FUSION_ITEM14: None,
            # TMCLocation.TRILBY_PUDDLE_FUSION_ITEM15: None,

            # TMCLocation.WESTERN_WOODS_FUSION_CHEST: None, # fusion 3A
            # TMCLocation.WESTERN_WOODS_TREE_FUSION_HP: None, # fusion 11
            TMCLocation.WESTERN_WOODS_TOP_DIG1:
                self.has(Items.MOLE_MITTS), # fusion 48
            TMCLocation.WESTERN_WOODS_TOP_DIG2:
                self.has(Items.MOLE_MITTS), # fusion 48
            TMCLocation.WESTERN_WOODS_TOP_DIG3:
                self.has(Items.MOLE_MITTS), # fusion 48
            TMCLocation.WESTERN_WOODS_TOP_DIG4:
                self.has(Items.MOLE_MITTS), # fusion 48
            TMCLocation.WESTERN_WOODS_TOP_DIG5:
                self.has(Items.MOLE_MITTS), # fusion 48
            TMCLocation.WESTERN_WOODS_TOP_DIG6:
                self.has(Items.MOLE_MITTS), # fusion 48
            TMCLocation.WESTERN_WOODS_PERCY_FUSION_MOBLIN:
                self.has(Items.LANTERN),
            TMCLocation.WESTERN_WOODS_PERCY_FUSION_PERCY:
                self.has(Items.LANTERN),
            TMCLocation.WESTERN_WOODS_BOTTOM_DIG1:
                self.has(Items.MOLE_MITTS), # fusion 4C
            TMCLocation.WESTERN_WOODS_BOTTOM_DIG2:
                self.has(Items.MOLE_MITTS), # fusion 4C
            TMCLocation.WESTERN_WOODS_GOLDEN_OCTO:
                self.can_attack(), # fusion 3D
            # All of the following require Fusion 24
            # TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_CHEST: None,
            # TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM1: None,
            # TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM2: None,
            # TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM3: None,
            # TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM4: None,
            # TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM5: None,
            # TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM6: None,
            # TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM7: None,
            # TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM8: None,
            # TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM9: None,
            # TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM10: None,
            # TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM11: None,
            # TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM12: None,
            # TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM13: None,
            # TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM14: None,
            # TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM15: None,
            # TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM16: None,
            #endregion

            #region Lake Hylia
            TMCLocation.HYLIA_SUNKEN_HP:
                self.has(Items.FLIPPERS),
            TMCLocation.HYLIA_DOG_NPC:
                self.has(Items.DOG_FOOD),
            TMCLocation.HYLIA_SMALL_ISLAND_HP:
                self.has(Items.ROCS_CAPE),
            TMCLocation.HYLIA_CAPE_CAVE_TOP_RIGHT:
                self.has_all([Items.MOLE_MITTS, Items.ROCS_CAPE]),
            TMCLocation.HYLIA_CAPE_CAVE_BOTTOM_LEFT:
                self.has_all([Items.MOLE_MITTS, Items.ROCS_CAPE]),
            TMCLocation.HYLIA_CAPE_CAVE_TOP_LEFT:
                self.has_all([Items.MOLE_MITTS, Items.ROCS_CAPE]),
            TMCLocation.HYLIA_CAPE_CAVE_TOP_MIDDLE:
                self.has_all([Items.MOLE_MITTS, Items.ROCS_CAPE]),
            TMCLocation.HYLIA_CAPE_CAVE_RIGHT:
                self.has_all([Items.MOLE_MITTS, Items.ROCS_CAPE]),
            TMCLocation.HYLIA_CAPE_CAVE_BOTTOM_RIGHT:
                self.has_all([Items.MOLE_MITTS, Items.ROCS_CAPE]),
            TMCLocation.HYLIA_CAPE_CAVE_BOTTOM_MIDDLE:
                self.has_all([Items.MOLE_MITTS, Items.ROCS_CAPE]),
            TMCLocation.HYLIA_CAPE_CAVE_LON_LON_HP:
                self.has_all([Items.MOLE_MITTS, Items.ROCS_CAPE]),
            TMCLocation.HYLIA_BEANSTALK_FUSION_LEFT_CHEST:
                # Fusion 23
                self.has_all([Items.MOLE_MITTS, Items.ROCS_CAPE]),
            TMCLocation.HYLIA_BEANSTALK_FUSION_HP:
                # Fusion 23
                self.has_all([Items.MOLE_MITTS, Items.ROCS_CAPE]),
            TMCLocation.HYLIA_BEANSTALK_FUSION_RIGHT_CHEST:
                # Fusion 23
                self.has_all([Items.MOLE_MITTS, Items.ROCS_CAPE]),
            TMCLocation.HYLIA_MIDDLE_ISLAND_FUSION_DIG_CAVE_CHEST:
                # Fusion 34
                self.has(Items.MOLE_MITTS),
            TMCLocation.HYLIA_BOTTOM_HP:
                self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
            TMCLocation.HYLIA_DOJO_HP:
                self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
            TMCLocation.HYLIA_DOJO_NPC:
                self.logic_and([
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
                    self.has_max_health(10),
                    self.has(Items.PROGRESSIVE_SWORD),
                ]),
            TMCLocation.HYLIA_CRACK_FUSION_LIBRARI_NPC:
                self.logic_and([
                    self.has(Items.OCARINA),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
                ]),
            TMCLocation.HYLIA_NORTH_MINISH_HOLE_CHEST:
                self.has_all([Items.FLIPPERS, Items.PEGASUS_BOOTS]),
            TMCLocation.HYLIA_SOUTH_MINISH_HOLE_CHEST:
                self.has_all([Items.FLIPPERS, Items.PEGASUS_BOOTS]),
            TMCLocation.HYLIA_CABIN_PATH_FUSION_CHEST:
                self.has_all([Items.PEGASUS_BOOTS, Items.GUST_JAR]), # fusion 51
            TMCLocation.HYLIA_MAYOR_CABIN_ITEM:
                self.has_all([Items.PEGASUS_BOOTS, Items.GUST_JAR, Items.POWER_BRACELETS]),
            #endregion

            #region Castor Wilds
            # TMCLocation.SWAMP_BUTTERFLY_FUSION_ITEM: None, # Fusion 10
            TMCLocation.SWAMP_CENTER_CAVE_DARKNUT_CHEST:
                self.has(Items.PROGRESSIVE_SWORD),
            TMCLocation.SWAMP_CENTER_CHEST:
                self.has(Items.PROGRESSIVE_BOW),
            TMCLocation.SWAMP_GOLDEN_ROPE: # Fusion 49
                self.can_attack(),
            TMCLocation.SWAMP_NEAR_WATERFALL_CAVE_HP:
                self.logic_and([
                    self.has(Items.PROGRESSIVE_BOW),
                    self.has_any([Items.ROCS_CAPE, Items.FLIPPERS]),
                ]),
            TMCLocation.SWAMP_WATERFALL_FUSION_DOJO_NPC: # Fusion 0C
                self.has_all([Items.PROGRESSIVE_BOW, Items.FLIPPERS]),
            TMCLocation.SWAMP_NORTH_CAVE_CHEST:
                self.has(Items.PROGRESSIVE_BOW),
            TMCLocation.SWAMP_DIGGING_CAVE_LEFT_CHEST:
                self.has(Items.MOLE_MITTS),
            TMCLocation.SWAMP_DIGGING_CAVE_RIGHT_CHEST:
                self.has(Items.MOLE_MITTS),
            TMCLocation.SWAMP_UNDERWATER_TOP:
                self.has(Items.FLIPPERS),
            TMCLocation.SWAMP_UNDERWATER_MIDDLE:
                self.has(Items.FLIPPERS),
            TMCLocation.SWAMP_UNDERWATER_BOTTOM:
                self.has(Items.FLIPPERS),
            TMCLocation.SWAMP_SOUTH_CAVE_CHEST:
                self.logic_or([
                    self.has_any([Items.ROCS_CAPE, Items.FLIPPERS]),
                    self.has_all([Items.PEGASUS_BOOTS, Items.PROGRESSIVE_BOW]),
                ]),
            TMCLocation.SWAMP_DOJO_HP:
                self.logic_or([
                    self.has_any([Items.ROCS_CAPE, Items.PROGRESSIVE_BOW]),
                    self.has_all([Items.PEGASUS_BOOTS, Items.FLIPPERS]),
                ]),
            TMCLocation.SWAMP_DOJO_NPC:
                self.logic_and([
                    self.logic_or([
                        self.has_any([Items.ROCS_CAPE, Items.PROGRESSIVE_BOW]),
                        self.has_all([Items.PEGASUS_BOOTS, Items.FLIPPERS]),
                    ]),
                    self.has(Items.PROGRESSIVE_SWORD),
                    self.has_group("Scrolls", 7),
                ]),
            TMCLocation.SWAMP_MINISH_FUSION_NORTH_CRACK_CHEST: # Fusion 4B
                self.has_any([Items.PEGASUS_BOOTS, Items.ROCS_CAPE, Items.PROGRESSIVE_BOW]),
            TMCLocation.SWAMP_MINISH_MULLDOZER_BIG_CHEST:
                self.logic_and([
                    self.has_any([Items.PEGASUS_BOOTS, Items.ROCS_CAPE, Items.PROGRESSIVE_BOW]),
                    self.has_any([Items.FLIPPERS, Items.GUST_JAR]),
                    self.can_attack(),
                ]),
            TMCLocation.SWAMP_MINISH_FUSION_NORTH_WEST_CRACK_CHEST: # Fusion 5B
                self.logic_and([
                    self.has_any([Items.PEGASUS_BOOTS, Items.ROCS_CAPE, Items.PROGRESSIVE_BOW]),
                    self.has_any([Items.FLIPPERS, Items.GUST_JAR]),
                ]),
            TMCLocation.SWAMP_MINISH_FUSION_WEST_CRACK_CHEST: # Fusion 57
                self.has_any([Items.PEGASUS_BOOTS, Items.ROCS_CAPE, Items.PROGRESSIVE_BOW]),
            TMCLocation.SWAMP_MINISH_FUSION_VINE_CRACK_CHEST: # Fusion 57 & 3E
                self.has_any([Items.PEGASUS_BOOTS, Items.ROCS_CAPE, Items.PROGRESSIVE_BOW]),
            TMCLocation.SWAMP_MINISH_FUSION_WATER_HOLE_CHEST: # Fusion 57
                self.logic_and([
                    self.has_any([Items.PEGASUS_BOOTS, Items.ROCS_CAPE, Items.PROGRESSIVE_BOW]),
                    self.has(Items.FLIPPERS),
                ]),
            TMCLocation.SWAMP_MINISH_FUSION_WATER_HOLE_HP: # Fusion 57
                self.logic_and([
                    self.has_any([Items.PEGASUS_BOOTS, Items.ROCS_CAPE, Items.PROGRESSIVE_BOW]),
                    self.has(Items.FLIPPERS),
                ]),
            #endregion

            #region Wind Ruins
            # TMCLocation.RUINS_BUTTERFLY_FUSION_ITEM: None, # Fusion 20
            TMCLocation.RUINS_BOMB_CAVE_CHEST:
                self.has(Items.BOMB_BAG),
            # TMCLocation.RUINS_MINISH_HOME_CHEST: None,
            # Everything beyond here requires at least 1 sword to pass the first armos
            TMCLocation.RUINS_PILLARS_FUSION_CHEST: # Fusion 64
                self.has(Items.PROGRESSIVE_SWORD),
            TMCLocation.RUINS_BEAN_STALK_FUSION_BIG_CHEST: # Fusion 17
                self.has(Items.PROGRESSIVE_SWORD),
            TMCLocation.RUINS_CRACK_FUSION_CHEST: # Fusion 41
                self.has(Items.PROGRESSIVE_SWORD),
            TMCLocation.RUINS_MINISH_CAVE_HP:
                self.has(Items.PROGRESSIVE_SWORD),
            TMCLocation.RUINS_ARMOS_KILL_LEFT_CHEST:
                self.has(Items.PROGRESSIVE_SWORD),
            TMCLocation.RUINS_ARMOS_KILL_RIGHT_CHEST:
                self.has(Items.PROGRESSIVE_SWORD),
            TMCLocation.RUINS_GOLDEN_OCTO: # Fusion 54
                self.has(Items.PROGRESSIVE_SWORD),
            TMCLocation.RUINS_NEAR_FOW_FUSION_CHEST: # Fusion 0A
                self.has(Items.PROGRESSIVE_SWORD),
            #endregion

            #region Royal Valley
            # TMCLocation.VALLEY_PRE_VALLEY_FUSION_CHEST: None, # Fusion 5F
            TMCLocation.VALLEY_GREAT_FAIRY_NPC:
                self.has(Items.BOMB_BAG),
            TMCLocation.VALLEY_LOST_WOODS_CHEST:
                self.has(Items.LANTERN),
            TMCLocation.VALLEY_DAMPE_NPC:
                self.has(Items.LANTERN),
            # Graveyard locations, require graveyard key and pegasus boots
            # TMCLocation.VALLEY_GRAVEYARD_BUTTERFLY_FUSION_ITEM: None, # Fusion 19
            # TMCLocation.VALLEY_GRAVEYARD_LEFT_FUSION_CHEST: None, # Fusion 5C
            TMCLocation.VALLEY_GRAVEYARD_LEFT_GRAVE_HP:
                self.split_rule(3),
            # TMCLocation.VALLEY_GRAVEYARD_RIGHT_FUSION_CHEST: None, # Fusion 5D
            # TMCLocation.VALLEY_GRAVEYARD_RIGHT_GRAVE_FUSION_CHEST: None, # Fusion 30
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
                self.has(Items.BOMB_BAG),
            TMCLocation.TOWN_SCHOOL_ROOF_CHEST:
                self.has(Items.CANE_OF_PACCI),
            TMCLocation.TOWN_SCHOOL_PATH_FUSION_CHEST:
                self.has(Items.CANE_OF_PACCI),
            TMCLocation.TOWN_SCHOOL_PATH_LEFT_CHEST:
                self.logic_and([
                    self.has(Items.CANE_OF_PACCI),
                    self.split_rule(4),
                ]),
            TMCLocation.TOWN_SCHOOL_PATH_MIDDLE_CHEST:
                self.logic_and([
                    self.has(Items.CANE_OF_PACCI),
                    self.split_rule(4),
                ]),
            TMCLocation.TOWN_SCHOOL_PATH_RIGHT_CHEST:
                self.logic_and([
                    self.has(Items.CANE_OF_PACCI),
                    self.split_rule(4),
                ]),
            TMCLocation.TOWN_SCHOOL_PATH_HP:
                self.logic_and([
                    self.has(Items.CANE_OF_PACCI),
                    self.split_rule(4),
                ]),
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
                self.logic_and([
                    self.access_town_left(),
                    self.has_bottle(),
                ]),
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
                self.logic_and([
                    self.can_reach([
                        TMCLocation.TOWN_WELL_LEFT_CHEST,
                        TMCLocation.TOWN_WELL_BOTTOM_CHEST,
                    ]),
                    self.split_rule(3),
                ]),
            TMCLocation.TOWN_DR_LEFT_ATTIC_ITEM:
                self.logic_and([
                    self.access_town_left(),
                    self.has(Items.POWER_BRACELETS),
                    self.has_any([Items.GUST_JAR, Items.BOMB_BAG]),
                    self.split_rule(2),
                ]),
            TMCLocation.TOWN_FOUNTAIN_BIG_CHEST:
                self.logic_and([
                    self.can_attack(),
                    self.access_town_fountain(),
                    self.has(Items.CANE_OF_PACCI),
                ]),
            TMCLocation.TOWN_FOUNTAIN_SMALL_CHEST:
                self.logic_and([
                    self.access_town_fountain(),
                    self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
                ]),
            TMCLocation.TOWN_FOUNTAIN_HP:
                self.logic_and([
                    self.access_town_fountain(),
                    self.has(Items.ROCS_CAPE),
                ]),
            TMCLocation.TOWN_LIBRARY_YELLOW_MINISH_NPC:
                self.complete_book_quest(),
            TMCLocation.TOWN_UNDER_LIBRARY_FROZEN_CHEST:
                self.has_all([Items.FLIPPERS, Items.LANTERN, Items.OCARINA, Items.CANE_OF_PACCI]),
            TMCLocation.TOWN_UNDER_LIBRARY_BIG_CHEST:
                self.logic_and([
                    self.can_attack(),
                    self.logic_or([
                        self.logic_and([
                            self.complete_book_quest(),
                            self.has(Items.GRIP_RING),
                            self.has_any([Items.GUST_JAR,Items.ROCS_CAPE]),
                        ]),
                        self.has_all([Items.FLIPPERS, Items.OCARINA, Items.CANE_OF_PACCI]),
                    ]),
                ]),
            TMCLocation.TOWN_UNDER_LIBRARY_UNDERWATER:
                self.has_all([Items.FLIPPERS, Items.OCARINA, Items.CANE_OF_PACCI]),
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
                self.has_any([Items.BOMB_BAG, Items.FLIPPERS]),
            TMCLocation.NORTH_FIELD_WATERFALL_FUSION_DOJO_NPC:
                self.has_all([Items.FLIPPERS, Items.PROGRESSIVE_SWORD]),
            #endregion

            #region DeepWoods
            TMCLocation.DEEPWOOD_2F_CHEST:
                self.has_any([Items.LANTERN, Items.GUST_JAR]),
            #TMCLocation.DEEPWOOD_1F_SLUG_TORCHES_CHEST : None,
            TMCLocation.DEEPWOOD_1F_BARREL_ROOM_CHEST:
                self.logic_and([
                    self.has(Items.SMALL_KEY_DWS,1),
                    self.has_any([Items.BOMB_BAG,Items.GUST_JAR])
                ]),
            TMCLocation.DEEPWOOD_1F_WEST_BIG_CHEST:
                self.has(Items.SMALL_KEY_DWS,1),
            TMCLocation.DEEPWOOD_1F_WEST_STATUE_PUZZLE_CHEST:
                self.has(Items.SMALL_KEY_DWS,1),
            TMCLocation.DEEPWOOD_1F_EAST_MULLDOZER_FIGHT_ITEM:
                self.logic_and([
                    self.has(Items.SMALL_KEY_DWS,4),
                    self.can_attack()
                ]),
            TMCLocation.DEEPWOOD_1F_NORTH_EAST_CHEST:
                self.logic_or([
                    self.logic_and([
                        self.has(Items.SMALL_KEY_DWS,2),
                        self.has(Items.BOMB_BAG)
                    ]),
                    self.logic_and([
                        self.has(Items.GUST_JAR),
                        self.has(Items.SMALL_KEY_DWS,1)
                    ])
                ]),
            TMCLocation.DEEPWOOD_B1_SWITCH_ROOM_BIG_CHEST:
                self.logic_or([
                    self.has(Items.SMALL_KEY_DWS,2),
                    self.logic_and([
                        self.has(Items.GUST_JAR),
                        self.has(Items.SMALL_KEY_DWS,1)
                    ])
                ]),
            TMCLocation.DEEPWOOD_B1_SWITCH_ROOM_CHEST:
                self.logic_or([
                    self.logic_and([
                        self.has(Items.SMALL_KEY_DWS,2),
                        self.has(Items.ROCS_CAPE)
                    ]),
                    self.logic_and([
                        self.has(Items.GUST_JAR),
                        self.has(Items.SMALL_KEY_DWS,1)
                    ])
                ]),

            TMCLocation.DEEPWOOD_1F_BLUE_WARP_HP:
                self.logic_or([
                    self.logic_and([
                        self.has(Items.SMALL_KEY_DWS,2),
                        self.has(Items.BOMB_BAG)
                    ]),
                    self.logic_and([
                        self.has(Items.GUST_JAR),
                        self.has(Items.SMALL_KEY_DWS,1)
                    ])
                ]),
            TMCLocation.DEEPWOOD_1F_BLUE_WARP_LEFT_CHEST:
                self.logic_or([
                    self.logic_and([
                        self.has(Items.SMALL_KEY_DWS,2),
                        self.has(Items.BOMB_BAG)
                    ]),
                    self.logic_and([
                        self.has(Items.GUST_JAR),
                        self.has(Items.SMALL_KEY_DWS,1)
                    ])
                ]),
            TMCLocation.DEEPWOOD_1F_BLUE_WARP_RIGHT_CHEST:
                self.logic_or([
                    self.logic_and([
                        self.has(Items.SMALL_KEY_DWS,2),
                        self.has(Items.BOMB_BAG)
                    ]),
                    self.logic_and([
                        self.has(Items.GUST_JAR),
                        self.has(Items.SMALL_KEY_DWS,1)
                    ])
                ]),
            TMCLocation.DEEPWOOD_1F_MADDERPILLAR_BIG_CHEST:
                self.logic_and([
                    self.can_attack(),
                    self.logic_or([
                        self.has(Items.SMALL_KEY_DWS,4),
                        self.logic_and([
                            self.has(Items.SMALL_KEY_DWS,2),
                            self.has(Items.LANTERN)
                        ]),
                        self.logic_and([
                            self.has_all([Items.GUST_JAR,Items.LANTERN]),
                            self.has(Items.SMALL_KEY_DWS,1)
                        ])
                    ])
                ]),
            TMCLocation.DEEPWOOD_1F_MADDERPILLAR_HP:
                    self.logic_or([
                        self.has(Items.SMALL_KEY_DWS,4),
                        self.logic_and([
                            self.has(Items.SMALL_KEY_DWS,2),
                            self.has(Items.LANTERN)
                        ]),
                        self.logic_and([
                            self.has_all([
                                Items.GUST_JAR,
                                Items.LANTERN
                            ]),
                            self.has(Items.SMALL_KEY_DWS,1)
                        ])
                    ]),
            TMCLocation.DEEPWOOD_B1_WEST_BIG_CHEST:
                self.logic_and([
                    self.has(Items.SMALL_KEY_DWS,4),
                    self.has(Items.GUST_JAR),
                ]),
            TMCLocation.DEEPWOOD_BOSS_ITEM:
                self.logic_and([
                    self.can_attack(),
                    self.has(Items.GUST_JAR),
                    self.has(Items.BIG_KEY_DWS)
                ]),
            TMCLocation.DEEPWOOD_PRIZE:
                self.logic_and([
                    self.can_attack(),
                    self.has(Items.GUST_JAR),
                    self.has(Items.BIG_KEY_DWS)
                ]),
             #endregion

            #region Dungeon CoF
            #TMCLocation.COF_1F_SPIKE_BEETLE_BIG_CHEST: none
            #TMCLocation.COF_1F_ITEM1: none
            #TMCLocation.COF_1F_ITEM2: none
            #TMCLocation.COF_1F_ITEM3: none
            #TMCLocation.COF_1F_ITEM4: none
            #TMCLocation.COF_1F_ITEM5: none
            #TMCLocation.COF_B1_HAZY_ROOM_BIG_CHEST: none
            #TMCLocation.COF_B1_HAZY_ROOM_SMALL_CHEST: none
            #TMCLocation.COF_B1_ROLLOBITE_CHEST: none
            #TMCLocation.COF_B1_ROLLOBITE_PILLAR_CHEST: none
            TMCLocation.COF_B1_SPIKEY_CHUS_PILLAR_CHEST:
                self.logic_and([
                    self.has(Items.CANE_OF_PACCI),
                    self.has(Items.SMALL_KEY_COF,1)
                ]),
            TMCLocation.COF_B1_HP:
                self.logic_and([
                    self.has(Items.BOMB_BAG),
                    self.has(Items.SMALL_KEY_COF,1)
                ]),
            TMCLocation.COF_B1_SPIKEY_CHUS_BIG_CHEST:
                self.logic_and([
                    self.can_attack(),
                    self.has(Items.SMALL_KEY_COF,1)
                ]),
            TMCLocation.COF_B2_PRE_LAVA_NORTH_CHEST:
                self.logic_and([
                    self.can_attack(),
                    self.has(Items.CANE_OF_PACCI),
                    self.has(Items.SMALL_KEY_COF,2)
                ]),
            TMCLocation.COF_B2_PRE_LAVA_SOUTH_CHEST:
                self.logic_and([
                    self.can_attack(),
                    self.has(Items.CANE_OF_PACCI),
                    self.has(Items.SMALL_KEY_COF,2)
                ]),
            TMCLocation.COF_B2_LAVA_ROOM_BLADE_CHEST:
                self.logic_and([
                    self.can_attack(),
                    self.has(Items.CANE_OF_PACCI),
                    self.has(Items.SMALL_KEY_COF,2),
                ]),
            TMCLocation.COF_B2_LAVA_ROOM_RIGHT_CHEST:
                self.logic_and([
                    self.can_attack(),
                    self.has(Items.CANE_OF_PACCI),
                    self.has(Items.SMALL_KEY_COF,2),
                ]),
            TMCLocation.COF_B2_LAVA_ROOM_LEFT_CHEST:
                self.logic_and([
                    self.can_attack(),
                    self.has(Items.CANE_OF_PACCI),
                    self.has(Items.SMALL_KEY_COF,2),
                ]),
            TMCLocation.COF_B2_LAVA_ROOM_BIG_CHEST:
                self.logic_and([
                    self.can_attack(),
                    self.has(Items.CANE_OF_PACCI),
                    self.has(Items.SMALL_KEY_COF,2),
                ]),
            TMCLocation.COF_BOSS_ITEM:
                self.logic_and([
                    self.can_attack(),
                    self.has_all([Items.CANE_OF_PACCI,Items.BIG_KEY_COF]),
                    self.has(Items.SMALL_KEY_COF,2),
                ]),
            TMCLocation.COF_PRIZE:
                self.logic_and([
                    self.can_attack(),
                    self.has_all([Items.CANE_OF_PACCI,Items.BIG_KEY_COF]),
                    self.has(Items.SMALL_KEY_COF,2),
                ]),
            #endregion

            #region Dungeon FOW
            TMCLocation.FORTRESS_ENTRANCE_1F_LEFT_CHEST:
                self.has(Items.MOLE_MITTS),
            TMCLocation.FORTRESS_ENTRANCE_1F_LEFT_WIZROBE_CHEST:
                self.has(Items.MOLE_MITTS),
            TMCLocation.FORTRESS_ENTRANCE_1F_RIGHT_ITEM:
                self.has(Items.MOLE_MITTS),
            TMCLocation.FORTRESS_LEFT_2F_DIG_CHEST:
                self.has_all([
                    Items.MOLE_MITTS,
                    Items.PROGRESSIVE_BOW
                ]),
            TMCLocation.FORTRESS_LEFT_2F_ITEM1:
                self.has(Items.PROGRESSIVE_BOW),
            TMCLocation.FORTRESS_LEFT_2F_ITEM2:
                self.has(Items.PROGRESSIVE_BOW),
            TMCLocation.FORTRESS_LEFT_2F_ITEM3:
                self.has(Items.PROGRESSIVE_BOW),
            TMCLocation.FORTRESS_LEFT_2F_ITEM4:
                self.has(Items.PROGRESSIVE_BOW),
            TMCLocation.FORTRESS_LEFT_2F_ITEM5:
                self.has(Items.PROGRESSIVE_BOW),
            TMCLocation.FORTRESS_LEFT_2F_ITEM6:
                self.has(Items.PROGRESSIVE_BOW),
            TMCLocation.FORTRESS_LEFT_2F_ITEM7:
                self.has(Items.PROGRESSIVE_BOW),
            TMCLocation.FORTRESS_LEFT_3F_SWITCH_CHEST:
                self.has_all([Items.MOLE_MITTS,Items.PROGRESSIVE_BOW]),
            TMCLocation.FORTRESS_LEFT_3F_EYEGORE_BIG_CHEST:
                self.has(Items.PROGRESSIVE_BOW),
            TMCLocation.FORTRESS_LEFT_3F_ITEM_DROP:
                self.logic_and([
                    self.has(Items.PROGRESSIVE_BOW),
                    self.logic_or([
                        self.has(Items.ROCS_CAPE),
                        self.split_rule(2),
                    ]),
                ]),
            TMCLocation.FORTRESS_MIDDLE_2F_BIG_CHEST:
                self.has(Items.PROGRESSIVE_BOW),
            TMCLocation.FORTRESS_MIDDLE_2F_STATUE_CHEST:
                self.has(Items.MOLE_MITTS),
            #TMCLocation.FORTRESS_RIGHT_2F_LEFT_CHEST: none
            #TMCLocation.FORTRESS_RIGHT_2F_RIGHT_CHEST: none
            TMCLocation.FORTRESS_RIGHT_2F_DIG_CHEST:
                self.has(Items.MOLE_MITTS),
            TMCLocation.FORTRESS_RIGHT_3F_DIG_CHEST:
                self.has(Items.MOLE_MITTS),
            #TMCLocation.FORTRESS_RIGHT_3F_ITEM_DROP: none
            #TMCLocation.FORTRESS_ENTRANCE_1F_RIGHT_HP: none
            TMCLocation.FORTRESS_BACK_LEFT_BIG_CHEST:
                self.logic_and([
                    self.has_all([
                        Items.PROGRESSIVE_BOW,
                        Items.BOMB_BAG
                    ]),
                    self.has(Items.SMALL_KEY_FOW,2)
                ]),
            TMCLocation.FORTRESS_BACK_LEFT_SMALL_CHEST:
                self.logic_and([
                    self.has_all([
                        Items.PROGRESSIVE_BOW,
                        Items.BOMB_BAG,
                        Items.MOLE_MITTS,
                    ]),
                    self.has(Items.SMALL_KEY_FOW,2)
                ]),
            TMCLocation.FORTRESS_BACK_RIGHT_STATUE_ITEM_DROP:
                self.logic_and([
                    self.has(Items.PROGRESSIVE_BOW),
                    self.has(Items.SMALL_KEY_FOW,2)
                ]),
            TMCLocation.FORTRESS_BACK_RIGHT_MINISH_ITEM_DROP:
                self.logic_and([
                    self.has_all([
                        Items.PROGRESSIVE_BOW,
                        Items.MOLE_MITTS,
                    ]),
                    self.has(Items.SMALL_KEY_FOW,3)
                ]),
            TMCLocation.FORTRESS_BACK_RIGHT_DIG_ROOM_TOP_POT:
                self.logic_and([
                    self.has_all([
                        Items.PROGRESSIVE_BOW,
                        Items.MOLE_MITTS,
                    ]),
                    self.has(Items.SMALL_KEY_FOW,3)
                ]),
            TMCLocation.FORTRESS_BACK_RIGHT_DIG_ROOM_BOTTOM_POT:
                self.logic_and([
                    self.has_all([
                        Items.PROGRESSIVE_BOW,
                        Items.MOLE_MITTS,
                    ]),
                    self.has(Items.SMALL_KEY_FOW,3)
                ]),
            TMCLocation.FORTRESS_BACK_RIGHT_BIG_CHEST:
                self.logic_and([
                    self.has_all([
                        Items.PROGRESSIVE_BOW,
                        Items.MOLE_MITTS,
                    ]),
                    self.has(Items.SMALL_KEY_FOW,4)
                ]),
            TMCLocation.FORTRESS_BOSS_ITEM:
                self.logic_and([
                    self.has_all([
                        Items.PROGRESSIVE_BOW,
                        Items.MOLE_MITTS,
                    ]),
                    self.has(Items.BIG_KEY_FOW)
                ]),
            TMCLocation.FORTRESS_PRIZE:
                self.logic_and([
                    self.has_all([
                        Items.PROGRESSIVE_BOW,
                        Items.MOLE_MITTS,
                    ]),
                    self.has(Items.BIG_KEY_FOW)
                ]),
            #endregion

            #region Dungeon TOD
            #TMCLocation.DROPLETS_ENTRANCE_B2_EAST_ICEBLOCK: none
            TMCLocation.DROPLETS_ENTRANCE_B2_WEST_ICEBLOCK:
                self.has(Items.SMALL_KEY_TOD,4),
            #endregion

            #region Dungeon TOD after Big Key
            #TMCLocation.DROPLETS_LEFT_PATH_B1_UNDERPASS_ITEM1:
            #TMCLocation.DROPLETS_LEFT_PATH_B1_UNDERPASS_ITEM2:
            #TMCLocation.DROPLETS_LEFT_PATH_B1_UNDERPASS_ITEM3:
            #TMCLocation.DROPLETS_LEFT_PATH_B1_UNDERPASS_ITEM4:
            #TMCLocation.DROPLETS_LEFT_PATH_B1_UNDERPASS_ITEM5:
            #TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_BIG_CHEST:
            TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_UNDERWATER1:
                self.has(Items.FLIPPERS),
            TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_UNDERWATER2:
                self.has(Items.FLIPPERS),
            TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_UNDERWATER3:
                self.has(Items.FLIPPERS),
            TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_UNDERWATER4:
                self.has(Items.FLIPPERS),
            TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_UNDERWATER5:
                self.has(Items.FLIPPERS),
            TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_UNDERWATER6:
                self.has(Items.FLIPPERS),
            TMCLocation.DROPLETS_LEFT_PATH_B2_WATERFALL_UNDERWATER1:
                self.logic_and([
                    self.has(Items.FLIPPERS),
                    self.has_any([
                        Items.GUST_JAR,
                        Items.ROCS_CAPE
                    ])
                ]),
            TMCLocation.DROPLETS_LEFT_PATH_B2_WATERFALL_UNDERWATER2:
                self.logic_and([
                    self.has(Items.FLIPPERS),
                    self.has_any([
                        Items.GUST_JAR,
                        Items.ROCS_CAPE
                    ])
                ]),
            TMCLocation.DROPLETS_LEFT_PATH_B2_WATERFALL_UNDERWATER3:
                self.logic_and([
                    self.has(Items.FLIPPERS),
                    self.has_any([
                        Items.GUST_JAR,
                        Items.ROCS_CAPE
                    ])
                ]),
            TMCLocation.DROPLETS_LEFT_PATH_B2_WATERFALL_UNDERWATER4:
                self.logic_and([
                    self.has(Items.FLIPPERS),
                    self.has_any([
                        Items.GUST_JAR,
                        Items.ROCS_CAPE
                    ])
                ]),
            TMCLocation.DROPLETS_LEFT_PATH_B2_WATERFALL_UNDERWATER5:
                self.logic_and([
                    self.has(Items.FLIPPERS),
                    self.has_any([
                        Items.GUST_JAR,
                        Items.ROCS_CAPE
                    ])
                ]),
            TMCLocation.DROPLETS_LEFT_PATH_B2_WATERFALL_UNDERWATER6:
                self.logic_and([
                    self.has(Items.FLIPPERS),
                    self.has_any([
                        Items.GUST_JAR,
                        Items.ROCS_CAPE
                    ])
                ]),
            TMCLocation.DROPLETS_LEFT_PATH_B2_UNDERWATER_POT:
                self.logic_and([
                    self.has(Items.FLIPPERS),
                    self.has_any([
                        Items.GUST_JAR,
                        Items.ROCS_CAPE
                    ])
                ]),
            TMCLocation.DROPLETS_LEFT_PATH_B2_ICE_MADDERPILLAR_BIG_CHEST:
                self.logic_and([
                    self.has(Items.SMALL_KEY_TOD,4),
                    self.can_attack(),
                    self.has_all([
                        Items.FLIPPERS,
                        Items.GUST_JAR
                    ])
                ]),
            TMCLocation.DROPLETS_LEFT_PATH_B2_ICE_PLAIN_FROZEN_CHEST:
                self.logic_and([
                    self.has(Items.SMALL_KEY_TOD,4),
                    self.has(Items.LANTERN),
                    self.logic_or([
                        self.has_all([
                            Items.FLIPPERS,
                            Items.GUST_JAR
                        ]),
                        self.logic_and([
                            self.can_attack(),
                            self.has(Items.ROCS_CAPE)
                        ]),
                    ]),
                ]),
            TMCLocation.DROPLETS_LEFT_PATH_B2_ICE_PLAIN_CHEST:
                self.logic_and([
                    self.has(Items.SMALL_KEY_TOD,4),
                    self.logic_or([
                        self.has_all([
                            Items.FLIPPERS,
                            Items.GUST_JAR
                        ]),
                        self.logic_and([
                            self.can_attack(),
                            self.has(Items.LANTERN),
                            self.has(Items.ROCS_CAPE)
                        ]),
                    ]),
                ]),
            TMCLocation.DROPLETS_LEFT_PATH_B2_LILYPAD_CORNER_FROZEN_CHEST:
                self.logic_and([
                    self.has(Items.SMALL_KEY_TOD,4),
                    self.has_all([
                        Items.FLIPPERS,
                        Items.GUST_JAR,
                        Items.LANTERN
                    ])
                ]),
            TMCLocation.DROPLETS_RIGHT_PATH_B1_1ST_CHEST:
                self.logic_or([
                    self.droplet_right_lever(),
                    self.has(Items.LANTERN)
                ]),
            TMCLocation.DROPLETS_RIGHT_PATH_B1_2ND_CHEST:
                self.logic_or([
                    self.droplet_right_lever(),
                    self.has(Items.LANTERN)
                ]),
            TMCLocation.DROPLETS_RIGHT_PATH_B1_POT:
                self.logic_or([
                    self.droplet_right_lever(),
                    self.has(Items.LANTERN)
                ]),
            TMCLocation.DROPLETS_RIGHT_PATH_B3_FROZEN_CHEST:
                self.logic_or([
                    self.droplet_right_lever(),
                    self.has(Items.LANTERN)
                ]),
            TMCLocation.DROPLETS_RIGHT_PATH_B1_BLU_CHU_BIG_CHEST:
                self.logic_and([
                    self.logic_or([
                        self.droplet_right_lever(),
                        self.has(Items.LANTERN)
                    ]),
                    self.has(Items.SMALL_KEY_TOD,4),
                    self.has(Items.GUST_JAR),
                    self.can_attack()
                ]),
            TMCLocation.DROPLETS_RIGHT_PATH_B2_FROZEN_CHEST:
                    self.has(Items.LANTERN),
            TMCLocation.DROPLETS_RIGHT_PATH_B2_DARK_MAZE_BOTTOM_CHEST:
                self.logic_and([
                    self.can_attack(),
                    self.has(Items.LANTERN),
                ]),
            TMCLocation.DROPLETS_RIGHT_PATH_B2_MULLDOZERS_ITEM_DROP:
                self.logic_and([
                    self.can_attack(),
                    self.has_all([
                        Items.LANTERN,
                        Items.BOMB_BAG
                    ]),
                ]),
            TMCLocation.DROPLETS_RIGHT_PATH_B2_DARK_MAZE_TOP_RIGHT_CHEST:
                self.logic_and([
                    self.can_attack(),
                    self.has(Items.LANTERN),
                ]),
            TMCLocation.DROPLETS_RIGHT_PATH_B2_DARK_MAZE_TOP_LEFT_CHEST:
                self.logic_and([
                    self.can_attack(),
                    self.has(Items.LANTERN),
                ]),
            TMCLocation.DROPLETS_RIGHT_PATH_B2_UNDERPASS_ITEM1:
                self.logic_and([
                    self.can_attack(),
                    self.has(Items.LANTERN),
                    self.has(Items.SMALL_KEY_TOD,4)
                ]),
            TMCLocation.DROPLETS_RIGHT_PATH_B2_UNDERPASS_ITEM2:
                self.logic_and([
                    self.can_attack(),
                    self.has(Items.LANTERN),
                    self.has(Items.SMALL_KEY_TOD,4)
                ]),
            TMCLocation.DROPLETS_RIGHT_PATH_B2_UNDERPASS_ITEM3:
                self.logic_and([
                    self.can_attack(),
                    self.has(Items.LANTERN),
                    self.has(Items.SMALL_KEY_TOD,4)
                ]),
            TMCLocation.DROPLETS_RIGHT_PATH_B2_UNDERPASS_ITEM4:
                self.logic_and([
                    self.can_attack(),
                    self.has(Items.LANTERN),
                    self.has(Items.SMALL_KEY_TOD,4)
                ]),
            TMCLocation.DROPLETS_RIGHT_PATH_B2_UNDERPASS_ITEM5:
                self.logic_and([
                    self.can_attack(),
                    self.has(Items.LANTERN),
                    self.has(Items.SMALL_KEY_TOD,4)
                ]),
            TMCLocation.DROPLETS_BOSS_ITEM:
                self.logic_and([
                    self.droplet_right_lever(),
                    self.droplet_left_lever()
                ]),
            TMCLocation.DROPLETS_PRIZE:
                self.logic_and([
                    self.droplet_right_lever(),
                    self.droplet_left_lever()
                ]),
            #endregion

            #region Dungeon RC
            TMCLocation.CRYPT_GIBDO_LEFT_ITEM:
                self.can_attack(),
            TMCLocation.CRYPT_GIBDO_RIGHT_ITEM:
                self.can_attack(),
            TMCLocation.CRYPT_LEFT_ITEM:
                self.logic_and([
                    self.split_rule(3),
                    self.has(Items.SMALL_KEY_RC,1),
                ]),
            TMCLocation.CRYPT_RIGHT_ITEM:
                self.logic_and([
                    self.split_rule(3),
                    self.has(Items.SMALL_KEY_RC,1),
                ]),
            TMCLocation.CRYPT_PRIZE:
                self.logic_and([
                    self.can_attack(),
                    self.has(Items.SMALL_KEY_RC,3),
                    self.has(Items.LANTERN)
                ]),
            #endregion

            #region Dungeon POW
            TMCLocation.PALACE_1ST_HALF_1F_GRATE_CHEST:
                self.has(Items.ROCS_CAPE),
            #TMCLocation.PALACE_1ST_HALF_1F_WIZROBE_BIG_CHEST: None
            TMCLocation.PALACE_1ST_HALF_2F_ITEM1:
                self.has_all([
                    Items.CANE_OF_PACCI,
                    Items.ROCS_CAPE
                ]),
            TMCLocation.PALACE_1ST_HALF_2F_ITEM2:
                self.has_all([
                    Items.CANE_OF_PACCI,
                    Items.ROCS_CAPE
                ]),
            TMCLocation.PALACE_1ST_HALF_2F_ITEM3:
                self.has_all([
                    Items.CANE_OF_PACCI,
                    Items.ROCS_CAPE
                ]),
            TMCLocation.PALACE_1ST_HALF_2F_ITEM4:
                self.has_all([
                    Items.CANE_OF_PACCI,
                    Items.ROCS_CAPE
                ]),
            TMCLocation.PALACE_1ST_HALF_2F_ITEM5:
                self.has_all([
                    Items.CANE_OF_PACCI,
                    Items.ROCS_CAPE
                ]),
            TMCLocation.PALACE_1ST_HALF_3F_POT_PUZZLE_ITEM_DROP:
                self.has_all([
                    Items.CANE_OF_PACCI,
                    Items.ROCS_CAPE,
                    Items.POWER_BRACELETS
                ]),
            TMCLocation.PALACE_1ST_HALF_4F_BOW_MOBLINS_CHEST:
                self.logic_and([
                    self.has_all([
                        Items.CANE_OF_PACCI,
                        Items.ROCS_CAPE
                    ]),
                    self.has(Items.SMALL_KEY_POW,1)
                ]),
            TMCLocation.PALACE_1ST_HALF_5F_BALL_AND_CHAIN_SOLDIERS_ITEM_DROP:
                self.logic_and([
                    self.has_all([
                        Items.CANE_OF_PACCI,
                        Items.ROCS_CAPE
                    ]),
                    self.has(Items.SMALL_KEY_POW,1)
                ]),
            TMCLocation.PALACE_1ST_HALF_5F_FAN_LOOP_CHEST:
                self.logic_and([
                    self.has_all([
                        Items.CANE_OF_PACCI,
                        Items.ROCS_CAPE
                    ]),
                    self.has(Items.SMALL_KEY_POW,5)
                ]),
            TMCLocation.PALACE_1ST_HALF_5F_BIG_CHEST:
                self.logic_and([
                    self.has_all([
                        Items.CANE_OF_PACCI,
                        Items.ROCS_CAPE
                    ]),
                    self.has(Items.SMALL_KEY_POW,6)
                ]),
            TMCLocation.PALACE_2ND_HALF_1F_DARK_ROOM_BIG_CHEST:
                self.logic_and([
                    self.has_all([
                        Items.CANE_OF_PACCI,
                        Items.ROCS_CAPE,
                        Items.BIG_KEY_POW,
                        Items.LANTERN
                    ]),
                    self.has(Items.SMALL_KEY_POW,4),
                ]),
            TMCLocation.PALACE_2ND_HALF_1F_DARK_ROOM_SMALL_CHEST:
                self.logic_and([
                    self.has_all([
                        Items.CANE_OF_PACCI,
                        Items.ROCS_CAPE,
                        Items.BIG_KEY_POW,
                        Items.LANTERN
                    ]),
                    self.has(Items.SMALL_KEY_POW,4),
                ]),
            TMCLocation.PALACE_2ND_HALF_2F_MANY_ROLLERS_CHEST:
                self.logic_and([
                    self.has_all([
                        Items.CANE_OF_PACCI,
                        Items.ROCS_CAPE,
                        Items.BIG_KEY_POW,
                        Items.LANTERN
                    ]),
                    self.has(Items.SMALL_KEY_POW,4)
                ]),
            TMCLocation.PALACE_2ND_HALF_2F_TWIN_WIZROBES_CHEST:
                self.logic_and([
                    self.has_all([
                        Items.CANE_OF_PACCI,
                        Items.ROCS_CAPE,
                        Items.BIG_KEY_POW,
                        Items.LANTERN
                    ]),
                    self.has(Items.SMALL_KEY_POW,4),
                ]),
            TMCLocation.PALACE_2ND_HALF_3F_FIRE_WIZROBES_BIG_CHEST:
                self.logic_and([
                    self.has_all([
                        Items.CANE_OF_PACCI,
                        Items.ROCS_CAPE,
                        Items.BIG_KEY_POW,
                        Items.LANTERN
                    ]),
                    self.has(Items.SMALL_KEY_POW,4),
                ]),
            TMCLocation.PALACE_2ND_HALF_4F_HP:
                self.logic_and([
                    self.has_all([
                        Items.CANE_OF_PACCI,
                        Items.ROCS_CAPE,
                        Items.BIG_KEY_POW,
                        Items.LANTERN
                    ]),
                    self.has(Items.SMALL_KEY_POW,4),
                ]),
            TMCLocation.PALACE_2ND_HALF_4F_SWITCH_HIT_CHEST:
                self.logic_and([
                    self.has_all([
                        Items.CANE_OF_PACCI,
                        Items.ROCS_CAPE,
                        Items.BIG_KEY_POW,
                        Items.LANTERN
                    ]),
                    self.has(Items.SMALL_KEY_POW,4),
                ]),
            TMCLocation.PALACE_2ND_HALF_5F_BOMBAROSSA_CHEST:
                self.logic_and([
                    self.has_all([
                        Items.CANE_OF_PACCI,
                        Items.ROCS_CAPE,
                        Items.BIG_KEY_POW,
                        Items.LANTERN
                    ]),
                    self.has(Items.SMALL_KEY_POW,5),
                ]),
            TMCLocation.PALACE_2ND_HALF_4F_BLOCK_MAZE_CHEST:
                self.logic_and([
                    self.has_all([
                        Items.CANE_OF_PACCI,
                        Items.ROCS_CAPE,
                        Items.BIG_KEY_POW,
                        Items.LANTERN
                    ]),
                    self.has(Items.SMALL_KEY_POW,6),
                ]),
            TMCLocation.PALACE_2ND_HALF_5F_RIGHT_SIDE_CHEST:
                self.logic_and([
                    self.has_all([
                        Items.CANE_OF_PACCI,
                        Items.ROCS_CAPE,
                        Items.BIG_KEY_POW,
                        Items.LANTERN
                    ]),
                    self.has(Items.SMALL_KEY_POW,6),
                ]),
            TMCLocation.PALACE_BOSS_ITEM:
                self.logic_and([
                    self.has_all([
                        Items.CANE_OF_PACCI,
                        Items.ROCS_CAPE,
                        Items.BIG_KEY_POW,
                        Items.LANTERN
                    ]),
                    self.has(Items.SMALL_KEY_POW,6),
                ]),
            TMCLocation.PALACE_PRIZE:
                self.logic_and([
                    self.has_all([
                        Items.CANE_OF_PACCI,
                        Items.ROCS_CAPE,
                        Items.BIG_KEY_POW,
                        Items.LANTERN
                    ]),
                    self.has(Items.SMALL_KEY_POW,6),
                ]),
            #endregion

            #region Sanctuary
            TMCLocation.SANCTUARY_PEDESTAL_ITEM1:
                self.has_group("Elements", 2),
            TMCLocation.SANCTUARY_PEDESTAL_ITEM2:
                self.has_group("Elements", 3),
            TMCLocation.SANCTUARY_PEDESTAL_ITEM3:
                self.has_group("Elements", 4),
            #endregion

            #region Dungeon DHC
            TMCLocation.DHC_B2_KING:
                 self.has(Items.PROGRESSIVE_SWORD,5),
            #TMCLocation.DHC_B1_BIG_CHEST: none
            TMCLocation.DHC_1F_BLADE_CHEST:
                self.split_rule(4),
            TMCLocation.DHC_1F_THRONE_BIG_CHEST:
                self.logic_and([
                    self.split_rule(4),
                    self.has(Items.SMALL_KEY_DHC,1),
                ]),
            TMCLocation.DHC_3F_NORTH_WEST_CHEST:
                self.logic_and([
                    self.split_rule(4),
                    self.has(Items.SMALL_KEY_DHC,1),
                    self.has_all([
                        Items.BOMB_BAG,
                        Items.PROGRESSIVE_BOW,
                        Items.ROCS_CAPE
                    ]),
                ]),
            TMCLocation.DHC_3F_NORTH_EAST_CHEST:
                self.logic_and([
                    self.split_rule(4),
                    self.has(Items.SMALL_KEY_DHC,1),
                    self.has_all([
                        Items.BOMB_BAG,
                        Items.ROCS_CAPE,
                        Items.LANTERN
                    ]),
                    self.logic_or([
                        self.has(Items.PROGRESSIVE_BOOMERANG,2),
                        self.has_any([
                            Items.PERIL_BEAM,
                            Items.SWORD_BEAM,
                            Items.PROGRESSIVE_BOW
                        ]),
                    ]),
                ]),
            TMCLocation.DHC_3F_SOUTH_WEST_CHEST:
                self.logic_and([
                    self.split_rule(4),
                    self.has(Items.SMALL_KEY_DHC,1),
                    self.has_all([
                        Items.BOMB_BAG,
                        Items.ROCS_CAPE,
                    ]),
                    self.logic_or([
                        self.has(Items.PROGRESSIVE_BOOMERANG,2),
                        self.has_any([
                            Items.PERIL_BEAM,
                            Items.SWORD_BEAM,
                            Items.PROGRESSIVE_BOW
                        ]),
                    ]),
                ]),
            TMCLocation.DHC_3F_SOUTH_EAST_CHEST:
                self.logic_and([
                    self.split_rule(4),
                    self.has(Items.SMALL_KEY_DHC,1),
                    self.has_all([
                        Items.BOMB_BAG,
                        Items.ROCS_CAPE,
                    ]),
                    self.logic_or([
                        self.has(Items.PROGRESSIVE_BOOMERANG,2),
                        self.has_any([
                            Items.PERIL_BEAM,
                            Items.SWORD_BEAM,
                            Items.PROGRESSIVE_BOW
                        ]),
                    ]),
                ]),
            TMCLocation.DHC_2F_BLUE_WARP_BIG_CHEST:
                self.logic_and([
                    self.split_rule(4),
                    self.has(Items.SMALL_KEY_DHC,5),
                    self.has_all([
                        Items.BOMB_BAG,
                        Items.ROCS_CAPE,
                    ]),
                    self.logic_or([
                        self.has(Items.PROGRESSIVE_BOOMERANG,2),
                        self.has_any([
                            Items.PERIL_BEAM,
                            Items.SWORD_BEAM,
                            Items.PROGRESSIVE_BOW
                        ]),
                    ]),
                ]),
            #endregion
        }


    def logic_or(self, rules: [CollectionRule]) -> CollectionRule:
        return lambda state: any(rule(state) for rule in rules)

    def logic_and(self, rules: [CollectionRule]) -> CollectionRule:
        return lambda state: all(rule(state) for rule in rules)

    def droplet_right_lever(self) -> CollectionRule:
        return self.logic_and([self.can_attack(), self.split_rule(2), self.has(Items.SMALL_KEY_TOD,4), self.has_all([Items.LANTERN,Items.BOMB_BAG,Items.FLIPPERS])])

    def droplet_left_lever(self) -> CollectionRule:
        return self.logic_and([self.has(Items.SMALL_KEY_TOD,4),self.logic_or([self.has_all([Items.FLIPPERS,Items.GUST_JAR]),self.logic_and([self.can_attack(),self.has(Items.LANTERN),self.has(Items.ROCS_CAPE),]),]),])

    def has_4_elements(self) -> CollectionRule:
        return self.has_all([Items.EARTH_ELEMENT, Items.WATER_ELEMENT, Items.FIRE_ELEMENT, Items.WIND_ELEMENT])

    def has_group(self, item_group_name: str, count: int = 1) -> CollectionRule:
        return lambda state: state.has_group(item_group_name, self.player, count)

    def has_max_health(self, hearts = 3) -> CollectionRule:
        def heart_count(state: CollectionState) -> bool:
            heart_containers = state.count(Items.HEART_CONTAINER.item_name, self.player)
            heart_pieces = state.count(Items.HEART_PIECE.item_name, self.player)

            max_health = heart_containers + (heart_pieces // 4) + 3
            return max_health >= hearts

        return heart_count

    def can_spin(self) -> CollectionRule:
        return self.logic_and([
            self.has(Items.PROGRESSIVE_SWORD),
            self.has_any([Items.SPIN_ATTACK, Items.FAST_SPIN_SCROLL])
        ])

    def split_rule(self, link_count: int = 2) -> CollectionRule:
        return self.logic_and([
            self.has(Items.PROGRESSIVE_SWORD, link_count + 1),
            self.can_spin()
        ])

    def can_shield(self) -> CollectionRule:
        return self.has_any([Items.SHIELD, Items.MIRROR_SHIELD])

    def can_attack(self) -> CollectionRule:
        return self.has(Items.PROGRESSIVE_SWORD)

    def can_pass_trees(self) -> CollectionRule:
        return self.logic_or([
            self.has_any([Items.PROGRESSIVE_SWORD, Items.BOMB_BAG, Items.LANTERN]),
            self.has(Items.PROGRESSIVE_BOW, 2)
        ])

    def access_town_left(self) -> CollectionRule:
        return self.has_any([Items.ROCS_CAPE, Items.FLIPPERS, Items.CANE_OF_PACCI])

    def has_bottle(self) -> CollectionRule:
        return self.has_any([Items.BOTTLE_1, Items.BOTTLE_2, Items.BOTTLE_3, Items.BOTTLE_4])

    def access_town_fountain(self) -> CollectionRule:
        return self.logic_and([
            self.access_town_left(),
            self.has_bottle(),
        ])

    def access_minish_woods_top_left(self) -> CollectionRule:
        return self.logic_or([
            self.has_any([Items.FLIPPERS, Items.ROCS_CAPE]),
            self.logic_and([
                self.access_lonlon_right(),
                self.has(Items.CANE_OF_PACCI),
            ])
        ])

    def access_melari(self) -> CollectionRule:
        return

    def complete_book_quest(self) -> CollectionRule:
        return self.has_all([
            Items.OCARINA,
            Items.CANE_OF_PACCI,
            Items.RED_BOOK,
            Items.BLUE_BOOK,
            Items.GREEN_BOOK,
        ])

    def access_lonlon_right(self) -> CollectionRule:
        """ Assumes can_pass_trees is already used somewhere in the chain """
        return self.logic_or([
            self.has_any([Items.LONLON_KEY, Items.ROCS_CAPE]),
            self.has_all([Items.FLIPPERS, Items.MOLE_MITTS]),
        ])

    def has(self, item: ItemData, count: int = 1) -> CollectionRule:
        return lambda state: state.has(item.item_name, self.player, count)

    def has_all(self, items: [ItemData]) -> CollectionRule:
        return lambda state: state.has_all(map(item_to_name, items), self.player)

    def has_any(self, items: [ItemData]) -> CollectionRule:
        return lambda state: state.has_any(map(item_to_name, items), self.player)

    def can_reach(self, locations: [str]) -> CollectionRule:
        return lambda state: all(state.can_reach(loc, "Location", self.player) for loc in locations)

    def set_rules(self, disabled_locations: set[int], location_name_to_id: dict[str, id], options: MinishCapOptions) -> None:
        multiworld = self.world.multiworld

        # menu_region = multiworld.get_region("Menu", self.player)
        for region_pair, rule in self.connection_rules.items():
            region_one = multiworld.get_region(region_pair[0], self.player)
            region_two = multiworld.get_region(region_pair[1], self.player)
            region_one.connect(region_two, rule=rule)

        for loc in multiworld.get_locations(self.player):
            if loc.name not in location_name_to_id or loc.name in disabled_locations:
                continue

            if loc.name in self.location_rules and self.location_rules[loc.name] is not None:
                add_rule(loc, self.location_rules[loc.name])

        multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
