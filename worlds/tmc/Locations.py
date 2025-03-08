import typing

from BaseClasses import Location
from .Constants.LocationName import TMCLocation
from . import Items


BASE_LOCATION_ID = 6_029_000

LOC_TYPE_CHEST = 0
LOC_TYPE_GROUND = 1
LOC_TYPE_GIFT = 2

class LocationData(typing.NamedTuple):
    id: int
    name: str
    """The item id of what is normally given in this location"""
    vanillaItem: int
    """The address in the rom for placing items"""
    romLoc: int
    """1st = The address in EWRAM to read/write to, 2nd = The bit mask for the address"""
    locCode: typing.Tuple[int,int]
    """
    The area (1st byte) and room (2nd byte) the check is found in. Intended to help filter the number of locations
    iterated per game watcher loop. Also helps keep track of whether items in the area need to be location scouted.
    """
    roomArea: int
    """0 = Chest, 1 = Ground Item. Intended to be used for location scouts."""
    locType: int
    romSubLoc: int = None

class MinishCapLocation(Location):
    game: str = "The Minish Cap"


south_field: typing.List[LocationData] = [
    LocationData(6029000, TMCLocation.SMITH_HOUSE_RUPEE,                     Items.RUPEES_20,     0x0F25AA, (0x2CDE, 0x40), 0x1122, LOC_TYPE_CHEST),
    LocationData(6029001, TMCLocation.SMITH_HOUSE_SWORD,                     Items.SMITHS_SWORD,  0x0F252B, (0x2CF5, 0x01), 0x1122, LOC_TYPE_GROUND), # New location from base patch after intro skip
    LocationData(6029002, TMCLocation.SMITH_HOUSE_SHIELD,                    Items.SHIELD,        0x0F253B, (0x2CF5, 0x02), 0x1122, LOC_TYPE_GROUND), # New location from base patch after intro skip
    LocationData(6029003, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM1,       Items.RUPEES_5,      0x0F8283, (0x2D1E, 0x20), 0x1032, LOC_TYPE_GROUND),
    LocationData(6029004, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM2,       Items.RUPEES_5,      0x0F8293, (0x2D1E, 0x40), 0x1032, LOC_TYPE_GROUND),
    LocationData(6029005, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM3,       Items.RUPEES_5,      0x0F82A3, (0x2D1E, 0x80), 0x1032, LOC_TYPE_GROUND),
    LocationData(6029006, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM4,       Items.RUPEES_5,      0x0F82B3, (0x2D1F, 0x01), 0x1032, LOC_TYPE_GROUND),
    LocationData(6029007, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM5,       Items.RUPEES_5,      0x0F82C3, (0x2D1F, 0x02), 0x1032, LOC_TYPE_GROUND),
    LocationData(6029008, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM6,       Items.RUPEES_5,      0x0F82D3, (0x2D1F, 0x04), 0x1032, LOC_TYPE_GROUND),
    LocationData(6029009, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM7,       Items.RUPEES_5,      0x0F82E3, (0x2D1F, 0x08), 0x1032, LOC_TYPE_GROUND),
    LocationData(6029010, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM8,       Items.RUPEES_5,      0x0F82F3, (0x2D1F, 0x10), 0x1032, LOC_TYPE_GROUND),
    LocationData(6029011, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM9,       Items.RUPEES_5,      0x0F8303, (0x2D1F, 0x20), 0x1032, LOC_TYPE_GROUND),
    LocationData(6029012, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM10,      Items.RUPEES_5,      0x0F8313, (0x2D1F, 0x40), 0x1032, LOC_TYPE_GROUND),
    LocationData(6029013, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM11,      Items.RUPEES_5,      0x0F8323, (0x2D1F, 0x80), 0x1032, LOC_TYPE_GROUND),
    LocationData(6029014, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM12,      Items.RUPEES_5,      0x0F8333, (0x2D20, 0x01), 0x1032, LOC_TYPE_GROUND),
    LocationData(6029015, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM13,      Items.RUPEES_5,      0x0F8343, (0x2D20, 0x02), 0x1032, LOC_TYPE_GROUND),
    LocationData(6029016, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM14,      Items.RUPEES_5,      0x0F8353, (0x2D20, 0x04), 0x1032, LOC_TYPE_GROUND),
    LocationData(6029017, TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM15,      Items.RUPEES_5,      0x0F8363, (0x2D20, 0x08), 0x1032, LOC_TYPE_GROUND),
    LocationData(6029018, TMCLocation.SOUTH_FIELD_FUSION_CHEST,              None,                0x0FE0D6, (0x2CD3, 0x02), 0x0103, LOC_TYPE_CHEST),
    LocationData(6029019, TMCLocation.SOUTH_FIELD_TREE_FUSION_HP,            Items.HEART_PIECE,   0x0F9BA7, (0x2CEE, 0x80), 0x1224, LOC_TYPE_GROUND),
    LocationData(6029020, TMCLocation.SOUTH_FIELD_MINISH_SIZE_WATER_HOLE_HP, Items.HEART_PIECE,   0x0DB55F, (0x2D2C, 0x02), 0x0435, LOC_TYPE_GROUND),
    LocationData(6029021, TMCLocation.SOUTH_FIELD_TINGLE_NPC,                Items.TINGLE_TROPHY, 0x016966, (0x2CA3, 0x04), 0x0103, LOC_TYPE_GIFT),
]

castle_exterior: typing.List[LocationData] = [
    LocationData(6029022, TMCLocation.CASTLE_MOAT_LEFT_CHEST,                         None,              None,     (0x2CBE, 0x04), 0x0070, None),
    LocationData(6029023, TMCLocation.CASTLE_MOAT_RIGHT_CHEST,                        Items.RUPEES_200,  None,     (0x2CBE, 0x08), 0x0070, None),
    LocationData(6029024, TMCLocation.CASTLE_GOLDEN_ROPE,                             Items.RUPEES_100,  None,     (0x2CA2, 0x20), 0x0070, None),
    LocationData(6029025, TMCLocation.CASTLE_RIGHT_FOUNTAIN_FUSION_HP,                Items.HEART_PIECE, 0x0D9C2B, (0x2D0E, 0x10), None,   None),
    LocationData(6029026, TMCLocation.CASTLE_DOJO_HP,                                 Items.HEART_PIECE, 0x0D79BB, (0x2D2C, 0x08), None,   None),
    LocationData(6029027, TMCLocation.CASTLE_DOJO_NPC,                                Items.SWORD_BEAM,  None,     (0x2EA6, 0x02), None,   None),
    LocationData(6029028, TMCLocation.CASTLE_RIGHT_FOUNTAIN_FUSION_MINISH_HOLE_CHEST, None,              None,     (0x2D28, 0x10), 0x0036, None),
    LocationData(6029029, TMCLocation.CASTLE_LEFT_FOUNTAIN_FUSION_MINISH_HOLE_CHEST,  None,              None,     (0x2D28, 0x20), 0x0136, None),
]

eastern_hills: typing.List[LocationData] = [
    LocationData(6029030, TMCLocation.HILLS_GOLDEN_ROPE,                  Items.RUPEES_100,   None,     (0x2CA2, 0x10), None,   None),
    LocationData(6029031, TMCLocation.HILLS_FUSION_CHEST,                 Items.EMPTY_BOTTLE, 0x0FE05E, (0x2CD2, 0x04), None,   None),
    LocationData(6029032, TMCLocation.HILLS_BEANSTALK_FUSION_LEFT_CHEST,  None,               None,     (0x2D0D, 0x02), 0x030D, None),
    LocationData(6029033, TMCLocation.HILLS_BEANSTALK_FUSION_HP,          Items.HEART_PIECE,  0x0F6073, (0x2D0D, 0x01), None,   None),
    LocationData(6029034, TMCLocation.HILLS_BEANSTALK_FUSION_RIGHT_CHEST, Items.RUPEES_200,   None,     (0x2D0D, 0x04), 0x030D, None),
    LocationData(6029035, TMCLocation.HILLS_BOMB_CAVE_CHEST,              None,               None,     (0x2D22, 0x08), 0x1332, None),
    LocationData(6029036, TMCLocation.MINISH_GREAT_FAIRY_NPC,             Items.BIG_WALLET,   0x00B7B4, (0x2CEF, 0x80), None,   None), # Technically Minish Woods but the only access is through Eastern Hills
    LocationData(6029037, TMCLocation.HILLS_FARM_DIG_CAVE_ITEM,           Items.RUPEES_20,    0x0F3C9F, (0x2CD2, 0x04), None,   None),
]

lonlon: typing.List[LocationData] = [
    LocationData(6029038, TMCLocation.LON_LON_RANCH_POT,                     Items.LONLON_KEY,   0x0F2C9B, (0x2CE5, 0x20), None,   None, 0x0F2C9D),
    LocationData(6029039, TMCLocation.LON_LON_PUDDLE_FUSION_BIG_CHEST,       Items.BIG_WALLET,   None,     (0x2D1E, 0x10), 0x0F32, None),
    LocationData(6029040, TMCLocation.LON_LON_CAVE_CHEST,                    Items.RUPEES_50,    None,     (0x2D1D, 0x80), 0x0C32, None),
    LocationData(6029041, TMCLocation.LON_LON_CAVE_SECRET_CHEST,             Items.KINSTONE,     None,     (0x2D1E, 0x04), 0x0D32, None),
    LocationData(6029042, TMCLocation.LON_LON_PATH_FUSION_CHEST,             Items.KINSTONE,     0x0FE086, (0x2D11, 0x02), None,   None),
    LocationData(6029043, TMCLocation.LON_LON_PATH_HP,                       Items.HEART_PIECE,  0x0D56EF, (0x2D13, 0x04), None,   None),
    LocationData(6029044, TMCLocation.LON_LON_DIG_SPOT,                      Items.RUPEES_50,    0x0F6CFF, (0x2CCB, 0x20), None,   None),
    LocationData(6029045, TMCLocation.LON_LON_NORTH_MINISH_CRACK_CHEST,      Items.KINSTONE,     None,     (0x2CF2, 0x04), 0x0027, None),
    LocationData(6029046, TMCLocation.LON_LON_GORON_CAVE_FUSION_SMALL_CHEST, Items.RUPEES_200,   None,     (0x2D2A, 0x80), 0x012F, None),
    LocationData(6029047, TMCLocation.LON_LON_GORON_CAVE_FUSION_BIG_CHEST,   Items.EMPTY_BOTTLE, None,     (0x2D2A, 0x40), 0x012F, None),
]

lower_falls: typing.List[LocationData] = [
    LocationData(6029048, TMCLocation.FALLS_LOWER_LON_LON_FUSION_CHEST,      Items.RUPEES_200,        0x0FE0FE, (0x2CD3, 0x40), None,   None),
    LocationData(6029049, TMCLocation.FALLS_LOWER_HP,                        Items.HEART_PIECE,       0x0F87D3, (0x2CD1, 0x02), None,   None),
    LocationData(6029050, TMCLocation.FALLS_LOWER_WATERFALL_FUSION_DOJO_NPC, Items.FAST_SPLIT_SCROLL, None,     (0x2EA6, 0x20), None,   None),
    LocationData(6029051, TMCLocation.FALLS_LOWER_ROCK_ITEM1,                Items.RUPEES_20,         0x0F87E3, (0x2CD0, 0x04), None,   None),
    LocationData(6029052, TMCLocation.FALLS_LOWER_ROCK_ITEM2,                Items.RUPEES_20,         0x0F87F3, (0x2CD0, 0x08), None,   None),
    LocationData(6029053, TMCLocation.FALLS_LOWER_ROCK_ITEM3,                Items.RUPEES_20,         0x0F8803, (0x2CD0, 0x10), None,   None),
    LocationData(6029054, TMCLocation.FALLS_LOWER_DIG_CAVE_LEFT_CHEST,       None,                    None,     (0x2D05, 0x08), 0x0016, None),
    LocationData(6029055, TMCLocation.FALLS_LOWER_DIG_CAVE_RIGHT_CHEST,      Items.RUPEES_50,         None,     (0x2D05, 0x10), 0x0016, None),
]

