import struct
from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification
from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from .constants import DUNGEON_ABBR, DUNGEON_OFFSET, EXTERNAL_ITEM_MAP, WIND_CRESTS, TMCLocation, TMCItem
from .Items import item_table
from .Locations import location_table_by_name, LocationData
from .Options import ShuffleElements, Kinstones

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

    write_fusion_settings(patch, world)

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

    # Dungeon Warps
    for dungeon in DUNGEON_ABBR:
        if dungeon == "RC":
            continue
        patch.write_token(APTokenTypes.WRITE, 0xFF127A + DUNGEON_OFFSET[dungeon],
                          bytes([world.options.dungeon_warps.get_warps(dungeon, world.options.dungeon_warps.value)]))

    # Wind Crests
    crest_value = 0x0
    enabled_crests = [WIND_CRESTS[crest] for crest in world.options.wind_crests.value]
    enabled_crests.append(0x10)  # Lake Hylia wind crest
    for crest in enabled_crests:
        crest_value |= crest
    patch.write_token(APTokenTypes.WRITE, 0xFF1279, bytes([crest_value]))

    # Patch Items into Locations
    for location_name, loc in location_table_by_name.items():
        if loc.rom_addr is None:
            continue
        if location_name in world.disabled_locations and (
                loc.vanilla_item is None or loc.vanilla_item in item_table and item_table[
                    loc.vanilla_item].classification != ItemClassification.filler):
            if loc.rom_addr[0] is None:
                continue
            item_inject(world, patch, location_table_by_name[location_name], world.create_filler())
            continue
        elif location_name in world.disabled_locations:
            continue
        location = world.get_location(location_name)
        item = location.item
        # Temporary if statement until I fill in all the rom addresses for each location
        if loc.rom_addr is not None and loc.rom_addr[0] is not None:
            item_inject(world, patch, location_table_by_name[location.name], item)

    patch.write_file("token_data.bin", patch.get_token_binary())


def item_inject(world: "MinishCapWorld", patch: MinishCapProcedurePatch, location: LocationData, item: Item):
    # item_byte_first = 0x00
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


# This is a really dumb way of implementing this but...
# write_fusion_settings iterates through this list to figure out whether it should write a bit for each fusion flag
# the outer list represents each flag from 0x2C81-0x2C8D
# the inner list represents the setting that needs to be either vanilla/combined in order to set that bit
FUSION_FLAGS = [
    [None, "kinstones_gold", "kinstones_gold", "kinstones_gold",
     "kinstones_gold", "kinstones_gold", "kinstones_gold", "kinstones_gold"],

    ["kinstones_gold", "kinstones_gold", "kinstones_red", "kinstones_red",
     "kinstones_red", "kinstones_red", "kinstones_red", "kinstones_red"],

    ["kinstones_red", "kinstones_red", "kinstones_red", "kinstones_red",
     "kinstones_red", "kinstones_red", "kinstones_red", "kinstones_red"],

    ["kinstones_red", "kinstones_red", "kinstones_red", "kinstones_red",
     "kinstones_red", "kinstones_red", "kinstones_red", "kinstones_red"],

    ["kinstones_red", "kinstones_red", "kinstones_blue", "kinstones_blue",
     "kinstones_blue", "kinstones_blue", "kinstones_blue", "kinstones_blue"],

    ["kinstones_blue", "kinstones_blue", "kinstones_blue", "kinstones_blue",
     "kinstones_blue", "kinstones_blue", "kinstones_blue", "kinstones_blue"],

    ["kinstones_blue", "kinstones_blue", "kinstones_blue", "kinstones_blue",
     "kinstones_green", "kinstones_green", "kinstones_green", "kinstones_green"],

    ["kinstones_green", "kinstones_green", "kinstones_green", "kinstones_green",
     "kinstones_green", "kinstones_green", "kinstones_green", "kinstones_green"],

    ["kinstones_green", "kinstones_green", "kinstones_green", "kinstones_green",
     "kinstones_green", "kinstones_green", "kinstones_green", "kinstones_green"],

    ["kinstones_green", "kinstones_green", "kinstones_green", "kinstones_green",
     "kinstones_green", "kinstones_green", "kinstones_green", "kinstones_green"],

    ["kinstones_green", "kinstones_green", "kinstones_green", "kinstones_green",
     "kinstones_green", "kinstones_green", "kinstones_green", "kinstones_green"],

    ["kinstones_green", "kinstones_green", "kinstones_green", "kinstones_green",
     "kinstones_green", "kinstones_green", "kinstones_green", "kinstones_green"],

    ["kinstones_green", "kinstones_green", "kinstones_green", "kinstones_green",
     "kinstones_green"],
]


