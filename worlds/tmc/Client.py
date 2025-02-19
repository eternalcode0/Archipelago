from typing import TYPE_CHECKING, Set, Dict

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .Locations import all_locations, LocationData
from .Items import item_table

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


ROM_ADDRS = {
    "game_identifier": (0xA0, 8, "ROM"), # TODO: double-check, copied from a different game
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
    "room_area_id": (0x0BF4, 2, "IWRAM"), # The room in the 1st byte, area in the 2nd
}

class MinishCapClient(BizHawkClient):
    game = "The Minish Cap"
    system = "GBA"
    patch_suffix = ".aptmc"
    local_checked_locations: Set[int]
    items_by_id: Dict[int, str]
    location_name_to_id: Dict[str, int]
    location_by_room_area: Dict[int, [LocationData]]

    def __init__(self) -> None:
        super().__init__()
        self.items_by_id = {name: data.itemID for name, data in item_table.items()}
        self.location_name_to_id = {loc_data.name: loc_data.locCode for loc_data in all_locations}
        self.local_checked_locations = set()
        self.location_by_room_area = {}

        for loc in all_locations:
            if loc.roomArea in self.location_by_room_area:
                self.location_by_room_area[loc.roomArea].append(loc)
            else:
                self.location_by_room_area[loc.roomArea] = [loc]

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [ROM_ADDRS["game_identifier"]]))[0]
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
            print(rom_name)
            if rom_name != "GBAZELDA":
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b001
        ctx.want_slot_data = True
        ctx.watcher_timeout = 1

        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None or ctx.server.socket.closed:
            return

        try:
            # Handle giving the player items
            read_result = await bizhawk.read(ctx.bizhawk_ctx, [
                RAM_ADDRS["game_state"], # Current state of game (is the player actually in-game?)
                RAM_ADDRS["room_area_id"]
            ])
            print(f"read_result: {read_result}")
            if read_result is None:
                return
            # [game_state, room_area_id] = read_result
            game_state = read_result[0][0]
            room_area_id = int.from_bytes(read_result[1], "little")

            locs_to_send = set()

            # Early return if player is not in game
            print(f"game_state: {game_state}")
            if game_state != 0x00:
                return

            # Read all pending receive items and dump into game ram

            # Read all location flags in area and add to pending location checks if updates
            for loc in self.location_by_room_area[room_area_id]:
                print(loc)
                if loc.id in self.local_checked_locations:
                    continue
                loc_bytes = await bizhawk.read(ctx.bizhawk_ctx, [(loc.locCode[0], 1, "EWRAM")])
                if loc_bytes[0][0] == loc.locCode[1]:
                    # Add the the pending send list and the local checked locations to skip checking again
                    locs_to_send.add(loc.id)
                    self.local_checked_locations.add(loc.id)

            # Send location checks
            if locs_to_send is not None:
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(locs_to_send)}])

            # Send game clear

        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass
