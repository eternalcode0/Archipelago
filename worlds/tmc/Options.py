from dataclasses import dataclass

from Options import (Choice, DeathLink, DefaultOnToggle, OptionSet, PerGameCommonOptions, Range, StartInventoryPool,
                     Toggle)
from .constants import ALL_TRICKS


class DungeonItem(Choice):
    value: int
    # EternalCode's note: I want to experiment with a `closed` for small/big keys to actually remove them from the pool
    #   entirely and keep the doors closed. All locations behind them would be removed & inaccessible.
    # Elements would need to be forced to be anywhere under this setting.
    # option_closed = 0 # New compared to TMCR (compass/map removed from pool, locations behind keys inaccessible,
    #   I doubt many would use this but it'd be relatively simple to implement)
    # option_open = 1 # TMCR Removed (compass/map start_inventory, keys removed from pool, doors are open at the
    #   start of the save)
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
    """
    Add all rupees locations to the pool to be randomized. This setting will not shuffle Rupees that also belong to
    another pool, i.e. An underwater rupee will instead be randomized by shuffle_underwater
    """
    display_name = "Rupee-sanity"


class ShufflePots(Toggle):
    """Add all special pots that drop a unique item to the pool. Includes the LonLon Ranch Pot."""
    display_name = "Shuffle Pots"


class ShuffleDigging(Toggle):
    """Add all dig spots that drop a unique item to the pool."""
    display_name = "Shuffle Digging"


class ShuffleUnderwater(Toggle):
    """Add all underwater items to the pool. Includes the ToD underwater pot"""
    display_name = "Shuffle Underwater"


class ObscureSpots(Toggle):
    """Add all special pots, dig spots, etc. that drop a unique item to the pool."""
    display_name = "Obscure Spots"


class ShuffleElements(Choice):
    # EternalCode's Note: I'd like to experiment with ElementShuffle extending DungeonItem choice, just for consistency.
    # The settings would be slightly repurposed to something like this
    # `closed`: elements removed from pool, goal_elements forced to 0
    # `open`: elements added to start inventory (pretty useless all things considered)
    # `vanilla`: elements in their usual dungeon prize location
    # `own_dungeon`: place an element anywhere in its usual dungeon
    # `own_region`: place element in the vicinity of its usual dungeon
    # `any_dungeon`: place elements anywhere in any dungeon
    # `any_region`: place elements anywhere in the vicinity of any dungeon
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
    *Note: If using anything other than "anywhere" and you include small keys in start_inventory_from_pool,
        you may get the warning "tried to remove items from their pool that don't exist". This is expected, the keys
        have safely been added to your inventory from the pool.
    """
    display_name = "Small Key Shuffle"
    default = 3


class BigKeys(DungeonItem):
    """
    Own Dungeon (default/false): Randomized within the dungeon they're normally found in
    Anywhere (true): Items are in completely random locations
    *Note: If using anything other than "anywhere" and you include big keys in start_inventory_from_pool,
        you may get the warning "tried to remove items from their pool that don't exist". This is expected, the keys
        have safely been added to your inventory from the pool.
    """
    display_name = "Big Key Shuffle"
    default = 3


class DungeonMaps(DungeonItem):
    """
    Own Dungeon (default/false): Randomized within the dungeon they're normally found in
    Anywhere (true): Items are in completely random locations
    *Note: If using anything other than "anywhere" and you include dungeon maps in start_inventory_from_pool,
        you may get the warning "tried to remove items from their pool that don't exist". This is expected, the maps
        have safely been added to your inventory from the pool.
    """
    display_name = "Dungeon Maps Shuffle"
    default = 3


class DungeonCompasses(DungeonItem):
    """
    Own Dungeon (default/false): Randomized within the dungeon they're normally found in
    Anywhere (true): Items are in completely random locations
    *Note: If using anything other than "anywhere" and you include dungeon compasses in start_inventory_from_pool,
        you may get the warning "tried to remove items from their pool that don't exist". This is expected, the compass
        has safely been added to your inventory from the pool.
    """
    display_name = "Dungeon Compasses Shuffle"
    default = 3


class Traps(Toggle):
    """
    Traps may be placed around the world. Traps for local items will have their
    sprite randomized to a local item before pickup. When picked up it'll turn
    into an exclamation mark (!) and activate a specific trap such as spawning
    enemies, setting you on fire, freezing you, etc.
    """
    display_name = "Traps Enabled"


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
    If GoalVaati is on then you need at least this many figurines before DHC opens,
    otherwise you goal immediately upon having this many figurines (and other goal conditions) and entering sanctuary
    """
    display_name = "Required Figurines to Pedestal"
    default = 0
    range_start = 0
    range_end = 136