lake_hylia: typing.List[LocationData] = [
    LocationData(6029056, TMCLocation.HYLIA_SUNKEN_HP,                           Items.HEART_PIECE,     0x0F323B, (0x2CBD, 0x02), None,   None),
    LocationData(6029057, TMCLocation.HYLIA_DOG_NPC,                             Items.EMPTY_BOTTLE,    0x094908, (0x2B3F, 0x20), None,   None, 0x09490A),
    LocationData(6029058, TMCLocation.HYLIA_SMALL_ISLAND_HP,                     Items.HEART_PIECE,     0x0F322B, (0x2CBD, 0x04), None,   None),
    LocationData(6029059, TMCLocation.HYLIA_CAPE_CAVE_TOP_RIGHT,                 None,                  None,     (0x2D02, 0x80), 0x0119, None),
    LocationData(6029060, TMCLocation.HYLIA_CAPE_CAVE_BOTTOM_LEFT,               None,                  None,     (0x2D03, 0x02), 0x0119, None),
    LocationData(6029061, TMCLocation.HYLIA_CAPE_CAVE_TOP_LEFT,                  Items.KINSTONE,        None,     (0x2D03, 0x04), 0x0119, None),
    LocationData(6029062, TMCLocation.HYLIA_CAPE_CAVE_TOP_MIDDLE,                Items.KINSTONE,        None,     (0x2D03, 0x08), 0x0119, None),
    LocationData(6029063, TMCLocation.HYLIA_CAPE_CAVE_RIGHT,                     Items.KINSTONE,        None,     (0x2D03, 0x10), 0x0119, None),
    LocationData(6029064, TMCLocation.HYLIA_CAPE_CAVE_BOTTOM_RIGHT,              Items.KINSTONE,        None,     (0x2D03, 0x20), 0x0119, None),
    LocationData(6029065, TMCLocation.HYLIA_CAPE_CAVE_BOTTOM_MIDDLE,             Items.KINSTONE,        None,     (0x2D03, 0x40), 0x0119, None),
    LocationData(6029066, TMCLocation.HYLIA_CAPE_CAVE_LON_LON_HP,                Items.HEART_PIECE,     0x0F6CEF, (0x2CCB, 0x10), None,   None),
    LocationData(6029067, TMCLocation.HYLIA_BEANSTALK_FUSION_LEFT_CHEST,         Items.RUPEES_200,      None,     (0x2D0C, 0x20), 0x010D, None),
    LocationData(6029068, TMCLocation.HYLIA_BEANSTALK_FUSION_HP,                 Items.HEART_PIECE,     0x0F5EDB, (0x2D0C, 0x10), None,   None),
    LocationData(6029069, TMCLocation.HYLIA_BEANSTALK_FUSION_RIGHT_CHEST,        None,                  None,     (0x2D0C, 0x40), 0x010D, None),
    LocationData(6029070, TMCLocation.HYLIA_MIDDLE_ISLAND_FUSION_DIG_CAVE_CHEST, Items.RUPEES_50,       None,     (0x2D02, 0x40), 0x0019, None),
    LocationData(6029071, TMCLocation.HYLIA_BOTTOM_HP,                           Items.HEART_PIECE,     0x0F324B, (0x2CBD, 0x02), None,   None),
    LocationData(6029072, TMCLocation.HYLIA_DOJO_HP,                             Items.HEART_PIECE,     0x0D7B03, (0x2D2C, 0x04), None,   None),
    LocationData(6029073, TMCLocation.HYLIA_DOJO_NPC,                            Items.PERIL_BEAM,      None,     (0x2EA6, 0x04), None,   None),
    LocationData(6029074, TMCLocation.HYLIA_CRACK_FUSION_LIBRARI_NPC,            Items.HEART_CONTAINER, 0x0124EC, (0x2CF2, 0x08), None,   None),
    LocationData(6029075, TMCLocation.HYLIA_NORTH_MINISH_HOLE_CHEST,             Items.KINSTONE,        None,     (0x2D2A, 0x04), 0x0735, None),
    LocationData(6029076, TMCLocation.HYLIA_SOUTH_MINISH_HOLE_CHEST,             Items.KINSTONE,        None,     (0x2D28, 0x04), 0x0535, None),
    LocationData(6029077, TMCLocation.HYLIA_CABIN_PATH_FUSION_CHEST,             Items.KINSTONE,        0x0FE09E, (0x2D11, 0x10), None,   None),
    LocationData(6029078, TMCLocation.HYLIA_MAYOR_CABIN_ITEM,                    Items.BLUE_BOOK,       None,     (0x2EA4, 0x40), None,   None),
]

minish_woods: typing.List[LocationData] = [
    LocationData(6029079, TMCLocation.MINISH_WOODS_GOLDEN_OCTO,                        Items.RUPEES_100,      None,     (0x2CA3, 0x01), None,   None),
    LocationData(6029080, TMCLocation.MINISH_WOODS_WITCH_HUT_ITEM,                     Items.WAKEUP_MUSHROOM, 0x0F94D7, (0x2EA4, 0x04), None,   None),
    LocationData(6029081, TMCLocation.WITCH_DIGGING_CAVE_CHEST,                        Items.KINSTONE,        None,     (0x2D02, 0x08), 0x000C, None),
    LocationData(6029082, TMCLocation.MINISH_WOODS_NORTH_FUSION_CHEST,                 Items.KINSTONE,        0x0FE07E, (0x2CD2, 0x08), None,   None),
    LocationData(6029083, TMCLocation.MINISH_WOODS_TOP_HP,                             Items.HEART_PIECE,     0x0F4347, (0x2CC3, 0x08), None,   None),
    LocationData(6029084, TMCLocation.MINISH_WOODS_WEST_FUSION_CHEST,                  Items.RUPEES_200,      0x0FE0CE, (0x2CD3, 0x01), 0x0000, None),
    LocationData(6029085, TMCLocation.MINISH_WOODS_LIKE_LIKE_DIGGING_CAVE_LEFT_CHEST,  Items.RUPEES_50,       None,     (0x2D02, 0x10), 0x000C, None),
    LocationData(6029086, TMCLocation.MINISH_WOODS_LIKE_LIKE_DIGGING_CAVE_RIGHT_CHEST, Items.KINSTONE,        None,     (0x2D02, 0x20), 0x000C, None),
    LocationData(6029087, TMCLocation.MINISH_WOODS_EAST_FUSION_CHEST,                  Items.KINSTONE,        0x0FE0B6, (0x2CD2, 0x20), None,   None),
    LocationData(6029088, TMCLocation.MINISH_WOODS_SOUTH_FUSION_CHEST,                 Items.KINSTONE,        0x0FE0C6, (0x2CD2, 0x80), None,   None),
    LocationData(6029089, TMCLocation.MINISH_WOODS_BOTTOM_HP,                          Items.HEART_PIECE,     0x0F4357, (0x2CC3, 0x10), None,   None),
    LocationData(6029090, TMCLocation.MINISH_WOODS_CRACK_FUSION_CHEST,                 Items.KINSTONE,        None,     (0x2CF0, 0x08), 0x0827, None),
    LocationData(6029091, TMCLocation.MINISH_WOODS_MINISH_PATH_FUSION_CHEST,           Items.RUPEES_200,      0x0FE08E, (0x2D11, 0x04), None,   None),
    LocationData(6029092, TMCLocation.MINISH_VILLAGE_BARREL_HOUSE_ITEM,                Items.JABBER_NUT,      0x0DA283, (0x2CF5, 0x04), None,   None),
    LocationData(6029093, TMCLocation.MINISH_VILLAGE_HP,                               Items.HEART_PIECE,     0x0DBCC7, (0x2CF4, 0x04), None,   None),
    LocationData(6029094, TMCLocation.MINISH_WOODS_BOMB_MINISH_NPC_1,                  Items.BOMB_BAG,        0x00A00C, (0x2EA5, 0x01), None,   None),
    LocationData(6029095, TMCLocation.MINISH_WOODS_BOMB_MINISH_NPC_2,                  Items.REMOTE_BOMB,     0x00A0A0, (0x2CF2, 0x01), None,   None),
    LocationData(6029096, TMCLocation.MINISH_WOODS_POST_VILLAGE_FUSION_CHEST,          Items.KINSTONE,        0x0FE0A6, (0x2CDB, 0x08), None,   None),
    LocationData(6029097, TMCLocation.MINISH_WOODS_FLIPPER_HOLE_MIDDLE_CHEST,          Items.KINSTONE,        None,     (0x2D2A, 0x08), 0x0935, None),
    LocationData(6029098, TMCLocation.MINISH_WOODS_FLIPPER_HOLE_RIGHT_CHEST,           Items.KINSTONE,        None,     (0x2D2A, 0x10), 0x0935, None),
    LocationData(6029099, TMCLocation.MINISH_WOODS_FLIPPER_HOLE_LEFT_CHEST,            Items.KINSTONE,        None,     (0x2D2A, 0x20), 0x0935, None),
    LocationData(6029100, TMCLocation.MINISH_WOODS_FLIPPER_HOLE_HP,                    Items.HEART_PIECE,     0x0DB8BF, (0x2D2B, 0x04), None,   None),
]

trilby_highlands: typing.List[LocationData] = [
    LocationData(6029101, TMCLocation.TRILBY_MIDDLE_FUSION_CHEST,         Items.KINSTONE,     0x0FE0EE, (0x2CD3, 0x10), None,   None),
    LocationData(6029102, TMCLocation.TRILBY_TOP_FUSION_CHEST,            Items.KINSTONE,     0x0FE0BE, (0x2CD2, 0x40), None,   None),
    LocationData(6029103, TMCLocation.TRILBY_DIG_CAVE_LEFT_CHEST,         Items.KINSTONE,     None,     (0x2D04, 0x80), 0x0313, None),
    LocationData(6029104, TMCLocation.TRILBY_DIG_CAVE_RIGHT_CHEST,        Items.KINSTONE,     None,     (0x2D05, 0x02), 0x0313, None),
    LocationData(6029105, TMCLocation.TRILBY_DIG_CAVE_WATER_FUSION_CHEST, Items.KINSTONE,     None,     (0x2D05, 0x01), 0x0313, None),
    LocationData(6029106, TMCLocation.TRILBY_SCRUB_NPC,                   Items.EMPTY_BOTTLE, None,     (0x2CA7, 0x04), None,   None),
    LocationData(6029107, TMCLocation.TRILBY_BOMB_CAVE_CHEST,             Items.KINSTONE,     None,     (0x2D1D, 0x20), 0x0732, None),
    LocationData(6029108, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM1,         Items.RUPEES_5,     0x0F83BB, (0x2D20, 0x10), None,   None),
    LocationData(6029109, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM2,         Items.RUPEES_5,     0x0F83CB, (0x2D20, 0x20), None,   None),
    LocationData(6029110, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM3,         Items.RUPEES_5,     0x0F83DB, (0x2D20, 0x40), None,   None),
    LocationData(6029111, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM4,         Items.RUPEES_5,     0x0F83EB, (0x2D20, 0x80), None,   None),
    LocationData(6029112, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM5,         Items.RUPEES_5,     0x0F83FB, (0x2D21, 0x01), None,   None),
    LocationData(6029113, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM6,         Items.RUPEES_5,     0x0F840B, (0x2D21, 0x02), None,   None),
    LocationData(6029114, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM7,         Items.RUPEES_5,     0x0F841B, (0x2D21, 0x04), None,   None),
    LocationData(6029115, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM8,         Items.RUPEES_5,     0x0F842B, (0x2D21, 0x08), None,   None),
    LocationData(6029116, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM9,         Items.RUPEES_5,     0x0F843B, (0x2D21, 0x10), None,   None),
    LocationData(6029117, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM10,        Items.RUPEES_5,     0x0F844B, (0x2D21, 0x20), None,   None),
    LocationData(6029118, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM11,        Items.RUPEES_5,     0x0F845B, (0x2D21, 0x40), None,   None),
    LocationData(6029119, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM12,        Items.RUPEES_5,     0x0F846B, (0x2D21, 0x80), None,   None),
    LocationData(6029120, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM13,        Items.RUPEES_5,     0x0F847B, (0x2D22, 0x01), None,   None),
    LocationData(6029121, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM14,        Items.RUPEES_5,     0x0F848B, (0x2D22, 0x02), None,   None),
    LocationData(6029122, TMCLocation.TRILBY_PUDDLE_FUSION_ITEM15,        Items.RUPEES_5,     0x0F849B, (0x2D22, 0x04), None,   None),
]

