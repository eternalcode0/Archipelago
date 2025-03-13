from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from settings import get_settings
from BaseClasses import Item

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

def write_tokens(world: "MinishCapWorld", patch: MinishCapProcedurePatch) -> None:
    # Patch Items into Locations
    for location_name in location_table_by_name.keys():
        if location_name in world.disabled_locations:
            continue
        location = world.get_location(location_name)
        item = location.item
        loc = location_table_by_name[location.name]
        # Temporary if statement until I fill in all the rom addresses for each location
        if loc.rom_addr[0] is not None:
            item_inject(world, patch, location_table_by_name[location.name], item)

    patch.write_file("token_data.bin", patch.get_token_binary())

def item_inject(world: "MinishCapWorld", patch: MinishCapProcedurePatch, location: LocationData, item: Item):
    # If the item belongs to that player than just use that item id (sprite id?)
    it = item_table[item.name]

    if item.player == world.player:
        # If the location has a secondary address for the sub id, write to the 2 different addresses
        if location.rom_addr[1] is not None:
            patch.write_token(APTokenTypes.WRITE, location.rom_addr[0], bytes([it.byte_ids[0]]))
            patch.write_token(APTokenTypes.WRITE, location.rom_addr[1], bytes([it.byte_ids[1]]))
        # Otherwise the sub id should be immediately after the first address
        else:
            patch.write_token(APTokenTypes.WRITE, location.rom_addr[0], bytes(list(it.byte_ids)))
    # Else use a substitute item id (sprite id?)
    else:
        patch.write_token(APTokenTypes.WRITE, location.rom_addr[0], bytes([0x18])) # Debug Book (Eventually use a patched in AP logo item? Prob item id 0x5A)
