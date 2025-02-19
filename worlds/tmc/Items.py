import typing

from BaseClasses import Item, ItemClassification

BASE_ITEM_ID = 27022001000

class ItemData(typing.NamedTuple):
    code: int
    itemName: str
    classification: ItemClassification
    itemID: int
    """The address in EWRAM to assign when the item is obtained. 1st = address, 2nd = bit flag"""
    address: typing.Tuple[int, int] = None

class MinishCapItem(Item):
    game: str = "The Minish Cap"



itemList: typing.List[ItemData] = [
    ItemData(27022001000, "Smith's Sword", ItemClassification.progression, 0x01, (0x2B32, 0x04)),
    ItemData(27022001001, "Small Shield", ItemClassification.progression, 0x0D, (0x2B35, 0x04)),
    ItemData(27022001002, "Rupee (20)", ItemClassification.filler, 0x56, None),
    ItemData(27022001003, "Jabber Nut", ItemClassification.progression, 0x5B, (0x2B48, 0x40)),
    ItemData(27022001004, "Gust Jar", ItemClassification.progression, 0x11, (0x2B36, 0x04)),
    ItemData(27022001005, "Heart Piece", ItemClassification.useful, 0x63),
    ItemData(27022001006, "Heart Container", ItemClassification.useful, 0x62),
    ItemData(27022001007, "Earth Element", ItemClassification.progression, 0x40, (0x2B42, 0x01)),
    # ItemData(27022001008, "Wallet", ItemClassification.progression, 0x64, (0x2A38, None)) # Only 1 item id per upgrade? | Increments the value for each upgrade
]

item_frequencies: typing.Dict[str, int] = {
    "Rupee (20)": 2,
}

item_table: typing.Dict[str, ItemData] = {item.itemName: item for item in itemList}
