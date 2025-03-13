import typing

from BaseClasses import Item, ItemClassification

class ItemData(typing.NamedTuple):
    item_name: str
    classification: ItemClassification
    byte_ids: typing.Tuple[int, int]
    handler: typing.Callable[[object, object], bool] = None

    @property
    def item_id(self): return (self.byte_ids[0] << 8) + self.byte_ids[1]


class MinishCapItem(Item):
    game: str = "The Minish Cap"

def handler_flag(ram_address: int, bit_flag: int):
    async def handler(bizhawk, ctx) -> bool:
        read_result: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(ram_address, 1, "EWRAM")]))[0]
        current = int.from_bytes(read_result, "little")
        new: int = current | bit_flag

        # Write to the address if it hasn't changed
        return await bizhawk.guarded_write(
            ctx.bizhawk_ctx,
            [(ram_address, [new], "EWRAM")],
            [(ram_address, [current], "EWRAM")]
        )
    return handler

SMITHS_SWORD          = ItemData("Smith's Sword",                ItemClassification.progression, (0x01, 0x00), handler_flag(0x2B32, 0x04))
WHITE_SWORD_GREEN     = ItemData("White Sword (Green)",          ItemClassification.progression, (0x02, 0x00), None)
WHITE_SWORD_RED       = ItemData("White Sword (Red)",            ItemClassification.progression, (0x03, 0x00), None)
WHITE_SWORD_BLUE      = ItemData("White Sword (Blue)",           ItemClassification.progression, (0x04, 0x00), None)
# UNUSED_SWORD        = ItemData("Unused Sword",                 ItemClassification.progression, (0x05, 0x00), None)
FOUR_SWORD            = ItemData("Four Sword",                   ItemClassification.progression, (0x06, 0x00), None)
BOMB                  = ItemData("Bomb",                         ItemClassification.progression, (0x07, 0x00), None)
REMOTE_BOMB           = ItemData("Remote Bomb",                  ItemClassification.progression, (0x08, 0x00), None)
BOW                   = ItemData("Bow",                          ItemClassification.progression, (0x09, 0x00), None)
LIGHT_ARROW           = ItemData("Light Arrow",                  ItemClassification.progression, (0x0A, 0x00), None)
BOOMERANG             = ItemData("Boomerang",                    ItemClassification.progression, (0x0B, 0x00), None)
MAGIC_BOOMERANG       = ItemData("Magic Boomerang",              ItemClassification.progression, (0x0C, 0x00), None)
SHIELD                = ItemData("Shield",                       ItemClassification.progression, (0x0D, 0x00), handler_flag(0x2B35, 0x04))
MIRROR_SHIELD         = ItemData("Mirror Shield",                ItemClassification.progression, (0x0E, 0x00), None)
# LANTERN             = ItemData("Lantern",                      ItemClassification.progression, (0x0F, 0x00), None) Lantern has two different item ids representing on and off
LANTERN               = ItemData("Lantern",                      ItemClassification.progression, (0x10, 0x00), handler_flag(0x2B35, 0x40))
GUST_JAR              = ItemData("Gust Jar",                     ItemClassification.progression, (0x11, 0x00), handler_flag(0x2B36, 0x04))
CANE_OF_PACCI         = ItemData("Cane of Pacci",                ItemClassification.progression, (0x12, 0x00), handler_flag(0x2B36, 0x10))
MOLE_MITTS            = ItemData("Mole Mitts",                   ItemClassification.progression, (0x13, 0x00), handler_flag(0x2B36, 0x40))
ROCS_CAPE             = ItemData("Roc's Cape",                   ItemClassification.progression, (0x14, 0x00), handler_flag(0x2B37, 0x01))
PEGASUS_BOOTS         = ItemData("Pegasus Boots",                ItemClassification.progression, (0x15, 0x00), handler_flag(0x2B37, 0x04))
# FIRE_ROD            = ItemData("Fire Rod",                     ItemClassification.progression, (0x16, 0x00), None) Fire rod is a leftover item from development that wasn't used
OCARINA               = ItemData("Ocarina",                      ItemClassification.progression, (0x17, 0x00), handler_flag(0x2B37, 0x40))
# DEBUG_BOOK          = ItemData("Debug Book",                   ItemClassification.progression, (0x18, 0x00), None)
# DEBUG_MUSHROOM      = ItemData("Debug Mushroom",               ItemClassification.progression, (0x19, 0x00), None)
# DEBUG_FLIPPERS      = ItemData("Debug Flippers",               ItemClassification.progression, (0x1A, 0x00), None)
# DEBUG_LANTERN       = ItemData("Debug Lantern",                ItemClassification.progression, (0x1B, 0x00), None)
BOTTLE_1              = ItemData("Bottle 1",                     ItemClassification.progression, (0x1C, 0x00), None) # Each bottle has a different item id?
BOTTLE_2              = ItemData("Bottle 2",                     ItemClassification.progression, (0x1D, 0x00), None) # Each bottle has a different item id?
BOTTLE_3              = ItemData("Bottle 3",                     ItemClassification.progression, (0x1E, 0x00), None) # Each bottle has a different item id?
BOTTLE_4              = ItemData("Bottle 4",                     ItemClassification.progression, (0x1F, 0x00), None) # Each bottle has a different item id?
EMPTY_BOTTLE          = ItemData("Empty Bottle",                 ItemClassification.progression, (0x20, 0x00), None) # Now I'm really confused...
# LON_LON_BUTTER      = ItemData("Lon Lon Butter",               ItemClassification.progression, (0x21, 0x00), None)
LON_LON_MILK          = ItemData("Lon Lon Milk",                 ItemClassification.progression, (0x22, 0x00), None) # Bottle contents
LON_LON_MILK_HALF     = ItemData("Lon Lon Milk (1/2)",           ItemClassification.progression, (0x23, 0x00), None) # Bottle contents
RED_POTION            = ItemData("Red Potion",                   ItemClassification.progression, (0x24, 0x00), None) # Bottle contents
BLUE_POTION           = ItemData("Blue Potion",                  ItemClassification.progression, (0x25, 0x00), None) # Bottle contents
WATER                 = ItemData("Water",                        ItemClassification.progression, (0x26, 0x00), None) # Bottle contents
MINERAL_WATER         = ItemData("Mineral Water",                ItemClassification.progression, (0x27, 0x00), None) # Bottle contents
BOTTLED_FAIRY         = ItemData("Bottled Fairy",                ItemClassification.progression, (0x28, 0x00), None) # Bottle contents
RED_PICOLYTE          = ItemData("Red Picolyte",                 ItemClassification.progression, (0x29, 0x00), None) # Bottle contents
ORANGE_PICOLYTE       = ItemData("Orange Picolyte",              ItemClassification.progression, (0x2A, 0x00), None) # Bottle contents
YELLOW_PICOLYTE       = ItemData("Yellow Picolyte",              ItemClassification.progression, (0x2B, 0x00), None) # Bottle contents
GREEN_PICOLYTE        = ItemData("Green Picolyte",               ItemClassification.progression, (0x2C, 0x00), None) # Bottle contents
BLUE_PICOLYTE         = ItemData("Blue Picolyte",                ItemClassification.progression, (0x2D, 0x00), None) # Bottle contents
WHITE_PICOLYTE        = ItemData("White Picolyte",               ItemClassification.progression, (0x2E, 0x00), None) # Bottle contents
NAYRU_CHARM           = ItemData("Nayru Charm",                  ItemClassification.progression, (0x2F, 0x00), None) # Bottle contents
FARORE_CHARM          = ItemData("Farore Charm",                 ItemClassification.progression, (0x30, 0x00), None) # Bottle contents
DINS_CHARM            = ItemData("Dins Charm",                   ItemClassification.progression, (0x31, 0x00), None) # Bottle contents
# UNUSED              = ItemData("Unused",                       ItemClassification.progression, (0x32, 0x00), None)
# UNUSED              = ItemData("Unused",                       ItemClassification.progression, (0x33, 0x00), None)
SMITH_SWORD_QUEST     = ItemData("Smith Sword (Quest)",          ItemClassification.progression, (0x34, 0x00), None)
BROKEN_PICORI_BLADE   = ItemData("Broken Picori Blade",          ItemClassification.progression, (0x35, 0x00), None)
DOG_FOOD              = ItemData("Dog Food",                     ItemClassification.progression, (0x36, 0x00), None) # Bottle contents
LONLON_KEY            = ItemData("LonLon Key",                   ItemClassification.progression, (0x37, 0x00), None)
WAKEUP_MUSHROOM       = ItemData("Wakeup Mushroom",              ItemClassification.progression, (0x38, 0x00), None)
RED_BOOK              = ItemData("Red Book (Hyrulian Bestiary)", ItemClassification.progression, (0x39, 0x00), None)
GREEN_BOOK            = ItemData("Green Book (Picori Legend)",   ItemClassification.progression, (0x3A, 0x00), None)
BLUE_BOOK             = ItemData("Blue Book (History of Masks)", ItemClassification.progression, (0x3B, 0x00), None)
GRAVEYARD_KEY         = ItemData("Graveyard Key",                ItemClassification.progression, (0x3C, 0x00), None)
TINGLE_TROPHY         = ItemData("Tingle Trophy",                ItemClassification.progression, (0x3D, 0x00), None)
CARLOV_MEDAL          = ItemData("Carlov Medal",                 ItemClassification.progression, (0x3E, 0x00), None)
# SHELLS              = ItemData("Shells",                       ItemClassification.progression, (0x3F, 0x00), None)
EARTH_ELEMENT         = ItemData("Earth Element",                ItemClassification.progression, (0x40, 0x00), handler_flag(0x2B42, 0x01))
FIRE_ELEMENT          = ItemData("Fire Element",                 ItemClassification.progression, (0x41, 0x00), None)
WATER_ELEMENT         = ItemData("Water Element",                ItemClassification.progression, (0x42, 0x00), None)
WIND_ELEMENT          = ItemData("Wind Element",                 ItemClassification.progression, (0x43, 0x00), None)
GRIP_RING             = ItemData("Grip Ring",                    ItemClassification.progression, (0x44, 0x00), None)
POWER_BRACELETS       = ItemData("Power Bracelets",              ItemClassification.progression, (0x45, 0x00), None)
FLIPPERS              = ItemData("Flippers",                     ItemClassification.progression, (0x46, 0x00), None)
HYRULE_MAP            = ItemData("Hyrule Map",                   ItemClassification.progression, (0x47, 0x00), None)
SPIN_ATTACK           = ItemData("Spin Attack",                  ItemClassification.progression, (0x48, 0x00), None)
ROLL_ATTACK           = ItemData("Roll Attack",                  ItemClassification.progression, (0x49, 0x00), None)
DASH_ATTACK           = ItemData("Dash Attack",                  ItemClassification.progression, (0x4A, 0x00), None)
ROCK_BREAKER          = ItemData("Rock Breaker",                 ItemClassification.progression, (0x4B, 0x00), None)
SWORD_BEAM            = ItemData("Sword Beam",                   ItemClassification.progression, (0x4C, 0x00), None)
GREATSPIN             = ItemData("Greatspin",                    ItemClassification.progression, (0x4D, 0x00), None)
DOWNTHRUST            = ItemData("DownThrust",                   ItemClassification.progression, (0x4E, 0x00), None)
PERIL_BEAM            = ItemData("Peril Beam",                   ItemClassification.progression, (0x4F, 0x00), None)
RUPEES_1              = ItemData("1 Rupee",                      ItemClassification.filler, (0x54, 0x00), None)
RUPEES_5              = ItemData("5 Rupees",                     ItemClassification.filler, (0x55, 0x00), None)
RUPEES_20             = ItemData("20 Rupees",                    ItemClassification.filler, (0x56, 0x00), None)
RUPEES_50             = ItemData("50 Rupees",                    ItemClassification.filler, (0x57, 0x00), None)
RUPEES_100            = ItemData("100 Rupees",                   ItemClassification.filler, (0x58, 0x00), None)
RUPEES_200            = ItemData("200 Rupees",                   ItemClassification.filler, (0x59, 0x00), None)
# UNUSED              = ItemData("Unused",                       ItemClassification.progression, (0x5A, 0x00), None)
JABBER_NUT            = ItemData("Jabber Nut",                   ItemClassification.progression, (0x5B, 0x00), handler_flag(0x2B48, 0x40))
KINSTONE              = ItemData("Broken Kinstone (Report Me!)", ItemClassification.progression, (0x5C, 0x00), None)
KINSTONE_GOLD_CLOUD   = ItemData("Kinstone Cloud Tops",          ItemClassification.progression, (0x5C, 0x65), None)
KINSTONE_GOLD_SWAMP   = ItemData("Kinstone Swamps",              ItemClassification.progression, (0x5C, 0x6A), None)
KINSTONE_GOLD_FALLS   = ItemData("Kinstone Falls",               ItemClassification.progression, (0x5C, 0x6D), None)
KINSTONE_RED_W        = ItemData("Kinstone Red W",               ItemClassification.progression, (0x5C, 0x6E), None)
KINSTONE_RED_ANGLE    = ItemData("Kinstone Red >",               ItemClassification.progression, (0x5C, 0x6F), None)
KINSTONE_RED_E        = ItemData("Kinstone Red E",               ItemClassification.progression, (0x5C, 0x70), None)
KINSTONE_BLUE_L       = ItemData("Kinstone Blue L",              ItemClassification.progression, (0x5C, 0x71), None)
KINSTONE_BLUE_6       = ItemData("Kinstone Blue 6",              ItemClassification.progression, (0x5C, 0x72), None)
KINSTONE_GREEN_ANGLE  = ItemData("Kinstone Green <",             ItemClassification.progression, (0x5C, 0x73), None)
KINSTONE_GREEN_SQUARE = ItemData("Kinstone Green [",             ItemClassification.progression, (0x5C, 0x74), None)
KINSTONE_GREEN_P      = ItemData("Kinstone Green P",             ItemClassification.progression, (0x5C, 0x75), None)
BOMB_REFILL_5         = ItemData("5 Bomb Refill",                ItemClassification.filler, (0x5D, 0x00), None)
ARROW_REFILL_5        = ItemData("5 Arrow Refill",               ItemClassification.filler, (0x5E, 0x00), None)
HEART_REFILL          = ItemData("Heart Refill",                 ItemClassification.filler, (0x5F, 0x00), None)
# FAIRY_REFILL        = ItemData("Fairy Refill",                 ItemClassification.filler, (0x60, 0x00), None) ???
# SHELLS_30           = ItemData("30 Shells",                    ItemClassification.progression, (0x61, 0x00), None)
HEART_CONTAINER       = ItemData("Heart Container",              ItemClassification.progression, (0x62, 0x00), None)
HEART_PIECE           = ItemData("Heart Piece",                  ItemClassification.progression, (0x63, 0x00), None)
BIG_WALLET            = ItemData("Big Wallet",                   ItemClassification.progression, (0x64, 0x00), None)
BOMB_BAG              = ItemData("Bomb Bag",                     ItemClassification.progression, (0x65, 0x00), None)
QUIVER                = ItemData("Quiver",                       ItemClassification.progression, (0x66, 0x00), None)
# KINSTONE_BAG        = ItemData("Kinstone Bag",                 ItemClassification.progression, (0x67, 0x00), None) Given to the player immediately via basepatch
# BRIOCHE             = ItemData("Brioche",                      ItemClassification.filler, (0x68, 0x00), None) Unused in the rando so far
# CROISSANT           = ItemData("Croissant",                    ItemClassification.filler, (0x69, 0x00), None)
# PIE                 = ItemData("Pie",                          ItemClassification.filler, (0x6A, 0x00), None)
# CAKE                = ItemData("Cake",                         ItemClassification.filler, (0x6B, 0x00), None)
BOMB_REFILL_10        = ItemData("10 Bomb Refill",               ItemClassification.filler, (0x6C, 0x00), None)
BOMB_REFILL_30        = ItemData("30 Bomb Refill",               ItemClassification.filler, (0x6D, 0x00), None)
ARROW_REFILL_10       = ItemData("10 Arrow Refill",              ItemClassification.filler, (0x6E, 0x00), None)
ARROW_REFILL_30       = ItemData("30 Arrow Refill",              ItemClassification.filler, (0x6F, 0x00), None)
BOW_BUTTERFLY         = ItemData("Bow Butterfly",                ItemClassification.useful, (0x70, 0x00), None)
DIG_BUTTERFLY         = ItemData("Dig Butterfly",                ItemClassification.useful, (0x71, 0x00), None)
SWIM_BUTTERFLY        = ItemData("Swim Butterfly",               ItemClassification.useful, (0x72, 0x00), None)
FAST_SPIN_SCROLL      = ItemData("Fast Spin Scroll",             ItemClassification.useful, (0x73, 0x00), None)
FAST_SPLIT_SCROLL     = ItemData("Fast Split Scroll",            ItemClassification.useful, (0x74, 0x00), None)
LONG_SPIN             = ItemData("Long Spin",                    ItemClassification.useful, (0x75, 0x00), None)

