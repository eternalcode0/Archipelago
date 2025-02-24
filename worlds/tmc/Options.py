from Options import Choice, Toggle, StartInventoryPool, PerGameCommonOptions, Range, Removed
from dataclasses import dataclass

class Rupeesanity(Toggle):
    """Add all rupees locations to the pool to be randomized."""
    display_name = "Rupeesanity"

class SpecialPots(Toggle):
    """Add all pots that drop a unique item to the pool."""
    display_name = "Special Pots"

class ProgressiveItems(Toggle):
    """
    Change Bow, Bombs, Mitts, Flippers, etc into unlocking progressively
    rather than potentially giving the upgrades before you have the base item.
    Ex. Larger Bomb Bag will instead give Bombs if you haven't received the
    latter first.
    """
    display_name = "Progressive Items"

@dataclass
class MinishCapOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    progressive_items: ProgressiveItems
    rupeesanity: Rupeesanity
    special_pots: SpecialPots