western_woods: typing.List[LocationData] = [
    LocationData(6029123, TMCLocation.WESTERN_WOODS_FUSION_CHEST,            None,              None,     (0x2CCF, 0x10), 0x0803, None),
    LocationData(6029124, TMCLocation.WESTERN_WOODS_TREE_FUSION_HP,          Items.HEART_PIECE, 0x0F9E1F, (0x2CEF, 0x01), None,   None),
    LocationData(6029125, TMCLocation.WESTERN_WOODS_TOP_DIG1,                Items.RUPEES_50,   0x0F77CF, (0x2CCE, 0x08), None,   None),
    LocationData(6029126, TMCLocation.WESTERN_WOODS_TOP_DIG2,                Items.RUPEES_50,   0x0F77DF, (0x2CCE, 0x10), None,   None),
    LocationData(6029127, TMCLocation.WESTERN_WOODS_TOP_DIG3,                Items.RUPEES_50,   0x0F77EF, (0x2CCE, 0x20), None,   None),
    LocationData(6029128, TMCLocation.WESTERN_WOODS_TOP_DIG4,                Items.RUPEES_50,   0x0F77FF, (0x2CCE, 0x40), None,   None),
    LocationData(6029129, TMCLocation.WESTERN_WOODS_TOP_DIG5,                Items.RUPEES_50,   0x0F780F, (0x2CCE, 0x80), None,   None),
    LocationData(6029130, TMCLocation.WESTERN_WOODS_TOP_DIG6,                Items.RUPEES_50,   0x0F781F, (0x2CCF, 0x01), None,   None),
    LocationData(6029131, TMCLocation.WESTERN_WOODS_PERCY_FUSION_MOBLIN,     Items.RUPEES_50,   0x0123D6, (0x2CE4, 0x04), None,   None),
    LocationData(6029132, TMCLocation.WESTERN_WOODS_PERCY_FUSION_PERCY,      None,              0x06B058, (0x2CE3, 0x80), None,   None, 0x06B05A),
    LocationData(6029133, TMCLocation.WESTERN_WOODS_BOTTOM_DIG1,             Items.RUPEES_200,  0x0F782F, (0x2CCF, 0x02), None,   None),
    LocationData(6029134, TMCLocation.WESTERN_WOODS_BOTTOM_DIG2,             Items.RUPEES_200,  0x0F783F, (0x2CCF, 0x04), None,   None),
    LocationData(6029135, TMCLocation.WESTERN_WOODS_GOLDEN_OCTO,             Items.RUPEES_100,  None,     (0x2CA3, 0x02), None,   None),
    LocationData(6029136, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_CHEST,  Items.KINSTONE,    None,     (0x2D0D, 0x08), 0x040D, None),
    LocationData(6029137, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM1,  Items.RUPEES_20,   0x0F6143, (0x2D0D, 0x10), None,   None),
    LocationData(6029138, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM2,  Items.RUPEES_20,   0x0F6153, (0x2D0D, 0x20), None,   None),
    LocationData(6029139, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM3,  Items.RUPEES_20,   0x0F6163, (0x2D0D, 0x40), None,   None),
    LocationData(6029140, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM4,  Items.RUPEES_20,   0x0F6173, (0x2D0D, 0x80), None,   None),
    LocationData(6029141, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM5,  Items.RUPEES_20,   0x0F6183, (0x2D0E, 0x01), None,   None),
    LocationData(6029142, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM6,  Items.RUPEES_20,   0x0F6193, (0x2D0E, 0x02), None,   None),
    LocationData(6029143, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM7,  Items.RUPEES_20,   0x0F61A3, (0x2D0E, 0x04), None,   None),
    LocationData(6029144, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM8,  Items.RUPEES_20,   0x0F61B3, (0x2D0E, 0x08), None,   None),
    LocationData(6029145, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM9,  Items.RUPEES_20,   0x0F61C3, (0x2D0F, 0x40), None,   None),
    LocationData(6029146, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM10, Items.RUPEES_20,   0x0F61D3, (0x2D0F, 0x80), None,   None),
    LocationData(6029147, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM11, Items.RUPEES_20,   0x0F61E3, (0x2D10, 0x01), None,   None),
    LocationData(6029148, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM12, Items.RUPEES_20,   0x0F61F3, (0x2D10, 0x02), None,   None),
    LocationData(6029149, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM13, Items.RUPEES_20,   0x0F6203, (0x2D10, 0x04), None,   None),
    LocationData(6029150, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM14, Items.RUPEES_20,   0x0F6213, (0x2D10, 0x08), None,   None),
    LocationData(6029151, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM15, Items.RUPEES_20,   0x0F6223, (0x2D10, 0x10), None,   None),
    LocationData(6029152, TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM16, Items.RUPEES_20,   0x0F6233, (0x2D10, 0x20), None,   None),
]

crenel: typing.List[LocationData] = [
    LocationData(6029153, TMCLocation.CRENEL_BASE_ENTRANCE_VINE,             Items.RUPEES_20,         0x0FAACF, (0x2CC5, 0x02), None,   None),
    LocationData(6029154, TMCLocation.CRENEL_BASE_FAIRY_CAVE_ITEM1,          Items.RUPEES_5,          0x0FB3F3, (0x2D24, 0x08), None,   None),
    LocationData(6029155, TMCLocation.CRENEL_BASE_FAIRY_CAVE_ITEM2,          Items.RUPEES_5,          0x0FB403, (0x2D24, 0x10), None,   None),
    LocationData(6029156, TMCLocation.CRENEL_BASE_FAIRY_CAVE_ITEM3,          Items.RUPEES_5,          0x0FB413, (0x2D24, 0x20), None,   None),
    LocationData(6029157, TMCLocation.CRENEL_BASE_GREEN_WATER_FUSION_CHEST,  Items.KINSTONE,          0x0FE06E, (0x2D10, 0x80), None,   None),
    LocationData(6029158, TMCLocation.CRENEL_BASE_WEST_FUSION_CHEST,         Items.RUPEES_200,        0x0FE116, (0x2CD4, 0x02), None,   None),
    LocationData(6029159, TMCLocation.CRENEL_BASE_WATER_CAVE_LEFT_CHEST,     Items.RUPEES_50,         None,     (0x2D24, 0x02), 0x0826, None),
    LocationData(6029160, TMCLocation.CRENEL_BASE_WATER_CAVE_RIGHT_CHEST,    Items.KINSTONE,          None,     (0x2D24, 0x04), 0x0826, None),
    LocationData(6029161, TMCLocation.CRENEL_BASE_WATER_CAVE_HP,             Items.HEART_PIECE,       0x0FB32B, (0x2D24, 0x01), None,   None),
    LocationData(6029162, TMCLocation.CRENEL_BASE_MINISH_VINE_HOLE_CHEST,    Items.KINSTONE,          None,     (0x2D28, 0x01), 0x0035, None),
    LocationData(6029163, TMCLocation.CRENEL_BASE_MINISH_CRACK_CHEST,        Items.KINSTONE,          None,     (0x2CDE, 0x02), 0x0327, None),
    LocationData(6029164, TMCLocation.CRENEL_VINE_TOP_GOLDEN_TEKTITE,        Items.RUPEES_100,        None,     (0x2CA2, 0x80), None,   None),
    LocationData(6029165, TMCLocation.CRENEL_BRIDGE_CAVE_CHEST,              Items.KINSTONE,          None,     (0x2D23, 0x80), 0x0726, None),
    LocationData(6029166, TMCLocation.CRENEL_FAIRY_CAVE_HP,                  Items.HEART_PIECE,       0x0FB0BB, (0x2D2B, 0x20), None,   None),
    LocationData(6029167, TMCLocation.CRENEL_BELOW_CO_F_GOLDEN_TEKTITE,      Items.RUPEES_100,        None,     (0x2CA2, 0x04), None,   None),
    LocationData(6029168, TMCLocation.CRENEL_SCRUB_NPC,                      Items.GRIP_RING,         None,     (0x2EA5, 0x04), None,   None),
    LocationData(6029169, TMCLocation.CRENEL_DOJO_LEFT_CHEST,                Items.RUPEES_50,         None,     (0x2D1C, 0x02), 0x0025, None),
    LocationData(6029170, TMCLocation.CRENEL_DOJO_RIGHT_CHEST,               Items.RUPEES_50,         None,     (0x2D1C, 0x04), 0x0025, None),
    LocationData(6029171, TMCLocation.CRENEL_DOJO_HP,                        Items.HEART_PIECE,       0x0D752B, (0x2D2C, 0x01), None,   None),
    LocationData(6029172, TMCLocation.CRENEL_DOJO_NPC,                       Items.ROLL_ATTACK,       None,     (0x2EA6, 0x01), None,   None),
    LocationData(6029173, TMCLocation.CRENEL_GREAT_FAIRY_NPC,                Items.BOMB_BAG,          0x00B828, (0x2CF0, 0x01), None,   None),
    LocationData(6029174, TMCLocation.CRENEL_CLIMB_FUSION_CHEST,             Items.KINSTONE,          0x0FE10E, (0x2CD4, 0x01), None,   None),
    LocationData(6029175, TMCLocation.CRENEL_DIG_CAVE_HP,                    Items.HEART_PIECE,       0x0F3BA7, (0x2D04, 0x20), None,   None),
    LocationData(6029176, TMCLocation.CRENEL_BEANSTALK_FUSION_HP,            Items.HEART_PIECE,       0x0F5D9B, (0x2D0C, 0x08), None,   None),
    LocationData(6029177, TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM1,         Items.RUPEES_20,         0x0F5DAB, (0x2D0E, 0x40), None,   None),
    LocationData(6029178, TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM2,         Items.RUPEES_20,         0x0F5DBB, (0x2D0E, 0x80), None,   None),
    LocationData(6029179, TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM3,         Items.RUPEES_20,         0x0F5DCB, (0x2D0F, 0x01), None,   None),
    LocationData(6029180, TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM4,         Items.RUPEES_20,         0x0F5DDB, (0x2D0F, 0x02), None,   None),
    LocationData(6029181, TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM5,         Items.RUPEES_20,         0x0F5DEB, (0x2D0F, 0x04), None,   None),
    LocationData(6029182, TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM6,         Items.RUPEES_20,         0x0F5DFB, (0x2D0F, 0x08), None,   None),
    LocationData(6029183, TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM7,         Items.RUPEES_20,         0x0F5E0B, (0x2D0F, 0x10), None,   None),
    LocationData(6029184, TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM8,         Items.RUPEES_20,         0x0F5E1B, (0x2D0F, 0x20), None,   None),
    LocationData(6029185, TMCLocation.CRENEL_RAIN_PATH_FUSION_CHEST,         Items.KINSTONE,          0x0FE066, (0x2D10, 0x40), None,   None),
    LocationData(6029186, TMCLocation.CRENEL_UPPER_BLOCK_CHEST,              Items.KINSTONE,          None,     (0x2D23, 0x20), None,   None),
    LocationData(6029187, TMCLocation.CRENEL_MINES_PATH_FUSION_CHEST,        None,                    0x0FE096, (0x2D11, 0x08), None,   None),
    LocationData(6029188, TMCLocation.CRENEL_MELARI_LOWER_MIDDLE_DIG,        Items.KINSTONE,          0x0DC8C3, (0x2CF3, 0x02), None,   None),
    LocationData(6029189, TMCLocation.CRENEL_MELARI_VERY_BOTTOM_DIG,         Items.KINSTONE,          0x0DC933, (0x2CF3, 0x04), None,   None),
    LocationData(6029190, TMCLocation.CRENEL_MELARI_UPPER_MIDDLE_LEFT_DIG,   Items.RUPEES_20,         0x0DC923, (0x2CF3, 0x08), None,   None),
    LocationData(6029191, TMCLocation.CRENEL_MELARI_UPPER_MIDDLE_MIDDLE_DIG, Items.KINSTONE,          0x0DC913, (0x2CF3, 0x10), None,   None),
    LocationData(6029192, TMCLocation.CRENEL_MELARI_UPPER_MIDDLE_RIGHT_DIG,  Items.RUPEES_20,         0x0DC903, (0x2CF3, 0x20), None,   None),
    LocationData(6029193, TMCLocation.CRENEL_MELARI_UPPER_TOP_RIGHT_DIG,     Items.RUPEES_20,         0x0DC8F3, (0x2CF3, 0x40), None,   None),
    LocationData(6029194, TMCLocation.CRENEL_MELARI_UPPER_TOP_MIDDLE_DIG,    Items.RUPEES_20,         0x0DC8D3, (0x2CF3, 0x80), None,   None),
    LocationData(6029195, TMCLocation.CRENEL_MELARI_UPPER_TOP_LEFT_DIG,      Items.KINSTONE,          0x0DC8E3, (0x2CF4, 0x01), None,   None),
    LocationData(6029196, TMCLocation.CRENEL_MELARI_NPC_COF,                 Items.WHITE_SWORD_GREEN, 0x00D26E, (0x2EA4, 0x80), None,   None), # Only attainable after COF cleared
]