DUNGEON_MAP_DWS = ItemData("Dungeon Map (DWS)",                  ItemClassification.useful, (0x50, 0x18), None)
DUNGEON_MAP_COF = ItemData("Dungeon Map (CoF)",                  ItemClassification.useful, (0x50, 0x19), None)
DUNGEON_MAP_FOW = ItemData("Dungeon Map (FoW)",                  ItemClassification.useful, (0x50, 0x1A), None)
DUNGEON_MAP_TOD = ItemData("Dungeon Map (ToD)",                  ItemClassification.useful, (0x50, 0x1B), None)
DUNGEON_MAP_POW = ItemData("Dungeon Map (PoW)",                  ItemClassification.useful, (0x50, 0x1C), None)
DUNGEON_MAP_DHC = ItemData("Dungeon Map (DHC)",                  ItemClassification.useful, (0x50, 0x1D), None)

DUNGEON_COMPASS_DWS = ItemData("Dungeon Compass (DWS)",          ItemClassification.useful, (0x51, 0x18), None)
DUNGEON_COMPASS_COF = ItemData("Dungeon Compass (CoF)",          ItemClassification.useful, (0x51, 0x19), None)
DUNGEON_COMPASS_FOW = ItemData("Dungeon Compass (FoW)",          ItemClassification.useful, (0x51, 0x1A), None)
DUNGEON_COMPASS_TOD = ItemData("Dungeon Compass (ToD)",          ItemClassification.useful, (0x51, 0x1B), None)
DUNGEON_COMPASS_POW = ItemData("Dungeon Compass (PoW)",          ItemClassification.useful, (0x51, 0x1C), None)
DUNGEON_COMPASS_DHC = ItemData("Dungeon Compass (DHC)",          ItemClassification.useful, (0x51, 0x1D), None)

