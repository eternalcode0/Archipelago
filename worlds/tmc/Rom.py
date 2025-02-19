from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from settings import get_settings
from BaseClasses import Item

from .Locations import location_table, all_locations
from .Items import itemList, item_table

class MinishCapProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "The Legend of Zelda - The Minish Cap"
    hash = "2af78edbe244b5de44471368ae2b6f0b"
    patch_file_ending = ".aptmc"
    result_file_ending = ".gba"

    procedure = [
        # ("apply_bsdiff4", ["base_patch.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().tmc_options.rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        return base_rom_bytes

def write_tokens(world: "MinishCapWorld", patch: MinishCapProcedurePatch) -> None:
    # Intro skip
    # patch.write_token(APTokenTypes.WRITE, 0x2002ce4, bytes([0x40]))

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
    # for location_name in location_table.keys():
    #     if location_name in world.disabled_locations:
    #         continue
    #     location = world.get_location(location_name)
    #     item = location.item
    #     print(location.address)
    #     # address = [address for address in all_locations if address.name == location.name]
    #     item_inject(world, patch, location.address, item)

    patch.write_file("token_data.bin", patch.get_token_binary())

def item_inject(world: "MinishCapWorld", patch: MinishCapProcedurePatch, location: int, item: Item):
    # If the item belongs to that player than just use that item id (sprite id?)
    if item.player == world.player:
        code = item_table[item.name].itemID
    # Else use a substitute item id (sprite id?)
    else:
        code = 0x18 # Debug Book (Eventually use a patched in AP logo item? Prob item id 0x5A)
    patch.write_token(APTokenTypes.WRITE, location, bytes([code]))