swamp: typing.List[LocationData] = [
    LocationData(6029197, TMCLocation.SWAMP_BUTTERFLY_FUSION_ITEM,                Items.DIG_BUTTERFLY,       0x0FE13F, (0x2EA7, 0x10), None,   None),
    LocationData(6029198, TMCLocation.SWAMP_CENTER_CAVE_DARKNUT_CHEST,            Items.KINSTONE_GOLD_SWAMP, None,     (0x2D23, 0x04), 0x002B, None),
    LocationData(6029199, TMCLocation.SWAMP_CENTER_CHEST,                         Items.KINSTONE,            None,     (0x2CBD, 0x10), 0x0004, None),
    LocationData(6029200, TMCLocation.SWAMP_GOLDEN_ROPE,                          Items.RUPEES_100,          None,     (0x2CA2, 0x08), None,   None),
    LocationData(6029201, TMCLocation.SWAMP_NEAR_WATERFALL_CAVE_HP,               Items.HEART_PIECE,         0x0D9907, (0x2D23, 0x01), None,   None),
    LocationData(6029202, TMCLocation.SWAMP_WATERFALL_FUSION_DOJO_NPC,            Items.FAST_SPIN_SCROLL,    None,     (0x2EA6, 0x10), None,   None),
    LocationData(6029203, TMCLocation.SWAMP_NORTH_CAVE_CHEST,                     Items.KINSTONE_GOLD_SWAMP, None,     (0x2D22, 0x40), 0x012A, None),
    LocationData(6029204, TMCLocation.SWAMP_DIGGING_CAVE_LEFT_CHEST,              None,                      None,     (0x2D04, 0x01), 0x0017, None),
    LocationData(6029205, TMCLocation.SWAMP_DIGGING_CAVE_RIGHT_CHEST,             Items.KINSTONE,            None,     (0x2D04, 0x02), 0x0017, None),
    LocationData(6029206, TMCLocation.SWAMP_UNDERWATER_TOP,                       Items.KINSTONE,            0x0D9347, (0x2CC0, 0x04), None,   None),
    LocationData(6029207, TMCLocation.SWAMP_UNDERWATER_MIDDLE,                    Items.KINSTONE,            0x0D9357, (0x2CC0, 0x08), None,   None),
    LocationData(6029208, TMCLocation.SWAMP_UNDERWATER_BOTTOM,                    Items.KINSTONE,            0x0D9367, (0x2CC0, 0x10), None,   None),
    LocationData(6029209, TMCLocation.SWAMP_SOUTH_CAVE_CHEST,                     Items.KINSTONE_GOLD_SWAMP, None,     (0x2D22, 0x10), 0x002A, None),
    LocationData(6029210, TMCLocation.SWAMP_DOJO_HP,                              Items.HEART_PIECE,         0x0D78CB, (0x2D2B, 0x80), None,   None),
    LocationData(6029211, TMCLocation.SWAMP_DOJO_NPC,                             Items.GREATSPIN,           None,     (0x2EA6, 0x08), None,   None),
    LocationData(6029212, TMCLocation.SWAMP_MINISH_FUSION_NORTH_CRACK_CHEST,      Items.KINSTONE,            None,     (0x2CDE, 0x08), 0x0927, None),
    LocationData(6029213, TMCLocation.SWAMP_MINISH_MULLDOZER_BIG_CHEST,           Items.BOW,                 None,     (0x2CDE, 0x01), 0x0627, None),
    LocationData(6029214, TMCLocation.SWAMP_MINISH_FUSION_NORTH_WEST_CRACK_CHEST, Items.KINSTONE,            None,     (0x2CF0, 0x20), 0x0D27, None),
    LocationData(6029215, TMCLocation.SWAMP_MINISH_FUSION_WEST_CRACK_CHEST,       Items.KINSTONE,            None,     (0x2CDE, 0x10), 0x0A27, None),
    LocationData(6029216, TMCLocation.SWAMP_MINISH_FUSION_VINE_CRACK_CHEST,       Items.KINSTONE,            None,     (0x2CDE, 0x20), 0x0B27, None),
    LocationData(6029217, TMCLocation.SWAMP_MINISH_FUSION_WATER_HOLE_CHEST,       Items.KINSTONE,            None,     (0x2D2C, 0x20), 0x0135, None),
    LocationData(6029218, TMCLocation.SWAMP_MINISH_FUSION_WATER_HOLE_HP,          Items.HEART_PIECE,         0x0DB3F7, (0x2D2C, 0x10), None,   None),
]

ruins: typing.List[LocationData] = [
    LocationData(6029219, TMCLocation.RUINS_BUTTERFLY_FUSION_ITEM,       Items.BOW_BUTTERFLY, 0x0FE12F, (0x2EA7, 0x08), None,   None),
    LocationData(6029220, TMCLocation.RUINS_BOMB_CAVE_CHEST,             Items.KINSTONE,      None,     (0x2D22, 0x80), 0x022A, None),
    LocationData(6029221, TMCLocation.RUINS_MINISH_HOME_CHEST,           Items.KINSTONE,      None,     (0x2CDE, 0x04), 0x0727, None),
    LocationData(6029222, TMCLocation.RUINS_PILLARS_FUSION_CHEST,        None,                0x0FE11E, (0x2CD4, 0x04), None,   None),
    LocationData(6029223, TMCLocation.RUINS_BEAN_STALK_FUSION_BIG_CHEST, Items.QUIVER,        None,     (0x2D0C, 0x80), 0x020D, None),
    LocationData(6029224, TMCLocation.RUINS_CRACK_FUSION_CHEST,          Items.KINSTONE,      None,     (0x2CF0, 0x10), 0x0C27, None),
    LocationData(6029225, TMCLocation.RUINS_MINISH_CAVE_HP,              Items.HEART_PIECE,   0x0DB4BF, (0x2D2B, 0x40), None,   None),
    LocationData(6029226, TMCLocation.RUINS_ARMOS_KILL_LEFT_CHEST,       Items.RUPEES_50,     None,     (0x2CC2, 0x08), 0x0505, None),
    LocationData(6029227, TMCLocation.RUINS_ARMOS_KILL_RIGHT_CHEST,      None,                None,     (0x2CC2, 0x10), 0x0505, None),
    LocationData(6029228, TMCLocation.RUINS_GOLDEN_OCTO,                 Items.RUPEES_100,    None,     (0x2CA2, 0x02), None,   None),
    LocationData(6029229, TMCLocation.RUINS_NEAR_FOW_FUSION_CHEST,       Items.BOMB_BAG,      0x0FE0AE, (0x2CD2, 0x10), None,   None),
]

valley: typing.List[LocationData] = [
    LocationData(6029230, TMCLocation.VALLEY_PRE_VALLEY_FUSION_CHEST,            None,                 0x0FE0F6, (0x2CD3, 0x20), None,   None),
    LocationData(6029231, TMCLocation.VALLEY_GREAT_FAIRY_NPC,                    Items.QUIVER,         0x00B722, (0x2CEF, 0x40), None,   None),
    LocationData(6029232, TMCLocation.VALLEY_LOST_WOODS_CHEST,                   None,                 0x0D8A86, (0x2CC7, 0x04), None,   None),
    LocationData(6029233, TMCLocation.VALLEY_DAMPE_NPC,                          Items.GRAVEYARD_KEY,  0x0096B6, (0x2CE9, 0x02), None,   None),
    LocationData(6029234, TMCLocation.VALLEY_GRAVEYARD_BUTTERFLY_FUSION_ITEM,    Items.SWIM_BUTTERFLY, 0x0FE14F, (0x2EA7, 0x20), None,   None),
    LocationData(6029235, TMCLocation.VALLEY_GRAVEYARD_LEFT_FUSION_CHEST,        Items.KINSTONE,       0x0FE0DE, (0x2CD3, 0x04), None,   None),
    LocationData(6029236, TMCLocation.VALLEY_GRAVEYARD_LEFT_GRAVE_HP,            Items.HEART_PIECE,    0x0D8AE7, (0x2D27, 0x20), None,   None),
    LocationData(6029237, TMCLocation.VALLEY_GRAVEYARD_RIGHT_FUSION_CHEST,       Items.KINSTONE,       0x0FE0E6, (0x2CD3, 0x08), None,   None),
    LocationData(6029238, TMCLocation.VALLEY_GRAVEYARD_RIGHT_GRAVE_FUSION_CHEST, None,                 None,     (0x2D27, 0x40), 0x0134, None),
]

dungeon_crypt: typing.List[LocationData] = [
    LocationData(6029239, TMCLocation.CRYPT_GIBDO_LEFT_ITEM,  Items.BOMB_REFILL_5,       0x0E688B, (0x2D14, 0x10), None, None),
    LocationData(6029240, TMCLocation.CRYPT_GIBDO_RIGHT_ITEM, Items.SMALL_KEY_RC,        0x0E68AB, (0x2D14, 0x20), None, None),
    LocationData(6029241, TMCLocation.CRYPT_LEFT_ITEM,        Items.SMALL_KEY_RC,        0x0E6357, (0x2D12, 0x40), None, None),
    LocationData(6029242, TMCLocation.CRYPT_RIGHT_ITEM,       Items.SMALL_KEY_RC,        0x0E63A7, (0x2D12, 0x80), None, None),
    LocationData(6029243, TMCLocation.CRYPT_PRIZE,            Items.KINSTONE_GOLD_FALLS, 0x00DA5A, (0x2D02, 0x04), None, None),
]

upper_falls: typing.List[LocationData] = [
    LocationData(6029244, TMCLocation.FALLS_ENTRANCE_HP,                        Items.HEART_PIECE, 0x0F87C3, (0x2CD0, 0x01), None,   None),
    LocationData(6029245, TMCLocation.FALLS_WATER_DIG_CAVE_FUSION_HP,           Items.HEART_PIECE, 0x0F3DD7, (0x2D05, 0x20), None,   None),
    LocationData(6029246, TMCLocation.FALLS_WATER_DIG_CAVE_FUSION_CHEST,        None,              None,     (0x2D05, 0x04), 0x0016, None),
    LocationData(6029247, TMCLocation.FALLS_1ST_CAVE_CHEST,                     None,              None,     (0x2D25, 0x10), 0x0533, None),
    LocationData(6029248, TMCLocation.FALLS_CLIFF_CHEST,                        None,              None,     (0x2CD0, 0x02), 0x000A, None),
    LocationData(6029249, TMCLocation.FALLS_SOUTH_DIG_SPOT,                     Items.RUPEES_50,   0x0F8823, (0x2CDA, 0x80), None,   None),
    LocationData(6029250, TMCLocation.FALLS_GOLDEN_TEKTITE,                     Items.RUPEES_100,  None,     (0x2CA2, 0x40), None,   None),
    LocationData(6029251, TMCLocation.FALLS_NORTH_DIG_SPOT,                     Items.RUPEES_50,   0x0F8813, (0x2CD0, 0x80), None,   None),
    LocationData(6029252, TMCLocation.FALLS_ROCK_FUSION_CHEST,                  Items.KINSTONE,    0x0FE106, (0x2CD3, 0x80), None,   None),
    LocationData(6029253, TMCLocation.FALLS_WATERFALL_FUSION_HP,                Items.HEART_PIECE, 0x0F906F, (0x2D27, 0x10), None,   None),
    LocationData(6029254, TMCLocation.FALLS_RUPEE_CAVE_TOP_TOP,                 Items.RUPEES_1,    0x0F8F27, (0x2D25, 0x20), None,   None),
    LocationData(6029255, TMCLocation.FALLS_RUPEE_CAVE_TOP_LEFT,                Items.RUPEES_1,    0x0F8F37, (0x2D25, 0x40), None,   None),
    LocationData(6029256, TMCLocation.FALLS_RUPEE_CAVE_TOP_MIDDLE,              Items.RUPEES_20,   0x0F8F47, (0x2D25, 0x80), None,   None),
    LocationData(6029257, TMCLocation.FALLS_RUPEE_CAVE_TOP_RIGHT,               Items.RUPEES_1,    0x0F8F57, (0x2D26, 0x01), None,   None),
    LocationData(6029258, TMCLocation.FALLS_RUPEE_CAVE_TOP_BOTTOM,              Items.RUPEES_1,    0x0F8F67, (0x2D26, 0x02), None,   None),
    LocationData(6029259, TMCLocation.FALLS_RUPEE_CAVE_SIDE_TOP,                Items.RUPEES_1,    0x0F8F77, (0x2D26, 0x04), None,   None),
    LocationData(6029260, TMCLocation.FALLS_RUPEE_CAVE_SIDE_LEFT,               Items.RUPEES_1,    0x0F8F87, (0x2D26, 0x08), None,   None),
    LocationData(6029261, TMCLocation.FALLS_RUPEE_CAVE_SIDE_RIGHT,              Items.RUPEES_1,    0x0F8F97, (0x2D26, 0x10), None,   None),
    LocationData(6029262, TMCLocation.FALLS_RUPEE_CAVE_SIDE_BOTTOM,             Items.RUPEES_1,    0x0F8FA7, (0x2D26, 0x20), None,   None),
    LocationData(6029263, TMCLocation.FALLS_RUPEE_CAVE_UNDERWATER_TOP_LEFT,     Items.RUPEES_1,    0x0F8FB7, (0x2D26, 0x40), None,   None),
    LocationData(6029264, TMCLocation.FALLS_RUPEE_CAVE_UNDERWATER_TOP_RIGHT,    Items.RUPEES_1,    0x0F8FC7, (0x2D26, 0x80), None,   None),
    LocationData(6029265, TMCLocation.FALLS_RUPEE_CAVE_UNDERWATER_MIDDLE_LEFT,  Items.RUPEES_5,    0x0F8FD7, (0x2D27, 0x01), None,   None),
    LocationData(6029266, TMCLocation.FALLS_RUPEE_CAVE_UNDERWATER_MIDDLE_RIGHT, Items.RUPEES_5,    0x0F8FE7, (0x2D27, 0x02), None,   None),
    LocationData(6029267, TMCLocation.FALLS_RUPEE_CAVE_UNDERWATER_BOTTOM_LEFT,  Items.RUPEES_20,   0x0F8FF7, (0x2D27, 0x04), None,   None),
    LocationData(6029268, TMCLocation.FALLS_RUPEE_CAVE_UNDERWATER_BOTTOM_RIGHT, Items.RUPEES_20,   0x0F9007, (0x2D27, 0x08), None,   None),
    LocationData(6029269, TMCLocation.FALLS_TOP_CAVE_BOMB_WALL_CHEST,           None,              None,     (0x2D25, 0x04), 0x0233, None),
    LocationData(6029270, TMCLocation.FALLS_TOP_CAVE_CHEST,                     Items.RUPEES_100,  None,     (0x2D25, 0x01), 0x0033, None),
]