BIG_KEY_DWS = ItemData("Big Key (DWS)",                          ItemClassification.progression, (0x52, 0x18), None)
BIG_KEY_COF = ItemData("Big Key (CoF)",                          ItemClassification.progression, (0x52, 0x19), None)
BIG_KEY_FOW = ItemData("Big Key (FoW)",                          ItemClassification.progression, (0x52, 0x1A), None)
BIG_KEY_TOD = ItemData("Big Key (ToD)",                          ItemClassification.progression, (0x52, 0x1B), None)
BIG_KEY_POW = ItemData("Big Key (PoW)",                          ItemClassification.progression, (0x52, 0x1C), None)
BIG_KEY_DHC = ItemData("Big Key (DHC)",                          ItemClassification.progression, (0x52, 0x1D), None)

SMALL_KEY_DWS = ItemData("Small Key (DWS)",                      ItemClassification.progression, (0x53, 0x18), None)
SMALL_KEY_COF = ItemData("Small Key (CoF)",                      ItemClassification.progression, (0x53, 0x19), None)
SMALL_KEY_FOW = ItemData("Small Key (FoW)",                      ItemClassification.progression, (0x53, 0x1A), None)
SMALL_KEY_TOD = ItemData("Small Key (ToD)",                      ItemClassification.progression, (0x53, 0x1B), None)
SMALL_KEY_POW = ItemData("Small Key (PoW)",                      ItemClassification.progression, (0x53, 0x1C), None)
SMALL_KEY_DHC = ItemData("Small Key (DHC)",                      ItemClassification.progression, (0x53, 0x1D), None)
SMALL_KEY_RC  = ItemData("Small Key (RC)",                       ItemClassification.progression, (0x53, 0x1E), None)

