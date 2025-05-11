from dataclasses import dataclass

from Options import (Choice, DeathLink, DefaultOnToggle, OptionSet, PerGameCommonOptions, Range, StartInventoryPool,
                     Toggle)
from .constants import ALL_TRICKS


class DungeonItem(Choice):
    value: int
    option_removed = 0
    option_vanilla = 1
    option_home_dungeon = 2
    option_home_region = 3
    option_any_dungeon = 4
    option_any_region = 5
    option_anywhere = 6
    alias_true = 6
    alias_false = 2


class Rupeesanity(Toggle):
    """Add all rupees locations to the pool to be randomized."""
    display_name = "Rupee-sanity"


class ObscureSpots(Toggle):
    """Add all special pots, dig spots, etc. that drop a unique item to the pool."""
    display_name = "Obscure Spots"


class ShuffleElements(Choice):
    """
    Lock elements to specific locations
    Original Dungeon: Elements are in the same dungeons as vanilla
    Own Dungeon (false): Elements are shuffled between the 6 dungeon prizes
    Anywhere (true): Elements are in completely random locations
    """
    display_name = "Element Shuffle"
    default = 1
    option_original_dungeon = 0
    option_own_dungeon = 1
    option_anywhere = 2
    alias_true = 2
    alias_false = 1


class SmallKeys(DungeonItem):
    display_name = "Small Key Shuffle"


class BigKeys(DungeonItem):
    display_name = "Big Key Shuffle"


class DungeonMaps(DungeonItem):
    display_name = "Dungeon Maps Shuffle"


class DungeonCompasses(DungeonItem):
    display_name = "Dungeon Compasses Shuffle"


class GoalVaati(DefaultOnToggle):
    """
    If enabled, DHC will open after completing Pedestal. Kill Vaati to goal.
    If disabled, complete Pedestal to goal. DHC/Vaati is unnecessary.
    """
    display_name = "Vaati Goal"


class GoalDungeons(Range):
    """
    How many dungeons are required to goal?
    If GoalVaati is on then you need this many dungeons cleared before DHC opens,
    otherwise you goal immediately upon having this many dungeons cleared
    (and other goal conditions) and entering sanctuary
    """
    display_name = "Required Dungeons to Goal"
    default = 0
    range_start = 0
    range_end = 6


class GoalElements(Range):
    """
    How many elements are required to goal?
    If GoalVaati is on then you need this many elements before DHC opens,
    otherwise you goal immediately upon having this many elements (and other goal conditions) and entering sanctuary
    """
    display_name = "Required Elements to Goal"
    default = 4
    range_start = 0
    range_end = 4