class FigurineAmount(Range):
    """
    How many figurines are added to the pool?
    Should not be lower than GoalFigurines, otherwise it will be overridden to match GoalFigurines.
    """
    display_name = "Figurines in Pool"
    default = 0
    range_start = 0
    range_end = 136


class EarlyWeapon(Toggle):
    """
    Force a weapon to be in your sphere 1.
    The weapon placed will be random based off the enabled `weapon` options.
    Swords will always be one of the possible weapons placed.
    """
    display_name = "Early Weapon"


class RandomBottleContents(Toggle):
    """Put random contents into the shuffled bottles, these contents are never considered in logic"""
    display_name = "Random Bottles Contents"


class DeathLinkGameover(Toggle):
    """
    If disabled, deathlinks are sent when reaching 0HP, before a fairy is used. Received deathlinks will drop you to
    0HP, using a fairy if you have one.
    If enabled, deathlinks are only sent when reaching the gameover screen. Received deathlinks will also send you
    straight to a gameover, fairy or not.
    """
    display_name = "Deathlink is Gameover"


class WeaponBomb(Choice):
    """
    Bombs can damage nearly every enemy, Bombs are never considered for Simon Simulations, and Golden Enemies.
    'No': Bombs are not considered as Weapons.
    'Yes': Bombs are considered as weapons for most regular enemy fights.
    'Yes + Bosses': Bombs are considered as weapons for most enemy fights. Fighting Green/Blu Chu, Madderpillars
    and Darknuts require only 10 bomb bag. Gleerok, Mazaal and Scissor Beetles require at least 30 bomb bag.
    Octo and Gyorg cannot be defeated with bombs.
    """
    display_name = "Bombs are considered Weapons"
    default = 0
    option_no = 0
    option_yes = 1
    option_yes_boss = 2
    alias_true = 1
    alias_false = 0


class WeaponBow(Toggle):
    """
    Bow can damage most enemies, many enemies are very resilient to damage. Chu Bosses and Darknuts are Immune.
    'false': Bows are not considered as Weapons.
    'true': Bows are considered as weapons for most enemy fights.
    Bows are never considered for Chu Bossfights, Darknuts, Scissor Beetles, Madderpillar, Wizzrobes, Simon Simulations,
    and Golden Enemies.
    """
    display_name = "Bows are considered Weapons"


class WeaponGust(Toggle):
    """
    Gust Jar can suck up various enemies like Ghini(Ghosts) and Beetles (The things that grab onto link).
    It can also grab objects and fire them like projectiles to kill enemies, some enemies or parts of enemies can be
    used as projectiles such as Helmasaurs and Stalfos.
    'false': Gust Jar is never considered for killing enemies.
    'true': Gust Jar is considered as weapons for all enemies that get sucked up by it, you are never expected to use
        objects as projectiles to kill enemies.
    """
    display_name = "Gust jar is considered a Weapon"


class WeaponLantern(Toggle):
    """
    The lit Lantern can instantly kill Wizzrobes by walking through them.
    'false': Lantern is not considered as a Weapon.
    'true': Lantern is considered as a weapon for fighting Wizzrobes.
    """
    display_name = "Lantern is considered a Weapon"


