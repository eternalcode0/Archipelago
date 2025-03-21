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
    if item.player == world.player:
        # If the item belongs to that player than just use that item id (sprite id?)
        it = item_table[item.name]
        # If the location has a secondary address for the sub id, write to the 2 different addresses
        if location.rom_addr[1] is not None:
            patch.write_token(APTokenTypes.WRITE, location.rom_addr[0], bytes([it.byte_ids[0]]))
            patch.write_token(APTokenTypes.WRITE, location.rom_addr[1], bytes([it.byte_ids[1]]))
        # Otherwise the sub id should be immediately after the first address
        else:
            patch.write_token(APTokenTypes.WRITE, location.rom_addr[0], bytes(list(it.byte_ids)))
    # Else use a substitute item id (sprite id?)
    else:
        if item.classification not in EXTERNAL_ITEM_MAP:
            patch.write_token(APTokenTypes.WRITE, location.rom_addr[0], bytes([0x18]))
        else:
            item_id = EXTERNAL_ITEM_MAP[item.classification](world.random)
            patch.write_token(APTokenTypes.WRITE, location.rom_addr[0], bytes([item_id]))
