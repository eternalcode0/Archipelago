from typing import TYPE_CHECKING, Set, Dict

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .Locations import all_locations
from .Items import item_table

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


ROM_ADDRS = {
    "game_identifier": (0x108, 9, "ROM"), # TODO: double-check, copied from a different game
}

RAM_ADDRS = {
    # 0x00: Gameplay
    # 0x01: File creation
    # 0x02: Language menu
    # 0x03: File options
    # 0x04: File select
    # 0x05: File copy
    # 0x06: File delete
    # 0x07: File load
    "game_state": (0x32EC4, 1, "EWRAM"),
}

class MinishCapClient(BizHawkClient):
    game = "The Legend of Zelda - The Minish Cap"
    system = "GBA"
    patch_suffix = ".aptmc"
    local_checked_locations: Set[int]
    item_id_to_name: Dict[int, str]
    location_name_to_id: Dict[str, int]

    def __init__(self) -> None:
        super().__init__()
        self.item_id_to_name = {name: data.itemID for name, data in item_table.items()}
        self.location_name_to_id = {loc_data.name: loc_data.locCode for loc_data in all_locations}
        self.local_checked_locations = set()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [ROM_ADDRS["game_identifier"]]))[0]
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
            if not rom_name == "ZELDA TMC": # TODO: placeholder name 'til I confirm what the name is supposed to be
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b001
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.5

        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:
            return

        try:
            # Handle giving the player items
            read_result = await bizhawk.read(ctx.bizhawk_ctx, [
                RAM_ADDRS["game_state"], # Current state of game (is the player actually in-game?)
            ])
            if read_result is None:
                return
            game_state, *other = read_result

            # Early return if player is not in game

            # Read all pending receive items and dump into game ram

            # Read all location flags in area and send if updates

            # Send game clear

        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass
