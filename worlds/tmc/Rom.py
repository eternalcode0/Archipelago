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
    # Test write static item into static location
    # Smith house chest - Area 0x22 - Room 0x11 - Number - 0x00
    # patch.write_token(APTokenTypes.WRITE, 0xf25aa, bytes([0x36]))
    # Minish barrel - Doesn't work
    # patch.write_token(APTokenTypes.WRITE, 0xDA283, bytes([0x36]))
    # Minish Dock - Area 01 - Room 01
    # patch.write_token(APTokenTypes.WRITE, 0xDBCC7, bytes([0x36]))

    # Deepwood Shrine - Area 48 - Room 04
    # patch.write_token(APTokenTypes.WRITE, 0xDE176, bytes([0x36]))

    # Patch Items into Locations
    for location_name in location_table_by_name.keys():
        if location_name in world.disabled_locations:
            continue
        location = world.get_location(location_name)
        item = location.item
        loc = location_table_by_name[location.name]
        # Temporary if statement until I fill in all the rom addresses for each location
        if loc.romLoc is not None and isinstance(loc.romLoc, int):
            item_inject(world, patch, location_table_by_name[location.name], item)

    patch.write_file("token_data.bin", patch.get_token_binary())

def item_inject(world: "MinishCapWorld", patch: MinishCapProcedurePatch, location: LocationData, item: Item):
    # If the item belongs to that player than just use that item id (sprite id?)
    it = item_table[item.name]
    if it.subID != 0x00:
        print(it)
    if item.player == world.player:
        if location.romSubLoc is not None:
            patch.write_token(APTokenTypes.WRITE, location.romLoc, bytes([it.itemID]))
            patch.write_token(APTokenTypes.WRITE, location.romSubLoc, bytes([it.subID]))
        else:
            patch.write_token(APTokenTypes.WRITE, location.romLoc, bytes([it.itemID, it.subID]))
    # Else use a substitute item id (sprite id?)
    else:
        patch.write_token(APTokenTypes.WRITE, location.romLoc, bytes([0x5A])) # Debug Book (Eventually use a patched in AP logo item? Prob item id 0x5A)
