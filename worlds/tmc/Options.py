from Options import Choice, DefaultOnToggle, Toggle, StartInventoryPool, PerGameCommonOptions, Range, Removed, DeathLink
from dataclasses import dataclass

# Copied from A Link to the Past for usability/accessibility
# start_with not supported, use start inventory instead
class DungeonItem(Choice):
    value: int
    option_original_dungeon = 0
    option_own_dungeons = 1
    option_own_world = 2
    option_any_world = 3
    option_different_world = 4
    alias_true = 3
    alias_false = 0

class Rupeesanity(Toggle):
    """Add all rupees locations to the pool to be randomized."""
    display_name = "Rupee-sanity"

class ObscureSpots(Toggle):
    """Add all special pots, dig spots, etc. that drop a unique item to the pool."""
    display_name = "Obscure Spots"

class SmallKeys(DungeonItem):
    display_name = "Small Key"

class BigKeys(DungeonItem):
    display_name = "Big Key"

class DungeonMaps(DungeonItem):
    display_name = "Dungeon Maps"

class DungeonCompasses(DungeonItem):
    display_name = "Dungeon Compasses"

class GoalVaati(DefaultOnToggle):
    """After completing the other goal conditions DHC will open. Kill Vaati to goal"""

class GoalDungeons(Range):
    """
    How many dungeons are required to goal?
    If GoalVaati is on then you need this many dungeons cleared before DHC opens,
    otherwise you goal immediately upon having this many dungeons cleared (and other goal conditions) and entering sanctuary
    """
    default = 0
    range_start = 0
    range_end = 6

class GoalElements(Range):
    """
    How many elements are required to goal?
    If GoalVaati is on then you need this many elements before DHC opens,
    otherwise you goal immediately upon having this many elements (and other goal conditions) and entering sanctuary
    """
    default = 4
    range_start = 0
    range_end = 4

class GoalSword(Choice):
    """
    What level of sword is required to goal?
    If GoalVaati is on then you need at least this sword level before DHC opens,
    otherwise you goal immediately upon having this sword level (and other goal conditions) and entering sanctuary
    """
    default = 0
    option_none = 0
    option_smith_sword = 1
    option_green_sword = 2
    option_red_sword = 3
    option_blue_sword = 4
    option_four_sword = 5

class GoalFigurines(Range):
    """
    How many figurines are required to goal?
    If GoalVatti is on then you need at least this many figurines before DHC opens,
    otherwise you goal immediately upon having this many figurines (and other goal conditons) and entering sanctuary
    """
    default = 0
    range_start = 0
    range_end = 136

class FigurineAmount(Range):
    """
    How many figurines are added to the pool?
    Should not be lower than GoalFigurines, otherwise it will be overriden to match GoalFigurines.
    """
    default = 0
    range_start = 0
    range_end = 136

class DeathLinkGameover(Toggle):
    """
    If disabled, deathlinks are sent when reaching 0 hp, fairy or not. Received deathlinks will drop you to 0 hp, using
    a fairy if you have one.
    If enabled, deathlinks are only sent when reaching the gameover screen. Received deathlinks will also send you straight to a gameover.
    """


@dataclass
class MinishCapOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
    death_link_gameover: DeathLinkGameover
    # goal_vaati: GoalVaati
    # goal_dungeons: GoalDungeons
    # goal_elements: GoalElements
    # goal_sword: GoalSword
    # goal_figurines: GoalFigurines
    # figurine_amount: FigurineAmount
    rupeesanity: Rupeesanity
    obscure_spots: ObscureSpots
    # dungeon_small_keys: SmallKeys
    # dungeon_big_keys: BigKeys
    # dungeon_maps: DungeonMaps
    # dungeon_compasses: DungeonCompasses
