import typing

from BaseClasses import Location
from .Constants.LocationName import TMCLocation
from .Constants.RegionName import TMCRegion
from . import Items


BASE_LOCATION_ID = 6_029_000

POOL_RUPEE       = "rupee" # for unique rupee spots only, ex. if it's a dig spot with a rupee then it's just a dig spot
POOL_PED         = "ped"
POOL_HP          = "hp" # heart pieces/containers
POOL_DIG         = "dig" # ground/wall
POOL_WATER       = "water"
POOL_ENEMY       = "enemy" # golden enemy
POOL_SCROLL      = "scroll"
POOL_FAIRY       = "fairy" # great fairy
POOL_SCRUB       = "scrub"
POOL_BUTTERFLY   = "butterfly"
POOL_POT         = "pot"
POOL_ELEMENT     = "element"
POOL_GORON       = "goron:" # Meant to be used as an fstring with the set number following it
POOL_CUCCO       = "cucco:" # Meant to be used as an fstring with the round number following it

DEFAULT_SET      = { POOL_HP, POOL_SCROLL, POOL_FAIRY, POOL_SCRUB, POOL_BUTTERFLY, POOL_ELEMENT, "cucco:10" }
OBSCURE_SET      = { POOL_DIG, POOL_WATER, POOL_POT }

class LocationData(typing.NamedTuple):
    id: int
    name: str
    region: str
    vanilla_item: int
    """The item id of what is normally given in this location"""
    rom_addr: typing.Tuple[int, int]
    """The address in the rom for placing items"""
    ram_addr: typing.Tuple[int, int]
    """1st = The address in EWRAM to read/write to, 2nd = The bit mask for the address"""
    room_area: int
    """
    The area (1st byte) and room (2nd byte) the check is found in. Intended to help filter the number of locations
    iterated per game watcher loop. Also helps keep track of whether items in the area need to be location scouted.
    """
    scoutable: bool = False
    """Whether the item should be auto-hinted when leaving the room it's in without collecting it"""
    pools: [str] = set()
    """Which location sets must be enabled for this spot to be randomized"""

class MinishCapLocation(Location):
    game: str = "The Minish Cap"