def pool_baseitems() -> [ItemData]:
    return [
        EARTH_ELEMENT,
        FIRE_ELEMENT,
        WATER_ELEMENT,
        WIND_ELEMENT,

        SMITHS_SWORD,
        WHITE_SWORD_GREEN,
        WHITE_SWORD_RED,
        WHITE_SWORD_BLUE,
        FOUR_SWORD,

        SHIELD,
        MIRROR_SHIELD,

        JABBER_NUT,
        GUST_JAR,
        LANTERN,
        CANE_OF_PACCI,
        ROCS_CAPE,
        PEGASUS_BOOTS,
        OCARINA,

        FLIPPERS,
        SWIM_BUTTERFLY,

        MOLE_MITTS,
        DIG_BUTTERFLY,

        BOMB,
        REMOTE_BOMB,
        BOMB_BAG,
        BOMB_BAG,
        BOMB_BAG,

        BOW,
        LIGHT_ARROW,
        BOW_BUTTERFLY,
        QUIVER,
        QUIVER,
        QUIVER,

        BOOMERANG,
        MAGIC_BOOMERANG,

        EMPTY_BOTTLE,
        EMPTY_BOTTLE,
        EMPTY_BOTTLE,
        DOG_FOOD,

        RUPEES_1,
        RUPEES_5,
        RUPEES_20,
        RUPEES_50,
        RUPEES_100,
        RUPEES_200,
        BIG_WALLET,
        BIG_WALLET,
        BIG_WALLET,

        SPIN_ATTACK,
        ROLL_ATTACK,
        DASH_ATTACK,
        ROCK_BREAKER,
        SWORD_BEAM,
        GREATSPIN,
        DOWNTHRUST,
        PERIL_BEAM,
        FAST_SPIN_SCROLL,
        FAST_SPLIT_SCROLL,
        LONG_SPIN,

        TINGLE_TROPHY,
        CARLOV_MEDAL,
        GRIP_RING,
        POWER_BRACELETS,
        LONLON_KEY,
        GRAVEYARD_KEY,
        RED_BOOK,
        GREEN_BOOK,
        BLUE_BOOK,
    ]

