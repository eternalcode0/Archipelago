import typing
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from settings import get_settings
from BaseClasses import Item, ItemClassification

from .Locations import location_table_by_name, all_locations, LocationData
from .Items import itemList, item_table

class MinishCapProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "The Legend of Zelda - The Minish Cap"
    hash = "2af78edbe244b5de44471368ae2b6f0b"
    patch_file_ending = ".aptmc"
    result_file_ending = ".gba"

    procedure = [
        ("apply_bsdiff4", ["base_patch.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().tmc_options.rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        return base_rom_bytes

EXTERNAL_ITEMS = [0x18, 0x19, 0x1A]
EXTERNAL_ITEM_MAP: dict[ItemClassification, typing.Callable[[object], int]] = {
    ItemClassification.filler: lambda random: 0x1A,
    ItemClassification.progression: lambda random: 0x18,
    ItemClassification.useful: lambda random: 0x19,
    ItemClassification.trap: lambda random: random.choice(EXTERNAL_ITEMS),
    ItemClassification.skip_balancing: lambda random: 0x19,
    ItemClassification.progression_skip_balancing: lambda random: 0x18,
}

def write_tokens(world: "MinishCapWorld", patch: MinishCapProcedurePatch) -> None:
    # Patch Items into Locations
    for location_name, loc in location_table_by_name.items():
        if loc.id in world.disabled_locations:
            continue
        location = world.get_location(location_name)
        item = location.item
        # Temporary if statement until I fill in all the rom addresses for each location
        if loc.rom_addr[0] is not None:
            item_inject(world, patch, location_table_by_name[location.name], item)

    patch.write_file("token_data.bin", patch.get_token_binary())

def item_inject(world: "MinishCapWorld", patch: MinishCapProcedurePatch, location: LocationData, item: Item):
    item_byte_first  = 0x00
    item_byte_second = 0x00

    if item.player == world.player:
        # The item belongs to this player's world, it should use local item ids
        item_byte_first = item_table[item.name].byte_ids[0]
        item_byte_second = item_table[item.name].byte_ids[1]
    elif item.classification not in EXTERNAL_ITEM_MAP:
        # The item belongs to an external player's world but we don't recognize the classification
        # default to green clock sprite, also used for progression item
        item_byte_first = 0x18
    else:
        # The item belongs to an external player's world, use the given classification to choose the item sprite
        item_byte_first = EXTERNAL_ITEM_MAP[item.classification](world.random)

    if hasattr(location.rom_addr[0], "__iter__") and hasattr(location.rom_addr[1], "__iter__"):
        for loc1, loc2 in zip(location.rom_addr[0], location.rom_addr[1]):
            write_single_byte(patch, loc1, item_byte_first)
            write_single_byte(patch, loc2, item_byte_second)
    else:
        loc2 = location.rom_addr[1] or location.rom_addr[0] + 1
        write_single_byte(patch, location.rom_addr[0], item_byte_first)
        write_single_byte(patch, loc2, item_byte_second)

def write_single_byte(patch: MinishCapProcedurePatch, address: int, byte: int):
    if address is None:
        return
    if byte is None:
        byte == 0x00
    patch.write_token(APTokenTypes.WRITE, address, bytes([byte]))