all_locations: typing.List[LocationData] = [
    #region South Field
    LocationData(
        6029000, TMCLocation.SMITH_HOUSE_RUPEE, TMCRegion.SOUTH_FIELD, Items.RUPEES_20,
        (0x0F25AA, None), (0x2CDE, 0x40), 0x1122),
    LocationData(
        6029001, TMCLocation.SMITH_HOUSE_SWORD, TMCRegion.SOUTH_FIELD, Items.PROGRESSIVE_SWORD, # New location from base patch after intro skip
        (0x0F252B, None), (0x2CF5, 0x01), 0x1122),
    LocationData(
        6029002, TMCLocation.SMITH_HOUSE_SHIELD, TMCRegion.SOUTH_FIELD, Items.PROGRESSIVE_SHIELD, # New location from base patch after intro skip
        (0x0F253B, None), (0x2CF5, 0x02), 0x1122),
    LocationData(
        6029003, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM1, TMCRegion.SOUTH_FIELD, Items.RUPEES_5,
        (0x0F8283, None), (0x2D1E, 0x20), 0x1032, pools={POOL_RUPEE}),
    LocationData(
        6029004, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM2, TMCRegion.SOUTH_FIELD, Items.RUPEES_5,
        (0x0F8293, None), (0x2D1E, 0x40), 0x1032, pools={POOL_RUPEE}),
    LocationData(
        6029005, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM3, TMCRegion.SOUTH_FIELD, Items.RUPEES_5,
        (0x0F82A3, None), (0x2D1E, 0x80), 0x1032, pools={POOL_RUPEE}),
    LocationData(
        6029006, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM4, TMCRegion.SOUTH_FIELD, Items.RUPEES_5,
        (0x0F82B3, None), (0x2D1F, 0x01), 0x1032, pools={POOL_RUPEE}),
    LocationData(
        6029007, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM5, TMCRegion.SOUTH_FIELD, Items.RUPEES_5,
        (0x0F82C3, None), (0x2D1F, 0x02), 0x1032, pools={POOL_RUPEE}),
    LocationData(
        6029008, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM6, TMCRegion.SOUTH_FIELD, Items.RUPEES_5,
        (0x0F82D3, None), (0x2D1F, 0x04), 0x1032, pools={POOL_RUPEE}),
    LocationData(
        6029009, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM7, TMCRegion.SOUTH_FIELD, Items.RUPEES_5,
        (0x0F82E3, None), (0x2D1F, 0x08), 0x1032, pools={POOL_RUPEE}),
    LocationData(
        6029010, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM8, TMCRegion.SOUTH_FIELD, Items.RUPEES_5,
        (0x0F82F3, None), (0x2D1F, 0x10), 0x1032, pools={POOL_RUPEE}),
    LocationData(
        6029011, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM9, TMCRegion.SOUTH_FIELD, Items.RUPEES_5,
        (0x0F8303, None), (0x2D1F, 0x20), 0x1032, pools={POOL_RUPEE}),
    LocationData(
        6029012, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM10, TMCRegion.SOUTH_FIELD, Items.RUPEES_5,
        (0x0F8313, None), (0x2D1F, 0x40), 0x1032, pools={POOL_RUPEE}),
    LocationData(
        6029013, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM11, TMCRegion.SOUTH_FIELD, Items.RUPEES_5,
        (0x0F8323, None), (0x2D1F, 0x80), 0x1032, pools={POOL_RUPEE}),
    LocationData(
        6029014, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM12, TMCRegion.SOUTH_FIELD, Items.RUPEES_5,
        (0x0F8333, None), (0x2D20, 0x01), 0x1032, pools={POOL_RUPEE}),
    LocationData(
        6029015, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM13, TMCRegion.SOUTH_FIELD, Items.RUPEES_5,
        (0x0F8343, None), (0x2D20, 0x02), 0x1032, pools={POOL_RUPEE}),
    LocationData(
        6029016, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM14, TMCRegion.SOUTH_FIELD, Items.RUPEES_5,
        (0x0F8353, None), (0x2D20, 0x04), 0x1032, pools={POOL_RUPEE}),
    LocationData(
        6029017, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM15, TMCRegion.SOUTH_FIELD, Items.RUPEES_5,
        (0x0F8363, None), (0x2D20, 0x08), 0x1032, pools={POOL_RUPEE}),
    LocationData(
        6029018, TMCLocation.SOUTH_FIELD_FUSION_CHEST, TMCRegion.SOUTH_FIELD, None,
        (0x0FE0D6, None), (0x2CD3, 0x02), 0x0103),
    LocationData(
        6029019, TMCLocation.SOUTH_FIELD_TREE_FUSION_HP, TMCRegion.SOUTH_FIELD, Items.HEART_PIECE,
        (0x0F9BA7, None), (0x2CEE, 0x80), 0x1224, pools={POOL_HP}),
    LocationData(
        6029020, TMCLocation.SOUTH_FIELD_MINISH_SIZE_WATER_HOLE_HP, TMCRegion.SOUTH_FIELD, Items.HEART_PIECE,
        (0x0DB55F, None), (0x2D2C, 0x02), 0x0435),
    LocationData(
        6029021, TMCLocation.SOUTH_FIELD_TINGLE_NPC, TMCRegion.SOUTH_FIELD, Items.TINGLE_TROPHY,
        (0x016966, None), (0x2CA3, 0x04), 0x0103),
    #endregion
    #region Castle Exterior
    LocationData(
        6029022, TMCLocation.CASTLE_MOAT_LEFT_CHEST, TMCRegion.CASTLE_EXTERIOR, None,
        (0x0F004E, None), (0x2CBE, 0x04), 0x0007),
    LocationData(
        6029023, TMCLocation.CASTLE_MOAT_RIGHT_CHEST, TMCRegion.CASTLE_EXTERIOR, Items.RUPEES_200,
        (0x0F0056, None), (0x2CBE, 0x08), 0x0007),
    LocationData(
        6029024, TMCLocation.CASTLE_GOLDEN_ROPE, TMCRegion.CASTLE_EXTERIOR, Items.RUPEES_100,
        (None, None), (0x2CA2, 0x20), 0x0007, pools={POOL_ENEMY}),
    LocationData(
        6029025, TMCLocation.CASTLE_RIGHT_FOUNTAIN_FUSION_HP, TMCRegion.CASTLE_EXTERIOR, Items.HEART_PIECE,
        (0x0D9C2B, None), (0x2D0E, 0x10), 0x0042, pools={POOL_HP}),
    LocationData(
        6029026, TMCLocation.CASTLE_DOJO_HP, TMCRegion.CASTLE_EXTERIOR, Items.HEART_PIECE,
        (0x0D79BB, None), (0x2D2C, 0x08), 0x0525, pools={POOL_HP}),
    LocationData(
        6029027, TMCLocation.CASTLE_DOJO_NPC, TMCRegion.CASTLE_EXTERIOR, Items.SWORD_BEAM,
        (0xEF64A4, None), (0x2EA6, 0x02), 0x0525, pools={POOL_SCROLL}),
    LocationData(
        6029028, TMCLocation.CASTLE_RIGHT_FOUNTAIN_FUSION_MINISH_HOLE_CHEST, TMCRegion.CASTLE_EXTERIOR, None,
        (0x0DBD3E, None), (0x2D28, 0x10), 0x0036),
    LocationData(
        6029029, TMCLocation.CASTLE_LEFT_FOUNTAIN_FUSION_MINISH_HOLE_CHEST, TMCRegion.CASTLE_EXTERIOR, None,
        (0x0DBD8E, None), (0x2D28, 0x20), 0x0136),
    #endregion
    #region Eastern Hills
    LocationData(
        6029030, TMCLocation.HILLS_GOLDEN_ROPE, TMCRegion.EASTERN_HILLS, Items.RUPEES_100,
        (None, None), (0x2CA2, 0x10), None, pools={POOL_ENEMY}),
    LocationData(
        6029031, TMCLocation.HILLS_FUSION_CHEST, TMCRegion.EASTERN_HILLS, Items.EMPTY_BOTTLE,
        (0x0FE05E, None), (0x2CD2, 0x04), 0x0403),
    LocationData(
        6029032, TMCLocation.HILLS_BEANSTALK_FUSION_LEFT_CHEST, TMCRegion.EASTERN_HILLS, None,
        (0x0F610A, None), (0x2D0D, 0x04), 0x030D),
    LocationData(
        6029033, TMCLocation.HILLS_BEANSTALK_FUSION_HP, TMCRegion.EASTERN_HILLS, Items.HEART_PIECE,
        (0x0F6073, None), (0x2D0D, 0x01), 0x030D, pools={POOL_HP}),
    LocationData(
        6029034, TMCLocation.HILLS_BEANSTALK_FUSION_RIGHT_CHEST, TMCRegion.EASTERN_HILLS, Items.RUPEES_200,
        (0x0F6102, None), (0x2D0D, 0x02), 0x030D),
    LocationData(
        6029035, TMCLocation.HILLS_BOMB_CAVE_CHEST, TMCRegion.EASTERN_HILLS, None,
        (0x0F85C2, None), (0x2D22, 0x08), 0x1332),
    LocationData(
        6029036, TMCLocation.MINISH_GREAT_FAIRY_NPC, TMCRegion.EASTERN_HILLS, Items.BIG_WALLET, # Technically Minish Woods but the only access is cutting through eastern woods from lonlon
        (0x00B7B4, None), (0x2CEF, 0x80), 0x0129, pools={POOL_FAIRY}),
    LocationData(
        6029037, TMCLocation.HILLS_FARM_DIG_CAVE_ITEM, TMCRegion.EASTERN_HILLS, Items.RUPEES_20,
        (0x0F3C9F, None), (0x2CD2, 0x04), 0x0013),
    #endregion
    #region Lonlon
    LocationData(
        6029038, TMCLocation.LON_LON_RANCH_POT, TMCRegion.LONLON, Items.LONLON_KEY,
        (0x0F2C9B, 0x0F2C9D), (0x2CE5, 0x20), 0x0228, pools={POOL_POT}),
    LocationData(
        6029039, TMCLocation.LON_LON_PUDDLE_FUSION_BIG_CHEST, TMCRegion.LONLON, Items.BIG_WALLET,
        (0x0F8252, None), (0x2D1E, 0x10), 0x0F32),
    LocationData(
        6029040, TMCLocation.LON_LON_CAVE_CHEST, TMCRegion.LONLON, Items.RUPEES_50,
        (0x0F80E2, None), (0x2D1D, 0x80), 0x0C32),
    LocationData(
        6029041, TMCLocation.LON_LON_CAVE_SECRET_CHEST, TMCRegion.LONLON, Items.KINSTONE,
        (0x0F817A, None), (0x2D1E, 0x04), 0x0D32),
    LocationData(
        6029042, TMCLocation.LON_LON_PATH_FUSION_CHEST, TMCRegion.LONLON, Items.KINSTONE,
        (0x0FE086, None), (0x2D11, 0x02), 0x0311),
    LocationData(
        6029043, TMCLocation.LON_LON_PATH_HP, TMCRegion.LONLON, Items.HEART_PIECE,
        (0x0D56EF, None), (0x2D13, 0x04), 0x0311, pools={POOL_HP}),
    LocationData(
        6029044, TMCLocation.LON_LON_DIG_SPOT, TMCRegion.LONLON, Items.RUPEES_50,
        (0x0F6CFF, None), (0x2CCB, 0x20), 0x0503),
    LocationData(
        6029045, TMCLocation.LON_LON_NORTH_MINISH_CRACK_CHEST, TMCRegion.LONLON, Items.KINSTONE,
        (0x0DBEBE, None), (0x2CF2, 0x04), 0x0027),
    LocationData(
        6029046, TMCLocation.LON_LON_GORON_CAVE_FUSION_SMALL_CHEST, TMCRegion.LONLON, Items.RUPEES_200,
        (0x0D8302, None), (0x2D2A, 0x80), 0x012F),
    LocationData(
        6029047, TMCLocation.LON_LON_GORON_CAVE_FUSION_BIG_CHEST, TMCRegion.LONLON, Items.EMPTY_BOTTLE,
        (0x0D830A, None), (0x2D2A, 0x40), 0x012F),
    #endregion
    #region Lower Falls
    LocationData(
        6029048, TMCLocation.FALLS_LOWER_LON_LON_FUSION_CHEST, TMCRegion.LOWER_FALLS, Items.RUPEES_200,
        (0x0FE0FE, None), (0x2CD3, 0x40), 0x0503),
    LocationData(
        6029049, TMCLocation.FALLS_LOWER_HP, TMCRegion.LOWER_FALLS, Items.HEART_PIECE,
        (0x0F87D3, None), (0x2CD1, 0x02), 0x000A, pools={POOL_HP}),
    LocationData(
        6029050, TMCLocation.FALLS_LOWER_WATERFALL_FUSION_DOJO_NPC, TMCRegion.LOWER_FALLS, Items.FAST_SPLIT_SCROLL,
        (0xEF64B0, None), (0x2EA6, 0x20), 0x0125, pools={POOL_SCROLL}),
    LocationData(
        6029051, TMCLocation.FALLS_LOWER_ROCK_ITEM1, TMCRegion.LOWER_FALLS, Items.RUPEES_20,
        (0x0F87E3, None), (0x2CD0, 0x04), 0x000A, pools={POOL_RUPEE}),
    LocationData(
        6029052, TMCLocation.FALLS_LOWER_ROCK_ITEM2, TMCRegion.LOWER_FALLS, Items.RUPEES_20,
        (0x0F87F3, None), (0x2CD0, 0x08), 0x000A, pools={POOL_RUPEE}),
    LocationData(
        6029053, TMCLocation.FALLS_LOWER_ROCK_ITEM3, TMCRegion.LOWER_FALLS, Items.RUPEES_20,
        (0x0F8803, None), (0x2CD0, 0x10), 0x000A, pools={POOL_RUPEE}),
    LocationData(
        6029054, TMCLocation.FALLS_LOWER_DIG_CAVE_LEFT_CHEST, TMCRegion.LOWER_FALLS, None,
        (0x0F3E2, None), (0x2D05, 0x08), 0x0016),
    LocationData(
        6029055, TMCLocation.FALLS_LOWER_DIG_CAVE_RIGHT_CHEST, TMCRegion.LOWER_FALLS, Items.RUPEES_50,
        (0x0F3E36, None), (0x2D05, 0x10), 0x0016),
    #endregion
    #region Lake Hylia
    LocationData(
        6029056, TMCLocation.HYLIA_SUNKEN_HP, TMCRegion.LAKE_HYLIA, Items.HEART_PIECE,
        (0x0F323B, None), (0x2CBD, 0x02), 0x000B, pools={POOL_HP}),
    LocationData(
        6029057, TMCLocation.HYLIA_DOG_NPC, TMCRegion.LAKE_HYLIA, Items.EMPTY_BOTTLE,
        (0x094908, 0x09490A), (0x2B3F, 0x20), 0x1422),
    LocationData(
        6029058, TMCLocation.HYLIA_SMALL_ISLAND_HP, TMCRegion.LAKE_HYLIA, Items.HEART_PIECE,
        (0x0F322B, None), (0x2CBD, 0x01), 0x000B, pools={POOL_HP}),
    LocationData(
        6029059, TMCLocation.HYLIA_CAPE_CAVE_TOP_RIGHT, TMCRegion.LAKE_HYLIA, None,
        (0x0F3A06, None), (0x2D02, 0x80), 0x0119),
    LocationData(
        6029060, TMCLocation.HYLIA_CAPE_CAVE_BOTTOM_LEFT, TMCRegion.LAKE_HYLIA, None,
        (0x0F3A16, None), (0x2D03, 0x02), 0x0119),
    LocationData(
        6029061, TMCLocation.HYLIA_CAPE_CAVE_TOP_LEFT, TMCRegion.LAKE_HYLIA, Items.KINSTONE,
        (0x0F3A1E, None), (0x2D03, 0x04), 0x0119),
    LocationData(
        6029062, TMCLocation.HYLIA_CAPE_CAVE_TOP_MIDDLE, TMCRegion.LAKE_HYLIA, Items.KINSTONE,
        (0x0F3A26, None), (0x2D03, 0x08), 0x0119),
    LocationData(
        6029063, TMCLocation.HYLIA_CAPE_CAVE_RIGHT, TMCRegion.LAKE_HYLIA, Items.KINSTONE,
        (0x0F3A2E, None), (0x2D03, 0x10), 0x0119),
    LocationData(
        6029064, TMCLocation.HYLIA_CAPE_CAVE_BOTTOM_RIGHT, TMCRegion.LAKE_HYLIA, Items.KINSTONE,
        (0x0F3A36, None), (0x2D03, 0x20), 0x0119),
    LocationData(
        6029065, TMCLocation.HYLIA_CAPE_CAVE_BOTTOM_MIDDLE, TMCRegion.LAKE_HYLIA, Items.KINSTONE,
        (0x0F3A3E, None), (0x2D03, 0x40), 0x0119),
    LocationData(
        6029066, TMCLocation.HYLIA_CAPE_CAVE_LON_LON_HP, TMCRegion.LAKE_HYLIA, Items.HEART_PIECE,
        (0x0F6CEF, None), (0x2CCB, 0x10), 0x0503, pools={POOL_HP}),
    LocationData(
        6029067, TMCLocation.HYLIA_BEANSTALK_FUSION_LEFT_CHEST, TMCRegion.LAKE_HYLIA, Items.RUPEES_200,
        (0x0F5F6A, None), (0x2D0C, 0x20), 0x010D),
    LocationData(
        6029068, TMCLocation.HYLIA_BEANSTALK_FUSION_HP, TMCRegion.LAKE_HYLIA, Items.HEART_PIECE,
        (0x0F5EDB, None), (0x2D0C, 0x10), 0x010D, pools={POOL_HP}),
    LocationData(
        6029069, TMCLocation.HYLIA_BEANSTALK_FUSION_RIGHT_CHEST, TMCRegion.LAKE_HYLIA, None,
        (0x0F5F72, None), (0x2D0C, 0x40), 0x010D),
    LocationData(
        6029070, TMCLocation.HYLIA_MIDDLE_ISLAND_FUSION_DIG_CAVE_CHEST, TMCRegion.LAKE_HYLIA, Items.RUPEES_50,
        (0x0F3916, None), (0x2D02, 0x40), 0x0019),
    LocationData(
        6029071, TMCLocation.HYLIA_BOTTOM_HP, TMCRegion.LAKE_HYLIA, Items.HEART_PIECE,
        (0x0F324B, None), (0x2CBD, 0x04), 0x000B, pools={POOL_HP}),
    LocationData(
        6029072, TMCLocation.HYLIA_DOJO_HP, TMCRegion.LAKE_HYLIA, Items.HEART_PIECE,
        (0x0D7B03, None), (0x2D2C, 0x04), 0x0625, pools={POOL_HP}),
    LocationData(
        6029073, TMCLocation.HYLIA_DOJO_NPC, TMCRegion.LAKE_HYLIA, Items.PERIL_BEAM,
        (0xEF64A7, None), (0x2EA6, 0x04), 0x0625, pools={POOL_SCROLL}),
    LocationData(
        6029074, TMCLocation.HYLIA_CRACK_FUSION_LIBRARI_NPC, TMCRegion.LAKE_HYLIA, Items.HEART_CONTAINER,
        (0x0124EC, None), (0x2CF2, 0x08), 0x2320),
    LocationData(
        6029075, TMCLocation.HYLIA_NORTH_MINISH_HOLE_CHEST, TMCRegion.LAKE_HYLIA, Items.KINSTONE,
        (0x0DB7CE, None), (0x2D2A, 0x04), 0x0735),
    LocationData(
        6029076, TMCLocation.HYLIA_SOUTH_MINISH_HOLE_CHEST, TMCRegion.LAKE_HYLIA, Items.KINSTONE,
        (0x0DB616, None), (0x2D28, 0x04), 0x0535),
    LocationData(
        6029077, TMCLocation.HYLIA_CABIN_PATH_FUSION_CHEST, TMCRegion.LAKE_HYLIA, Items.KINSTONE,
        (0x0FE09E, None), (0x2D11, 0x10), 0x0411),
    LocationData(
        6029078, TMCLocation.HYLIA_MAYOR_CABIN_ITEM, TMCRegion.LAKE_HYLIA, Items.BLUE_BOOK,
        (0x0F306F, None), (0x2EA4, 0x40), 0x0528),
    #endregion
    #region Minish Woods
    LocationData(
        6029079, TMCLocation.MINISH_WOODS_GOLDEN_OCTO, TMCRegion.MINISH_WOODS, Items.RUPEES_100,
        (None, None), (0x2CA3, 0x01), None, pools={POOL_ENEMY}),
    LocationData(
        6029080, TMCLocation.MINISH_WOODS_WITCH_HUT_ITEM, TMCRegion.MINISH_WOODS, Items.WAKEUP_MUSHROOM,
        (0x0F94D7, None), (0x2EA4, 0x04), 0x0024),
    LocationData(
        6029081, TMCLocation.WITCH_DIGGING_CAVE_CHEST, TMCRegion.MINISH_WOODS, Items.KINSTONE,
        (0x0F38A6, None), (0x2D02, 0x08), 0x000C),
    LocationData(
        6029082, TMCLocation.MINISH_WOODS_NORTH_FUSION_CHEST, TMCRegion.MINISH_WOODS, Items.KINSTONE,
        (0x0FE07E, None), (0x2CD2, 0x08), 0x0000),
    LocationData(
        6029083, TMCLocation.MINISH_WOODS_TOP_HP, TMCRegion.MINISH_WOODS, Items.HEART_PIECE,
        (0x0F4347, None), (0x2CC3, 0x08), 0x0000, pools={POOL_HP}),
    LocationData(
        6029084, TMCLocation.MINISH_WOODS_WEST_FUSION_CHEST, TMCRegion.MINISH_WOODS, Items.RUPEES_200,
        (0x0FE0CE, None), (0x2CD3, 0x01), 0x0000),
    LocationData(
        6029085, TMCLocation.MINISH_WOODS_LIKE_LIKE_DIGGING_CAVE_LEFT_CHEST, TMCRegion.MINISH_WOODS, Items.RUPEES_50,
        (0x0F38AE, None), (0x2D02, 0x10), 0x000C),
    LocationData(
        6029086, TMCLocation.MINISH_WOODS_LIKE_LIKE_DIGGING_CAVE_RIGHT_CHEST, TMCRegion.MINISH_WOODS, Items.KINSTONE,
        (0x0F38B6, None), (0x2D02, 0x20), 0x000C),
    LocationData(
        6029087, TMCLocation.MINISH_WOODS_EAST_FUSION_CHEST, TMCRegion.MINISH_WOODS, Items.KINSTONE,
        (0x0FE0B6, None), (0x2CD2, 0x20), 0x0000),
    LocationData(
        6029088, TMCLocation.MINISH_WOODS_SOUTH_FUSION_CHEST, TMCRegion.MINISH_WOODS, Items.KINSTONE,
        (0x0FE0C6, None), (0x2CD2, 0x80), 0x0000),
    LocationData(
        6029089, TMCLocation.MINISH_WOODS_BOTTOM_HP, TMCRegion.MINISH_WOODS, Items.HEART_PIECE,
        (0x0F4357, None), (0x2CC3, 0x10), 0x0000, pools={POOL_HP}),
    LocationData(
        6029090, TMCLocation.MINISH_WOODS_CRACK_FUSION_CHEST, TMCRegion.MINISH_WOODS, Items.KINSTONE,
        (0x0DC42A, None), (0x2CF0, 0x08), 0x0827),
    LocationData(
        6029091, TMCLocation.MINISH_WOODS_MINISH_PATH_FUSION_CHEST, TMCRegion.MINISH_WOODS, Items.RUPEES_200,
        (0x0FE08E, None), (0x2D11, 0x04), 0x0011),
    LocationData(
        6029092, TMCLocation.MINISH_VILLAGE_BARREL_HOUSE_ITEM, TMCRegion.MINISH_WOODS, Items.JABBER_NUT,
        (0x0DA283, None), (0x2CF5, 0x04), 0x0920),
    LocationData(
        6029093, TMCLocation.MINISH_VILLAGE_HP, TMCRegion.MINISH_WOODS, Items.HEART_PIECE,
        (0x0DBCC7, None), (0x2CF4, 0x04), 0x0101, pools={POOL_HP}),
    LocationData(
        6029094, TMCLocation.MINISH_WOODS_BOMB_MINISH_NPC_1, TMCRegion.MINISH_WOODS, Items.PROGRESSIVE_BOMB,
        (0x00A00C, None), (0x2EA5, 0x01), 0x2620),
    LocationData(
        6029095, TMCLocation.MINISH_WOODS_BOMB_MINISH_NPC_2, TMCRegion.MINISH_WOODS, Items.PROGRESSIVE_BOMB,
        (0x00A0A0, None), (0x2CF2, 0x01), 0x2620),
    LocationData(
        6029096, TMCLocation.MINISH_WOODS_POST_VILLAGE_FUSION_CHEST, TMCRegion.MINISH_WOODS, Items.KINSTONE,
        (0x0FE0A6, None), (0x2CDB, 0x08), 0x0000),
    LocationData(
        6029097, TMCLocation.MINISH_WOODS_FLIPPER_HOLE_MIDDLE_CHEST, TMCRegion.MINISH_WOODS, Items.KINSTONE,
        (0x0DB97E, None), (0x2D2A, 0x08), 0x0935),
    LocationData(
        6029098, TMCLocation.MINISH_WOODS_FLIPPER_HOLE_RIGHT_CHEST, TMCRegion.MINISH_WOODS, Items.KINSTONE,
        (0x0DB986, None), (0x2D2A, 0x10), 0x0935),
    LocationData(
        6029099, TMCLocation.MINISH_WOODS_FLIPPER_HOLE_LEFT_CHEST, TMCRegion.MINISH_WOODS, Items.KINSTONE,
        (0x0DB98E, None), (0x2D2A, 0x20), 0x0935),
    LocationData(
        6029100, TMCLocation.MINISH_WOODS_FLIPPER_HOLE_HP, TMCRegion.MINISH_WOODS, Items.HEART_PIECE,
        (0x0DB8BF, None), (0x2D2B, 0x04), 0x0935, pools={POOL_HP}),
    #endregion
    #region Trilby Highlands
    LocationData(
        6029101, TMCLocation.TRILBY_MIDDLE_FUSION_CHEST, TMCRegion.TRILBY_HIGHLANDS, Items.KINSTONE,
        (0x0FE0EE, None), (0x2CD3, 0x10), 0x0703),
    LocationData(
        6029102, TMCLocation.TRILBY_TOP_FUSION_CHEST, TMCRegion.TRILBY_HIGHLANDS, Items.KINSTONE,
        (0x0FE0BE, None), (0x2CD2, 0x40), 0x0703),
    LocationData(
        6029103, TMCLocation.TRILBY_DIG_CAVE_LEFT_CHEST, TMCRegion.TRILBY_HIGHLANDS, Items.KINSTONE,
        (0x0F3D86, None), (0x2D04, 0x80), 0x0313),
    LocationData(
        6029104, TMCLocation.TRILBY_DIG_CAVE_RIGHT_CHEST, TMCRegion.TRILBY_HIGHLANDS, Items.KINSTONE,
        (0x0F3D96, None), (0x2D05, 0x02), 0x0313),
    LocationData(
        6029105, TMCLocation.TRILBY_DIG_CAVE_WATER_FUSION_CHEST, TMCRegion.TRILBY_HIGHLANDS, Items.KINSTONE,
        (0x0F3D8E, None), (0x2D05, 0x01), 0x0313),
    LocationData(
        6029106, TMCLocation.TRILBY_SCRUB_NPC, TMCRegion.TRILBY_HIGHLANDS, Items.EMPTY_BOTTLE,
        (0xEF50FC, None), (0x2CA7, 0x04), 0x1432, pools={POOL_SCRUB}),
    LocationData(
        6029107, TMCLocation.TRILBY_BOMB_CAVE_CHEST, TMCRegion.TRILBY_HIGHLANDS, Items.KINSTONE,
        (0x0F7EEA, None), (0x2D1D, 0x20), 0x0732),
    LocationData(
        6029108, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM1, TMCRegion.TRILBY_HIGHLANDS, Items.RUPEES_5,
        (0x0F83BB, None), (0x2D20, 0x10), 0x1132, pools={POOL_RUPEE}),
    LocationData(
        6029109, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM2, TMCRegion.TRILBY_HIGHLANDS, Items.RUPEES_5,
        (0x0F83CB, None), (0x2D20, 0x20), 0x1132, pools={POOL_RUPEE}),
    LocationData(
        6029110, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM3, TMCRegion.TRILBY_HIGHLANDS, Items.RUPEES_5,
        (0x0F83DB, None), (0x2D20, 0x40), 0x1132, pools={POOL_RUPEE}),
    LocationData(
        6029111, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM4, TMCRegion.TRILBY_HIGHLANDS, Items.RUPEES_5,
        (0x0F83EB, None), (0x2D20, 0x80), 0x1132, pools={POOL_RUPEE}),
    LocationData(
        6029112, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM5, TMCRegion.TRILBY_HIGHLANDS, Items.RUPEES_5,
        (0x0F83FB, None), (0x2D21, 0x01), 0x1132, pools={POOL_RUPEE}),
    LocationData(
        6029113, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM6, TMCRegion.TRILBY_HIGHLANDS, Items.RUPEES_5,
        (0x0F840B, None), (0x2D21, 0x02), 0x1132, pools={POOL_RUPEE}),
    LocationData(
        6029114, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM7, TMCRegion.TRILBY_HIGHLANDS, Items.RUPEES_5,
        (0x0F841B, None), (0x2D21, 0x04), 0x1132, pools={POOL_RUPEE}),
    LocationData(
        6029115, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM8, TMCRegion.TRILBY_HIGHLANDS, Items.RUPEES_5,
        (0x0F842B, None), (0x2D21, 0x08), 0x1132, pools={POOL_RUPEE}),
    LocationData(
        6029116, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM9, TMCRegion.TRILBY_HIGHLANDS, Items.RUPEES_5,
        (0x0F843B, None), (0x2D21, 0x10), 0x1132, pools={POOL_RUPEE}),
    LocationData(
        6029117, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM10, TMCRegion.TRILBY_HIGHLANDS, Items.RUPEES_5,
        (0x0F844B, None), (0x2D21, 0x20), 0x1132, pools={POOL_RUPEE}),
    LocationData(
        6029118, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM11, TMCRegion.TRILBY_HIGHLANDS, Items.RUPEES_5,
        (0x0F845B, None), (0x2D21, 0x40), 0x1132, pools={POOL_RUPEE}),
    LocationData(
        6029119, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM12, TMCRegion.TRILBY_HIGHLANDS, Items.RUPEES_5,
        (0x0F846B, None), (0x2D21, 0x80), 0x1132, pools={POOL_RUPEE}),
    LocationData(
        6029120, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM13, TMCRegion.TRILBY_HIGHLANDS, Items.RUPEES_5,
        (0x0F847B, None), (0x2D22, 0x01), 0x1132, pools={POOL_RUPEE}),
    LocationData(
        6029121, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM14, TMCRegion.TRILBY_HIGHLANDS, Items.RUPEES_5,
        (0x0F848B, None), (0x2D22, 0x02), 0x1132, pools={POOL_RUPEE}),
    LocationData(
        6029122, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM15, TMCRegion.TRILBY_HIGHLANDS, Items.RUPEES_5,
        (0x0F849B, None), (0x2D22, 0x04), 0x1132, pools={POOL_RUPEE}),
    #endregion
    #region Western Woods
    LocationData(
        6029123, TMCLocation.WESTERN_WOODS_FUSION_CHEST, TMCRegion.WESTERN_WOODS, None,
        (0x0F7976, None), (0x2CCF, 0x10), 0x0803),
    LocationData(
        6029124, TMCLocation.WESTERN_WOODS_TREE_FUSION_HP, TMCRegion.WESTERN_WOODS, Items.HEART_PIECE,
        (0x0F9E1F, None), (0x2CEF, 0x01), 0x1924, pools={POOL_HP}),
    LocationData(
        6029125, TMCLocation.WESTERN_WOODS_TOP_DIG1, TMCRegion.WESTERN_WOODS, Items.RUPEES_50,
        (0x0F77CF, None), (0x2CCE, 0x08), 0x0803, pools={POOL_DIG}),
    LocationData(
        6029126, TMCLocation.WESTERN_WOODS_TOP_DIG2, TMCRegion.WESTERN_WOODS, Items.RUPEES_50,
        (0x0F77DF, None), (0x2CCE, 0x10), 0x0803, pools={POOL_DIG}),
    LocationData(
        6029127, TMCLocation.WESTERN_WOODS_TOP_DIG3, TMCRegion.WESTERN_WOODS, Items.RUPEES_50,
        (0x0F77EF, None), (0x2CCE, 0x20), 0x0803, pools={POOL_DIG}),
    LocationData(
        6029128, TMCLocation.WESTERN_WOODS_TOP_DIG4, TMCRegion.WESTERN_WOODS, Items.RUPEES_50,
        (0x0F77FF, None), (0x2CCE, 0x40), 0x0803, pools={POOL_DIG}),
    LocationData(
        6029129, TMCLocation.WESTERN_WOODS_TOP_DIG5, TMCRegion.WESTERN_WOODS, Items.RUPEES_50,
        (0x0F780F, None), (0x2CCE, 0x80), 0x0803, pools={POOL_DIG}),
    LocationData(
        6029130, TMCLocation.WESTERN_WOODS_TOP_DIG6, TMCRegion.WESTERN_WOODS, Items.RUPEES_50,
        (0x0F781F, None), (0x2CCF, 0x01), 0x0803, pools={POOL_DIG}),
    LocationData(
        6029131, TMCLocation.WESTERN_WOODS_PERCY_FUSION_MOBLIN, TMCRegion.WESTERN_WOODS, Items.RUPEES_50,
        (0x0123D6, None), (0x2CE4, 0x04), 0x0822),
    LocationData(
        6029132, TMCLocation.WESTERN_WOODS_PERCY_FUSION_PERCY, TMCRegion.WESTERN_WOODS, None,
        (0x06B058, 0x06B05A), (0x2CE3, 0x80), 0x0822),
    LocationData(
        6029133, TMCLocation.WESTERN_WOODS_BOTTOM_DIG1, TMCRegion.WESTERN_WOODS, Items.RUPEES_200,
        (0x0F782F, None), (0x2CCF, 0x02), 0x0803, pools={POOL_DIG}),
    LocationData(
        6029134, TMCLocation.WESTERN_WOODS_BOTTOM_DIG2, TMCRegion.WESTERN_WOODS, Items.RUPEES_200,
        (0x0F783F, None), (0x2CCF, 0x04), 0x0803, pools={POOL_DIG}),
    LocationData(
        6029135, TMCLocation.WESTERN_WOODS_GOLDEN_OCTO, TMCRegion.WESTERN_WOODS, Items.RUPEES_100,
        (None,     None), (0x2CA3, 0x02), 0x0903, pools={POOL_ENEMY}),
    LocationData(
        6029136, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_CHEST, TMCRegion.WESTERN_WOODS, Items.KINSTONE,
        (0x0F62C2, None), (0x2D0D, 0x08), 0x040D),
    LocationData(
        6029137, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM1, TMCRegion.WESTERN_WOODS, Items.RUPEES_20,
        (0x0F6143, None), (0x2D0D, 0x10), 0x040D, pools={POOL_RUPEE}),
    LocationData(
        6029138, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM2, TMCRegion.WESTERN_WOODS, Items.RUPEES_20,
        (0x0F6153, None), (0x2D0D, 0x20), 0x040D, pools={POOL_RUPEE}),
    LocationData(
        6029139, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM3, TMCRegion.WESTERN_WOODS, Items.RUPEES_20,
        (0x0F6163, None), (0x2D0D, 0x40), 0x040D, pools={POOL_RUPEE}),
    LocationData(
        6029140, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM4, TMCRegion.WESTERN_WOODS, Items.RUPEES_20,
        (0x0F6173, None), (0x2D0D, 0x80), 0x040D, pools={POOL_RUPEE}),
    LocationData(
        6029141, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM5, TMCRegion.WESTERN_WOODS, Items.RUPEES_20,
        (0x0F6183, None), (0x2D0E, 0x01), 0x040D, pools={POOL_RUPEE}),
    LocationData(
        6029142, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM6, TMCRegion.WESTERN_WOODS, Items.RUPEES_20,
        (0x0F6193, None), (0x2D0E, 0x02), 0x040D, pools={POOL_RUPEE}),
    LocationData(
        6029143, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM7, TMCRegion.WESTERN_WOODS, Items.RUPEES_20,
        (0x0F61A3, None), (0x2D0E, 0x04), 0x040D, pools={POOL_RUPEE}),
    LocationData(
        6029144, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM8, TMCRegion.WESTERN_WOODS, Items.RUPEES_20,
        (0x0F61B3, None), (0x2D0E, 0x08), 0x040D, pools={POOL_RUPEE}),
    LocationData(
        6029145, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM9, TMCRegion.WESTERN_WOODS, Items.RUPEES_20,
        (0x0F61C3, None), (0x2D0F, 0x40), 0x040D, pools={POOL_RUPEE}),
    LocationData(
        6029146, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM10, TMCRegion.WESTERN_WOODS, Items.RUPEES_20,
        (0x0F61D3, None), (0x2D0F, 0x80), 0x040D, pools={POOL_RUPEE}),
    LocationData(
        6029147, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM11, TMCRegion.WESTERN_WOODS, Items.RUPEES_20,
        (0x0F61E3, None), (0x2D10, 0x01), 0x040D, pools={POOL_RUPEE}),
    LocationData(
        6029148, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM12, TMCRegion.WESTERN_WOODS, Items.RUPEES_20,
        (0x0F61F3, None), (0x2D10, 0x02), 0x040D, pools={POOL_RUPEE}),
    LocationData(
        6029149, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM13, TMCRegion.WESTERN_WOODS, Items.RUPEES_20,
        (0x0F6203, None), (0x2D10, 0x04), 0x040D, pools={POOL_RUPEE}),
    LocationData(
        6029150, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM14, TMCRegion.WESTERN_WOODS, Items.RUPEES_20,
        (0x0F6213, None), (0x2D10, 0x08), 0x040D, pools={POOL_RUPEE}),
    LocationData(
        6029151, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM15, TMCRegion.WESTERN_WOODS, Items.RUPEES_20,
        (0x0F6223, None), (0x2D10, 0x10), 0x040D, pools={POOL_RUPEE}),
    LocationData(
        6029152, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM16, TMCRegion.WESTERN_WOODS, Items.RUPEES_20,
        (0x0F6233, None), (0x2D10, 0x20), 0x040D, pools={POOL_RUPEE}),
    #endregion
    #region Crenel
    LocationData(
        6029153, TMCLocation.CRENEL_BASE_ENTRANCE_VINE, TMCRegion.CRENEL, Items.RUPEES_20,
        (0x0FAACF, None), (0x2CC5, 0x02), 0x0406, pools={POOL_RUPEE}),
    LocationData(
        6029154, TMCLocation.CRENEL_BASE_FAIRY_CAVE_ITEM1, TMCRegion.CRENEL, Items.RUPEES_5,
        (0x0FB3F3, None), (0x2D24, 0x08), 0x0926, pools={POOL_RUPEE}),
    LocationData(
        6029155, TMCLocation.CRENEL_BASE_FAIRY_CAVE_ITEM2, TMCRegion.CRENEL, Items.RUPEES_5,
        (0x0FB403, None), (0x2D24, 0x10), 0x0926, pools={POOL_RUPEE}),
    LocationData(
        6029156, TMCLocation.CRENEL_BASE_FAIRY_CAVE_ITEM3, TMCRegion.CRENEL, Items.RUPEES_5,
        (0x0FB413, None), (0x2D24, 0x20), 0x0926, pools={POOL_RUPEE}),
    LocationData(
        6029157, TMCLocation.CRENEL_BASE_GREEN_WATER_FUSION_CHEST, TMCRegion.CRENEL, Items.KINSTONE,
        (0x0FE06E, None), (0x2D10, 0x80), 0x0112),
    LocationData(
        6029158, TMCLocation.CRENEL_BASE_WEST_FUSION_CHEST, TMCRegion.CRENEL, Items.RUPEES_200,
        (0x0FE116, None), (0x2CD4, 0x02), 0x0406),
    LocationData(
        6029159, TMCLocation.CRENEL_BASE_WATER_CAVE_LEFT_CHEST, TMCRegion.CRENEL, Items.RUPEES_50,
        (0x0FB38A, None), (0x2D24, 0x02), 0x0826),
    LocationData(
        6029160, TMCLocation.CRENEL_BASE_WATER_CAVE_RIGHT_CHEST, TMCRegion.CRENEL, Items.KINSTONE,
        (0x0FB392, None), (0x2D24, 0x04), 0x0826),
    LocationData(
        6029161, TMCLocation.CRENEL_BASE_WATER_CAVE_HP, TMCRegion.CRENEL, Items.HEART_PIECE,
        (0x0FB32B, None), (0x2D24, 0x01), 0x0826, pools={POOL_HP}),
    LocationData(
        6029162, TMCLocation.CRENEL_BASE_MINISH_VINE_HOLE_CHEST, TMCRegion.CRENEL, Items.KINSTONE,
        (0x0DB376, None), (0x2D28, 0x01), 0x0035),
    LocationData(
        6029163, TMCLocation.CRENEL_BASE_MINISH_CRACK_CHEST, TMCRegion.CRENEL, Items.KINSTONE,
        (0x0DC0CE, None), (0x2CDE, 0x02), 0x0327),
    LocationData(
        6029164, TMCLocation.CRENEL_VINE_TOP_GOLDEN_TEKTITE, TMCRegion.CRENEL, Items.RUPEES_100,
        (None, None), (0x2CA2, 0x80), None, pools={POOL_ENEMY}),
    LocationData(
        6029165, TMCLocation.CRENEL_BRIDGE_CAVE_CHEST, TMCRegion.CRENEL, Items.KINSTONE,
        (0x0FB2FA, None), (0x2D23, 0x80), 0x0726),
    LocationData(
        6029166, TMCLocation.CRENEL_FAIRY_CAVE_HP, TMCRegion.CRENEL, Items.HEART_PIECE,
        (0x0FB0BB, None), (0x2D2B, 0x20), 0x0526),
    LocationData(
        6029167, TMCLocation.CRENEL_BELOW_COF_GOLDEN_TEKTITE, TMCRegion.CRENEL, Items.RUPEES_100,
        (None, None), (0x2CA2, 0x04), None, pools={POOL_ENEMY}),
    LocationData(
        6029168, TMCLocation.CRENEL_SCRUB_NPC, TMCRegion.CRENEL, Items.GRIP_RING,
        (0xEF5104, None), (0x2EA5, 0x04), 0x0426, pools={POOL_SCRUB}),
    LocationData(
        6029169, TMCLocation.CRENEL_DOJO_LEFT_CHEST, TMCRegion.CRENEL, Items.RUPEES_50,
        (0x0D75DA, None), (0x2D1C, 0x02), 0x0025),
    LocationData(
        6029170, TMCLocation.CRENEL_DOJO_RIGHT_CHEST, TMCRegion.CRENEL, Items.RUPEES_50,
        (0x0D75E2, None), (0x2D1C, 0x04), 0x0025),
    LocationData(
        6029171, TMCLocation.CRENEL_DOJO_HP, TMCRegion.CRENEL, Items.HEART_PIECE,
        (0x0D752B, None), (0x2D2C, 0x01), 0x0025, pools={POOL_HP}),
    LocationData(
        6029172, TMCLocation.CRENEL_DOJO_NPC, TMCRegion.CRENEL, Items.ROLL_ATTACK,
        (0xEF64A1, None), (0x2EA6, 0x01), 0x0025, pools={POOL_SCROLL}),
    LocationData(
        6029173, TMCLocation.CRENEL_GREAT_FAIRY_NPC, TMCRegion.CRENEL, Items.BOMB_BAG,
        (0x00B828, None), (0x2CF0, 0x01), 0x0229, pools={POOL_FAIRY}),
    LocationData(
        6029174, TMCLocation.CRENEL_CLIMB_FUSION_CHEST, TMCRegion.CRENEL, Items.KINSTONE,
        (0x0FE10E, None), (0x2CD4, 0x01), 0x0106),
    LocationData(
        6029175, TMCLocation.CRENEL_DIG_CAVE_HP, TMCRegion.CRENEL, Items.HEART_PIECE,
        (0x0F3BA7, None), (0x2D04, 0x20), 0x0014, pools={POOL_HP}),
    LocationData(
        6029176, TMCLocation.CRENEL_BEANSTALK_FUSION_HP, TMCRegion.CRENEL, Items.HEART_PIECE,
        (0x0F5D9B, None), (0x2D0C, 0x08), 0x000D, pools={POOL_HP}),
    LocationData(
        6029177, TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM1, TMCRegion.CRENEL, Items.RUPEES_20,
        (0x0F5DAB, None), (0x2D0E, 0x40), 0x000D, pools={POOL_RUPEE}),
    LocationData(
        6029178, TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM2, TMCRegion.CRENEL, Items.RUPEES_20,
        (0x0F5DBB, None), (0x2D0E, 0x80), 0x000D, pools={POOL_RUPEE}),
    LocationData(
        6029179, TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM3, TMCRegion.CRENEL, Items.RUPEES_20,
        (0x0F5DCB, None), (0x2D0F, 0x01), 0x000D, pools={POOL_RUPEE}),
    LocationData(
        6029180, TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM4, TMCRegion.CRENEL, Items.RUPEES_20,
        (0x0F5DDB, None), (0x2D0F, 0x02), 0x000D, pools={POOL_RUPEE}),
    LocationData(
        6029181, TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM5, TMCRegion.CRENEL, Items.RUPEES_20,
        (0x0F5DEB, None), (0x2D0F, 0x04), 0x000D, pools={POOL_RUPEE}),
    LocationData(
        6029182, TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM6, TMCRegion.CRENEL, Items.RUPEES_20,
        (0x0F5DFB, None), (0x2D0F, 0x08), 0x000D, pools={POOL_RUPEE}),
    LocationData(
        6029183, TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM7, TMCRegion.CRENEL, Items.RUPEES_20,
        (0x0F5E0B, None), (0x2D0F, 0x10), 0x000D, pools={POOL_RUPEE}),
    LocationData(
        6029184, TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM8, TMCRegion.CRENEL, Items.RUPEES_20,
        (0x0F5E1B, None), (0x2D0F, 0x20), 0x000D, pools={POOL_RUPEE}),
    LocationData(
        6029185, TMCLocation.CRENEL_RAIN_PATH_FUSION_CHEST, TMCRegion.CRENEL, Items.KINSTONE,
        (0x0FE066, None), (0x2D10, 0x40), 0x0212),
    LocationData(
        6029186, TMCLocation.CRENEL_UPPER_BLOCK_CHEST, TMCRegion.CRENEL, Items.KINSTONE,
        (0x0FB022, None), (0x2D23, 0x20), 0x0326),
    LocationData(
        6029187, TMCLocation.CRENEL_MINES_PATH_FUSION_CHEST, TMCRegion.CRENEL, None,
        (0x0FE096, None), (0x2D11, 0x08), 0x0312),
    LocationData(
        6029188, TMCLocation.CRENEL_MELARI_MIDDLE_LEFT_DIG, TMCRegion.CRENEL, Items.KINSTONE,
        (0x0DC8C3, None), (0x2CF3, 0x02), 0x0010, pools={POOL_DIG}),
    LocationData(
        6029189, TMCLocation.CRENEL_MELARI_TOP_MIDDLE_DIG, TMCRegion.CRENEL, Items.KINSTONE,
        (0x0DC8D3, None), (0x2CF3, 0x04), 0x0010, pools={POOL_DIG}),
    LocationData(
        6029190, TMCLocation.CRENEL_MELARI_TOP_LEFT_DIG, TMCRegion.CRENEL, Items.RUPEES_20,
        (0x0DC8E3, None), (0x2CF3, 0x08), 0x0010, pools={POOL_DIG}),
    LocationData(
        6029191, TMCLocation.CRENEL_MELARI_TOP_RIGHT_DIG, TMCRegion.CRENEL, Items.KINSTONE,
        (0x0DC8F3, None), (0x2CF3, 0x10), 0x0010, pools={POOL_DIG}),
    LocationData(
        6029192, TMCLocation.CRENEL_MELARI_BOTTOM_RIGHT_DIG, TMCRegion.CRENEL, Items.RUPEES_20,
        (0x0DC903, None), (0x2CF3, 0x20), 0x0010, pools={POOL_DIG}),
    LocationData(
        6029193, TMCLocation.CRENEL_MELARI_BOTTOM_MIDDLE_DIG, TMCRegion.CRENEL, Items.RUPEES_20,
        (0x0DC913, None), (0x2CF3, 0x40), 0x0010, pools={POOL_DIG}),
    LocationData(
        6029194, TMCLocation.CRENEL_MELARI_BOTTOM_LEFT_DIG, TMCRegion.CRENEL, Items.RUPEES_20,
        (0x0DC923, None), (0x2CF3, 0x80), 0x0010, pools={POOL_DIG}),
    LocationData(
        6029195, TMCLocation.CRENEL_MELARI_CENTER_DIG, TMCRegion.CRENEL, Items.KINSTONE,
        (0x0DC933, None), (0x2CF4, 0x01), 0x0010, pools={POOL_DIG}),
    LocationData(
        6029196, TMCLocation.CRENEL_MELARI_NPC_COF, TMCRegion.CRENEL, Items.PROGRESSIVE_SWORD,
        (0x00D26E, None), (0x2EA4, 0x80), 0x0010), # Only attainable after COF cleared
    #endregion
    #region Castor Wilds
    LocationData(
        6029197, TMCLocation.SWAMP_BUTTERFLY_FUSION_ITEM, TMCRegion.CASTOR_WILDS, Items.DIG_BUTTERFLY,
        (0x0FE13F, None), (0x2EA7, 0x10), 0x0004, pools={POOL_BUTTERFLY}),
    LocationData(
        6029198, TMCLocation.SWAMP_CENTER_CAVE_DARKNUT_CHEST, TMCRegion.CASTOR_WILDS, Items.KINSTONE_GOLD_SWAMP,
        (0x0D9A0E, None), (0x2D23, 0x04), 0x002B),
    LocationData(
        6029199, TMCLocation.SWAMP_CENTER_CHEST, TMCRegion.CASTOR_WILDS, Items.KINSTONE,
        (0x0D95A6, None), (0x2CBD, 0x10), 0x0004),
    LocationData(
        6029200, TMCLocation.SWAMP_GOLDEN_ROPE, TMCRegion.CASTOR_WILDS, Items.RUPEES_100,
        (None, None), (0x2CA2, 0x08), 0x0004, pools={POOL_ENEMY}),
    LocationData(
        6029201, TMCLocation.SWAMP_NEAR_WATERFALL_CAVE_HP, TMCRegion.CASTOR_WILDS, Items.HEART_PIECE,
        (0x0D9907, None), (0x2D23, 0x01), 0x042A, pools={POOL_HP}),
    LocationData(
        6029202, TMCLocation.SWAMP_WATERFALL_FUSION_DOJO_NPC, TMCRegion.CASTOR_WILDS, Items.FAST_SPIN_SCROLL,
        (0xEF64AD, None), (0x2EA6, 0x10), 0x0325, pools={POOL_SCROLL}),
    LocationData(
        6029203, TMCLocation.SWAMP_NORTH_CAVE_CHEST, TMCRegion.CASTOR_WILDS, Items.KINSTONE_GOLD_SWAMP,
        (0x0D97B6, None), (0x2D22, 0x40), 0x012A),
    LocationData(
        6029204, TMCLocation.SWAMP_DIGGING_CAVE_LEFT_CHEST, TMCRegion.CASTOR_WILDS, None,
        (0x0F3AAE, None), (0x2D04, 0x01), 0x0017),
    LocationData(
        6029205, TMCLocation.SWAMP_DIGGING_CAVE_RIGHT_CHEST, TMCRegion.CASTOR_WILDS, Items.KINSTONE,
        (0x0F3AB6, None), (0x2D04, 0x02), 0x0017),
    LocationData(
        6029206, TMCLocation.SWAMP_UNDERWATER_TOP, TMCRegion.CASTOR_WILDS, Items.KINSTONE,
        (0x0D9347, None), (0x2CC0, 0x04), 0x0004, pools={POOL_WATER}),
    LocationData(
        6029207, TMCLocation.SWAMP_UNDERWATER_MIDDLE, TMCRegion.CASTOR_WILDS, Items.KINSTONE,
        (0x0D9357, None), (0x2CC0, 0x08), 0x0004, pools={POOL_WATER}),
    LocationData(
        6029208, TMCLocation.SWAMP_UNDERWATER_BOTTOM, TMCRegion.CASTOR_WILDS, Items.KINSTONE,
        (0x0D9367, None), (0x2CC0, 0x10), 0x0004, pools={POOL_WATER}),
    LocationData(
        6029209, TMCLocation.SWAMP_SOUTH_CAVE_CHEST, TMCRegion.CASTOR_WILDS, Items.KINSTONE_GOLD_SWAMP,
        (0x0D9746, None), (0x2D22, 0x10), 0x002A),
    LocationData(
        6029210, TMCLocation.SWAMP_DOJO_HP, TMCRegion.CASTOR_WILDS, Items.HEART_PIECE,
        (0x0D78CB, None), (0x2D2B, 0x80), 0x0425, pools={POOL_HP}),
    LocationData(
        6029211, TMCLocation.SWAMP_DOJO_NPC, TMCRegion.CASTOR_WILDS, Items.GREATSPIN,
        (0xEF64AA, None), (0x2EA6, 0x08), 0x0425, pools={POOL_SCROLL}),
    LocationData(
        6029212, TMCLocation.SWAMP_MINISH_FUSION_NORTH_CRACK_CHEST, TMCRegion.CASTOR_WILDS, Items.KINSTONE,
        (0x0DC49A, None), (0x2CDE, 0x08), 0x0927),
    LocationData(
        6029213, TMCLocation.SWAMP_MINISH_MULLDOZER_BIG_CHEST, TMCRegion.CASTOR_WILDS, Items.PROGRESSIVE_BOW,
        (0x0DC2FE, None), (0x2CDE, 0x01), 0x0627),
    LocationData(
        6029214, TMCLocation.SWAMP_MINISH_FUSION_NORTH_WEST_CRACK_CHEST, TMCRegion.CASTOR_WILDS, Items.KINSTONE,
        (0x0DC67A, None), (0x2CF0, 0x20), 0x0D27),
    LocationData(
        6029215, TMCLocation.SWAMP_MINISH_FUSION_WEST_CRACK_CHEST, TMCRegion.CASTOR_WILDS, Items.KINSTONE,
        (0x0DC512, None), (0x2CDE, 0x10), 0x0A27),
    LocationData(
        6029216, TMCLocation.SWAMP_MINISH_FUSION_VINE_CRACK_CHEST, TMCRegion.CASTOR_WILDS, Items.KINSTONE,
        (0x0DC58A, None), (0x2CDE, 0x20), 0x0B27),
    LocationData(
        6029217, TMCLocation.SWAMP_MINISH_FUSION_WATER_HOLE_CHEST, TMCRegion.CASTOR_WILDS, Items.KINSTONE,
        (0x0DB3C6, None), (0x2D2C, 0x20), 0x0135),
    LocationData(
        6029218, TMCLocation.SWAMP_MINISH_FUSION_WATER_HOLE_HP, TMCRegion.CASTOR_WILDS, Items.HEART_PIECE,
        (0x0DB3F7, None), (0x2D2C, 0x10), 0x0235, pools={POOL_HP}),
    #endregion
    #region Castor Ruins
    LocationData(
        6029219, TMCLocation.RUINS_BUTTERFLY_FUSION_ITEM, TMCRegion.RUINS, Items.BOW_BUTTERFLY,
        (0x0FE12F, None), (0x2EA7, 0x08), 0x0005, pools={POOL_BUTTERFLY}),
    LocationData(
        6029220, TMCLocation.RUINS_BOMB_CAVE_CHEST, TMCRegion.RUINS, Items.KINSTONE,
        (0x0D981E, None), (0x2D22, 0x80), 0x022A),
    LocationData(
        6029221, TMCLocation.RUINS_MINISH_HOME_CHEST, TMCRegion.RUINS, Items.KINSTONE,
        (0x0DC3BA, None), (0x2CDE, 0x04), 0x0727),
    LocationData(
        6029222, TMCLocation.RUINS_PILLARS_FUSION_CHEST, TMCRegion.RUINS, None,
        (0x0FE11E, None), (0x2CD4, 0x04), 0x0305),
    LocationData(
        6029223, TMCLocation.RUINS_BEAN_STALK_FUSION_BIG_CHEST, TMCRegion.RUINS, Items.QUIVER,
        (0x0F603A, None), (0x2D0C, 0x80), 0x020D),
    LocationData(
        6029224, TMCLocation.RUINS_CRACK_FUSION_CHEST, TMCRegion.RUINS, Items.KINSTONE,
        (0x0DC602, None), (0x2CF0, 0x10), 0x0C27),
    LocationData(
        6029225, TMCLocation.RUINS_MINISH_CAVE_HP, TMCRegion.RUINS, Items.HEART_PIECE,
        (0x0DB4BF, None), (0x2D2B, 0x40), 0x0335, pools={POOL_HP}),
    LocationData(
        6029226, TMCLocation.RUINS_ARMOS_KILL_LEFT_CHEST, TMCRegion.RUINS, Items.RUPEES_50,
        (0x0DDA5E, None), (0x2CC2, 0x08), 0x0505),
    LocationData(
        6029227, TMCLocation.RUINS_ARMOS_KILL_RIGHT_CHEST, TMCRegion.RUINS, None,
        (0x0DDA66, None), (0x2CC2, 0x10), 0x0505),
    LocationData(
        6029228, TMCLocation.RUINS_GOLDEN_OCTO, TMCRegion.RUINS, Items.RUPEES_100,
        (None, None), (0x2CA2, 0x02), 0x0505, pools={POOL_ENEMY}),
    LocationData(
        6029229, TMCLocation.RUINS_NEAR_FOW_FUSION_CHEST, TMCRegion.RUINS, Items.BOMB_BAG,
        (0x0FE0AE, None), (0x2CD2, 0x10), 0x0405),
    #endregion
    #region Royal Valley
    LocationData(
        6029230, TMCLocation.VALLEY_PRE_VALLEY_FUSION_CHEST, TMCRegion.VALLEY, None,
        (0x0FE0F6, None), (0x2CD3, 0x20), 0x0603),
    LocationData(
        6029231, TMCLocation.VALLEY_GREAT_FAIRY_NPC, TMCRegion.VALLEY, Items.QUIVER,
        (0x00B722, None), (0x2CEF, 0x40), 0x0029, pools={POOL_FAIRY}),
    LocationData(
        6029232, TMCLocation.VALLEY_LOST_WOODS_CHEST, TMCRegion.VALLEY, None,
        (0x0D8A86, None), (0x2CC7, 0x04), 0x0109),
    LocationData(
        6029233, TMCLocation.VALLEY_DAMPE_NPC, TMCRegion.VALLEY, Items.GRAVEYARD_KEY,
        (0x0096B6, None), (0x2CE9, 0x02), 0x1222),
    LocationData(
        6029234, TMCLocation.VALLEY_GRAVEYARD_BUTTERFLY_FUSION_ITEM, TMCRegion.VALLEY, Items.SWIM_BUTTERFLY,
        (0x0FE14F, None), (0x2EA7, 0x20), 0x0009, pools={POOL_BUTTERFLY}),
    LocationData(
        6029235, TMCLocation.VALLEY_GRAVEYARD_LEFT_FUSION_CHEST, TMCRegion.VALLEY, Items.KINSTONE,
        (0x0FE0DE, None), (0x2CD3, 0x04), 0x0009),
    LocationData(
        6029236, TMCLocation.VALLEY_GRAVEYARD_LEFT_GRAVE_HP, TMCRegion.VALLEY, Items.HEART_PIECE,
        (0x0D8AE7, None), (0x2D27, 0x20), 0x0034, scoutable=True),
    LocationData(
        6029237, TMCLocation.VALLEY_GRAVEYARD_RIGHT_FUSION_CHEST, TMCRegion.VALLEY, Items.KINSTONE,
        (0x0FE0E6, None), (0x2CD3, 0x08), 0x0009),
    LocationData(
        6029238, TMCLocation.VALLEY_GRAVEYARD_RIGHT_GRAVE_FUSION_CHEST, TMCRegion.VALLEY, None,
        (0x0D8B6E, None), (0x2D27, 0x40), 0x0134),
    #endregion
    #region Dungeon RC
    LocationData(
        6029239, TMCLocation.CRYPT_GIBDO_LEFT_ITEM, TMCRegion.DUNGEON_RC, Items.BOMB_REFILL_5,
        (0x0E688B, None), (0x2D14, 0x10), 0x0868),
    LocationData(
        6029240, TMCLocation.CRYPT_GIBDO_RIGHT_ITEM, TMCRegion.DUNGEON_RC, Items.SMALL_KEY_RC,
        (0x0E68AB, None), (0x2D14, 0x20), 0x0868),
    LocationData(
        6029241, TMCLocation.CRYPT_LEFT_ITEM, TMCRegion.DUNGEON_RC, Items.SMALL_KEY_RC,
        (0x0E6357, None), (0x2D12, 0x40), 0x0468),
    LocationData(
        6029242, TMCLocation.CRYPT_RIGHT_ITEM, TMCRegion.DUNGEON_RC, Items.SMALL_KEY_RC,
        (0x0E63A7, None), (0x2D12, 0x80), 0x0468),
    LocationData(
        6029243, TMCLocation.CRYPT_PRIZE, TMCRegion.DUNGEON_RC, Items.KINSTONE_GOLD_FALLS,
        (0x00DA5A, None), (0x2D02, 0x04), 0x0068),
    #endregion
    #region Upper Falls
    LocationData(
        6029244, TMCLocation.FALLS_ENTRANCE_HP, TMCRegion.UPPER_FALLS, Items.HEART_PIECE,
        (0x0F87C3, None), (0x2CD0, 0x01), 0x000A, pools={POOL_HP}),
    LocationData(
        6029245, TMCLocation.FALLS_WATER_DIG_CAVE_FUSION_HP, TMCRegion.UPPER_FALLS, Items.HEART_PIECE,
        (0x0F3DD7, None), (0x2D05, 0x20), 0x0016, pools={POOL_HP}),
    LocationData(
        6029246, TMCLocation.FALLS_WATER_DIG_CAVE_FUSION_CHEST, TMCRegion.UPPER_FALLS, None,
        (0x0F3E26, None), (0x2D05, 0x04), 0x0016),
    LocationData(
        6029247, TMCLocation.FALLS_1ST_CAVE_CHEST, TMCRegion.UPPER_FALLS, None,
        (0x0F8E0E, None), (0x2D25, 0x10), 0x0533),
    LocationData(
        6029248, TMCLocation.FALLS_CLIFF_CHEST, TMCRegion.UPPER_FALLS, None,
        (0x0F89C2, None), (0x2CD0, 0x02), 0x000A),
    LocationData(
        6029249, TMCLocation.FALLS_SOUTH_DIG_SPOT, TMCRegion.UPPER_FALLS, Items.RUPEES_50,
        (0x0F8823, None), (0x2CDA, 0x80), 0x000A, pools={POOL_DIG}),
    LocationData(
        6029250, TMCLocation.FALLS_GOLDEN_TEKTITE, TMCRegion.UPPER_FALLS, Items.RUPEES_100,
        (None,     None), (0x2CA2, 0x40), 0x000A, pools={POOL_ENEMY}),
    LocationData(
        6029251, TMCLocation.FALLS_NORTH_DIG_SPOT, TMCRegion.UPPER_FALLS, Items.RUPEES_50,
        (0x0F8813, None), (0x2CD0, 0x80), 0x000A, pools={POOL_DIG}),
    LocationData(
        6029252, TMCLocation.FALLS_ROCK_FUSION_CHEST, TMCRegion.UPPER_FALLS, Items.KINSTONE,
        (0x0FE106, None), (0x2CD3, 0x80), 0x000A),
    LocationData(
        6029253, TMCLocation.FALLS_WATERFALL_FUSION_HP, TMCRegion.UPPER_FALLS, Items.HEART_PIECE,
        (0x0F906F, None), (0x2D27, 0x10), 0x0933, pools={POOL_HP}),
    LocationData(
        6029254, TMCLocation.FALLS_RUPEE_CAVE_TOP_TOP, TMCRegion.UPPER_FALLS, Items.RUPEES_1,
        (0x0F8F27, None), (0x2D25, 0x20), 0x0833, pools={POOL_RUPEE}),
    LocationData(
        6029255, TMCLocation.FALLS_RUPEE_CAVE_TOP_LEFT, TMCRegion.UPPER_FALLS, Items.RUPEES_1,
        (0x0F8F37, None), (0x2D25, 0x40), 0x0833, pools={POOL_RUPEE}),
    LocationData(
        6029256, TMCLocation.FALLS_RUPEE_CAVE_TOP_MIDDLE, TMCRegion.UPPER_FALLS, Items.RUPEES_20,
        (0x0F8F47, None), (0x2D25, 0x80), 0x0833, pools={POOL_RUPEE}),
    LocationData(
        6029257, TMCLocation.FALLS_RUPEE_CAVE_TOP_RIGHT, TMCRegion.UPPER_FALLS, Items.RUPEES_1,
        (0x0F8F57, None), (0x2D26, 0x01), 0x0833, pools={POOL_RUPEE}),
    LocationData(
        6029258, TMCLocation.FALLS_RUPEE_CAVE_TOP_BOTTOM, TMCRegion.UPPER_FALLS, Items.RUPEES_1,
        (0x0F8F67, None), (0x2D26, 0x02), 0x0833, pools={POOL_RUPEE}),
    LocationData(
        6029259, TMCLocation.FALLS_RUPEE_CAVE_SIDE_TOP, TMCRegion.UPPER_FALLS, Items.RUPEES_1,
        (0x0F8F77, None), (0x2D26, 0x04), 0x0833, pools={POOL_RUPEE}),
    LocationData(
        6029260, TMCLocation.FALLS_RUPEE_CAVE_SIDE_LEFT, TMCRegion.UPPER_FALLS, Items.RUPEES_1,
        (0x0F8F87, None), (0x2D26, 0x08), 0x0833, pools={POOL_RUPEE}),
    LocationData(
        6029261, TMCLocation.FALLS_RUPEE_CAVE_SIDE_RIGHT, TMCRegion.UPPER_FALLS, Items.RUPEES_1,
        (0x0F8F97, None), (0x2D26, 0x10), 0x0833, pools={POOL_RUPEE}),
    LocationData(
        6029262, TMCLocation.FALLS_RUPEE_CAVE_SIDE_BOTTOM, TMCRegion.UPPER_FALLS, Items.RUPEES_1,
        (0x0F8FA7, None), (0x2D26, 0x20), 0x0833, pools={POOL_RUPEE}),
    LocationData(
        6029263, TMCLocation.FALLS_RUPEE_CAVE_UNDERWATER_TOP_LEFT, TMCRegion.UPPER_FALLS, Items.RUPEES_1,
        (0x0F8FB7, None), (0x2D26, 0x40), 0x0833, pools={POOL_RUPEE}),
    LocationData(
        6029264, TMCLocation.FALLS_RUPEE_CAVE_UNDERWATER_TOP_RIGHT, TMCRegion.UPPER_FALLS, Items.RUPEES_1,
        (0x0F8FC7, None), (0x2D26, 0x80), 0x0833, pools={POOL_RUPEE}),
    LocationData(
        6029265, TMCLocation.FALLS_RUPEE_CAVE_UNDERWATER_MIDDLE_LEFT, TMCRegion.UPPER_FALLS, Items.RUPEES_5,
        (0x0F8FD7, None), (0x2D27, 0x01), 0x0833, pools={POOL_RUPEE}),
    LocationData(
        6029266, TMCLocation.FALLS_RUPEE_CAVE_UNDERWATER_MIDDLE_RIGHT, TMCRegion.UPPER_FALLS, Items.RUPEES_5,
        (0x0F8FE7, None), (0x2D27, 0x02), 0x0833, pools={POOL_RUPEE}),
    LocationData(
        6029267, TMCLocation.FALLS_RUPEE_CAVE_UNDERWATER_BOTTOM_LEFT, TMCRegion.UPPER_FALLS, Items.RUPEES_20,
        (0x0F8FF7, None), (0x2D27, 0x04), 0x0833, pools={POOL_RUPEE}),
    LocationData(
        6029268, TMCLocation.FALLS_RUPEE_CAVE_UNDERWATER_BOTTOM_RIGHT, TMCRegion.UPPER_FALLS, Items.RUPEES_20,
        (0x0F9007, None), (0x2D27, 0x08), 0x0833, pools={POOL_RUPEE}),
    LocationData(
        6029269, TMCLocation.FALLS_TOP_CAVE_BOMB_WALL_CHEST, TMCRegion.UPPER_FALLS, None,
        (0x0F8C2E, None), (0x2D25, 0x04), 0x0233),
    LocationData(
        6029270, TMCLocation.FALLS_TOP_CAVE_CHEST, TMCRegion.UPPER_FALLS, Items.RUPEES_100,
        (0x0F8ADE, None), (0x2D25, 0x01), 0x0033),
    #endreigon
    #region Cloudtops
    LocationData(
        6029271, TMCLocation.CLOUDS_FREE_CHEST, TMCRegion.CLOUDS, Items.KINSTONE_GOLD_CLOUD,
        (0x0DCE0A, None), (0x2CD7, 0x08), 0x0108),
    LocationData(
        6029272, TMCLocation.CLOUDS_NORTH_EAST_DIG_SPOT, TMCRegion.CLOUDS, Items.KINSTONE,
        (0x0DCB5B, None), (0x2CD8, 0x08), 0x0108, pools={POOL_DIG}),
    LocationData(
        6029273, TMCLocation.CLOUDS_NORTH_KILL, TMCRegion.CLOUDS, Items.KINSTONE_GOLD_CLOUD,
        (0x0DCEDF, None), (0x2CDA, 0x02), 0x0208),
    LocationData(
        6029274, TMCLocation.CLOUDS_NORTH_WEST_LEFT_CHEST, TMCRegion.CLOUDS, None,
        (0x0DCE22, None), (0x2CD7, 0x40), 0x0108),
    LocationData(
        6029275, TMCLocation.CLOUDS_NORTH_WEST_RIGHT_CHEST, TMCRegion.CLOUDS, None,
        (0x0DCE2A, None), (0x2CD7, 0x80), 0x0108),
    LocationData(
        6029276, TMCLocation.CLOUDS_NORTH_WEST_DIG_SPOT, TMCRegion.CLOUDS, Items.KINSTONE,
        (0x0DCB4B, None), (0x2CD8, 0x04), 0x0108, pools={POOL_DIG}),
    LocationData(
        6029277, TMCLocation.CLOUDS_NORTH_WEST_BOTTOM_CHEST, TMCRegion.CLOUDS, Items.KINSTONE_GOLD_CLOUD,
        (0x0DCE1A, None), (0x2CD7, 0x20), 0x0108),
    LocationData(
        6029278, TMCLocation.CLOUDS_SOUTH_LEFT_CHEST, TMCRegion.CLOUDS, None,
        (0x0DCE32, None), (0x2CD8, 0x01), 0x0108),
    LocationData(
        6029279, TMCLocation.CLOUDS_SOUTH_DIG_SPOT, TMCRegion.CLOUDS, Items.KINSTONE,
        (0x0DCB8B, None), (0x2CD8, 0x40), 0x0108, pools={POOL_DIG}),
    LocationData(
        6029280, TMCLocation.CLOUDS_SOUTH_MIDDLE_CHEST, TMCRegion.CLOUDS, Items.KINSTONE_GOLD_CLOUD,
        (0x0DCE12, None), (0x2CD7, 0x10), 0x0108),
    LocationData(
        6029281, TMCLocation.CLOUDS_SOUTH_MIDDLE_DIG_SPOT, TMCRegion.CLOUDS, Items.KINSTONE,
        (0x0DCB6B, None), (0x2CD8, 0x10), 0x0108, pools={POOL_DIG}),
    LocationData(
        6029282, TMCLocation.CLOUDS_SOUTH_KILL, TMCRegion.CLOUDS, Items.KINSTONE_GOLD_CLOUD,
        (0x0DCEEF, None), (0x2CDA, 0x08), 0x0208),
    LocationData(
        6029283, TMCLocation.CLOUDS_SOUTH_RIGHT_CHEST, TMCRegion.CLOUDS, None,
        (0x0DCE3A, None), (0x2CD8, 0x02), 0x0108),
    LocationData(
        6029284, TMCLocation.CLOUDS_SOUTH_RIGHT_DIG_SPOT, TMCRegion.CLOUDS, Items.KINSTONE,
        (0x0DCB9B, None), (0x2CD8, 0x80), 0x0108, pools={POOL_DIG}),
    LocationData(
        6029285, TMCLocation.CLOUDS_SOUTH_EAST_BOTTOM_DIG_SPOT, TMCRegion.CLOUDS, Items.KINSTONE,
        (0x0DCBAB, None), (0x2CD9, 0x01), 0x0108, pools={POOL_DIG}),
    LocationData(
        6029286, TMCLocation.CLOUDS_SOUTH_EAST_TOP_DIG_SPOT, TMCRegion.CLOUDS, Items.KINSTONE,
        (0x0DCB7B, None), (0x2CD8, 0x20), 0x0108, pools={POOL_DIG}),
    #endregion
    #region Wind Tribe
    LocationData(
        6029287, TMCLocation.WIND_TRIBE_1F_LEFT_CHEST, TMCRegion.WIND_TRIBE, Items.KINSTONE,
        (0x0F582A, None), (0x2CDC, 0x20), 0x0030),
    LocationData(
        6029288, TMCLocation.WIND_TRIBE_1F_RIGHT_CHEST, TMCRegion.WIND_TRIBE, Items.KINSTONE,
        (0x0F5832, None), (0x2CDC, 0x40), 0x0030),
    LocationData(
        6029289, TMCLocation.WIND_TRIBE_2F_CHEST, TMCRegion.WIND_TRIBE, Items.KINSTONE,
        (0x0F5972, None), (0x2CDC, 0x80), 0x0130),
    LocationData(
        6029290, TMCLocation.WIND_TRIBE_2F_GREGAL_NPC_1, TMCRegion.WIND_TRIBE, None,
        (0x014C5C, None), (0x2CE8, 0x20), 0x0130),
    LocationData(
        6029291, TMCLocation.WIND_TRIBE_2F_GREGAL_NPC_2, TMCRegion.WIND_TRIBE, Items.PROGRESSIVE_BOW,
        (0x014CBC, None), (0x2CE8, 0x40), 0x0130),
    LocationData(
        6029292, TMCLocation.WIND_TRIBE_3F_LEFT_CHEST, TMCRegion.WIND_TRIBE, Items.KINSTONE,
        (0x0F5A92, None), (0x2CDD, 0x01), 0x0230),
    LocationData(
        6029293, TMCLocation.WIND_TRIBE_3F_CENTER_CHEST, TMCRegion.WIND_TRIBE, Items.KINSTONE,
        (0x0F5A8A, None), (0x2CDD, 0x02), 0x0230),
    LocationData(
        6029294, TMCLocation.WIND_TRIBE_3F_RIGHT_CHEST, TMCRegion.WIND_TRIBE, Items.KINSTONE,
        (0x0F5A82, None), (0x2CDD, 0x04), 0x0230),
    LocationData(
        6029295, TMCLocation.WIND_TRIBE_4F_LEFT_CHEST, TMCRegion.WIND_TRIBE, Items.KINSTONE,
        (0x0F5BD2, None), (0x2CDD, 0x40), 0x0330),
    LocationData(
        6029296, TMCLocation.WIND_TRIBE_4F_RIGHT_CHEST, TMCRegion.WIND_TRIBE, Items.KINSTONE,
        (0x0F5BDA, None), (0x2CDD, 0x80), 0x0330),
    #endregion
    #region Dungeon DWS
    LocationData(
        6029297, TMCLocation.DEEPWOOD_2F_CHEST, TMCRegion.DUNGEON_DWS, Items.RUPEES_20,
        (0x0DF17E, None), (0x2D45, 0x04), 0x1748),
    LocationData(
        6029298, TMCLocation.DEEPWOOD_1F_SLUG_TORCHES_CHEST, TMCRegion.DUNGEON_DWS, Items.SMALL_KEY_DWS,
        (0x0DEA4A, None), (0x2D43, 0x20), 0x1048),
    LocationData(
        6029299, TMCLocation.DEEPWOOD_1F_BARREL_ROOM_CHEST, TMCRegion.DUNGEON_DWS, None,
        (0x0DE396, None), (0x2D41, 0x08), 0x0648),
    LocationData(
        6029300, TMCLocation.DEEPWOOD_1F_WEST_BIG_CHEST, TMCRegion.DUNGEON_DWS, Items.DUNGEON_COMPASS_DWS,
        (0x0DE23E, None), (0x2D41, 0x02), 0x0548),
    LocationData(
        6029301, TMCLocation.DEEPWOOD_1F_WEST_STATUE_PUZZLE_CHEST, TMCRegion.DUNGEON_DWS, Items.SMALL_KEY_DWS,
        (0x0DE176, None), (0x2D40, 0x80), 0x0448),
    LocationData(
        6029302, TMCLocation.DEEPWOOD_1F_EAST_MULLDOZER_FIGHT_ITEM, TMCRegion.DUNGEON_DWS, Items.SMALL_KEY_DWS,
        (0x0DE51B, None), (0x2D42, 0x01), 0x0848),
    LocationData(
        6029303, TMCLocation.DEEPWOOD_1F_NORTH_EAST_CHEST, TMCRegion.DUNGEON_DWS, None,
        (0x0DE176, None), (0x2D40, 0x10), 0x0248),
    LocationData(
        6029304, TMCLocation.DEEPWOOD_B1_SWITCH_ROOM_BIG_CHEST, TMCRegion.DUNGEON_DWS, Items.DUNGEON_MAP_DWS,
        (0x0DECDA, None), (0x2D44, 0x04), 0x1248),
    LocationData(
        6029305, TMCLocation.DEEPWOOD_B1_SWITCH_ROOM_CHEST, TMCRegion.DUNGEON_DWS, Items.SMALL_KEY_DWS,
        (0x0DECD2, None), (0x2D44, 0x02), 0x1248),
    LocationData(
        6029306, TMCLocation.DEEPWOOD_1F_BLUE_WARP_HP, TMCRegion.DUNGEON_DWS, Items.HEART_PIECE,
        (0x0DDE03, None), (0x2D45, 0x80), 0x0148),
    LocationData(
        6029307, TMCLocation.DEEPWOOD_1F_BLUE_WARP_LEFT_CHEST, TMCRegion.DUNGEON_DWS, None,
        (0x0DDEDA, None), (0x2D40, 0x04), 0x0148),
    LocationData(
        6029308, TMCLocation.DEEPWOOD_1F_BLUE_WARP_RIGHT_CHEST, TMCRegion.DUNGEON_DWS, None,
        (0x0DDEE2, None), (0x2D40, 0x08), 0x0148),
    LocationData(
        6029309, TMCLocation.DEEPWOOD_1F_MADDERPILLAR_BIG_CHEST, TMCRegion.DUNGEON_DWS, Items.GUST_JAR,
        (0x0DDC7E, None), (0x2D3F, 0x08), 0x0048),
    LocationData(
        6029310, TMCLocation.DEEPWOOD_1F_MADDERPILLAR_HP, TMCRegion.DUNGEON_DWS, Items.HEART_PIECE,
        (0x0DE1F7, None), (0x2D46, 0x04), 0x0548, scoutable=True),
    LocationData(
        6029311, TMCLocation.DEEPWOOD_B1_WEST_BIG_CHEST, TMCRegion.DUNGEON_DWS, Items.BIG_KEY_DWS,
        (0x0DEB9A, None), (0x2D43, 0x80), 0x1148),
    LocationData(
        6029312, TMCLocation.DEEPWOOD_BOSS_ITEM, TMCRegion.DUNGEON_DWS, Items.HEART_CONTAINER,
        (0x0DF07B, None), (0x2D44, 0x80), 0x0049),
    LocationData(
        6029313, TMCLocation.DEEPWOOD_PRIZE, TMCRegion.DUNGEON_DWS, Items.EARTH_ELEMENT,
        (0x0DF03B, None), (0x2C9C, 0x04), 0x0049, pools={POOL_ELEMENT}),
    #endregion
    #region Dungeon CoF
    LocationData(
        6029314, TMCLocation.COF_1F_SPIKE_BEETLE_BIG_CHEST, TMCRegion.DUNGEON_COF, Items.DUNGEON_MAP_COF,
        (0x0E09C6, None), (0x2D5A, 0x04), 0x1550),
    LocationData(
        6029315, TMCLocation.COF_1F_ITEM1, TMCRegion.DUNGEON_COF, Items.RUPEES_1,
        (0x0DFAEB, None), (0x2D5B, 0x40), 0x0550, pools={POOL_RUPEE}),
    LocationData(
        6029316, TMCLocation.COF_1F_ITEM2, TMCRegion.DUNGEON_COF, Items.RUPEES_1,
        (0x0DFAFB, None), (0x2D5B, 0x80), 0x0550, pools={POOL_RUPEE}),
    LocationData(
        6029317, TMCLocation.COF_1F_ITEM3, TMCRegion.DUNGEON_COF, Items.RUPEES_1,
        (0x0DFB0B, None), (0x2D5C, 0x01), 0x0550, pools={POOL_RUPEE}),
    LocationData(
        6029318, TMCLocation.COF_1F_ITEM4, TMCRegion.DUNGEON_COF, Items.RUPEES_1,
        (0x0DFB1B, None), (0x2D5C, 0x02), 0x0550, pools={POOL_RUPEE}),
    LocationData(
        6029319, TMCLocation.COF_1F_ITEM5, TMCRegion.DUNGEON_COF, Items.RUPEES_1,
        (0x0DFB2B, None), (0x2D5C, 0x04), 0x0550, pools={POOL_RUPEE}),
    LocationData(
        6029320, TMCLocation.COF_B1_HAZY_ROOM_BIG_CHEST, TMCRegion.DUNGEON_COF, Items.DUNGEON_COMPASS_COF,
        (0x0E028A, None), (0x2D59, 0x02), 0x0950),
    LocationData(
        6029321, TMCLocation.COF_B1_HAZY_ROOM_SMALL_CHEST, TMCRegion.DUNGEON_COF, Items.KINSTONE,
        (0x0E0282, None), (0x2D59, 0x04), 0x0950),
    LocationData(
        6029322, TMCLocation.COF_B1_ROLLOBITE_CHEST, TMCRegion.DUNGEON_COF, Items.RUPEES_50,
        (0x0E00E2, None), (0x2D58, 0x40), 0x0850),
    LocationData(
        6029323, TMCLocation.COF_B1_ROLLOBITE_PILLAR_CHEST, TMCRegion.DUNGEON_COF, Items.SMALL_KEY_COF,
        (0x0E00DA, None), (0x2D58, 0x80), 0x0850),
    LocationData(
        6029324, TMCLocation.COF_B1_SPIKEY_CHUS_PILLAR_CHEST, TMCRegion.DUNGEON_COF, Items.SMALL_KEY_COF,
        (0x0DF50A, None), (0x2D57, 0x01), 0x0150),
    LocationData(
        6029325, TMCLocation.COF_B1_HP, TMCRegion.DUNGEON_COF, Items.HEART_PIECE,
        (0x0DFC9F, None), (0x2D5B, 0x10), 0x0650, pools={POOL_HP}),
    LocationData(
        6029326, TMCLocation.COF_B1_SPIKEY_CHUS_BIG_CHEST, TMCRegion.DUNGEON_COF, Items.CANE_OF_PACCI,
        (0x0DF512, None), (0x2D57, 0x02), 0x0150),
    LocationData(
        6029327, TMCLocation.COF_B2_PRE_LAVA_NORTH_CHEST, TMCRegion.DUNGEON_COF, Items.KINSTONE,
        (0x0E04F6, None), (0x2D59, 0x10), 0x1050),
    LocationData(
        6029328, TMCLocation.COF_B2_PRE_LAVA_SOUTH_CHEST, TMCRegion.DUNGEON_COF, Items.KINSTONE,
        (0x0E04FE, None), (0x2D59, 0x20), 0x1050),
    LocationData(
        6029329, TMCLocation.COF_B2_LAVA_ROOM_BLADE_CHEST, TMCRegion.DUNGEON_COF, Items.KINSTONE,
        (0x0E08BA, None), (0x2D5A, 0x01), 0x1450),
    LocationData(
        6029330, TMCLocation.COF_B2_LAVA_ROOM_RIGHT_CHEST, TMCRegion.DUNGEON_COF, Items.RUPEES_100,
        (0x0E0CC2, None), (0x2D5B, 0x01), 0x1750),
    LocationData(
        6029331, TMCLocation.COF_B2_LAVA_ROOM_LEFT_CHEST, TMCRegion.DUNGEON_COF, Items.KINSTONE,
        (0x0E0CBA, None), (0x2D5A, 0x80), 0x1750),
    LocationData(
        6029332, TMCLocation.COF_B2_LAVA_ROOM_BIG_CHEST, TMCRegion.DUNGEON_COF, Items.BIG_KEY_COF,
        (0x0E0CCA, None), (0x2D5B, 0x02), 0x1750),
    LocationData(
        6029333, TMCLocation.COF_BOSS_ITEM, TMCRegion.DUNGEON_COF, Items.HEART_CONTAINER,
        (0x0E0F43, None), (0x2D5B, 0x04), 0x0051, pools={POOL_HP}),
    LocationData(
        6029334, TMCLocation.COF_PRIZE, TMCRegion.DUNGEON_COF, Items.FIRE_ELEMENT,
        (0x0E0F03, None), (0x2C9C, 0x08), 0x0051, pools={POOL_ELEMENT}),
    #endregion
    #region Dungeon FoW
    LocationData(
        6029335, TMCLocation.FORTRESS_ENTRANCE_1F_LEFT_CHEST, TMCRegion.DUNGEON_FOW, Items.KINSTONE,
        (0x0F3E96, None), (0x2D05, 0x80), 0x0018),
    LocationData(
        6029336, TMCLocation.FORTRESS_ENTRANCE_1F_LEFT_WIZROBE_CHEST, TMCRegion.DUNGEON_FOW, None,
        (0x0E2D4A, None), (0x2D74, 0x08), 0x2358),
    LocationData(
        6029337, TMCLocation.FORTRESS_ENTRANCE_1F_RIGHT_ITEM, TMCRegion.DUNGEON_FOW, Items.RUPEES_50,
        (0x0F3E67, None), (0x2D05, 0x40), None),
    LocationData(
        6029338, TMCLocation.FORTRESS_LEFT_2F_DIG_CHEST, TMCRegion.DUNGEON_FOW, Items.KINSTONE,
        (0x0F4086, None), (0x2D06, 0x01), 0x0118),
    LocationData(
        6029339, TMCLocation.FORTRESS_LEFT_2F_ITEM1, TMCRegion.DUNGEON_FOW, Items.RUPEES_1,
        (0x0F3F37, None), (0x2D06, 0x20), None),
    LocationData(
        6029340, TMCLocation.FORTRESS_LEFT_2F_ITEM2, TMCRegion.DUNGEON_FOW, Items.RUPEES_1,
        (0x0F3F47, None), (0x2D06, 0x40), None),
    LocationData(
        6029341, TMCLocation.FORTRESS_LEFT_2F_ITEM3, TMCRegion.DUNGEON_FOW, Items.RUPEES_1,
        (0x0F3F57, None), (0x2D06, 0x80), None),
    LocationData(
        6029342, TMCLocation.FORTRESS_LEFT_2F_ITEM4, TMCRegion.DUNGEON_FOW, Items.RUPEES_1,
        (0x0F3F67, None), (0x2D07, 0x01), None),
    LocationData(
        6029343, TMCLocation.FORTRESS_LEFT_2F_ITEM5, TMCRegion.DUNGEON_FOW, Items.RUPEES_1,
        (0x0F3F77, None), (0x2D07, 0x04), None),
    LocationData(
        6029344, TMCLocation.FORTRESS_LEFT_2F_ITEM6, TMCRegion.DUNGEON_FOW, Items.RUPEES_5,
        (0x0F3F87, None), (0x2D07, 0x08), None),
    LocationData(
        6029345, TMCLocation.FORTRESS_LEFT_2F_ITEM7, TMCRegion.DUNGEON_FOW, Items.RUPEES_5,
        (0x0F3F97, None), (0x2D07, 0x02), None),
    LocationData(
        6029346, TMCLocation.FORTRESS_LEFT_3F_SWITCH_CHEST, TMCRegion.DUNGEON_FOW, Items.KINSTONE,
        (0x0F4146, None), (0x2D07, 0x20), 0x0218),
    LocationData(
        6029347, TMCLocation.FORTRESS_LEFT_3F_EYEGORE_BIG_CHEST, TMCRegion.DUNGEON_FOW, Items.DUNGEON_MAP_FOW,
        (0x0E105E, None), (0x2D6F, 0x10), 0x0058),
    LocationData(
        6029348, TMCLocation.FORTRESS_LEFT_3F_ITEM_DROP, TMCRegion.DUNGEON_FOW, Items.SMALL_KEY_FOW,
        (None,     None), (0x2D73, 0x80), 0x0458), # room_area is a complete guess
    LocationData(
        6029349, TMCLocation.FORTRESS_MIDDLE_2F_BIG_CHEST, TMCRegion.DUNGEON_FOW, Items.DUNGEON_COMPASS_FOW,
        (0x0E26FA, None), (0x2D73, 0x02), 0x1958),
    LocationData(
        6029350, TMCLocation.FORTRESS_MIDDLE_2F_STATUE_CHEST, TMCRegion.DUNGEON_FOW, Items.KINSTONE,
        (0x0F408E, None), (0x2D06, 0x02), 0x0118),
    LocationData(
        6029351, TMCLocation.FORTRESS_RIGHT_2F_LEFT_CHEST, TMCRegion.DUNGEON_FOW, Items.KINSTONE,
        (None,     None), (0x2D73, 0x20), 0x1D58),
    LocationData(
        6029352, TMCLocation.FORTRESS_RIGHT_2F_RIGHT_CHEST, TMCRegion.DUNGEON_FOW, Items.KINSTONE,
        (None,     None), (0x2D73, 0x40), 0x1D58),
    LocationData(
        6029353, TMCLocation.FORTRESS_RIGHT_2F_DIG_CHEST, TMCRegion.DUNGEON_FOW, Items.KINSTONE,
        (0x0F4096, None), (0x2D06, 0x04), 0x0118),
    LocationData(
        6029354, TMCLocation.FORTRESS_RIGHT_3F_DIG_CHEST, TMCRegion.DUNGEON_FOW, Items.KINSTONE,
        (0x0F4146, None), (0x2D07, 0x40), 0x0218),
    LocationData(
        6029355, TMCLocation.FORTRESS_RIGHT_3F_ITEM_DROP, TMCRegion.DUNGEON_FOW, Items.SMALL_KEY_FOW,
        (None,     None), (0x2D74, 0x02), None),
    LocationData(
        6029356, TMCLocation.FORTRESS_ENTRANCE_1F_RIGHT_HP, TMCRegion.DUNGEON_FOW, Items.HEART_PIECE,
        (0x0E2DD7, None), (0x2D74, 0x80), None, pools={POOL_HP}),
    LocationData(
        6029357, TMCLocation.FORTRESS_BACK_LEFT_BIG_CHEST, TMCRegion.DUNGEON_FOW, Items.MOLE_MITTS,
        (0x0F41DE, None), (0x2D08, 0x01), 0x0318),
    LocationData(
        6029358, TMCLocation.FORTRESS_BACK_LEFT_SMALL_CHEST, TMCRegion.DUNGEON_FOW, Items.RUPEES_100,
        (0x0F41E6, None), (0x2D08, 0x02), 0x0318),
    LocationData(
        6029359, TMCLocation.FORTRESS_BACK_RIGHT_STATUE_ITEM_DROP, TMCRegion.DUNGEON_FOW, Items.SMALL_KEY_FOW,
        (0x0E1E8B, None), (0x2D71, 0x40), None),
    LocationData(
        6029360, TMCLocation.FORTRESS_BACK_RIGHT_MINISH_ITEM_DROP, TMCRegion.DUNGEON_FOW, Items.SMALL_KEY_FOW,
        (0x0F424F, None), (0x2D08, 0x10), None),
    LocationData(
        6029361, TMCLocation.FORTRESS_BACK_RIGHT_DIG_ROOM_TOP_POT, TMCRegion.DUNGEON_FOW, Items.RUPEES_50,
        (0x0F3FC7, 0x0F3FC9), (0x2D06, 0x08), None, pools={POOL_POT}),
    LocationData(
        6029362, TMCLocation.FORTRESS_BACK_RIGHT_DIG_ROOM_BOTTOM_POT, TMCRegion.DUNGEON_FOW, None,
        (0x0F3FD7, 0x0F3FD9), (0x2D06, 0x10), None, pools={POOL_POT}),
    LocationData(
        6029363, TMCLocation.FORTRESS_BACK_RIGHT_BIG_CHEST, TMCRegion.DUNGEON_FOW, Items.BIG_KEY_FOW,
        (None,     None), (0x2D73, 0x04), 0x1B58),
    LocationData(
        6029364, TMCLocation.FORTRESS_BOSS_ITEM, TMCRegion.DUNGEON_FOW, Items.HEART_CONTAINER,
        (0x0E22E7, None), (0x2D72, 0x04), None, pools={POOL_HP}),
    LocationData(
        6029365, TMCLocation.FORTRESS_PRIZE, TMCRegion.DUNGEON_FOW, Items.OCARINA,
        (0x09C9E6, 0x09C9E8), (0x2D74, 0x20), None, pools={POOL_ELEMENT}),
    #endregion
    #region Dungeon ToD
    LocationData(
        6029366, TMCLocation.DROPLETS_ENTRANCE_B2_EAST_ICEBLOCK, TMCRegion.DUNGEON_TOD, Items.SMALL_KEY_TOD,
        (0x098C1A, 0x098C1C), (0x2D8E, 0x04), 0x1260),
    LocationData(
        6029367, TMCLocation.DROPLETS_ENTRANCE_B2_WEST_ICEBLOCK, TMCRegion.DUNGEON_TOD, Items.BIG_KEY_TOD,
        (0x098C3C, 0x098C3E), (0x2D8D, 0x80), 0x2060),
    LocationData(
        6029368, TMCLocation.DROPLETS_LEFT_PATH_B1_UNDERPASS_ITEM1, TMCRegion.DUNGEON_TOD, Items.RUPEES_1,
        (0x0E3F8B, None), (0x2D94, 0x20), None, pools={POOL_RUPEE}),
    LocationData(
        6029369, TMCLocation.DROPLETS_LEFT_PATH_B1_UNDERPASS_ITEM2, TMCRegion.DUNGEON_TOD, Items.RUPEES_1,
        (0x0E3F9B, None), (0x2D94, 0x40), None, pools={POOL_RUPEE}),
    LocationData(
        6029370, TMCLocation.DROPLETS_LEFT_PATH_B1_UNDERPASS_ITEM3, TMCRegion.DUNGEON_TOD, Items.RUPEES_1,
        (0x0E3FAB, None), (0x2D94, 0x80), None, pools={POOL_RUPEE}),
    LocationData(
        6029371, TMCLocation.DROPLETS_LEFT_PATH_B1_UNDERPASS_ITEM4, TMCRegion.DUNGEON_TOD, Items.RUPEES_1,
        (0x0E3FBB, None), (0x2D95, 0x01), None, pools={POOL_RUPEE}),
    LocationData(
        6029372, TMCLocation.DROPLETS_LEFT_PATH_B1_UNDERPASS_ITEM5, TMCRegion.DUNGEON_TOD, Items.RUPEES_1,
        (0x0E3FCB, None), (0x2D95, 0x02), None, pools={POOL_RUPEE}),
    LocationData(
        6029373, TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_BIG_CHEST, TMCRegion.DUNGEON_TOD, Items.DUNGEON_MAP_TOD,
        (0x0E400A, None), (0x2D8B, 0x80), 0x0D60),
    LocationData(
        6029374, TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_UNDERWATER1, TMCRegion.DUNGEON_TOD, Items.RUPEES_5,
        (0x0E3593, None), (0x2D96, 0x20), None, pools={POOL_WATER}),
    LocationData(
        6029375, TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_UNDERWATER2, TMCRegion.DUNGEON_TOD, Items.RUPEES_5,
        (0x0E35A3, None), (0x2D96, 0x40), None, pools={POOL_WATER}),
    LocationData(
        6029376, TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_UNDERWATER3, TMCRegion.DUNGEON_TOD, Items.RUPEES_5,
        (0x0E35B3, None), (0x2D96, 0x80), None, pools={POOL_WATER}),
    LocationData(
        6029377, TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_UNDERWATER4, TMCRegion.DUNGEON_TOD, Items.RUPEES_5,
        (0x0E35C3, None), (0x2D97, 0x01), None, pools={POOL_WATER}),
    LocationData(
        6029378, TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_UNDERWATER5, TMCRegion.DUNGEON_TOD, Items.RUPEES_5,
        (0x0E35D3, None), (0x2D97, 0x02), None, pools={POOL_WATER}),
    LocationData(
        6029379, TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_UNDERWATER6, TMCRegion.DUNGEON_TOD, Items.RUPEES_5,
        (0x0E35E3, None), (0x2D97, 0x04), None, pools={POOL_WATER}),
    LocationData(
        6029380, TMCLocation.DROPLETS_LEFT_PATH_B2_WATERFALL_UNDERWATER1, TMCRegion.DUNGEON_TOD, Items.RUPEES_5,
        (0x0E58DF, None), (0x2D95, 0x80), None, pools={POOL_WATER}),
    LocationData(
        6029381, TMCLocation.DROPLETS_LEFT_PATH_B2_WATERFALL_UNDERWATER2, TMCRegion.DUNGEON_TOD, Items.RUPEES_5,
        (0x0E58EF, None), (0x2D96, 0x01), None, pools={POOL_WATER}),
    LocationData(
        6029382, TMCLocation.DROPLETS_LEFT_PATH_B2_WATERFALL_UNDERWATER3, TMCRegion.DUNGEON_TOD, Items.RUPEES_5,
        (0x0E58FF, None), (0x2D96, 0x02), None, pools={POOL_WATER}),
    LocationData(
        6029383, TMCLocation.DROPLETS_LEFT_PATH_B2_WATERFALL_UNDERWATER4, TMCRegion.DUNGEON_TOD, Items.RUPEES_5,
        (0x0E590F, None), (0x2D96, 0x04), None, pools={POOL_WATER}),
    LocationData(
        6029384, TMCLocation.DROPLETS_LEFT_PATH_B2_WATERFALL_UNDERWATER5, TMCRegion.DUNGEON_TOD, Items.RUPEES_5,
        (0x0E591F, None), (0x2D96, 0x08), None, pools={POOL_WATER}),
    LocationData(
        6029385, TMCLocation.DROPLETS_LEFT_PATH_B2_WATERFALL_UNDERWATER6, TMCRegion.DUNGEON_TOD, Items.RUPEES_5,
        (0x0E592F, None), (0x2D96, 0x10), None, pools={POOL_WATER}),
    LocationData(
        6029386, TMCLocation.DROPLETS_LEFT_PATH_B2_UNDERWATER_POT, TMCRegion.DUNGEON_TOD, Items.SMALL_KEY_TOD,
        (0x0E5BC7, None), (0x2D93, 0x04), None, pools={POOL_WATER}),
    LocationData(
        6029387, TMCLocation.DROPLETS_LEFT_PATH_B2_ICE_MADDERPILLAR_BIG_CHEST, TMCRegion.DUNGEON_TOD, Items.DUNGEON_COMPASS_TOD,
        (0x0E5A62, None), (0x2D92, 0x80), 0x3260),
    LocationData(
        6029388, TMCLocation.DROPLETS_LEFT_PATH_B2_ICE_PLAIN_FROZEN_CHEST, TMCRegion.DUNGEON_TOD, None,
        (0x0E4E0E, None), (0x2D8F, 0x04), 0x2860),
    LocationData(
        6029389, TMCLocation.DROPLETS_LEFT_PATH_B2_ICE_PLAIN_CHEST, TMCRegion.DUNGEON_TOD, Items.RUPEES_50,
        (0x0E4E16, None), (0x2D8F, 0x08), 0x2860),
    LocationData(
        6029390, TMCLocation.DROPLETS_LEFT_PATH_B2_LILYPAD_CORNER_FROZEN_CHEST, TMCRegion.DUNGEON_TOD, Items.KINSTONE,
        (0x0E5492, None), (0x2D93, 0x40), 0x2D60),
    LocationData(
        6029391, TMCLocation.DROPLETS_RIGHT_PATH_B1_1ST_CHEST, TMCRegion.DUNGEON_TOD, Items.KINSTONE,
        (0x0E3A2A, None), (0x2D8B, 0x01), 0x0960),
    LocationData(
        6029392, TMCLocation.DROPLETS_RIGHT_PATH_B1_2ND_CHEST, TMCRegion.DUNGEON_TOD, Items.KINSTONE,
        (0x0E3B92, None), (0x2D8B, 0x04), 0x0A60),
    LocationData(
        6029393, TMCLocation.DROPLETS_RIGHT_PATH_B1_POT, TMCRegion.DUNGEON_TOD, Items.KINSTONE,
        (0x0E3A73, 0x0E3A75), (0x2D8B, 0x02), None, pools={POOL_POT}),
    LocationData(
        6029394, TMCLocation.DROPLETS_RIGHT_PATH_B3_FROZEN_CHEST, TMCRegion.DUNGEON_TOD, Items.SMALL_KEY_TOD,
        (0x0E4426, None), (0x2D8D, 0x10), 0x1160),
    LocationData(
        6029395, TMCLocation.DROPLETS_RIGHT_PATH_B1_BLU_CHU_BIG_CHEST, TMCRegion.DUNGEON_TOD, Items.LANTERN,
        (0x0E434E, None), (0x2D8C, 0x80), 0x1060),
    LocationData(
        6029396, TMCLocation.DROPLETS_RIGHT_PATH_B2_FROZEN_CHEST, TMCRegion.DUNGEON_TOD, Items.RUPEES_100,
        (0x0E5A5A, None), (0x2D92, 0x40), 0x3260),
    LocationData(
        6029397, TMCLocation.DROPLETS_RIGHT_PATH_B2_DARK_MAZE_BOTTOM_CHEST, TMCRegion.DUNGEON_TOD, Items.KINSTONE,
        (0x0E5216, None), (0x2D8F, 0x80), 0x2B60),
    LocationData(
        6029398, TMCLocation.DROPLETS_RIGHT_PATH_B2_MULLDOZERS_ITEM_DROP, TMCRegion.DUNGEON_TOD, Items.SMALL_KEY_TOD,
        (0x0E55CB, None), (0x2D91, 0x80), None),
    LocationData(
        6029399, TMCLocation.DROPLETS_RIGHT_PATH_B2_DARK_MAZE_TOP_RIGHT_CHEST, TMCRegion.DUNGEON_TOD, Items.KINSTONE,
        (0x0E5206, None), (0x2D8F, 0x20), 0x2B60),
    LocationData(
        6029400, TMCLocation.DROPLETS_RIGHT_PATH_B2_DARK_MAZE_TOP_LEFT_CHEST, TMCRegion.DUNGEON_TOD, Items.KINSTONE,
        (0x0E520E, None), (0x2D8F, 0x40), 0x2B60),
    LocationData(
        6029401, TMCLocation.DROPLETS_RIGHT_PATH_B2_UNDERPASS_ITEM1, TMCRegion.DUNGEON_TOD, Items.RUPEES_1,
        (0x0E483F, None), (0x2D95, 0x10), 0x0D60, pools={POOL_WATER}),
    LocationData(
        6029402, TMCLocation.DROPLETS_RIGHT_PATH_B2_UNDERPASS_ITEM2, TMCRegion.DUNGEON_TOD, Items.RUPEES_1,
        (0x0E484F, None), (0x2D95, 0x20), 0x0D60, pools={POOL_WATER}),
    LocationData(
        6029403, TMCLocation.DROPLETS_RIGHT_PATH_B2_UNDERPASS_ITEM3, TMCRegion.DUNGEON_TOD, Items.RUPEES_1,
        (0x0E485F, None), (0x2D95, 0x40), 0x0D60, pools={POOL_WATER}),
    LocationData(
        6029404, TMCLocation.DROPLETS_RIGHT_PATH_B2_UNDERPASS_ITEM4, TMCRegion.DUNGEON_TOD, Items.RUPEES_1,
        (0x0E486F, None), (0x2D95, 0x04), 0x0D60, pools={POOL_WATER}),
    LocationData(
        6029405, TMCLocation.DROPLETS_RIGHT_PATH_B2_UNDERPASS_ITEM5, TMCRegion.DUNGEON_TOD, Items.RUPEES_1,
        (0x0E487F, None), (0x2D95, 0x08), 0x0D60, pools={POOL_WATER}),
    LocationData(
        6029406, TMCLocation.DROPLETS_BOSS_ITEM, TMCRegion.DUNGEON_TOD, Items.HEART_CONTAINER,
        (0x0E4103, None), (0x2D8C, 0x01), None),
    LocationData(
        6029407, TMCLocation.DROPLETS_PRIZE, TMCRegion.DUNGEON_TOD, Items.WATER_ELEMENT,
        (0x0E40C3, None), (0x2C9C, 0x20), None, pools={POOL_ELEMENT}),
    #endregion
    #region Dungeon PoW
    LocationData(
        6029408, TMCLocation.PALACE_1ST_HALF_1F_GRATE_CHEST, TMCRegion.DUNGEON_POW, Items.KINSTONE,
        (0x0E99DE, None), (0x2DAA, 0x40), 0x2D70),
    LocationData(
        6029409, TMCLocation.PALACE_1ST_HALF_1F_WIZROBE_BIG_CHEST, TMCRegion.DUNGEON_POW, Items.ROCS_CAPE,
        (0x0E980A, None), (0x2DAA, 0x10), 0x2C70),
    LocationData(
        6029410, TMCLocation.PALACE_1ST_HALF_2F_ITEM1, TMCRegion.DUNGEON_POW, Items.RUPEES_1,
        (0x0E8B1F, None), (0x2DA7, 0x04), None, pools={POOL_RUPEE}),
    LocationData(
        6029411, TMCLocation.PALACE_1ST_HALF_2F_ITEM2, TMCRegion.DUNGEON_POW, Items.RUPEES_1,
        (0x0E8B2F, None), (0x2DA7, 0x08), None, pools={POOL_RUPEE}),
    LocationData(
        6029412, TMCLocation.PALACE_1ST_HALF_2F_ITEM3, TMCRegion.DUNGEON_POW, Items.RUPEES_1,
        (0x0E8B3F, None), (0x2DA7, 0x10), None, pools={POOL_RUPEE}),
    LocationData(
        6029413, TMCLocation.PALACE_1ST_HALF_2F_ITEM4, TMCRegion.DUNGEON_POW, Items.RUPEES_1,
        (0x0E8B4F, None), (0x2DA7, 0x20), None, pools={POOL_RUPEE}),
    LocationData(
        6029414, TMCLocation.PALACE_1ST_HALF_2F_ITEM5, TMCRegion.DUNGEON_POW, Items.RUPEES_1,
        (0x0E8B5F, None), (0x2DA7, 0x40), None, pools={POOL_RUPEE}),
    LocationData(
        6029415, TMCLocation.PALACE_1ST_HALF_3F_POT_PUZZLE_ITEM_DROP, TMCRegion.DUNGEON_POW, Items.SMALL_KEY_POW,
        (0x0E896F, None), (0x2DA7, 0x02), None),
    LocationData(
        6029416, TMCLocation.PALACE_1ST_HALF_4F_BOW_MOBLINS_CHEST, TMCRegion.DUNGEON_POW, Items.KINSTONE,
        (0x0E77F6, None), (0x2DA4, 0x80), 0x0F70),
    LocationData(
        6029417, TMCLocation.PALACE_1ST_HALF_5F_BALL_AND_CHAIN_SOLDIERS_ITEM_DROP, TMCRegion.DUNGEON_POW, Items.SMALL_KEY_POW,
        (0x0E719F, None), (0x2DA4, 0x02), 0x0870),
    LocationData(
        6029418, TMCLocation.PALACE_1ST_HALF_5F_FAN_LOOP_CHEST, TMCRegion.DUNGEON_POW, Items.SMALL_KEY_POW,
        (0x0E7116, None), (0x2DA3, 0x40), 0x0770),
    LocationData(
        6029419, TMCLocation.PALACE_1ST_HALF_5F_BIG_CHEST, TMCRegion.DUNGEON_POW, Items.BIG_KEY_POW,
        (0x0E6ACA, None), (0x2DA2, 0x10), 0x0170),
    LocationData(
        6029420, TMCLocation.PALACE_2ND_HALF_1F_DARK_ROOM_BIG_CHEST, TMCRegion.DUNGEON_POW, Items.DUNGEON_COMPASS_POW,
        (0x0EA0B6, None), (0x2DAB, 0x02), 0x3270),
    LocationData(
        6029421, TMCLocation.PALACE_2ND_HALF_1F_DARK_ROOM_SMALL_CHEST, TMCRegion.DUNGEON_POW, Items.SMALL_KEY_POW,
        (0x0EA0BE, None), (0x2DAB, 0x04), 0x3270),
    LocationData(
        6029422, TMCLocation.PALACE_2ND_HALF_2F_MANY_ROLLERS_CHEST, TMCRegion.DUNGEON_POW, Items.SMALL_KEY_POW,
        (0x0E95AA, None), (0x2DA9, 0x80), 0x2B70),
    LocationData(
        6029423, TMCLocation.PALACE_2ND_HALF_2F_TWIN_WIZROBES_CHEST, TMCRegion.DUNGEON_POW, Items.KINSTONE,
        (0x0E945E, None), (0x2DA9, 0x40), 0x2970),
    LocationData(
        6029424, TMCLocation.PALACE_2ND_HALF_3F_FIRE_WIZROBES_BIG_CHEST, TMCRegion.DUNGEON_POW, Items.DUNGEON_MAP_POW,
        (0x0E86F2, None), (0x2DA6, 0x80), 0x1C70),
    LocationData(
        6029425, TMCLocation.PALACE_2ND_HALF_4F_HP, TMCRegion.DUNGEON_POW, Items.HEART_PIECE,
        (0x0E77A7, None), (0x2DAC, 0x01), None, pools={POOL_HP}),
    LocationData(
        6029426, TMCLocation.PALACE_2ND_HALF_4F_SWITCH_HIT_CHEST, TMCRegion.DUNGEON_POW, Items.RUPEES_200,
        (0x0E7ED6, None), (0x2DA5, 0x80), 0x1570),
    LocationData(
        6029427, TMCLocation.PALACE_2ND_HALF_5F_BOMBAROSSA_CHEST, TMCRegion.DUNGEON_POW, Items.SMALL_KEY_POW,
        (0x0E6D22, None), (0x2DA2, 0x20), 0x0370),
    LocationData(
        6029428, TMCLocation.PALACE_2ND_HALF_4F_BLOCK_MAZE_CHEST, TMCRegion.DUNGEON_POW, Items.KINSTONE,
        (0x0E7A2E, None), (0x2DA5, 0x02), 0x1070),
    LocationData(
        6029429, TMCLocation.PALACE_2ND_HALF_5F_RIGHT_SIDE_CHEST, TMCRegion.DUNGEON_POW, Items.KINSTONE,
        (0x0E6D8A, None), (0x2DA2, 0x80), 0x0470),
    LocationData(
        6029430, TMCLocation.PALACE_BOSS_ITEM, TMCRegion.DUNGEON_POW, Items.HEART_CONTAINER,
        (0x0E6A23, None), (0x2DAB, 0x20), None, pools={POOL_HP}),
    LocationData(
        6029431, TMCLocation.PALACE_PRIZE, TMCRegion.DUNGEON_POW, Items.WIND_ELEMENT,
        (0x0E69E3, None), (0x2C9C, 0x40), None, pools={POOL_ELEMENT}),
    #endregion
    #region Sanctuary
    LocationData(
        6029432, TMCLocation.SANCTUARY_PEDESTAL_ITEM1, TMCRegion.SANCTUARY, Items.PROGRESSIVE_SWORD,
        (None, None), (0x2EA7, 0x80), None, pools={POOL_PED}),
    LocationData(
        6029433, TMCLocation.SANCTUARY_PEDESTAL_ITEM2, TMCRegion.SANCTUARY, Items.PROGRESSIVE_SWORD,
        (None, None), (0x2EA8, 0x01), None, pools={POOL_PED}),
    LocationData(
        6029434, TMCLocation.SANCTUARY_PEDESTAL_ITEM3, TMCRegion.SANCTUARY, Items.PROGRESSIVE_SWORD,
        (None, None), (0x2EA8, 0x02), None, pools={POOL_PED}),
    #endregion
    #region Dungeon DHC
    LocationData(
        6029435, TMCLocation.DHC_B2_KING, TMCRegion.DUNGEON_DHC, Items.RUPEES_1,
        (0x00E46A, None), (0x2DC2, 0x02), 0x3988),
    LocationData(
        6029436, TMCLocation.DHC_B1_BIG_CHEST, TMCRegion.DUNGEON_DHC, Items.DUNGEON_MAP_DHC,
        (0x0EDC12, None), (0x2DC1, 0x08), 0x3788),
    LocationData(
        6029437, TMCLocation.DHC_1F_BLADE_CHEST, TMCRegion.DUNGEON_DHC, Items.SMALL_KEY_DHC,
        (0x0ECE22, None), (0x2DC0, 0x20), 0x2788),
    LocationData(
        6029438, TMCLocation.DHC_1F_THRONE_BIG_CHEST, TMCRegion.DUNGEON_DHC, Items.DUNGEON_COMPASS_DHC,
        (0x0EC94E, None), (0x2DBF, 0x80), 0x2088),
    LocationData(
        6029439, TMCLocation.DHC_3F_NORTH_WEST_CHEST, TMCRegion.DUNGEON_DHC, Items.SMALL_KEY_DHC,
        (0x0EAE12, None), (0x2DBB, 0x40), 0x0188),
    LocationData(
        6029440, TMCLocation.DHC_3F_NORTH_EAST_CHEST, TMCRegion.DUNGEON_DHC, Items.SMALL_KEY_DHC,
        (0x0EAE6A, None), (0x2DBB, 0x80), 0x0288),
    LocationData(
        6029441, TMCLocation.DHC_3F_SOUTH_WEST_CHEST, TMCRegion.DUNGEON_DHC, Items.SMALL_KEY_DHC,
        (0x0EAEC2, None), (0x2DBC, 0x01), 0x0388),
    LocationData(
        6029442, TMCLocation.DHC_3F_SOUTH_EAST_CHEST, TMCRegion.DUNGEON_DHC, Items.SMALL_KEY_DHC,
        (0x0EAF1A, None), (0x2DBC, 0x02), 0x0488),
    LocationData(
        6029443, TMCLocation.DHC_2F_BLUE_WARP_BIG_CHEST, TMCRegion.DUNGEON_DHC, Items.BIG_KEY_DHC,
        (0x0EB556, None), (0x2DBC, 0x08), 0x0988),
    #endregion
    #region Hyrule Town
    LocationData(
        6029444, TMCLocation.TOWN_CAFE_LADY_NPC, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (0x00EDDA, None), (0x2CD6, 0x40), 0x0002),
    LocationData(
        6029445, TMCLocation.TOWN_SHOP_80_ITEM, TMCRegion.HYRULE_TOWN, Items.BIG_WALLET,
        (0xEF6720, 0xEF6724), (0x2EA7, 0x01), 0x0023, scoutable=True),
    LocationData(
        6029446, TMCLocation.TOWN_SHOP_300_ITEM, TMCRegion.HYRULE_TOWN, Items.PROGRESSIVE_BOOMERANG,
        (0xEF6728, 0xEF672C), (0x2EA7, 0x02), 0x0023, scoutable=True),
    LocationData(
        6029447, TMCLocation.TOWN_SHOP_600_ITEM, TMCRegion.HYRULE_TOWN, Items.QUIVER,
        (0xEF6730, 0xEF6734), (0x2EA7, 0x04), 0x0023, scoutable=True),
    LocationData(
        6029448, TMCLocation.TOWN_SHOP_BEHIND_COUNTER_ITEM, TMCRegion.HYRULE_TOWN, Items.DOG_FOOD,
        (0xEF6A3F, None), (0x2CE6, 0x08), 0x0023),
    LocationData(
        6029449, TMCLocation.TOWN_SHOP_ATTIC_CHEST, TMCRegion.HYRULE_TOWN, None,
        (0x0D8EE6, None), (0x2D0A, 0x80), 0x012E),
    LocationData(
        6029450, TMCLocation.TOWN_BAKERY_ATTIC_CHEST, TMCRegion.HYRULE_TOWN, Items.RUPEES_100,
        (0x0D9206, None), (0x2D13, 0x20), 0x032E),
    LocationData(
        6029451, TMCLocation.TOWN_INN_BACKDOOR_HP, TMCRegion.HYRULE_TOWN, Items.HEART_PIECE,
        (0x0D66D7, None), (0x2CF3, 0x01), 0x0A21),
    LocationData(
        6029452, TMCLocation.TOWN_INN_LEDGE_CHEST, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (0x0EE35A, None), (0x2CD5, 0x01), 0x0002),
    LocationData(
        6029453, TMCLocation.TOWN_INN_POT, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (0x0D663B, 0x0D663D), (0x2CE0, 0x80), 0x0921),
    LocationData(
        6029454, TMCLocation.TOWN_WELL_RIGHT_CHEST, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (0x0EFBDE, None), (0x2CFD, 0x01), 0x0041),
    LocationData(
        6029455, TMCLocation.TOWN_GORON_MERCHANT_1_LEFT, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (None, None), (0x2CA4, 0x04), 0x0002, pools={f"{POOL_GORON}1"}), # Goron merchant stores the individual item *positions*
    LocationData(
        6029456, TMCLocation.TOWN_GORON_MERCHANT_1_MIDDLE, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (None, None), (0x2CA4, 0x08), 0x0002, pools={f"{POOL_GORON}1"}), # inside 0x2CA4 from left-right in bits 0x04-0x10
    LocationData(
        6029457, TMCLocation.TOWN_GORON_MERCHANT_1_RIGHT, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (None, None), (0x2CA4, 0x10), 0x0002, pools={f"{POOL_GORON}1"}),
    LocationData(
        6029458, TMCLocation.TOWN_GORON_MERCHANT_2_LEFT, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (None, None), (None,   None), 0x0002, pools={f"{POOL_GORON}2"}), # There is a separate bit that stores how many times
    LocationData(
        6029459, TMCLocation.TOWN_GORON_MERCHANT_2_MIDDLE, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (None, None), (None,   None), 0x0002, pools={f"{POOL_GORON}2"}), # there's been a restock across 0x2CA3 0x40 - 0x2CA4 0x02
    LocationData(
        6029460, TMCLocation.TOWN_GORON_MERCHANT_2_RIGHT, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (None, None), (None,   None), 0x0002, pools={f"{POOL_GORON}2"}),
    LocationData(
        6029461, TMCLocation.TOWN_GORON_MERCHANT_3_LEFT, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (None, None), (None,   None), 0x0002, pools={f"{POOL_GORON}3"}),
    LocationData(
        6029462, TMCLocation.TOWN_GORON_MERCHANT_3_MIDDLE, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (None, None), (None,   None), 0x0002, pools={f"{POOL_GORON}3"}),
    LocationData(
        6029463, TMCLocation.TOWN_GORON_MERCHANT_3_RIGHT, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (None, None), (None,   None), 0x0002, pools={f"{POOL_GORON}3"}),
    LocationData(
        6029464, TMCLocation.TOWN_GORON_MERCHANT_4_LEFT, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (None, None), (None,   None), 0x0002, pools={f"{POOL_GORON}4"}),
    LocationData(
        6029465, TMCLocation.TOWN_GORON_MERCHANT_4_MIDDLE, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (None, None), (None,   None), 0x0002, pools={f"{POOL_GORON}4"}),
    LocationData(
        6029466, TMCLocation.TOWN_GORON_MERCHANT_4_RIGHT, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (None, None), (None,   None), 0x0002, pools={f"{POOL_GORON}4"}),
    LocationData(
        6029467, TMCLocation.TOWN_GORON_MERCHANT_5_LEFT, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (None, None), (None,   None), 0x0002, pools={f"{POOL_GORON}5"}),
    LocationData(
        6029468, TMCLocation.TOWN_GORON_MERCHANT_5_MIDDLE, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (None, None), (None,   None), 0x0002, pools={f"{POOL_GORON}5"}),
    LocationData(
        6029469, TMCLocation.TOWN_GORON_MERCHANT_5_RIGHT, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (None, None), (None,   None), 0x0002, pools={f"{POOL_GORON}5"}),
    LocationData(
        6029470, TMCLocation.TOWN_DOJO_NPC_1, TMCRegion.HYRULE_TOWN, Items.SPIN_ATTACK,
        (0xEF6495, None), (0x2EA5, 0x10), 0x0128, pools={POOL_SCROLL}),
    LocationData(
        6029471, TMCLocation.TOWN_DOJO_NPC_2, TMCRegion.HYRULE_TOWN, Items.ROCK_BREAKER,
        (0xEF6498, None), (0x2EA5, 0x20), 0x0128, pools={POOL_SCROLL}),
    LocationData(
        6029472, TMCLocation.TOWN_DOJO_NPC_3, TMCRegion.HYRULE_TOWN, Items.DASH_ATTACK,
        (0xEF649B, None), (0x2EA5, 0x40), 0x0128, pools={POOL_SCROLL}),
    LocationData(
        6029473, TMCLocation.TOWN_DOJO_NPC_4, TMCRegion.HYRULE_TOWN, Items.DOWNTHRUST,
        (0xEF649E, None), (0x2EA5, 0x80), 0x0128, pools={POOL_SCROLL}),
    LocationData(
        6029474, TMCLocation.TOWN_WELL_TOP_CHEST, TMCRegion.HYRULE_TOWN, Items.RUPEES_100,
        (0x0EFBBE, None), (0x2CFC, 0x40), 0x0041),
    LocationData(
        6029475, TMCLocation.TOWN_SCHOOL_ROOF_CHEST, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (0x0EE362, None), (0x2CD5, 0x02), 0x0002),
    LocationData(
        6029476, TMCLocation.TOWN_SCHOOL_PATH_FUSION_CHEST, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (0x0FE076, None), (0x2D11, 0x01), 0x0211),
    LocationData(
        6029477, TMCLocation.TOWN_SCHOOL_PATH_LEFT_CHEST, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (0x0D56A6, None), (0x2D0B, 0x80), 0x0211),
    LocationData(
        6029478, TMCLocation.TOWN_SCHOOL_PATH_MIDDLE_CHEST, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (0x0D56AE, None), (0x2D0C, 0x01), 0x0211),
    LocationData(
        6029479, TMCLocation.TOWN_SCHOOL_PATH_RIGHT_CHEST, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (0x0D56B6, None), (0x2D0C, 0x02), 0x0211),
    LocationData(
        6029480, TMCLocation.TOWN_SCHOOL_PATH_HP, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (0x0D5557, None), (0x2D0B, 0x40), 0x0211),
    LocationData(
        6029481, TMCLocation.TOWN_DIGGING_TOP_CHEST, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (0x0F3B46, None), (0x2D04, 0x04), 0x000F),
    LocationData(
        6029482, TMCLocation.TOWN_DIGGING_RIGHT_CHEST, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (0x0F3B4E, None), (0x2D04, 0x08), 0x000F),
    LocationData(
        6029483, TMCLocation.TOWN_DIGGING_LEFT_CHEST, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (0x0F3B56, None), (0x2D04, 0x10), 0x000F),
    LocationData(
        6029484, TMCLocation.TOWN_WELL_LEFT_CHEST, TMCRegion.HYRULE_TOWN, Items.RUPEES_100,
        (0x0EFBC6, None), (0x2CFC, 0x80), 0x0041),
    LocationData(
        6029485, TMCLocation.TOWN_BELL_HP, TMCRegion.HYRULE_TOWN, Items.HEART_PIECE,
        (0x05D602, 0x05D604), (0x2CD5, 0x20), 0x0002, pools={POOL_HP}),
    LocationData(
        6029486, TMCLocation.TOWN_WATERFALL_FUSION_CHEST, TMCRegion.HYRULE_TOWN, None,
        (0x0F8082, None), (0x2D1D, 0x40), 0x0B32),
    LocationData(
        6029487, TMCLocation.TOWN_CARLOV_NPC, TMCRegion.HYRULE_TOWN, Items.CARLOV_MEDAL,
        (0xEF614C, 0xEF6150), (0x2EA5, 0x02), 0x0723),
    LocationData(
        6029488, TMCLocation.TOWN_WELL_BOTTOM_CHEST, TMCRegion.HYRULE_TOWN, Items.RUPEES_100,
        (0x0EFBCE, None), (0x2CFD, 0x02), 0x0041),
    LocationData(
        6029489, TMCLocation.TOWN_CUCCOS_LV_1_NPC, TMCRegion.HYRULE_TOWN, None,
        (0x1245E8, None), (None,   None), 0x0002, pools={f"{POOL_CUCCO}1"}), # Cucco game uses an incremented number in 0x2CA5
    LocationData(
        6029490, TMCLocation.TOWN_CUCCOS_LV_2_NPC, TMCRegion.HYRULE_TOWN, None,
        (0x1245EC, None), (None,   None), 0x0002, pools={f"{POOL_CUCCO}2"}), # it takes up the space of bits between 0x08-0x80
    LocationData(
        6029491, TMCLocation.TOWN_CUCCOS_LV_3_NPC, TMCRegion.HYRULE_TOWN, None,
        (0x1245F0, None), (None,   None), 0x0002, pools={f"{POOL_CUCCO}3"}),
    LocationData(
        6029492, TMCLocation.TOWN_CUCCOS_LV_4_NPC, TMCRegion.HYRULE_TOWN, None,
        (0x1245F4, None), (None,   None), 0x0002, pools={f"{POOL_CUCCO}4"}),
    LocationData(
        6029493, TMCLocation.TOWN_CUCCOS_LV_5_NPC, TMCRegion.HYRULE_TOWN, None,
        (0x1245F8, None), (None,   None), 0x0002, pools={f"{POOL_CUCCO}5"}),
    LocationData(
        6029494, TMCLocation.TOWN_CUCCOS_LV_6_NPC, TMCRegion.HYRULE_TOWN, None,
        (0x1245FC, None), (None,   None), 0x0002, pools={f"{POOL_CUCCO}6"}),
    LocationData(
        6029495, TMCLocation.TOWN_CUCCOS_LV_7_NPC, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (0x124600, None), (None,   None), 0x0002, pools={f"{POOL_CUCCO}7"}),
    LocationData(
        6029496, TMCLocation.TOWN_CUCCOS_LV_8_NPC, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (0x124604, None), (None,   None), 0x0002, pools={f"{POOL_CUCCO}8"}),
    LocationData(
        6029497, TMCLocation.TOWN_CUCCOS_LV_9_NPC, TMCRegion.HYRULE_TOWN, Items.KINSTONE,
        (0x124608, None), (None,   None), 0x0002, pools={f"{POOL_CUCCO}9"}),
    LocationData(
        6029498, TMCLocation.TOWN_CUCCOS_LV_10_NPC, TMCRegion.HYRULE_TOWN, Items.HEART_PIECE,
        (0x12460C, None), (0x2CA5, 0x80), 0x0002, pools={f"{POOL_CUCCO}10"}),
    LocationData(
        6029499, TMCLocation.TOWN_JULLIETA_ITEM, TMCRegion.HYRULE_TOWN, Items.RED_BOOK,
        (0x0F1BF7, None), (0x2EA4, 0x10), 0x0722, scoutable=True),
    LocationData(
        6029500, TMCLocation.TOWN_SIMULATION_CHEST, TMCRegion.HYRULE_TOWN, Items.HEART_PIECE,
        (0x0F04C2, None), (0x2C9C, 0x02), 0x0044),
    LocationData(
        6029501, TMCLocation.TOWN_SHOE_SHOP_NPC, TMCRegion.HYRULE_TOWN, Items.PEGASUS_BOOTS,
        (0x0130EE, None), (0x2EA4, 0x08), 0x0223),
    LocationData(
        6029502, TMCLocation.TOWN_MUSIC_HOUSE_LEFT_CHEST, TMCRegion.HYRULE_TOWN, Items.RUPEES_200,
        (0x0F5496, None), (0x2CF2, 0x20), 0x0523),
    LocationData(
        6029503, TMCLocation.TOWN_MUSIC_HOUSE_MIDDLE_CHEST, TMCRegion.HYRULE_TOWN, Items.RUPEES_200,
        (0x0F549E, None), (0x2CF2, 0x40), 0x0523),
    LocationData(
        6029504, TMCLocation.TOWN_MUSIC_HOUSE_RIGHT_CHEST, TMCRegion.HYRULE_TOWN, Items.RUPEES_200,
        (0x0F54A6, None), (0x2CF2, 0x80), 0x0523),
    LocationData(
        6029505, TMCLocation.TOWN_MUSIC_HOUSE_HP, TMCRegion.HYRULE_TOWN, Items.HEART_PIECE,
        (0x0F5407, None), (0x2CF2, 0x10), 0x0523),
    LocationData(
        6029506, TMCLocation.TOWN_WELL_PILLAR_CHEST, TMCRegion.HYRULE_TOWN, Items.RUPEES_200,
        (0x0EFBD6, None), (0x2CFD, 0x04), 0x0041),
    LocationData(
        6029507, TMCLocation.TOWN_DR_LEFT_ATTIC_ITEM, TMCRegion.HYRULE_TOWN, Items.GREEN_BOOK,
        (0x0F17CB, None), (0x2EA4, 0x20), 0x022E),
    LocationData(
        6029508, TMCLocation.TOWN_FOUNTAIN_BIG_CHEST, TMCRegion.HYRULE_TOWN, Items.POWER_BRACELETS,
        (0x0EF686, None), (0x2CFD, 0x80), 0x0362),
    LocationData(
        6029509, TMCLocation.TOWN_FOUNTAIN_SMALL_CHEST, TMCRegion.HYRULE_TOWN, Items.RUPEES_100,
        (0x0EF72A, None), (0x2CFE, 0x01), 0x0462),
    LocationData(
        6029510, TMCLocation.TOWN_FOUNTAIN_HP, TMCRegion.HYRULE_TOWN, Items.HEART_PIECE,
        (0x0EF3B7, None), (0x2D14, 0x08), 0x0062, pools={POOL_HP}),
    LocationData(
        6029511, TMCLocation.TOWN_LIBRARY_YELLOW_MINISH_NPC, TMCRegion.HYRULE_TOWN, Items.RUPEES_50,
        (0x00E7BE, None), (0x2CEB, 0x01), 0x102D),
    LocationData(
        6029512, TMCLocation.TOWN_UNDER_LIBRARY_FROZEN_CHEST, TMCRegion.HYRULE_TOWN, None,
        (0x0EF8B6, None), (0x2CFE, 0x20), 0x1262),
    LocationData(
        6029513, TMCLocation.TOWN_UNDER_LIBRARY_BIG_CHEST, TMCRegion.HYRULE_TOWN, Items.FLIPPERS,
        (0x0EF7CA, None), (0x2CFE, 0x10), 0x1062),
    LocationData(
        6029514, TMCLocation.TOWN_UNDER_LIBRARY_UNDERWATER, TMCRegion.HYRULE_TOWN, Items.RUPEES_50,
        (0x0EF79B, None), (0x2CFE, 0x08), 0x1062),
    #endregion
    #region North Fields
    LocationData(
        6029515, TMCLocation.NORTH_FIELD_DIG_SPOT, TMCRegion.NORTH_FIELD, Items.RUPEES_50,
        (0x0F720F, None), (0x2CCD, 0x20), 0x0603, pools={POOL_DIG}),
    LocationData(
        6029516, TMCLocation.NORTH_FIELD_HP, TMCRegion.NORTH_FIELD, Items.HEART_PIECE,
        (0x0F864B, None), (0x2D2B, 0x08), 0x1532, pools={POOL_HP}),
    LocationData(
        6029517, TMCLocation.NORTH_FIELD_TREE_FUSION_TOP_LEFT_CHEST, TMCRegion.NORTH_FIELD, Items.KINSTONE,
        (0x0F7BE6, None), (0x2D1C, 0x10), 0x0032),
    LocationData(
        6029518, TMCLocation.NORTH_FIELD_TREE_FUSION_TOP_RIGHT_CHEST, TMCRegion.NORTH_FIELD, Items.KINSTONE,
        (0x0F7BEE, None), (0x2D1C, 0x20), 0x0032),
    LocationData(
        6029519, TMCLocation.NORTH_FIELD_TREE_FUSION_BOTTOM_LEFT_CHEST, TMCRegion.NORTH_FIELD, Items.KINSTONE,
        (0x0F7BF6, None), (0x2D1C, 0x40), 0x0032),
    LocationData(
        6029520, TMCLocation.NORTH_FIELD_TREE_FUSION_BOTTOM_RIGHT_CHEST, TMCRegion.NORTH_FIELD, None,
        (0x0F7BFE, None), (0x2D1C, 0x80), 0x0032),
    LocationData(
        6029521, TMCLocation.NORTH_FIELD_TREE_FUSION_CENTER_BIG_CHEST, TMCRegion.NORTH_FIELD, Items.PROGRESSIVE_BOOMERANG,
        (0x0F7C06, None), (0x2D1D, 0x01), 0x0032),
    LocationData(
        6029522, TMCLocation.NORTH_FIELD_WATERFALL_FUSION_DOJO_NPC, TMCRegion.NORTH_FIELD, Items.LONG_SPIN,
        (0xEF64B3, None), (0x2EA6, 0x40), 0x0225, pools={POOL_SCROLL}),
    #endregion
]

events: typing.Dict[str, typing.Tuple[int, int]] = {
    (0x2B44, 0x01): "scroll_spin",
    (0x2B4E, 0x40): "scroll_fast_spin",
    (0x2B4F, 0x01): "scroll_fast_split",
    (0x2B45, 0x04): "scroll_great_spin",
    (0x2B4F, 0x04): "scroll_long_spin",
    (0x2C9C, 0x04): "dungeon_dws",
    (0x2C9C, 0x08): "dungeon_cof",
    (0x2D72, 0x02): "dungeon_fow",
    (0x2C9C, 0x20): "dungeon_tod",
    (0x2C9C, 0x40): "dungeon_pow",
    (0x2D02, 0x04): "dungeon_rc",
}

location_table_by_name: typing.Dict[str, LocationData] = {location.name: location for location in all_locations}
