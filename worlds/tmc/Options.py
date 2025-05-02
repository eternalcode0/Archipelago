from dataclasses import dataclass
from Options import Choice, DefaultOnToggle, Toggle, StartInventoryPool, PerGameCommonOptions, Range, DeathLink

class DungeonItem(Choice):
    value: int
    # EternalCode's note: I want to experiment with a `closed` for small/big keys to actually remove them from the pool
    # entirely and keep the doors closed. All locations behind them would be removed & inaccessible.
    # Elements would need to be forced to be anywhere under this setting.
    # option_closed = 0 # New compared to TMCR (compass/map removed from pool, locations behind keys inaccessible, I doubt many would use this but it'd be relatively simple to implement)
    # option_open = 1 # TMCR Removed (compass/map start_inventory, keys removed from pool, doors are open at the start of the save)
    # option_vanilla = 2
    option_own_dungeon = 3
    # option_own_region = 4
    # option_any_dungeon = 5
    # option_any_region = 6
    # 7 reserved for option specific settings (small key = universal)
    option_anywhere = 8
    alias_true = 8
    alias_false = 3

class Rupeesanity(Toggle):
    """Add all rupees locations to the pool to be randomized."""
    display_name = "Rupee-sanity"

class ObscureSpots(Toggle):
    """Add all special pots, dig spots, etc. that drop a unique item to the pool."""
    display_name = "Obscure Spots"

class ShuffleElements(Choice):
    # EternalCode's Note: I'd like to experiment with ElementShuffle extending DungeonItem choice, just for consistency.
    # The settings would be slightly repurposed to something like this
    # `closed`: elements removed from pool, goal_elements forced to 0
    # `open`: elements added to start inventory (pretty useless all things considered)
    # `vanilla`: elements in their usual dungeon prize location
    # `own_dungeon`: place a element anywhere in it's usual dungeon
    # `own_region`: place element in the vacinity of it's usual dungeon
    # `any_dungeon`: place elements anywhere in any dungeon
    # `any_region`: place elements anywhere in the vacinity of any dungeon
    # `dungeon_prize` (default): Elements are shuffled between the 6 dungeon prizes
    # `anywhere`: full random
    """
    Lock elements to specific locations
    Vanilla: Elements are in the same dungeons as vanilla
    Dungeon Prize (false/default): Elements are shuffled between the 6 dungeon prizes
    Anywhere (true): Elements are in completely random locations
    """
    display_name = "Element Shuffle"
    default = 7
    option_vanilla = 2
    option_dungeon_prize = 7
    option_anywhere = 8
    alias_true = 8
    alias_false = 7

class SmallKeys(DungeonItem):
    """
    Own Dungeon (false/default): Randomized within the dungeon they're normally found in
    Anywhere (true): Items are in completely random locations
    """
    display_name = "Small Key Shuffle"
    default = 3

class BigKeys(DungeonItem):
    """
    Own Dungeon (default/false): Randomized within the dungeon they're normally found in
    Anywhere (true): Items are in completely random locations
    """
    display_name = "Big Key Shuffle"
    default = 3

class DungeonMaps(DungeonItem):
    """
    Own Dungeon (default/false): Randomized within the dungeon they're normally found in
    Anywhere (true): Items are in completely random locations
    """
    display_name = "Dungeon Maps Shuffle"
    default = 3

class DungeonCompasses(DungeonItem):
    """
    Own Dungeon (default/false): Randomized within the dungeon they're normally found in
    Anywhere (true): Items are in completely random locations
    """
    display_name = "Dungeon Compasses Shuffle"
    default = 3

class GoalVaati(DefaultOnToggle):
    """
    If enabled, DHC will open after completing Pedestal. Kill Vaati to goal.
    If disabled, complete Pedestal to goal. DHC/Vaati is unnecessary.
    """
    display_name = "Vaati Goal"

class PedDungeons(Range):
    """
    How many dungeons are required to activate Pedestal?
    If GoalVaati is on then you need this many dungeons cleared before DHC opens,
    otherwise you goal immediately upon having this many dungeons cleared
    (and other goal conditions) and entering sanctuary
    """
    display_name = "Required Dungeons to Pedestal"
    default = 0
    range_start = 0
    range_end = 6

class PedElements(Range):
    """
    How many elements are required to activate Pedestal?
    If GoalVaati is on then you need this many elements before DHC opens,
    otherwise you goal immediately upon having this many elements (and other goal conditions) and entering sanctuary
    """
    display_name = "Required Elements to Pedestal"
    default = 4
    range_start = 0
    range_end = 4

class PedSword(Range):
    """
    What level of sword is required to activate Pedestal?
    If GoalVaati is on then you need at least this sword level before DHC opens,
    otherwise you goal immediately upon having this sword level (and other goal conditions) and entering sanctuary
    """
    display_name = "Required Swords to Pedestal"
    default = 5
    range_start = 0
    range_end = 5

class PedFigurines(Range):
    """
    How many figurines are required to activate Pedestal?
    If GoalVatti is on then you need at least this many figurines before DHC opens,
    otherwise you goal immediately upon having this many figurines (and other goal conditons) and entering sanctuary
    """
    display_name = "Required Figurines to Pedestal"
    default = 0
    range_start = 0
    range_end = 136