clouds: typing.List[LocationData] = [
    LocationData(6029271, TMCLocation.CLOUDS_FREE_CHEST,                 Items.KINSTONE_GOLD_CLOUD, None,     (0x2CD7, 0x08), 0x0108, None),
    LocationData(6029272, TMCLocation.CLOUDS_NORTH_EAST_DIG_SPOT,        Items.KINSTONE,            0x0DCB5B, (0x2CD8, 0x08), None,   None),
    LocationData(6029273, TMCLocation.CLOUDS_NORTH_KILL,                 Items.KINSTONE_GOLD_CLOUD, 0x0DCEDF, (0x2CDA, 0x02), None,   None),
    LocationData(6029274, TMCLocation.CLOUDS_NORTH_WEST_LEFT_CHEST,      None,                      None,     (0x2CD7, 0x40), 0x0108, None),
    LocationData(6029275, TMCLocation.CLOUDS_NORTH_WEST_RIGHT_CHEST,     None,                      None,     (0x2CD7, 0x80), 0x0108, None),
    LocationData(6029276, TMCLocation.CLOUDS_NORTH_WEST_DIG_SPOT,        Items.KINSTONE,            0x0DCB4B, (0x2CD8, 0x04), None,   None),
    LocationData(6029277, TMCLocation.CLOUDS_NORTH_WEST_BOTTOM_CHEST,    Items.KINSTONE_GOLD_CLOUD, None,     (0x2CD7, 0x20), None,   None),
    LocationData(6029278, TMCLocation.CLOUDS_SOUTH_LEFT_CHEST,           None,                      None,     (0x2CD8, 0x01), 0x0108, None),
    LocationData(6029279, TMCLocation.CLOUDS_SOUTH_DIG_SPOT,             Items.KINSTONE,            0x0DCB8B, (0x2CD8, 0x40), None,   None),
    LocationData(6029280, TMCLocation.CLOUDS_SOUTH_MIDDLE_CHEST,         Items.KINSTONE_GOLD_CLOUD, None,     (0x2CD7, 0x10), None,   None),
    LocationData(6029281, TMCLocation.CLOUDS_SOUTH_MIDDLE_DIG_SPOT,      Items.KINSTONE,            0x0DCB6B, (0x2CD8, 0x10), None,   None),
    LocationData(6029282, TMCLocation.CLOUDS_SOUTH_KILL,                 Items.KINSTONE_GOLD_CLOUD, 0x0DCEEF, (0x2CDA, 0x08), None,   None),
    LocationData(6029283, TMCLocation.CLOUDS_SOUTH_RIGHT_CHEST,          None,                      None,     (0x2CD8, 0x02), 0x0108, None),
    LocationData(6029284, TMCLocation.CLOUDS_SOUTH_RIGHT_DIG_SPOT,       Items.KINSTONE,            0x0DCB9B, (0x2CD8, 0x80), None,   None),
    LocationData(6029285, TMCLocation.CLOUDS_SOUTH_EAST_BOTTOM_DIG_SPOT, Items.KINSTONE,            0x0DCBAB, (0x2CD9, 0x01), None,   None),
    LocationData(6029286, TMCLocation.CLOUDS_SOUTH_EAST_TOP_DIG_SPOT,    Items.KINSTONE,            0x0DCB7B, (0x2CD8, 0x20), None,   None),
]

wind_tribe: typing.List[LocationData] = [
    LocationData(6029287, TMCLocation.WIND_TRIBE_1F_LEFT_CHEST,   Items.KINSTONE,    None,     (0x2CDC, 0x20), 0x0030, None),
    LocationData(6029288, TMCLocation.WIND_TRIBE_1F_RIGHT_CHEST,  Items.KINSTONE,    None,     (0x2CDC, 0x40), 0x0030, None),
    LocationData(6029289, TMCLocation.WIND_TRIBE_2F_CHEST,        Items.KINSTONE,    None,     (0x2CDC, 0x80), 0x0130, None),
    LocationData(6029290, TMCLocation.WIND_TRIBE_2F_GREGAL_NPC_1, None,              0x014C5C, (0x2CE8, 0x20), None,   None),
    LocationData(6029291, TMCLocation.WIND_TRIBE_2F_GREGAL_NPC_2, Items.LIGHT_ARROW, 0x014CBC, (0x2CE8, 0x40), None,   None),
    LocationData(6029292, TMCLocation.WIND_TRIBE_3F_LEFT_CHEST,   Items.KINSTONE,    None,     (0x2CDD, 0x01), 0x0230, None),
    LocationData(6029293, TMCLocation.WIND_TRIBE_3F_CENTER_CHEST, Items.KINSTONE,    None,     (0x2CDD, 0x02), 0x0230, None),
    LocationData(6029294, TMCLocation.WIND_TRIBE_3F_RIGHT_CHEST,  Items.KINSTONE,    None,     (0x2CDD, 0x04), 0x0230, None),
    LocationData(6029295, TMCLocation.WIND_TRIBE_4F_LEFT_CHEST,   Items.KINSTONE,    None,     (0x2CDD, 0x40), 0x0330, None),
    LocationData(6029296, TMCLocation.WIND_TRIBE_4F_RIGHT_CHEST,  Items.KINSTONE,    None,     (0x2CDD, 0x80), 0x0330, None),
]

dungeon_dws: typing.List[LocationData] = [
    LocationData(6029297, TMCLocation.DEEPWOOD_2F_CHEST,                     Items.RUPEES_20,           0x0DF17E, (0x2D45, 0x04), 0x1748, None),
    LocationData(6029298, TMCLocation.DEEPWOOD_1F_SLUG_TORCHES_CHEST,        Items.SMALL_KEY_DWS,       0x0DEA4A, (0x2D43, 0x20), 0x1048, None),
    LocationData(6029299, TMCLocation.DEEPWOOD_1F_BARREL_ROOM_CHEST,         None,                      0x0DE396, (0x2D41, 0x08), 0x0648, None),
    LocationData(6029300, TMCLocation.DEEPWOOD_1F_WEST_BIG_CHEST,            Items.DUNGEON_COMPASS_DWS, 0x0DE23E, (0x2D41, 0x02), 0x0548, None),
    LocationData(6029301, TMCLocation.DEEPWOOD_1F_WEST_STATUE_PUZZLE_CHEST,  Items.SMALL_KEY_DWS,       0x0DE176, (0x2D40, 0x80), 0x0448, None),
    LocationData(6029302, TMCLocation.DEEPWOOD_1F_EAST_MULLDOZER_FIGHT_ITEM, Items.SMALL_KEY_DWS,       0x0DE51B, (0x2D42, 0x01), 0x0848, None),
    LocationData(6029303, TMCLocation.DEEPWOOD_1F_NORTH_EAST_CHEST,          None,                      0x0DE176, (0x2D40, 0x10), 0x0248, None),
    LocationData(6029304, TMCLocation.DEEPWOOD_B1_SWITCH_ROOM_BIG_CHEST,     Items.DUNGEON_MAP_DWS,     0x0DECDA, (0x2D44, 0x04), 0x1248, None),
    LocationData(6029305, TMCLocation.DEEPWOOD_B1_SWITCH_ROOM_CHEST,         Items.SMALL_KEY_DWS,       0x0DECD2, (0x2D44, 0x02), 0x1248, None),
    LocationData(6029306, TMCLocation.DEEPWOOD_1F_BLUE_WARP_HP,              Items.HEART_PIECE,         0x0DDE03, (0x2D45, 0x80), 0x0148, None),
    LocationData(6029307, TMCLocation.DEEPWOOD_1F_BLUE_WARP_LEFT_CHEST,      None,                      None,     (0x2D40, 0x04), 0x0148, None),
    LocationData(6029308, TMCLocation.DEEPWOOD_1F_BLUE_WARP_RIGHT_CHEST,     None,                      None,     (0x2D40, 0x08), 0x0148, None),
    LocationData(6029309, TMCLocation.DEEPWOOD_1F_MADDERPILLAR_BIG_CHEST,    Items.GUST_JAR,            0x0DDC7E, (0x2D3F, 0x08), 0x0048, None),
    LocationData(6029310, TMCLocation.DEEPWOOD_1F_MADDERPILLAR_HP,           Items.HEART_PIECE,         0x0DE1F7, (0x2D46, 0x04), 0x0548, None),
    LocationData(6029311, TMCLocation.DEEPWOOD_B1_WEST_BIG_CHEST,            Items.BIG_KEY_DWS,         0x0DEB9A, (0x2D43, 0x80), 0x1148, None),
    LocationData(6029312, TMCLocation.DEEPWOOD_BOSS_ITEM,                    Items.HEART_CONTAINER,     None,     (0x2D44, 0x80), 0x0049, None),
    LocationData(6029313, TMCLocation.DEEPWOOD_PRIZE,                        Items.EARTH_ELEMENT,       0x0DF03B, (0x2C9C, 0x04), 0x0049, None),
]

dungeon_cof: typing.List[LocationData] = [
    LocationData(6029314, TMCLocation.COF_1F_SPIKE_BEETLE_BIG_CHEST,   Items.DUNGEON_MAP_COF,     0x0E09C6, (0x2D5A, 0x04), 0x1550, None),
    LocationData(6029315, TMCLocation.COF_1F_ITEM1,                    Items.RUPEES_1,            0x0DFAEB, (0x2D5B, 0x40), None,   None),
    LocationData(6029316, TMCLocation.COF_1F_ITEM2,                    Items.RUPEES_1,            0x0DFAFB, (0x2D5B, 0x80), None,   None),
    LocationData(6029317, TMCLocation.COF_1F_ITEM3,                    Items.RUPEES_1,            0x0DFB0B, (0x2D5C, 0x01), None,   None),
    LocationData(6029318, TMCLocation.COF_1F_ITEM4,                    Items.RUPEES_1,            0x0DFB1B, (0x2D5C, 0x02), None,   None),
    LocationData(6029319, TMCLocation.COF_1F_ITEM5,                    Items.RUPEES_1,            0x0DFB2B, (0x2D5C, 0x04), None,   None),
    LocationData(6029320, TMCLocation.COF_B1_HAZY_ROOM_BIG_CHEST,      Items.DUNGEON_COMPASS_COF, 0x0E028A, (0x2D59, 0x02), 0x0950, None),
    LocationData(6029321, TMCLocation.COF_B1_HAZY_ROOM_SMALL_CHEST,    Items.KINSTONE,            0x0E0282, (0x2D59, 0x04), 0x0950, None),
    LocationData(6029322, TMCLocation.COF_B1_ROLLOBITE_CHEST,          Items.RUPEES_50,           0x0E00E2, (0x2D58, 0x40), 0x0850, None),
    LocationData(6029323, TMCLocation.COF_B1_ROLLOBITE_PILLAR_CHEST,   Items.SMALL_KEY_COF,       0x0E00DA, (0x2D58, 0x80), 0x0850, None),
    LocationData(6029324, TMCLocation.COF_B1_SPIKEY_CHUS_PILLAR_CHEST, Items.SMALL_KEY_COF,       0x0DF50A, (0x2D57, 0x01), 0x0150, None),
    LocationData(6029325, TMCLocation.COF_B1_HP,                       Items.HEART_PIECE,         0x0DFC9F, (0x2D5B, 0x10), None,   None),
    LocationData(6029326, TMCLocation.COF_B1_SPIKEY_CHUS_BIG_CHEST,    Items.CANE_OF_PACCI,       0x0DF512, (0x2D57, 0x02), 0x0150, None),
    LocationData(6029327, TMCLocation.COF_B2_PRE_LAVA_NORTH_CHEST,     Items.KINSTONE,            None,     (0x2D59, 0x10), 0x1050, None),
    LocationData(6029328, TMCLocation.COF_B2_PRE_LAVA_SOUTH_CHEST,     Items.KINSTONE,            None,     (0x2D59, 0x20), 0x1050, None),
    LocationData(6029329, TMCLocation.COF_B2_LAVA_ROOM_BLADE_CHEST,    Items.KINSTONE,            0x0E08BA, (0x2D5A, 0x01), 0x1450, None),
    LocationData(6029330, TMCLocation.COF_B2_LAVA_ROOM_RIGHT_CHEST,    Items.RUPEES_100,          0x0E0CC2, (0x2D5B, 0x01), 0x1750, None),
    LocationData(6029331, TMCLocation.COF_B2_LAVA_ROOM_LEFT_CHEST,     Items.KINSTONE,            0x0E0CBA, (0x2D5A, 0x80), 0x1750, None),
    LocationData(6029332, TMCLocation.COF_B2_LAVA_ROOM_BIG_CHEST,      Items.BIG_KEY_COF,         0x0E0CCA, (0x2D5B, 0x02), 0x1750, None),
    LocationData(6029333, TMCLocation.COF_BOSS_ITEM,                   Items.HEART_CONTAINER,     None,     (0x2D5B, 0x04), None,   None),
    LocationData(6029334, TMCLocation.COF_PRIZE,                       Items.FIRE_ELEMENT,        0x0E0F03, (0x2C9C, 0x08), None,   None),
]