def pool_dungeonmaps() -> [ItemData]:
    return [
        DUNGEON_MAP_DWS,
        DUNGEON_MAP_COF,
        DUNGEON_MAP_FOW,
        DUNGEON_MAP_TOD,
        DUNGEON_MAP_POW,
        DUNGEON_MAP_DHC,
    ]

def pool_compass() -> [ItemData]:
    return [
        DUNGEON_COMPASS_DWS,
        DUNGEON_COMPASS_COF,
        DUNGEON_COMPASS_FOW,
        DUNGEON_COMPASS_TOD,
        DUNGEON_COMPASS_POW,
        DUNGEON_COMPASS_DHC,
    ]

def pool_bigkeys() -> [ItemData]:
    return [
        BIG_KEY_DWS,
        BIG_KEY_COF,
        BIG_KEY_FOW,
        BIG_KEY_TOD,
        BIG_KEY_POW,
        BIG_KEY_DHC,
    ]

def pool_smallkeys() -> [ItemData]:
    return [
        *[*[SMALL_KEY_DWS] * 4],
        *[*[SMALL_KEY_COF] * 2],
        *[*[SMALL_KEY_FOW] * 4],
        *[*[SMALL_KEY_TOD] * 4],
        *[*[SMALL_KEY_POW] * 6],
        *[*[SMALL_KEY_DHC] * 5],
        *[*[SMALL_KEY_RC] * 3],
    ]