class FigurineAmount(Range):
    """
    How many figurines are added to the pool?
    Should not be lower than GoalFigurines, otherwise it will be overriden to match GoalFigurines.
    """
    display_name = "Figurines in Pool"
    default = 0
    range_start = 0
    range_end = 136

class EarlyWeapon(Toggle):
    """Force a weapon to be in your sphere 1"""
    display_name = "Early Weapon"

class DeathLinkGameover(Toggle):
    """
    If disabled, deathlinks are sent when reaching 0HP, before a fairy is used. Received deathlinks will drop you to
    0HP, using a fairy if you have one.
    If enabled, deathlinks are only sent when reaching the gameover screen. Received deathlinks will also send you
    straight to a gameover, fairy or not.
    """
    display_name = "Deathlink is Gameover"

@dataclass
class MinishCapOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
    death_link_gameover: DeathLinkGameover
    goal_vaati: GoalVaati
    ped_elements: PedElements
    ped_swords: PedSword
    ped_dungeons: PedDungeons
    # ped_figurines: GoalFigurines
    # figurine_amount: FigurineAmount
    shuffle_elements: ShuffleElements
    rupeesanity: Rupeesanity
    obscure_spots: ObscureSpots
    early_weapon: EarlyWeapon
    dungeon_small_keys: SmallKeys
    dungeon_big_keys: BigKeys
    dungeon_maps: DungeonMaps
    dungeon_compasses: DungeonCompasses

def get_option_data(options: MinishCapOptions):
    """
    Template for the options that will likely be added in the future.
    Intended for trackers to properly match the logic between the standalone randomizer (TMCR) and AP
    """
    return {
        "goal_dungeons": options.ped_dungeons.value, # 0-6
        "goal_swords": options.ped_swords.value, # 0-5
        "goal_elements": options.ped_elements.value, # 0-4
        "goal_figurines": 0, # 0-136
        "dungeon_warp_dws": 0, # 0 = None, 1 = Blue, 2 = Red, 3 = Both
        "dungeon_warp_cof": 0,
        "dungeon_warp_fow": 0,
        "dungeon_warp_tod": 0,
        "dungeon_warp_pow": 0,
        "dungeon_warp_dhc": 0,
        "cucco_rounds": 1, # 0-10
        "goron_sets": 0, # 0-5
        "shuffle_heart_pieces": 1,
        "shuffle_rupees": options.rupeesanity.value,
        "shuffle_pots": options.obscure_spots.value,
        "shuffle_digging": options.obscure_spots.value,
        "shuffle_underwater": options.obscure_spots.value,
        "shuffle_gold_enemies": 0,
        "shuffle_pedestal": 0,
        "kinstones_gold": 1, # 0 = Closed, 1 = Vanilla, 2 = Combined, 3 = Open
        "kinstones_red": 3, # 0 = Closed, 1 = Vanilla, 2 = Combined, 3 = Open
        "kinstones_blue": 3, # 0 = Closed, 1 = Vanilla, 2 = Combined, 3 = Open
        "kinstones_green": 3, # 0 = Closed, 1 = Vanilla, 2 = Combined, 3 = Open
        "grabbables": 0, # 0 = Not Allowed, 1 = Allowed, 2 = Required, 3 = Required (Hard)
        "open_world": 0, # No, Yes
        "extra_shop_item": 0,
        "wind_crest_crenel": 0,
        "wind_crest_castor": 0,
        "wind_crest_clouds": 0,
        "wind_crest_lake": 1,
        "wind_crest_town": 1,
        "wind_crest_falls": 0,
        "wind_crest_south_field": 0,
        "wind_crest_minish_woods": 0,
        "weapon_bombs": 0, # No, Yes, Yes + Bosses
        "weapon_bows": 0,
        "weapon_gust_jar": 0, # No, Yes
        "weapon_lantern": 0,
        "trick_mitts_farm_rupees": 0, # No, Yes
        "trick_bombable_dust": 0,
        "trick_crenel_mushroom_gust_jar": 0,
        "trick_light_arrows_break_objects": 1,
        "trick_bobombs_destroy_walls": 0,
        "trick_like_like_cave_no_sword": 0,
        "trick_boots_skip_town_guard": 0,
        "trick_beam_crenel_switch": 0,
        "trick_down_thrust_spikey_beetle": 1,
        "trick_dark_rooms_no_lantern": 0,
        "trick_cape_extensions": 0,
        "trick_lake_minish_no_boots": 0,
        "trick_cabin_swim_no_lilypad": 0,
        "trick_cloud_sharks_no_weapons": 0,
        "trick_pow_2f_no_cane": 0,
        "trick_pot_puzzle_no_bracelets": 0,
        "trick_fow_pot_gust_jar": 0,
        "trick_dhc_cannons_no_four_sword": 0,
        "trick_dhc_pads_no_four_sword": 0,
        "trick_dhc_switches_no_four_sword": 0,
    }
