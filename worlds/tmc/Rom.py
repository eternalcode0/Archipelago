from .Locations import location_table_by_name, LocationData
from .Items import item_table
from .constants import EXTERNAL_ITEM_MAP
from BaseClasses import Item, ItemClassification
from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
import struct
from dataclasses import dataclass
from typing import TYPE_CHECKING


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


@dataclass
class Transition:
    start_x: int
    start_y: int
    end_x: int
    end_y: int
    area_id: int
    room_id: int
    warp_type: int = 0
    subtype: int = 0
    shape: int = 0
    height: int = 1
    transition_type: int = 0
    facing_direction: int = 0

    def serialize(self) -> bytes:
        return struct.pack("<BBHHHHBBBBBB", self.warp_type, self.subtype, self.start_x, self.start_y, self.end_x,
                           self.end_y, self.shape, self.area_id, self.room_id, self.height, self.transition_type,
                           self.facing_direction)


def write_tokens(world: "MinishCapWorld", patch: MinishCapProcedurePatch) -> None:
    # Bake player name into ROM
    patch.write_token(APTokenTypes.WRITE, 0x000600, world.multiworld.player_name[world.player].encode("UTF-8"))

    # Bake seed name into ROM
    patch.write_token(APTokenTypes.WRITE, 0x000620, world.multiworld.seed_name.encode("UTF-8"))

    if 0 <= world.options.ped_elements.value <= 4:
        patch.write_token(APTokenTypes.WRITE, 0xFE0001, bytes([world.options.ped_elements.value]))
    if 0 <= world.options.ped_swords.value <= 5:
        patch.write_token(APTokenTypes.WRITE, 0xFE0002, bytes([world.options.ped_swords.value]))
    if 0 <= world.options.ped_dungeons.value <= 6:
        patch.write_token(APTokenTypes.WRITE, 0xFE0003, bytes([world.options.ped_dungeons.value]))

    if world.options.skip_dhc.value and world.options.goal_vaati.value:
        ped_to_altar = Transition(warp_type=1, start_x=0xE8, start_y=0x28, end_x=0x78, end_y=0x168,
                                  area_id=0x89, room_id=0)
        patch.write_token(APTokenTypes.WRITE, 0x139E80, ped_to_altar.serialize())

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