def pool_kinstone_gold() -> [ItemData]:
    return [
        *[*[KINSTONE_GOLD_CLOUD] * 5],
        *[*[KINSTONE_GOLD_SWAMP] * 3],
        *[*[KINSTONE_GOLD_FALLS] * 1],
    ]

def pool_kinstone_red() -> [ItemData]:
    return [
        *[*[KINSTONE_RED_W] * 9],
        *[*[KINSTONE_RED_ANGLE] * 7],
        *[*[KINSTONE_RED_E] * 8],
    ]

def pool_kinstone_blue() -> [ItemData]:
    return [
        *[*[KINSTONE_BLUE_L] * 9],
        *[*[KINSTONE_BLUE_6] * 9],
    ]

def pool_kinstone_green() -> [ItemData]:
    return [
        *[*[KINSTONE_GREEN_ANGLE] * 17],
        *[*[KINSTONE_GREEN_SQUARE] * 16],
        *[*[KINSTONE_GREEN_P] * 16],
    ]

itemList: typing.List[ItemData] = [
    *(pool_baseitems()),
    *(pool_bigkeys()),
    *(pool_smallkeys()),
    *(pool_dungeonmaps()),
    *(pool_compass()),
    *(pool_kinstone_gold()),
    # *(pool_kinstone_red()),
    # *(pool_kinstone_blue()),
    # *(pool_kinstone_green()),
]

item_frequencies: typing.Dict[str, int] = {
    "1 Rupee": 72,
    "5 Rupees": 98,
    "20 Rupees": 106,
    "50 Rupees": 50,
    "100 Rupees": 36,
    "200 Rupees": 30,
}

item_table: typing.Dict[str, ItemData] = {item.item_name: item for item in itemList}
items_by_id: typing.Dict[int, ItemData] = {item.item_id: item for item in itemList}
