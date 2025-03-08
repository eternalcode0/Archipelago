from Options import Choice, DefaultOnToggle, Toggle, StartInventoryPool, PerGameCommonOptions, Range, Removed
from dataclasses import dataclass

# Copied from A Link to the Past for usability/accessibility
# start with not supported, use start inventory instead
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

class SpecialPots(Toggle):
    """Add all pots that drop a unique item to the pool."""
    display_name = "Pot-sanity"

class SmallKeysanity(DungeonItem):
    display_name = "Small Key-sanity"

class BigKeysanity(DungeonItem):
    display_name = "Big Key-sanity"

class DungeonMapSanity(DungeonItem):
    display_name = "Dungeon Map-sanity"

class DungeonCompassSanity(DungeonItem):
    display_name = "Dungeon Compass-sanity"

class ProgressiveItems(Toggle):
    """
    Change Bow, Bombs, Mitts, Flippers, etc into unlocking progressively
    rather than potentially giving the upgrades before you have the base item.
    Ex. Larger Bomb Bag will instead give Bombs if you haven't received the
    latter first.
    """
    display_name = "Progressive Items"

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
    default = 5
    none = 0
    smith_sword = 1
    green_sword = 2
    red_sword = 3
    blue_sword = 4
    four_sword = 5

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


@dataclass
class MinishCapOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    progressive_items: ProgressiveItems
    rupeesanity: Rupeesanity
    special_pots: SpecialPots