dungeon_fow: typing.List[LocationData] = [
    LocationData(6029335, TMCLocation.FORTRESS_ENTRANCE_1F_LEFT_CHEST,         Items.KINSTONE,            None,     (0x2D05, 0x80), 0x0018, None),
    LocationData(6029336, TMCLocation.FORTRESS_ENTRANCE_1F_LEFT_WIZROBE_CHEST, None,                      None,     (0x2D74, 0x08), 0x2358, None),
    LocationData(6029337, TMCLocation.FORTRESS_ENTRANCE_1F_RIGHT_ITEM,         Items.RUPEES_50,           0x0F3E67, (0x2D05, 0x40), None,   None),
    LocationData(6029338, TMCLocation.FORTRESS_LEFT_2F_DIG_CHEST,              Items.KINSTONE,            None,     (0x2D06, 0x01), 0x0118, None),
    LocationData(6029339, TMCLocation.FORTRESS_LEFT_2F_ITEM1,                  Items.RUPEES_1,            0x0F3F37, (0x2D06, 0x20), None,   None),
    LocationData(6029340, TMCLocation.FORTRESS_LEFT_2F_ITEM2,                  Items.RUPEES_1,            0x0F3F47, (0x2D06, 0x40), None,   None),
    LocationData(6029341, TMCLocation.FORTRESS_LEFT_2F_ITEM3,                  Items.RUPEES_1,            0x0F3F57, (0x2D06, 0x80), None,   None),
    LocationData(6029342, TMCLocation.FORTRESS_LEFT_2F_ITEM4,                  Items.RUPEES_1,            0x0F3F67, (0x2D07, 0x01), None,   None),
    LocationData(6029343, TMCLocation.FORTRESS_LEFT_2F_ITEM5,                  Items.RUPEES_1,            0x0F3F77, (0x2D07, 0x04), None,   None),
    LocationData(6029344, TMCLocation.FORTRESS_LEFT_2F_ITEM6,                  Items.RUPEES_5,            0x0F3F87, (0x2D07, 0x08), None,   None),
    LocationData(6029345, TMCLocation.FORTRESS_LEFT_2F_ITEM7,                  Items.RUPEES_5,            0x0F3F97, (0x2D07, 0x02), None,   None),
    LocationData(6029346, TMCLocation.FORTRESS_LEFT_3F_SWITCH_CHEST,           Items.KINSTONE,            None,     (0x2D07, 0x20), 0x0218, None),
    LocationData(6029347, TMCLocation.FORTRESS_LEFT_3F_EYEGORE_BIG_CHEST,      Items.DUNGEON_MAP_FOW,     None,     (0x2D6F, 0x10), 0x0058, None),
    LocationData(6029348, TMCLocation.FORTRESS_LEFT_3F_ITEM_DROP,              Items.SMALL_KEY_FOW,       None,     (0x2D73, 0x80), None,   None),
    LocationData(6029349, TMCLocation.FORTRESS_MIDDLE_2F_BIG_CHEST,            Items.DUNGEON_COMPASS_FOW, None,     (0x2D73, 0x02), 0x1958, None),
    LocationData(6029350, TMCLocation.FORTRESS_MIDDLE_2F_STATUE_CHEST,         Items.KINSTONE,            None,     (0x2D06, 0x02), 0x0118, None),
    LocationData(6029351, TMCLocation.FORTRESS_RIGHT_2F_LEFT_CHEST,            Items.KINSTONE,            None,     (0x2D73, 0x20), 0x1D58, None),
    LocationData(6029352, TMCLocation.FORTRESS_RIGHT_2F_RIGHT_CHEST,           Items.KINSTONE,            None,     (0x2D73, 0x40), 0x1D58, None),
    LocationData(6029353, TMCLocation.FORTRESS_RIGHT_2F_DIG_CHEST,             Items.KINSTONE,            None,     (0x2D06, 0x04), 0x0118, None),
    LocationData(6029354, TMCLocation.FORTRESS_RIGHT_3F_DIG_CHEST,             Items.KINSTONE,            None,     (0x2D07, 0x40), 0x0218, None),
    LocationData(6029355, TMCLocation.FORTRESS_RIGHT_3F_ITEM_DROP,             Items.SMALL_KEY_FOW,       None,     (0x2D74, 0x02), None,   None),
    LocationData(6029356, TMCLocation.FORTRESS_ENTRANCE_1F_RIGHT_HP,           Items.HEART_PIECE,         0x0E2DD7, (0x2D74, 0x80), None,   None),
    LocationData(6029357, TMCLocation.FORTRESS_BACK_LEFT_BIG_CHEST,            Items.MOLE_MITTS,          None,     (0x2D08, 0x01), 0x0318, None),
    LocationData(6029358, TMCLocation.FORTRESS_BACK_LEFT_SMALL_CHEST,          Items.RUPEES_100,          None,     (0x2D08, 0x02), 0x0318, None),
    LocationData(6029359, TMCLocation.FORTRESS_BACK_RIGHT_STATUE_ITEM_DROP,    Items.SMALL_KEY_FOW,       0x0E1E8B, (0x2D71, 0x40), None,   None),
    LocationData(6029360, TMCLocation.FORTRESS_BACK_RIGHT_MINISH_ITEM_DROP,    Items.SMALL_KEY_FOW,       0x0F424F, (0x2D08, 0x10), None,   None),
    LocationData(6029361, TMCLocation.FORTRESS_BACK_RIGHT_DIG_ROOM_TOP_POT,    Items.RUPEES_50,           0x0F3FC7, (0x2D06, 0x08), None,   None, 0x0F3FC9),
    LocationData(6029362, TMCLocation.FORTRESS_BACK_RIGHT_DIG_ROOM_BOTTOM_POT, None,                      0x0F3FD7, (0x2D06, 0x10), None,   None, 0x0F3FD9),
    LocationData(6029363, TMCLocation.FORTRESS_BACK_RIGHT_BIG_CHEST,           Items.BIG_KEY_FOW,         None,     (0x2D73, 0x04), 0x1B58, None),
    LocationData(6029364, TMCLocation.FORTRESS_BOSS_ITEM,                      Items.HEART_CONTAINER,     None,     (0x2D72, 0x04), None,   None),
    LocationData(6029365, TMCLocation.FORTRESS_PRIZE,                          Items.OCARINA,             0x09C9E6, (0x2D74, 0x20), None,   None, 0x09C9E8),
]

dungeon_tod: typing.List[LocationData] = [
    LocationData(6029366, TMCLocation.DROPLETS_ENTRANCE_B2_EAST_ICEBLOCK,                Items.SMALL_KEY_TOD,       0x098C1A, (0x2D8E, 0x04), None,   None, 0x098C1C),
    LocationData(6029367, TMCLocation.DROPLETS_ENTRANCE_B2_WEST_ICEBLOCK,                Items.BIG_KEY_TOD,         0x098C3C, (0x2D8D, 0x80), None,   None, 0x098C3E),
    LocationData(6029368, TMCLocation.DROPLETS_LEFT_PATH_B1_UNDERPASS_ITEM1,             Items.RUPEES_1,            0x0E3F8B, (0x2D94, 0x20), None,   None),
    LocationData(6029369, TMCLocation.DROPLETS_LEFT_PATH_B1_UNDERPASS_ITEM2,             Items.RUPEES_1,            0x0E3F9B, (0x2D94, 0x40), None,   None),
    LocationData(6029370, TMCLocation.DROPLETS_LEFT_PATH_B1_UNDERPASS_ITEM3,             Items.RUPEES_1,            0x0E3FAB, (0x2D94, 0x80), None,   None),
    LocationData(6029371, TMCLocation.DROPLETS_LEFT_PATH_B1_UNDERPASS_ITEM4,             Items.RUPEES_1,            0x0E3FBB, (0x2D95, 0x01), None,   None),
    LocationData(6029372, TMCLocation.DROPLETS_LEFT_PATH_B1_UNDERPASS_ITEM5,             Items.RUPEES_1,            0x0E3FCB, (0x2D95, 0x02), None,   None),
    LocationData(6029373, TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_BIG_CHEST,         Items.DUNGEON_MAP_TOD,     None,     (0x2D8B, 0x80), 0x0D60, None),
    LocationData(6029374, TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_UNDERWATER1,       Items.RUPEES_5,            0x0E3593, (0x2D96, 0x20), None,   None),
    LocationData(6029375, TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_UNDERWATER2,       Items.RUPEES_5,            0x0E35A3, (0x2D96, 0x40), None,   None),
    LocationData(6029376, TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_UNDERWATER3,       Items.RUPEES_5,            0x0E35B3, (0x2D96, 0x80), None,   None),
    LocationData(6029377, TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_UNDERWATER4,       Items.RUPEES_5,            0x0E35C3, (0x2D97, 0x01), None,   None),
    LocationData(6029378, TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_UNDERWATER5,       Items.RUPEES_5,            0x0E35D3, (0x2D97, 0x02), None,   None),
    LocationData(6029379, TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_UNDERWATER6,       Items.RUPEES_5,            0x0E35E3, (0x2D97, 0x04), None,   None),
    LocationData(6029380, TMCLocation.DROPLETS_LEFT_PATH_B2_WATERFALL_UNDERWATER1,       Items.RUPEES_5,            0x0E58DF, (0x2D95, 0x80), None,   None),
    LocationData(6029381, TMCLocation.DROPLETS_LEFT_PATH_B2_WATERFALL_UNDERWATER2,       Items.RUPEES_5,            0x0E58EF, (0x2D96, 0x01), None,   None),
    LocationData(6029382, TMCLocation.DROPLETS_LEFT_PATH_B2_WATERFALL_UNDERWATER3,       Items.RUPEES_5,            0x0E58FF, (0x2D96, 0x02), None,   None),
    LocationData(6029383, TMCLocation.DROPLETS_LEFT_PATH_B2_WATERFALL_UNDERWATER4,       Items.RUPEES_5,            0x0E590F, (0x2D96, 0x04), None,   None),
    LocationData(6029384, TMCLocation.DROPLETS_LEFT_PATH_B2_WATERFALL_UNDERWATER5,       Items.RUPEES_5,            0x0E591F, (0x2D96, 0x08), None,   None),
    LocationData(6029385, TMCLocation.DROPLETS_LEFT_PATH_B2_WATERFALL_UNDERWATER6,       Items.RUPEES_5,            0x0E592F, (0x2D96, 0x10), None,   None),
    LocationData(6029386, TMCLocation.DROPLETS_LEFT_PATH_B2_UNDERWATER_POT,              Items.SMALL_KEY_TOD,       0x0E5BC7, (0x2D93, 0x04), None,   None),
    LocationData(6029387, TMCLocation.DROPLETS_LEFT_PATH_B2_ICE_MADDERPILLAR_BIG_CHEST,  Items.DUNGEON_COMPASS_TOD, None,     (0x2D92, 0x80), 0x3260, None),
    LocationData(6029388, TMCLocation.DROPLETS_LEFT_PATH_B2_ICE_PLAIN_FROZEN_CHEST,      None,                      None,     (0x2D8F, 0x04), 0x2860, None),
    LocationData(6029389, TMCLocation.DROPLETS_LEFT_PATH_B2_ICE_PLAIN_CHEST,             Items.RUPEES_50,           None,     (0x2D8F, 0x08), 0x2860, None),
    LocationData(6029390, TMCLocation.DROPLETS_LEFT_PATH_B2_LILYPAD_CORNER_FROZEN_CHEST, Items.KINSTONE,            None,     (0x2D93, 0x40), 0x2D60, None),
    LocationData(6029391, TMCLocation.DROPLETS_RIGHT_PATH_B1_1ST_CHEST,                  Items.KINSTONE,            None,     (0x2D8B, 0x01), 0x0960, None),
    LocationData(6029392, TMCLocation.DROPLETS_RIGHT_PATH_B1_2ND_CHEST,                  Items.KINSTONE,            None,     (0x2D8B, 0x04), 0x0A60, None),
    LocationData(6029393, TMCLocation.DROPLETS_RIGHT_PATH_B1_POT,                        Items.KINSTONE,            0x0E3A73, (0x2D8B, 0x02), None,   None, 0x0E3A75),
    LocationData(6029394, TMCLocation.DROPLETS_RIGHT_PATH_B3_FROZEN_CHEST,               Items.SMALL_KEY_TOD,       None,     (0x2D8D, 0x10), 0x1160, None),
    LocationData(6029395, TMCLocation.DROPLETS_RIGHT_PATH_B1_BLU_CHU_BIG_CHEST,          Items.LANTERN,             None,     (0x2D8C, 0x80), 0x1060, None),
    LocationData(6029396, TMCLocation.DROPLETS_RIGHT_PATH_B2_FROZEN_CHEST,               Items.RUPEES_100,          None,     (0x2D92, 0x40), 0x3260, None),
    LocationData(6029397, TMCLocation.DROPLETS_RIGHT_PATH_B2_DARK_MAZE_BOTTOM_CHEST,     Items.KINSTONE,            None,     (0x2D8F, 0x80), 0x2B60, None),
    LocationData(6029398, TMCLocation.DROPLETS_RIGHT_PATH_B2_MULLDOZERS_ITEM_DROP,       Items.SMALL_KEY_TOD,       0x0E55CB, (0x2D91, 0x80), None,   None),
    LocationData(6029399, TMCLocation.DROPLETS_RIGHT_PATH_B2_DARK_MAZE_TOP_RIGHT_CHEST,  Items.KINSTONE,            None,     (0x2D8F, 0x20), 0x2B60, None),
    LocationData(6029400, TMCLocation.DROPLETS_RIGHT_PATH_B2_DARK_MAZE_TOP_LEFT_CHEST,   Items.KINSTONE,            None,     (0x2D8F, 0x40), 0x2B60, None),
    LocationData(6029401, TMCLocation.DROPLETS_RIGHT_PATH_B2_UNDERPASS_ITEM1,            Items.RUPEES_1,            0x0E483F, (0x2D95, 0x10), None,   None),
    LocationData(6029402, TMCLocation.DROPLETS_RIGHT_PATH_B2_UNDERPASS_ITEM2,            Items.RUPEES_1,            0x0E484F, (0x2D95, 0x20), None,   None),
    LocationData(6029403, TMCLocation.DROPLETS_RIGHT_PATH_B2_UNDERPASS_ITEM3,            Items.RUPEES_1,            0x0E485F, (0x2D95, 0x40), None,   None),
    LocationData(6029404, TMCLocation.DROPLETS_RIGHT_PATH_B2_UNDERPASS_ITEM4,            Items.RUPEES_1,            0x0E486F, (0x2D95, 0x04), None,   None),
    LocationData(6029405, TMCLocation.DROPLETS_RIGHT_PATH_B2_UNDERPASS_ITEM5,            Items.RUPEES_1,            0x0E487F, (0x2D95, 0x08), None,   None),
    LocationData(6029406, TMCLocation.DROPLETS_BOSS_ITEM,                                Items.HEART_CONTAINER,     None,     (0x2D8C, 0x01), None,   None),
    LocationData(6029407, TMCLocation.DROPLETS_PRIZE,                                    Items.WATER_ELEMENT,       0x0E40C3, (0x2C9C, 0x20), None,   None),
]

