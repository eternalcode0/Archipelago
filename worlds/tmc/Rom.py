import struct
from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification
from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from .constants import EXTERNAL_ITEM_MAP, TMCLocation, TMCItem
from .Items import item_table
from .Locations import location_table_by_name, LocationData
from .Options import ShuffleElements

if TYPE_CHECKING:
    from . import MinishCapWorld


class MinishCapProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "The Minish Cap"
    hash = "2af78edbe244b5de44471368ae2b6f0b"
    patch_file_ending = ".aptmc"
    result_file_ending = ".gba"

    procedure = [("apply_bsdiff4", ["base_patch.bsdiff4"]), ("apply_tokens", ["token_data.bin"])]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().tmc_options.rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        return base_rom_bytes


def write_tokens(world: "MinishCapWorld", patch: MinishCapProcedurePatch) -> None:
    # Bake player name into ROM
    patch.write_token(APTokenTypes.WRITE, 0x000600, world.multiworld.player_name[world.player].encode("UTF-8"))

    # Bake seed name into ROM
    patch.write_token(APTokenTypes.WRITE, 0x000620, world.multiworld.seed_name.encode("UTF-8"))

    # Sanctuary fix
    if world.options.goal_vaati.value:
        # Skip stained glass scene
        patch.write_token(APTokenTypes.WRITE, 0x0532F6, bytes([0x10, 0x23]))
    else:
        # Jump to credits on the stained glass scene
        func = [0x00, 0x22, 0x05, 0x48, 0x04, 0x23, 0x03, 0x70, 0x42, 0x70, 0x82, 0x70, 0x01, 0x23, 0x8B, 0x71, 0x00,
                0x24, 0x78, 0x20, 0x01, 0x4B, 0x00, 0x00, 0x02, 0x10, 0x00, 0x03, 0xFF, 0x32, 0x05, 0x08]
        patch.write_token(APTokenTypes.WRITE, 0x0532F4, bytes(func))

    # Goal Settings
    if world.options.goal_vaati.value:
        # 0b0000_0001 = Goal Vaati
        # 0b0000_0010 = Open DHC
        patch.write_token(APTokenTypes.WRITE, 0xFE0000, bytes([1]))

    # Pedestal Settings
    if 0 <= world.options.ped_elements.value <= 4:
        patch.write_token(APTokenTypes.WRITE, 0xFE0001, bytes([world.options.ped_elements.value]))
    if 0 <= world.options.ped_swords.value <= 5:
        patch.write_token(APTokenTypes.WRITE, 0xFE0002, bytes([world.options.ped_swords.value]))
    if 0 <= world.options.ped_dungeons.value <= 6:
        patch.write_token(APTokenTypes.WRITE, 0xFE0003, bytes([world.options.ped_dungeons.value]))
    # if 0 <= world.options.ped_figurines.value <= 136:
    #     patch.write_token(APTokenTypes.WRITE, 0xFE0004, bytes([world.options.ped_figurines.value]))

    # Element map update
    if world.options.shuffle_elements.value == ShuffleElements.option_dungeon_prize:
        # Pack 1 = world map x pos: u8, world map y pos: u8,
        # Skip 1 byte in between (the ui element icon)
        # Pack 2 = region map x pos: u16, region map y pos: u16
        prize_locs = {TMCLocation.DEEPWOOD_PRIZE: [[0xB2, 0x7A], [0x0D6C, 0x0AC0]],
                      TMCLocation.COF_PRIZE: [[0x3B, 0x1B], [0x01E8, 0x0178]],
                      TMCLocation.FORTRESS_PRIZE: [[0x4B, 0x77], [0x0378, 0x0A78]],
                      TMCLocation.DROPLETS_PRIZE: [[0xB5, 0x4B], [0x0DB8, 0x0638]],
                      TMCLocation.CRYPT_PRIZE: [[0x5A, 0x15], [0x04DC, 0x0148]],
                      TMCLocation.PALACE_PRIZE: [[0xB5, 0x1B], [0x0D88, 0x00E8]]}
        element_address = {TMCItem.EARTH_ELEMENT: 0x128699,
                           TMCItem.FIRE_ELEMENT: 0x1286A1,
                           TMCItem.WIND_ELEMENT: 0x1286A9,
                           TMCItem.WATER_ELEMENT: 0x1286B1}
        for loc, data in prize_locs.items():
            placed_item = world.get_location(loc).item.name
            if element_address.get(placed_item, 0) == 0:
                continue
            patch.write_token(APTokenTypes.WRITE, element_address[placed_item], struct.pack("<BB", *data[0]))
            patch.write_token(APTokenTypes.WRITE, element_address[placed_item]+3, struct.pack("<HH", *data[1]))
    elif world.options.shuffle_elements.value != ShuffleElements.option_vanilla:
        patch.write_token(APTokenTypes.WRITE, 0x128673, bytes([0x0, 0xF, 0x0, 0xF, 0x0, 0xF, 0x0]))

    # Patch Items into Locations
    for location_name, loc in location_table_by_name.items():
        if loc.rom_addr is None:
            continue
        if location_name in world.disabled_locations and (
                loc.vanilla_item is None or loc.vanilla_item in item_table and item_table[
                    loc.vanilla_item].classification != ItemClassification.filler):
            if loc.rom_addr[0] is None:
                continue
            item_inject(world, patch, location_table_by_name[location_name], world.create_item(TMCItem.RUPEES_1))
            continue
        if location_name in world.disabled_locations:
            continue
        location = world.get_location(location_name)
        item = location.item
        # Temporary if statement until I fill in all the rom addresses for each location
        if loc.rom_addr is not None and loc.rom_addr[0] is not None:
            item_inject(world, patch, location_table_by_name[location.name], item)

    patch.write_file("token_data.bin", patch.get_token_binary())


def item_inject(world: "MinishCapWorld", patch: MinishCapProcedurePatch, location: LocationData, item: Item):
    item_byte_first = 0x00
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
            write_single_byte(patch, loc2 or loc1 + 1, item_byte_second)
    else:
        loc2 = location.rom_addr[1] or location.rom_addr[0] + 1
        write_single_byte(patch, location.rom_addr[0], item_byte_first)
        write_single_byte(patch, loc2, item_byte_second)


def write_single_byte(patch: MinishCapProcedurePatch, address: int, byte: int):
    if address is None:
        return
    if byte is None:
        byte = 0x00
    patch.write_token(APTokenTypes.WRITE, address, bytes([byte]))