class Tricks(OptionSet):
    """
    mitts_farm_rupees: Mole Mitts may be required to farm rupees by digging an infinitely respawning red rupee next to
        link's house
    bombable_dust: Bombs may be required to blow away dust instead of Gust Jar
    crenel_mushroom_gust_jar: The mushroom near the edge of a cliff on Mt Crenel may be required to be grabbed with the
        gust jar to climb higher
    light_arrows_break_objects: A charged light arrow shot may be required to destroy obstacles like pots or small trees
    bobombs_destroy_walls: Either a Sword or the Gust Jar may be required to blow up walls near Bobombs
    like_like_cave_no_sword: Opening the chests in the digging cave in Minish Woods, guarded by a pair of LikeLikes,
        may be required without a weapon
    boots_skip_town_guard: A very precise boot dash may be required to skip the guard blocking the west exit of town
    beam_crenel_switch: A switch across a gap on Mt Crenel must be hit to extend a bridge to reach cave of flames,
        hitting it with a sword beam may be required
    down_thrust_spikey_beetle: Spikey Beetles can be flipped over with a down thrust, which may be required to kill them
    dark_rooms_no_lantern: Dark rooms may require being traversed without the lantern. Link always has a small light
        source revealing his surroundings
    cape_extensions: Some larger gaps across water can be crossed by extending the distance you can jump (Release cape
        after the hop, then press and hold the glide)
    lake_minish_no_boots: Lake hylia can be explored as minish without using the boots to bonk a tree by jumping down
        from the middle island
    cabin_swim_no_lilypad: Lake Cabin has a path used to enter as minish, the screen transition can be touched by
        swimming into it
    cloud_sharks_no_weapons: The Sharks in cloud tops can be killed by standing near the edge and watching them jump off
    fow_pot_gust_jar: A pot near the end of Fortress can be grabbed with the gust jar through a wall from near the
        beginning of the dungeon
    pow_2f_no_cane: After climbing the first clouds of Palace, a moving platform can be reached with a precise jump
    pot_puzzle_no_bracelets: The Minish sized pot puzzle in Palace can be avoided by hitting the switch that drops the
        item at a later point in the dungeon
    dhc_cannons_no_four_sword: The Cannon puzzle rooms of DHC can be completed without the four sword by using a well
        timed bomb strat and sword slash
    dhc_pads_no_four_sword: The clone puzzles that press down four pads in DHC can be completed with less clones by
        shuffling across the pads
    dhc_switches_no_four_sword: The clone puzzle that slashes 4 switches in DHC can be completed with a well placed spin
        attack
    """
    display_name = "Tricks"
    valid_keys = ALL_TRICKS


@dataclass
class MinishCapOptions(PerGameCommonOptions):
    # AP settings / DL settings
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
    death_link_gameover: DeathLinkGameover
    # Goal Settings
    goal_vaati: GoalVaati
    ped_elements: PedElements
    ped_swords: PedSword
    ped_dungeons: PedDungeons
    # ped_figurines: GoalFigurines
    # figurine_amount: FigurineAmount
    # Pool Settings
    dungeon_small_keys: SmallKeys
    dungeon_big_keys: BigKeys
    dungeon_maps: DungeonMaps
    dungeon_compasses: DungeonCompasses
    shuffle_elements: ShuffleElements
    rupeesanity: Rupeesanity
    shuffle_pots: ShufflePots
    shuffle_digging: ShuffleDigging
    shuffle_underwater: ShuffleUnderwater
    traps_enabled: Traps
    random_bottle_contents: RandomBottleContents
    # Weapon Settings
    early_weapon: EarlyWeapon
    weapon_bomb: WeaponBomb
    weapon_bow: WeaponBow
    weapon_gust: WeaponGust
    weapon_lantern: WeaponLantern
    # Logic Settings
    tricks: Tricks