dungeon_pow: typing.List[LocationData] = [
    LocationData(6029408, TMCLocation.PALACE_1ST_HALF_1F_GRATE_CHEST,                       Items.KINSTONE,            None,     (0x2DAA, 0x40), 0x2D70, None),
    LocationData(6029409, TMCLocation.PALACE_1ST_HALF_1F_WIZROBE_BIG_CHEST,                 Items.ROCS_CAPE,           None,     (0x2DAA, 0x10), 0x2C70, None),
    LocationData(6029410, TMCLocation.PALACE_1ST_HALF_2F_ITEM1,                             Items.RUPEES_1,            0x0E8B1F, (0x2DA7, 0x04), None,   None),
    LocationData(6029411, TMCLocation.PALACE_1ST_HALF_2F_ITEM2,                             Items.RUPEES_1,            0x0E8B2F, (0x2DA7, 0x08), None,   None),
    LocationData(6029412, TMCLocation.PALACE_1ST_HALF_2F_ITEM3,                             Items.RUPEES_1,            0x0E8B3F, (0x2DA7, 0x10), None,   None),
    LocationData(6029413, TMCLocation.PALACE_1ST_HALF_2F_ITEM4,                             Items.RUPEES_1,            0x0E8B4F, (0x2DA7, 0x20), None,   None),
    LocationData(6029414, TMCLocation.PALACE_1ST_HALF_2F_ITEM5,                             Items.RUPEES_1,            0x0E8B5F, (0x2DA7, 0x40), None,   None),
    LocationData(6029415, TMCLocation.PALACE_1ST_HALF_3F_POT_PUZZLE_ITEM_DROP,              Items.SMALL_KEY_POW,       0x0E896F, (0x2DA7, 0x02), None,   None),
    LocationData(6029416, TMCLocation.PALACE_1ST_HALF_4F_BOW_MOBLINS_CHEST,                 Items.KINSTONE,            None,     (0x2DA4, 0x80), 0x0F70, None),
    LocationData(6029417, TMCLocation.PALACE_1ST_HALF_5F_BALL_AND_CHAIN_SOLDIERS_ITEM_DROP, Items.SMALL_KEY_POW,       0x0E719F, (0x2DA4, 0x02), None,   None),
    LocationData(6029418, TMCLocation.PALACE_1ST_HALF_5F_FAN_LOOP_CHEST,                    Items.SMALL_KEY_POW,       None,     (0x2DA3, 0x40), 0x0770, None),
    LocationData(6029419, TMCLocation.PALACE_1ST_HALF_5F_BIG_CHEST,                         Items.BIG_KEY_POW,         None,     (0x2DA2, 0x10), 0x0170, None),
    LocationData(6029420, TMCLocation.PALACE_2ND_HALF_1F_DARK_ROOM_BIG_CHEST,               Items.DUNGEON_COMPASS_POW, None,     (0x2DAB, 0x02), 0x3270, None),
    LocationData(6029421, TMCLocation.PALACE_2ND_HALF_1F_DARK_ROOM_SMALL_CHEST,             Items.SMALL_KEY_POW,       None,     (0x2DAB, 0x04), 0x3270, None),
    LocationData(6029422, TMCLocation.PALACE_2ND_HALF_2F_MANY_ROLLERS_CHEST,                Items.SMALL_KEY_POW,       None,     (0x2DA9, 0x80), 0x2B70, None),
    LocationData(6029423, TMCLocation.PALACE_2ND_HALF_2F_TWIN_WIZROBES_CHEST,               Items.KINSTONE,            None,     (0x2DA9, 0x40), 0x2970, None),
    LocationData(6029424, TMCLocation.PALACE_2ND_HALF_3F_FIRE_WIZROBES_BIG_CHEST,           Items.DUNGEON_MAP_POW,     None,     (0x2DA6, 0x80), 0x1C70, None),
    LocationData(6029425, TMCLocation.PALACE_2ND_HALF_4F_HP,                                Items.HEART_PIECE,         0x0E77A7, (0x2DAC, 0x01), None,   None),
    LocationData(6029426, TMCLocation.PALACE_2ND_HALF_4F_SWITCH_HIT_CHEST,                  Items.RUPEES_200,          None,     (0x2DA5, 0x80), 0x1570, None),
    LocationData(6029427, TMCLocation.PALACE_2ND_HALF_5F_BOMBAROSSA_CHEST,                  Items.SMALL_KEY_POW,       None,     (0x2DA2, 0x20), 0x0370, None),
    LocationData(6029428, TMCLocation.PALACE_2ND_HALF_4F_BLOCK_MAZE_CHEST,                  Items.KINSTONE,            None,     (0x2DA5, 0x02), 0x1070, None),
    LocationData(6029429, TMCLocation.PALACE_2ND_HALF_5F_RIGHT_SIDE_CHEST,                  Items.KINSTONE,            None,     (0x2DA2, 0x80), 0x0470, None),
    LocationData(6029430, TMCLocation.PALACE_BOSS_ITEM,                                     Items.HEART_CONTAINER,     None,     (0x2DAB, 0x20), None,   None),
    LocationData(6029431, TMCLocation.PALACE_PRIZE,                                         Items.WIND_ELEMENT,        0x0E69E3, (0x2C9C, 0x40), None,   None),
]

sanctuary: typing.List[LocationData] = [
    LocationData(6029432, TMCLocation.SANCTUARY_PEDESTAL_ITEM1, Items.WHITE_SWORD_RED,  None, (0x2EA7, 0x80), None, None),
    LocationData(6029433, TMCLocation.SANCTUARY_PEDESTAL_ITEM2, Items.WHITE_SWORD_BLUE, None, (0x2EA8, 0x01), None, None),
    LocationData(6029434, TMCLocation.SANCTUARY_PEDESTAL_ITEM3, Items.FOUR_SWORD,       None, (0x2EA8, 0x02), None, None),
]

dungeon_dhc: typing.List[LocationData] = [
    LocationData(6029435, TMCLocation.DHC_B2_KING,                Items.RUPEES_1,            0x00E46A, (0x2DC2, 0x02), None,   None),
    LocationData(6029436, TMCLocation.DHC_B1_BIG_CHEST,           Items.DUNGEON_MAP_DHC,     None,     (0x2DC1, 0x08), 0x3788, None),
    LocationData(6029437, TMCLocation.DHC_1F_BLADE_CHEST,         Items.SMALL_KEY_DHC,       None,     (0x2DC0, 0x20), 0x2788, None),
    LocationData(6029438, TMCLocation.DHC_1F_THRONE_BIG_CHEST,    Items.DUNGEON_COMPASS_DHC, None,     (0x2DBF, 0x80), 0x2088, None),
    LocationData(6029439, TMCLocation.DHC_3F_NORTH_WEST_CHEST,    Items.SMALL_KEY_DHC,       None,     (0x2DBB, 0x40), 0x0188, None),
    LocationData(6029440, TMCLocation.DHC_3F_NORTH_EAST_CHEST,    Items.SMALL_KEY_DHC,       None,     (0x2DBB, 0x80), 0x0288, None),
    LocationData(6029441, TMCLocation.DHC_3F_SOUTH_WEST_CHEST,    Items.SMALL_KEY_DHC,       None,     (0x2DBC, 0x01), 0x0388, None),
    LocationData(6029442, TMCLocation.DHC_3F_SOUTH_EAST_CHEST,    Items.SMALL_KEY_DHC,       None,     (0x2DBC, 0x02), 0x0488, None),
    LocationData(6029443, TMCLocation.DHC_2F_BLUE_WARP_BIG_CHEST, Items.BIG_KEY_DHC,         None,     (0x2DBC, 0x08), 0x0988, None),
]