def write_fusion_settings(patch: MinishCapProcedurePatch, world: "MinishCapWorld"):
    # Fusion requests
    placeholder = []
    if world.options.kinstones_gold.value == Kinstones.option_closed:
        patch.write_token(APTokenTypes.WRITE, 0x07E4AE, bytes([0xBD, 0x00]))  # pop {pc}
    if world.options.kinstones_red.value == Kinstones.option_closed:
        placeholder.extend([0x2061, 0x2077, 0x2085, 0x208C, 0x2093, 0x215A, 0x21B6, 0x21BD, 0x2208, 0x2238, 0x2240,
                            0x2241, 0x2248, 0x2249, 0x2250, 0x2251, 0x2270, 0x2296, 0x2297, 0x229E, 0x22C8, 0x22E6,
                            0x22ED, 0x2310, 0x238B])
    if world.options.kinstones_blue.value == Kinstones.option_closed:
        placeholder.extend([0x2127, 0x213E, 0x2199, 0x21FF, 0x2225, 0x2226, 0x2227, 0x2228, 0x2229, 0x222A, 0x2258,
                            0x2259, 0x22C1, 0x22D6, 0x22F4, 0x2348, 0x2349, 0x234A, 0x234B, 0x234C, 0x234D, 0x2354,
                            0x2355, 0x2356, 0x2357, 0x2358, 0x2359, 0x2360, 0x2361, 0x2362, 0x2363, 0x2364, 0x2365,
                            0x236C, 0x236D, 0x236E, 0x236F, 0x2370, 0x2371, 0x2378, 0x2379, 0x237A, 0x237B, 0x237C,
                            0x237D, 0x2384, 0x2399])
    if world.options.kinstones_green.value == Kinstones.option_closed:
        placeholder.extend([0x2062, 0x20AC, 0x20DD, 0x212E, 0x212F, 0x2130, 0x21C4, 0x21CB, 0x21D2, 0x21D3, 0x21DA,
                            0x21DB, 0x2200, 0x2207, 0x220F, 0x2216, 0x221D, 0x221E, 0x2231, 0x2260, 0x2261, 0x2285,
                            0x2286, 0x2287, 0x22A5, 0x22AC, 0x22B3, 0x22BA, 0x22CF, 0x22DD, 0x22DE, 0x22DF, 0x22FB,
                            0x2302, 0x2309, 0x233A, 0x23A0, 0x23A1, 0x23A8])
        # Restore Magic Boomerang requirement for Tingle 2
        patch.write_token(APTokenTypes.WRITE, 0x064952, bytes([0x46, 0x60]))
    for addr in placeholder:
        patch.write_token(APTokenTypes.WRITE, addr, bytes([0xF2]))

    # Kinstone packs
    multiplier_options = ["kinstones_cloud_pack", "kinstones_castor_pack",
                          "kinstones_redw_pack", "kinstones_redv_pack", "kinstones_rede_pack",
                          "kinstones_bluel_pack", "kinstones_blues_pack",
                          "kinstones_greenc_pack", "kinstones_greeng_pack", "kinstones_greenp_pack"]
    options = world.options.as_dict(*multiplier_options)
    multiplier_addr = 0xFE0020
    for multi in multiplier_options:
        patch.write_token(APTokenTypes.WRITE, multiplier_addr, bytes([options[multi]]))
        multiplier_addr += 1

    fusion_options = ["kinstones_gold", "kinstones_red", "kinstones_blue", "kinstones_green"]
    options = world.options.as_dict(*fusion_options)
    # Fusion Flags
    flag = 0xFF1241
    for bits in FUSION_FLAGS:
        for i, setting in enumerate(bits):
            if setting is not None and options[setting] == Kinstones.option_open:
                patch.write_token(APTokenTypes.OR_8, flag, 2 ** i)
        flag += 1