def get_option_data(options: MinishCapOptions):
    """
    Template for the options that will likely be added in the future.
    Intended for trackers to properly match the logic between the standalone randomizer (TMCR) and AP
    """
    return {
        "goal_dungeons": options.ped_dungeons.value,  # 0-6
        "goal_swords": options.ped_swords.value,  # 0-5
        "goal_elements": options.ped_elements.value,  # 0-4
        "goal_figurines": 0,  # 0-136
        "dungeon_warp_dws": 0,  # 0 = None, 1 = Blue, 2 = Red, 3 = Both
        "dungeon_warp_cof": 0,
        "dungeon_warp_fow": 0,
        "dungeon_warp_tod": 0,
        "dungeon_warp_pow": 0,
        "dungeon_warp_dhc": 0,
        "cucco_rounds": 1,  # 0-10
        "goron_sets": 0,  # 0-5
        "goron_jp_prices": 0,  # 0 = EU prices, 1 = JP/US prices
        "shuffle_heart_pieces": 1,
        "shuffle_rupees": options.rupeesanity.value,
        "shuffle_gold_enemies": 0,
        "shuffle_pedestal": 0,
        "shuffle_biggoron": 0,  # 0 = Disabled, 1 = Requires Shield, 2 = Requires Mirror Shield
        "kinstones_gold": 1,  # 0 = Closed, 1 = Vanilla, 2 = Combined, 3 = Open
        "kinstones_red": 3,  # 0 = Closed, 1 = Vanilla, 2 = Combined, 3 = Open
        "kinstones_blue": 3,  # 0 = Closed, 1 = Vanilla, 2 = Combined, 3 = Open
        "kinstones_green": 3,  # 0 = Closed, 1 = Vanilla, 2 = Combined, 3 = Open
        "grabbables": 0,  # 0 = Not Allowed, 1 = Allowed, 2 = Required, 3 = Required (Hard)
        "open_world": 0,  # No, Yes
        "open_wind_tribe": 0,
        "open_tingle_brothers": 0,
        "open_library": 0,
        "extra_shop_item": 0,
        "wind_crest_crenel": 0,
        "wind_crest_castor": 0,
        "wind_crest_clouds": 0,
        "wind_crest_lake": 1,
        "wind_crest_town": 1,
        "wind_crest_falls": 0,
        "wind_crest_south_field": 0,
        "wind_crest_minish_woods": 0,
        "weapon_bombs": options.weapon_bomb.value,  # No, Yes, Yes + Bosses
        "weapon_bows": options.weapon_bow.value,
        "weapon_gust_jar": options.weapon_gust.value,  # No, Yes
        "weapon_lantern": options.weapon_lantern.value,
        "entrance_rando": 0,  # 0 = Disabled, 1 = Dungeons, 2 = Regions?, 3 = Rooms? (? = subject to change)
        "trick_mitts_farm_rupees": int(ALL_TRICKS[0] in options.tricks),  # No, Yes
        "trick_bombable_dust": int(ALL_TRICKS[1] in options.tricks),
        "trick_crenel_mushroom_gust_jar": int(ALL_TRICKS[2] in options.tricks),
        "trick_light_arrows_break_objects": int(ALL_TRICKS[3] in options.tricks),
        "trick_bobombs_destroy_walls": int(ALL_TRICKS[4] in options.tricks),
        "trick_like_like_cave_no_sword": int(ALL_TRICKS[5] in options.tricks),
        "trick_boots_skip_town_guard": int(ALL_TRICKS[6] in options.tricks),
        "trick_beam_crenel_switch": int(ALL_TRICKS[7] in options.tricks),
        "trick_down_thrust_spikey_beetle": int(ALL_TRICKS[8] in options.tricks),
        "trick_dark_rooms_no_lantern": int(ALL_TRICKS[9] in options.tricks),
        "trick_cape_extensions": int(ALL_TRICKS[10] in options.tricks),
        "trick_lake_minish_no_boots": int(ALL_TRICKS[11] in options.tricks),
        "trick_cabin_swim_no_lilypad": int(ALL_TRICKS[12] in options.tricks),
        "trick_cloud_sharks_no_weapons": int(ALL_TRICKS[13] in options.tricks),
        "trick_pow_2f_no_cane": int(ALL_TRICKS[14] in options.tricks),
        "trick_pot_puzzle_no_bracelets": int(ALL_TRICKS[15] in options.tricks),
        "trick_fow_pot_gust_jar": int(ALL_TRICKS[16] in options.tricks),
        "trick_dhc_cannons_no_four_sword": int(ALL_TRICKS[17] in options.tricks),
        "trick_dhc_pads_no_four_sword": int(ALL_TRICKS[18] in options.tricks),
        "trick_dhc_switches_no_four_sword": int(ALL_TRICKS[19] in options.tricks),
    }