hyrule_town: typing.List[LocationData] = [
    LocationData(6029444, TMCLocation.TOWN_CAFE_LADY_NPC,              Items.KINSTONE,        0x00EDDA, (0x2CD6, 0x10), 0x0002, None),
    LocationData(6029445, TMCLocation.TOWN_SHOP_80_ITEM,               Items.BIG_WALLET,      None,     (0x2CE6, 0x20), None,   None),
    LocationData(6029446, TMCLocation.TOWN_SHOP_300_ITEM,              Items.BOOMERANG,       None,     (0x2B34, 0x40), None,   None),
    LocationData(6029447, TMCLocation.TOWN_SHOP_600_ITEM,              Items.QUIVER,          None,     (0x2CE6, 0x40), None,   None),
    LocationData(6029448, TMCLocation.TOWN_SHOP_BEHIND_COUNTER_ITEM,   Items.DOG_FOOD,        None,     (0x2B3F, 0x10), None,   None),
    LocationData(6029449, TMCLocation.TOWN_SHOP_ATTIC_CHEST,           None,                  None,     (0x2D0A, 0x80), 0x012E, None),
    LocationData(6029450, TMCLocation.TOWN_BAKERY_ATTIC_CHEST,         Items.RUPEES_100,      None,     (0x2D13, 0x20), 0x032E, None),
    LocationData(6029451, TMCLocation.TOWN_INN_BACKDOOR_HP,            Items.HEART_PIECE,     0x0D66D7, (0x2CF3, 0x01), None,   None),
    LocationData(6029452, TMCLocation.TOWN_INN_LEDGE_CHEST,            Items.KINSTONE,        None,     (0x2CD5, 0x01), 0x0002, None),
    LocationData(6029453, TMCLocation.TOWN_INN_POT,                    Items.KINSTONE,        0x0D663B, (0x2CE0, 0x80), None,   None, 0x0D663D),
    LocationData(6029454, TMCLocation.TOWN_WELL_RIGHT_CHEST,           Items.KINSTONE,        None,     (0x2CFD, 0x01), 0x0041, None),
    LocationData(6029455, TMCLocation.TOWN_GORON_MERCHANT_1_LEFT,      Items.KINSTONE,        None,     (None,   None), 0x0002, None), # Goron merchant stores the individual item *positions*
    LocationData(6029456, TMCLocation.TOWN_GORON_MERCHANT_1_MIDDLE,    Items.KINSTONE,        None,     (None,   None), 0x0002, None), # inside 0x2CA4 from left-right in bits 0x04-0x10
    LocationData(6029457, TMCLocation.TOWN_GORON_MERCHANT_1_RIGHT,     Items.KINSTONE,        None,     (None,   None), 0x0002, None),
    LocationData(6029458, TMCLocation.TOWN_GORON_MERCHANT_2_LEFT,      Items.KINSTONE,        None,     (None,   None), 0x0002, None), # There is a separate bit that stores how many times
    LocationData(6029459, TMCLocation.TOWN_GORON_MERCHANT_2_MIDDLE,    Items.KINSTONE,        None,     (None,   None), 0x0002, None), # there's been a restock across 0x2CA3 0x40 - 0x2CA4 0x02
    LocationData(6029460, TMCLocation.TOWN_GORON_MERCHANT_2_RIGHT,     Items.KINSTONE,        None,     (None,   None), 0x0002, None),
    LocationData(6029461, TMCLocation.TOWN_GORON_MERCHANT_3_LEFT,      Items.KINSTONE,        None,     (None,   None), 0x0002, None),
    LocationData(6029462, TMCLocation.TOWN_GORON_MERCHANT_3_MIDDLE,    Items.KINSTONE,        None,     (None,   None), 0x0002, None),
    LocationData(6029463, TMCLocation.TOWN_GORON_MERCHANT_3_RIGHT,     Items.KINSTONE,        None,     (None,   None), 0x0002, None),
    LocationData(6029464, TMCLocation.TOWN_GORON_MERCHANT_4_LEFT,      Items.KINSTONE,        None,     (None,   None), 0x0002, None),
    LocationData(6029465, TMCLocation.TOWN_GORON_MERCHANT_4_MIDDLE,    Items.KINSTONE,        None,     (None,   None), 0x0002, None),
    LocationData(6029466, TMCLocation.TOWN_GORON_MERCHANT_4_RIGHT,     Items.KINSTONE,        None,     (None,   None), 0x0002, None),
    LocationData(6029467, TMCLocation.TOWN_GORON_MERCHANT_5_LEFT,      Items.KINSTONE,        None,     (None,   None), 0x0002, None),
    LocationData(6029468, TMCLocation.TOWN_GORON_MERCHANT_5_MIDDLE,    Items.KINSTONE,        None,     (None,   None), 0x0002, None),
    LocationData(6029469, TMCLocation.TOWN_GORON_MERCHANT_5_RIGHT,     Items.KINSTONE,        None,     (None,   None), 0x0002, None),
    LocationData(6029470, TMCLocation.TOWN_DOJO_NPC_1,                 Items.SPIN_ATTACK,     None,     (0x2EA5, 0x10), None,   None),
    LocationData(6029471, TMCLocation.TOWN_DOJO_NPC_2,                 Items.ROCK_BREAKER,    None,     (0x2EA5, 0x20), None,   None),
    LocationData(6029472, TMCLocation.TOWN_DOJO_NPC_3,                 Items.DASH_ATTACK,     None,     (0x2EA5, 0x40), None,   None),
    LocationData(6029473, TMCLocation.TOWN_DOJO_NPC_4,                 Items.DOWNTHRUST,      None,     (0x2EA5, 0x80), None,   None),
    LocationData(6029474, TMCLocation.TOWN_WELL_TOP_CHEST,             Items.RUPEES_100,      None,     (0x2CFD, 0x04), 0x0041, None),
    LocationData(6029475, TMCLocation.TOWN_SCHOOL_ROOF_CHEST,          Items.KINSTONE,        None,     (0x2CD5, 0x02), 0x0002, None),
    LocationData(6029476, TMCLocation.TOWN_SCHOOL_PATH_FUSION_CHEST,   Items.KINSTONE,        0x0FE076, (0x2D11, 0x01), None,   None),
    LocationData(6029477, TMCLocation.TOWN_SCHOOL_PATH_LEFT_CHEST,     Items.KINSTONE,        None,     (0x2D0B, 0x80), 0x0211, None),
    LocationData(6029478, TMCLocation.TOWN_SCHOOL_PATH_MIDDLE_CHEST,   Items.KINSTONE,        None,     (0x2D0C, 0x01), 0x0211, None),
    LocationData(6029479, TMCLocation.TOWN_SCHOOL_PATH_RIGHT_CHEST,    Items.KINSTONE,        None,     (0x2D0C, 0x02), 0x0211, None),
    LocationData(6029480, TMCLocation.TOWN_SCHOOL_PATH_HP,             Items.KINSTONE,        0x0D5557, (0x2D0B, 0x40), None,   None),
    LocationData(6029481, TMCLocation.TOWN_DIGGING_TOP_CHEST,          Items.KINSTONE,        None,     (0x2D04, 0x04), 0x000F, None),
    LocationData(6029482, TMCLocation.TOWN_DIGGING_RIGHT_CHEST,        Items.KINSTONE,        None,     (0x2D04, 0x08), 0x000F, None),
    LocationData(6029483, TMCLocation.TOWN_DIGGING_LEFT_CHEST,         Items.KINSTONE,        None,     (0x2D04, 0x10), 0x000F, None),
    LocationData(6029484, TMCLocation.TOWN_WELL_LEFT_CHEST,            Items.RUPEES_100,      None,     (0x2CFC, 0x80), 0x0041, None),
    LocationData(6029485, TMCLocation.TOWN_BELL_HP,                    Items.HEART_PIECE,     0x05D602, (0x2CD5, 0x20), 0x0002, None, 0x05D604),
    LocationData(6029486, TMCLocation.TOWN_WATERFALL_FUSION_CHEST,     None,                  None,     (0x2D1D, 0x40), 0x0B32, None),
    LocationData(6029487, TMCLocation.TOWN_CARLOV_NPC,                 Items.CARLOV_MEDAL,    None,     (0x2EA5, 0x02), None,   None),
    LocationData(6029488, TMCLocation.TOWN_WELL_BOTTOM_CHEST,          Items.RUPEES_100,      None,     (0x2CFD, 0x02), 0x0041, None),
    LocationData(6029489, TMCLocation.TOWN_CUCCOS_LV_1_NPC,            None,                  0x1245E8, (None,   None), 0x0002, None), # Cucco game uses an incremented number in 0x2CA5
    LocationData(6029490, TMCLocation.TOWN_CUCCOS_LV_2_NPC,            None,                  0x1245EC, (None,   None), 0x0002, None), # it takes up the space of bits between 0x08-0x80
    LocationData(6029491, TMCLocation.TOWN_CUCCOS_LV_3_NPC,            None,                  0x1245F0, (None,   None), 0x0002, None),
    LocationData(6029492, TMCLocation.TOWN_CUCCOS_LV_4_NPC,            None,                  0x1245F4, (None,   None), 0x0002, None),
    LocationData(6029493, TMCLocation.TOWN_CUCCOS_LV_5_NPC,            None,                  0x1245F8, (None,   None), 0x0002, None),
    LocationData(6029494, TMCLocation.TOWN_CUCCOS_LV_6_NPC,            None,                  0x1245FC, (None,   None), 0x0002, None),
    LocationData(6029495, TMCLocation.TOWN_CUCCOS_LV_7_NPC,            Items.KINSTONE,        0x124600, (None,   None), 0x0002, None),
    LocationData(6029496, TMCLocation.TOWN_CUCCOS_LV_8_NPC,            Items.KINSTONE,        0x124604, (None,   None), 0x0002, None),
    LocationData(6029497, TMCLocation.TOWN_CUCCOS_LV_9_NPC,            Items.KINSTONE,        0x124608, (None,   None), 0x0002, None),
    LocationData(6029498, TMCLocation.TOWN_CUCCOS_LV_10_NPC,           Items.HEART_PIECE,     0x12460C, (0x2CA5, 0x80), 0x0002, None),
    LocationData(6029499, TMCLocation.TOWN_JULLIETA_ITEM,              Items.RED_BOOK,        None,     (0x2EA4, 0x10), None,   None),
    LocationData(6029500, TMCLocation.TOWN_SIMULATION_CHEST,           Items.HEART_PIECE,     0x0F04C2, (0x2C9C, 0x02), None,   None),
    LocationData(6029501, TMCLocation.TOWN_SHOE_SHOP_NPC,              Items.PEGASUS_BOOTS,   0x0130EE, (0x2EA4, 0x08), None,   None),
    LocationData(6029502, TMCLocation.TOWN_MUSIC_HOUSE_LEFT_CHEST,     Items.RUPEES_200,      None,     (0x2CF2, 0x20), 0x0523, None),
    LocationData(6029503, TMCLocation.TOWN_MUSIC_HOUSE_MIDDLE_CHEST,   Items.RUPEES_200,      None,     (0x2CF2, 0x40), 0x0523, None),
    LocationData(6029504, TMCLocation.TOWN_MUSIC_HOUSE_RIGHT_CHEST,    Items.RUPEES_200,      None,     (0x2CF2, 0x80), 0x0523, None),
    LocationData(6029505, TMCLocation.TOWN_MUSIC_HOUSE_HP,             Items.HEART_PIECE,     0x0F5407, (0x2CF2, 0x10), 0x0523, None),
    LocationData(6029506, TMCLocation.TOWN_WELL_PILLAR_CHEST,          Items.RUPEES_200,      None,     (0x2CFD, 0x02), 0x0041, None),
    LocationData(6029507, TMCLocation.TOWN_DR_LEFT_ATTIC_ITEM,         Items.RED_BOOK,        None,     (0x2EA4, 0x20), None,   None),
    LocationData(6029508, TMCLocation.TOWN_FOUNTAIN_BIG_CHEST,         Items.POWER_BRACELETS, None,     (0x2CFD, 0x80), 0x0362, None),
    LocationData(6029509, TMCLocation.TOWN_FOUNTAIN_SMALL_CHEST,       Items.RUPEES_100,      None,     (0x2CFE, 0x01), 0x0462, None),
    LocationData(6029510, TMCLocation.TOWN_FOUNTAIN_HP,                Items.HEART_PIECE,     0x0EF3B7, (0x2D14, 0x08), None,   None),
    LocationData(6029511, TMCLocation.TOWN_LIBRARY_YELLOW_MINISH_NPC,  Items.RUPEES_50,       0x00E7BE, (0x2CEB, 0x01), None,   None),
    LocationData(6029512, TMCLocation.TOWN_UNDER_LIBRARY_FROZEN_CHEST, None,                  None,     (0x2CFE, 0x20), 0x1262, None),
    LocationData(6029513, TMCLocation.TOWN_UNDER_LIBRARY_BIG_CHEST,    Items.FLIPPERS,        None,     (0x2CFE, 0x10), 0x1062, None),
    LocationData(6029514, TMCLocation.TOWN_UNDER_LIBRARY_UNDERWATER,   Items.RUPEES_50,       0x0EF79B, (0x2CFE, 0x08), None,   None),
]

north_field: typing.List[LocationData] = [
    LocationData(6029515, TMCLocation.NORTH_FIELD_DIG_SPOT,                       Items.RUPEES_50,       0x0F720F, (0x2CCD, 0x20), None,   None),
    LocationData(6029516, TMCLocation.NORTH_FIELD_HP,                             Items.HEART_PIECE,     0x0F864B, (0x2D2B, 0x08), None,   None),
    LocationData(6029517, TMCLocation.NORTH_FIELD_TREE_FUSION_TOP_LEFT_CHEST,     Items.KINSTONE,        None,     (0x2D1C, 0x10), 0x0032, None),
    LocationData(6029518, TMCLocation.NORTH_FIELD_TREE_FUSION_TOP_RIGHT_CHEST,    Items.KINSTONE,        None,     (0x2D1C, 0x20), 0x0032, None),
    LocationData(6029519, TMCLocation.NORTH_FIELD_TREE_FUSION_BOTTOM_LEFT_CHEST,  Items.KINSTONE,        None,     (0x2D1C, 0x40), 0x0032, None),
    LocationData(6029520, TMCLocation.NORTH_FIELD_TREE_FUSION_BOTTOM_RIGHT_CHEST, None,                  None,     (0x2D1C, 0x80), 0x0032, None),
    LocationData(6029521, TMCLocation.NORTH_FIELD_TREE_FUSION_CENTER_BIG_CHEST,   Items.MAGIC_BOOMERANG, None,     (0x2D1D, 0x01), 0x0032, None),
    LocationData(6029522, TMCLocation.NORTH_FIELD_WATERFALL_FUSION_DOJO_NPC,      Items.LONG_SPIN,       None,     (0x2EA6, 0x20), None,   None),
]

all_locations: typing.List[MinishCapLocation] = (south_field
    + castle_exterior
    + eastern_hills
    + lonlon
    + lower_falls
    + lake_hylia
    + minish_woods
    + trilby_highlands
    + western_woods
    + crenel
    + swamp
    + ruins
    + valley
    + dungeon_crypt
    + upper_falls
    + clouds
    + wind_tribe
    + dungeon_dws
    + dungeon_cof
    + dungeon_fow
    + dungeon_tod
    + dungeon_pow
    + sanctuary
    + dungeon_dhc
    + hyrule_town
    + north_field
)

location_table_by_name: typing.Dict[str, int] = {location.name: location for location in all_locations}