class GoalSword(Choice):
    """
    What level of sword is required to goal?
    If GoalVaati is on then you need at least this sword level before DHC opens,
    otherwise you goal immediately upon having this sword level (and other goal conditions) and entering sanctuary
    """
    display_name = "Required Swords to Goal"
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
    If GoalVaati is on then you need at least this many figurines before DHC opens,
    otherwise you goal immediately upon having this many figurines (and other goal conditions) and entering sanctuary
    """
    display_name = "Required Figurines to Goal"
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
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
    death_link_gameover: DeathLinkGameover
    goal_vaati: GoalVaati
    # goal_dungeons: GoalDungeons
    # goal_elements: GoalElements
    # goal_sword: GoalSword
    # goal_figurines: GoalFigurines
    # figurine_amount: FigurineAmount
    shuffle_elements: ShuffleElements
    weapon_bomb: WeaponBomb
    weapon_bow: WeaponBow
    weapon_gust: WeaponGust
    weapon_lantern: WeaponLantern
    tricks: Tricks
    rupeesanity: Rupeesanity
    obscure_spots: ObscureSpots
    early_weapon: EarlyWeapon
    # dungeon_small_keys: SmallKeys
    # dungeon_big_keys: BigKeys
    # dungeon_maps: DungeonMaps
    # dungeon_compasses: DungeonCompasses


def get_option_data(options: MinishCapOptions):
    """
    Template for the options that will likely be added in the future.
    Intended for trackers to properly match the logic between the standalone randomizer (TMCR) and AP
    """
    return {
        "goal_dungeons": 0,  # 0-6
        "goal_swords": 0,  # 0-5
        "goal_elements": 4,  # 0-4
        "goal_figurines": 0,  # 0-136
        "dungeon_small_keys": DungeonItem.option_anywhere,
        "dungeon_big_keys": DungeonItem.option_anywhere,
        "dungeon_maps": DungeonItem.option_anywhere,
        "dungeon_compasses": DungeonItem.option_anywhere,
        "dungeon_warp_dws": 0,  # 0 = None, 1 = Blue, 2 = Red, 3 = Both
        "dungeon_warp_cof": 0,
        "dungeon_warp_fow": 0,
        "dungeon_warp_tod": 0,
        "dungeon_warp_pow": 0,
        "dungeon_warp_dhc": 0,
        "cucco_rounds": 1,  # 0-10
        "goron_sets": 0,  # 0-5
        "shuffle_heart_pieces": 1,
        "shuffle_rupees": options.rupeesanity.value,
        "shuffle_pots": options.obscure_spots.value,
        "shuffle_digging": options.obscure_spots.value,
        "shuffle_underwater": options.obscure_spots.value,
        "shuffle_gold_enemies": 0,
        "shuffle_pedestal": 0,
        "kinstones_gold": 1,  # 0 = Closed, 1 = Vanilla, 2 = Combined, 3 = Open
        "kinstones_red": 3,  # 0 = Closed, 1 = Vanilla, 2 = Combined, 3 = Open
        "kinstones_blue": 3,  # 0 = Closed, 1 = Vanilla, 2 = Combined, 3 = Open
        "kinstones_green": 3,  # 0 = Closed, 1 = Vanilla, 2 = Combined, 3 = Open
        "grabbables": 0,  # 0 = Not Allowed, 1 = Allowed, 2 = Required, 3 = Required (Hard)
        "open_world": 0,  # No, Yes
        "extra_shop_item": 0,
        "wind_crest_crenel": 0,
        "wind_crest_castor": 0,
        "wind_crest_clouds": 0,
        "wind_crest_lake": 0,
        "wind_crest_falls": 0,
        "wind_crest_south_field": 0,
        "wind_crest_minish_woods": 0,
        "weapon_bombs": options.weapon_bomb.value,  # No, Yes, Yes + Bosses
        "weapon_bows": options.weapon_bow.value,
        "weapon_gust_jar": options.weapon_gust.value,  # No, Yes
        "weapon_lantern": options.weapon_lantern.value,
        "trick_mitts_farm_rupees": ALL_TRICKS[0] in options.tricks,  # No, Yes
        "trick_bombable_dust": ALL_TRICKS[1] in options.tricks,
        "trick_crenel_mushroom_gust_jar": ALL_TRICKS[2] in options.tricks,
        "trick_light_arrows_break_objects": ALL_TRICKS[3] in options.tricks,
        "trick_bobombs_destroy_walls": ALL_TRICKS[4] in options.tricks,
        "trick_like_like_cave_no_sword": ALL_TRICKS[5] in options.tricks,
        "trick_boots_skip_town_guard": ALL_TRICKS[6] in options.tricks,
        "trick_beam_crenel_switch": ALL_TRICKS[7] in options.tricks,
        "trick_down_thrust_spikey_beetle": ALL_TRICKS[8] in options.tricks,
        "trick_dark_rooms_no_lantern": ALL_TRICKS[9] in options.tricks,
        "trick_cape_extensions": ALL_TRICKS[10] in options.tricks,
        "trick_lake_minish_no_boots": ALL_TRICKS[11] in options.tricks,
        "trick_cabin_swim_no_lilypad": ALL_TRICKS[12] in options.tricks,
        "trick_cloud_sharks_no_weapons": ALL_TRICKS[13] in options.tricks,
        "trick_pow_2f_no_cane": ALL_TRICKS[14] in options.tricks,
        "trick_pot_puzzle_no_bracelets": ALL_TRICKS[15] in options.tricks,
        "trick_fow_pot_gust_jar": ALL_TRICKS[16] in options.tricks,
        "trick_dhc_cannons_no_four_sword": ALL_TRICKS[17] in options.tricks,
        "trick_dhc_pads_no_four_sword": ALL_TRICKS[18] in options.tricks,
        "trick_dhc_switches_no_four_sword": ALL_TRICKS[19] in options.tricks,
    }
